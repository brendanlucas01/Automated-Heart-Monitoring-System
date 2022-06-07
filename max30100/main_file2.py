LYNK_TEMPLATE_ID="TMPLO70ofd3T"
BLYNK_DEVICE_NAME="Affordable AED"
BLYNK_AUTH_TOKEN="haazNLOV3L5xtF2M1bwD26FksDXDbS2k"
from threading import *
import max30100
import BlynkLib
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn


last_read = 0       # this keeps track of the last potentiometer value
tolerance = 70     # to keep from being jittery we'll only change
set_volume=0         # volume when the pot has moved a significant amount
volume=0                   # on a 16-bit ADC
#blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)
ecg_data = []

class read_ECG(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.last_read = 0
        self.tolerance = 10
        self.set_volume=0
        self.volume=0
        # create the spi bus
        self.spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

        # create the cs (chip select)
        self.cs = digitalio.DigitalInOut(board.D22)
        self.lo2 = digitalio.DigitalInOut(board.D27)
        self.lo1 = digitalio.DigitalInOut(board.D17)
        self.lo2.direction = digitalio.Direction.INPUT
        self.lo1.direction = digitalio.Direction.INPUT
        # create the mcp object
        self.mcp = MCP.MCP3008(self.spi, self.cs)

        # create an analog input channel on pin 0
        self.chan0 = AnalogIn(self.mcp, MCP.P7)
        
        
    def remap_range(self, value, left_min, left_max, right_min, right_max):
        # this remaps a value from original (left) range to new (right) range
        # Figure out how 'wide' each range is
        left_span = left_max - left_min
        right_span = right_max - right_min
        # Convert the left range into a 0-1 range (int)
        valueScaled = int(value - left_min) / int(left_span)
        # Convert the 0-1 range into a value in the right range.
        return int(right_min + (valueScaled * right_span))
    def run(self):
        global ecg_data
        while True:
            if self.lo2.value==True or self.lo1.value==True:
                continue
            self.trim_pot = self.chan0.value
            self.set_volume = self.remap_range(self.trim_pot, 0, 65535, 0, 1023)
            self.pot_adjust = abs(self.set_volume - self.last_read)
            if self.pot_adjust < self.tolerance:
                self.set_volume = self.last_read
            self.volume=self.set_volume
            ecg_data.append(self.volume)
                # set OS volume playback volume
            self.last_read=self.set_volume

class read_oxy(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.mx30 = max30100.MAX30100()
        self.mx30.enable_spo2()
        global BLYNK_AUTH_TOKEN
        self.blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)
        self.max_value=100
        self.i = 0
    def run(self):
        while True:
            self.i+=1
            self.blynk.run()
            self.mx30.read_sensor()
            self.mx30.ir, self.mx30.red
            
            #if abs((self.mx30.red-self.mx30.buffer_red[0])/self.mx30.buffer_red[0]*100)>15:
             #   continue
            
            hb = int(self.mx30.ir / 100)
            spo2 = int(self.mx30.red / 100)
            if spo2>self.max_value:
                self.max_value=spo2
                
            if spo2>100:
                #print("spoof")
                spo2 = int(spo2/self.max_value*100)
                
            
            if self.mx30.ir != self.mx30.buffer_ir :
                print("Pulse:",hb);
                self.blynk.virtual_write(1, hb)
                
            if self.mx30.red != self.mx30.buffer_red:
                print("SPO2:",spo2);
                self.blynk.virtual_write(0, spo2)
                
                
            if self.i%20==0:
                self.max_value-=5
                
            global ecg_data
            if len(ecg_data)>0:
                val1 = ecg_data.pop()
                print("ECG Value: ",val1)
                self.blynk.virtual_write(2, val1)
        #    print("Temperature: ",mx30.get_temperature())
            time.sleep(0.2)
            
            
thread1 = read_ECG()
thread2 = read_oxy()

# Start new Threads
thread1.start()
thread2.start()
