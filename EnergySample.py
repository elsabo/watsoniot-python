'''
Created on May, 2016

Quick demo to publish mqtt messages to WatsonIoT

It takes data from sample file an publishes the data

@author: Jesus Chavez
 
chavezj@mx1.ibm.com | elsabo@gmail.com
'''
import paho.mqtt.client as watsonIoT

import time
import csv

from iot.bluemix import WatsonIoTCnxHelper
from iot.bluemix import D

'''
Define your class to hold the data you want to publish to WatsonIoT
'''
class EnergyReading(object):
    def __init__(self):
        self.metricDateTime = 0
        self.storeTemperature = 0
        self.tempFridge  = 0
        self.tempIceMaker  = 0
        self.meterKWH  = 0
        self.doorIceMaker  = 0
        self.storeHumidity = 0

    #takenAt    storeTemperature    storeHumidity    tempFridge    tempIceMaker    meterKWH    doorIceMaker
    def set(self, row):
        self.metricDateTime = row['takenAt']
        self.storeTemperature = float(row['storeTemperature'])
        self.tempFridge  = float(row['tempFridge'])
        self.tempIceMaker  = float(row['tempIceMaker'])
        self.meterKWH  = float(row['meterKWH'])
        self.doorIceMaker  = int(row['doorIceMaker'])
        self.storeHumidity = float(row['storeHumidity'])
        
    def get(self):
        return ""

'''
The on_connect and on_message events

on_connect will be fired as soon as we have a response to our connect attempt

on_message will be fired whenever we have a message back to our subscription
'''
def on_connect(client, userdata, rc):
    print("Connected with result code " + watsonIoT.connack_string(rc))

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


'''
The following 3 lines is the only you need to setup the connection ton WatsonIoT
'''
watsonIoTHelper = WatsonIoTCnxHelper()
watsonIoTHelper.setBluemixIoT("your-watsoniot-org-name", "name-of-your-device-type", "your-device-id")
watsonIoTHelper.setCredentials("use-token-auth", "token-for-the-device")

'''
Time to prepare the client 
the watsonIoTHelper.getClientId() call builds the cliente Id WatsonIoT needs
'''
watsonIoTClient = watsonIoT.Client(watsonIoTHelper.getClientId())
watsonIoTClient.username_pw_set(watsonIoTHelper.userName, password=watsonIoTHelper.password)
watsonIoTClient.connect(host=watsonIoTHelper.broker, port=watsonIoTHelper.port, keepalive=60)

'''
Wire the eventHandlers
'''
watsonIoTClient.on_connect = on_connect
watsonIoTClient.on_message = on_message

'''
This is optional only if you want to handle cmd events back
'''
watsonIoTClient.subscribe(watsonIoTHelper.cmdSubject)

#The fun begings
watsonIoTClient.loop_start() 

while watsonIoTClient.loop() == 0:
    jsonData = D()
    jsonData.d = EnergyReading()

    #Parse the file and build the message
    with open('WatsonIotSampleData.csv') as csvfile:
        energyReader = csv.DictReader(csvfile)
    
        for row in energyReader:
            jsonData.d.set(row)
            msg = jsonData.to_JSON()
            watsonIoTClient.publish(watsonIoTHelper.topic, payload=msg, qos=0, retain=False)
            print "Temprature metric taken at %s was %s was published to WatsonIoT..." % (row['takenAt'], row['storeTemperature'])
            time.sleep(5)


    pass