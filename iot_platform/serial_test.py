# -*- coding: utf-8 -*-
import requests
import serial
import time

url = "http://ithaca-klaytn.ml:9000/co2"

ard = serial.Serial('/dev/cu.usbserial-14340', 9600)

while True:
    if ard.readable():
        res = ard.readline()
        usage = res.decode()[:len(res) - 1]
        govalue = int(usage)
        print(govalue)

        data = {'vehicleId': "byc3230-iot-0008", 'usage': govalue}
        res = requests.post(url, data=data)
        time.sleep(1)
        print(res)
