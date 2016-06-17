# watsoniot-python
Small module to wrap basic functionality to connect to Bluemix based WatsoIoT platform

The idea of this project is to help you write quick demos and samples to connect to WatsonIoT Platform using Python

> **Note**
> 
> You need a WatsonIoT account, you can start your free trial here: http://www.ibm.com/internet-of-things/trial.htm
> 



On your WatsonIoT platform make sure you register a device, even if you don't a physical device, we have a quick samples
that would work without a physical device, once you have your device created as well as the access token 
https://developer.ibm.com/recipes/tutorials/how-to-register-devices-in-ibm-iot-foundation/ 

Write down your organization, the device type, device id and the access token.


#### The iot.bluemix package holds the **WatsonIoTCnxHelper** class that's the only thing you need

``` python
	watsonIoTHelper = WatsonIoTCnxHelper()
	watsonIoTHelper.setBluemixIoT("your-watsoniot-org-name", "name-of-your-device-type", "your-device-id")
	watsonIoTHelper.setCredentials("use-token-auth", "token-for-the-device")
```

## JSON Data to publish
WatsonIoT needs accepts json, make sure you create a python class to hold your data and then use the **D()** object 

``` python

	from iot.bluemix import D

	class payloadData:
		def __init__(self):
			self.metricA = 0
			self.sensorA = 0
			self.temperature  = 0

    my_watsonIoT_message = D()
    my_watsonIoT_message.d = payloadData() #Your own defined object
    
    my_watsonIoT_message.d.metric1 = 502
    my_watsonIoT_message.d.sensorA = 0.77415198
    my_watsonIoT_message.d.temperature = 17.822
	
	json_to_send = my_watsonIoT_message.to_JSON()
``` 

## Paho mqtt Client for python
You'll need to install the Mqtt paho client for python

```
>pip install paho-mqtt
```
You can find more information here https://pypi.python.org/pypi/paho-mqtt/1.1

Once you're set and done with the client you issue the following lines of code to connect to the WatsonIoT Platform

``` python
import paho.mqtt.client as watsonIoT

'''
  other stuff
'''

	watsonIoTClient = watsonIoT.Client(watsonIoTHelper.getClientId())
	watsonIoTClient.username_pw_set(watsonIoTHelper.userName, password=watsonIoTHelper.password)
	watsonIoTClient.connect(host=watsonIoTHelper.broker, port=watsonIoTHelper.port, keepalive=60)

```

## Send the data
After that you only need to send the data to WatsonIoT

´´´
     
	json_to_send = my_watsonIoT_message.to_JSON()	 
    watsonIoTClient.publish(watsonIoTHelper.topic, payload=json_to_send, qos=0, retain=False)

´´´

## Sample
The **EnergySample.py** sample should be a good starting point; take the date **WatsonIotSampleData.csv** file and sends it to WatsonIoT platform

Hope this helps, if you need further clarification be sure to drop me a tweet @Sabo_IBM more than glad to help

