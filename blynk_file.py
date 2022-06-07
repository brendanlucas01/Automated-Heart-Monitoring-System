BLYNK_TEMPLATE_ID="TMPLO70ofd3T"
BLYNK_DEVICE_NAME="Affordable AED"
BLYNK_AUTH_TOKEN="haazNLOV3L5xtF2M1bwD26FksDXDbS2k"

import blynklib
import time
# import blynklib_mp as blynklib # micropython import

# base lib init
blynk = blynklib.Blynk(BLYNK_AUTH_TOKEN,log=print)
#https://github.com/blynkkk/lib-python

# advanced options of lib init
#from __future__ import print_function
#blynk = blynklib.Blynk(BLYNK_AUTH_TOKEN, server='blynk-cloud.com', port=80, ssl_cert=None,heartbeat=10, rcv_buffer=1024, log=print)
#blynk = blynklib.Blynk(BLYNK_AUTH_TOKEN, server='blynk.cloud', port=80, ssl_cert=None,heartbeat=10, rcv_buffer=1024, log=print)
# Lib init with SSL socket connection
# blynk = blynklib.Blynk(BLYNK_AUTH, port=443, ssl_cert='<path to local blynk server certificate>')
# current blynk-cloud.com certificate stored in project as 
# https://github.com/blynkkk/lib-python/blob/master/certificate/blynk-cloud.com.crt
# Note! ssl feature supported only by cPython

# register handler for Virtual Pin V22 reading by Blynk App.
# when a widget in Blynk App asks Virtual Pin data from server within given configurable interval (1,2,5,10 sec etc) 
# server automatically sends notification about read virtual pin event to hardware
# this notification captured by current handler 
def virtual_data():
    for i in range(100):
        print(i)
        blynk.virtual_write("V0", i)
        blynk.virtual_write("V1", i)
        blynk.virtual_write("V2", i)
        time.sleep(1)

        
# main loop that starts program and handles registered events
while True:
    blynk.run()
    virtual_data()