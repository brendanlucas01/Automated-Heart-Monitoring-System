import BlynkLib
import time
BLYNK_TEMPLATE_ID="TMPLO70ofd3T"
BLYNK_DEVICE_NAME="Affordable AED"
BLYNK_AUTH_TOKEN="haazNLOV3L5xtF2M1bwD26FksDXDbS2k"
# Initialize Blynk

#https://github.com/vshymanskyy/blynk-library-python
# pip3 install https://github.com/vshymanskyy/blynk-library-python/archive/master.tar.gz
blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)

tmr_start_time = time.time()
while True:
    blynk.run()
    for i in range(10):
        blynk.virtual_write(0, i)
        blynk.virtual_write(1, i)
        print(i)
        time.sleep(3)