import time
import max30100

# https://github.com/rravivarman/RaspberryPi/tree/master/MAX30100
# https://github.com/whilemind/MAX30100u

mx30 = max30100.MAX30100()
mx30.enable_spo2()

while 1:
#    mx30.reinit()
    mx30.read_sensor()

    mx30.ir, mx30.red
    
    hb = int(mx30.ir / 100)
    spo2 = int(mx30.red / 100)
    
    if mx30.ir != mx30.buffer_ir :
        print("Pulse:",hb);
    if mx30.red != mx30.buffer_red:
        print("SPO2:",spo2);
#    print("Temperature: ",mx30.get_temperature())
    time.sleep(0.1) 