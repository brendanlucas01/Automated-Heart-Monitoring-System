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

mx30 = max30100.MAX30100()
mx30.enable_spo2()
# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D22)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan0 = AnalogIn(mcp, MCP.P7)

blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)

print('Raw ADC Value: ', chan0.value)
print('ADC Voltage: ' + str(chan0.voltage) + 'V')

last_read = 0       # this keeps track of the last potentiometer value
tolerance = 70     # to keep from being jittery we'll only change
set_volume=0         # volume when the pot has moved a significant amount
volume=0                   # on a 16-bit ADC


def read_data():
    max_value=100
    for i in range(60):
        mx30.read_sensor()
        mx30.ir, mx30.red
        
        hb = int(mx30.ir / 100)
        spo2 = int(mx30.red / 100)
        trim_pot_changed = False
        last_read = 0
        set_volume=0
        # read the analog pin
        trim_pot = chan0.value

        # how much has it changed since the last read?
        trim_pot_changed = True
        
        if spo2>max_value:
            max_value=spo2
            
        if spo2>100:
            #print("spoof")
            spo2 = int(spo2/max_value*100)
            
        
        if mx30.ir != mx30.buffer_ir :
            print("Pulse:",hb);
            blynk.virtual_write(1, hb)
            
        if mx30.red != mx30.buffer_red:
            print("SPO2:",spo2);
            blynk.virtual_write(0, spo2)
            
        set_volume = remap_range(trim_pot, 0, 65535, 0, 1023)
        
        if trim_pot_changed:
            # convert 16bit adc0 (0-65535) trim pot read into 0-100 volume level
            
            # save the potentiometer reading for the next loop
            pot_adjust = abs(set_volume - last_read)
            if pot_adjust < tolerance:
                set_volume = last_read
#        if set_volume>600:
#            volume=600
#        elif set_volume>550:
#            volume=550
#        elif set_volume>480:
#            volume=480
#        elif set_volume>400:
#            volume=450
#        else:
            volume=set_volume
            # set OS volume playback volume
        print('Volume = {volume}%' .format(volume = volume))
        last_read=set_volume
        blynk.virtual_write(2, volume)
    #    print("Temperature: ",mx30.get_temperature())
        time.sleep(0.03)
        

def remap_range(value, left_min, left_max, right_min, right_max):
    # this remaps a value from original (left) range to new (right) range
    # Figure out how 'wide' each range is
    left_span = left_max - left_min
    right_span = right_max - right_min

    # Convert the left range into a 0-1 range (int)
    valueScaled = int(value - left_min) / int(left_span)

    # Convert the 0-1 range into a value in the right range.
    return int(right_min + (valueScaled * right_span))


while True:
    blynk.run()
    read_data()
    