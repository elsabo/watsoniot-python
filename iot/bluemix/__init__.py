'''
Created on May, 2016

Helper to easy Connect to IBM Watson IoT Platform
Not an extended implementation but rather a quick wrapper to 
quicly build demos and samples

@author: Jesus Chavez
 
chavezj@mx1.ibm.com | elsabo@gmail.com

'''
import json

'''
The D object would helps us create the required json payload format
{
    "d": {
            ...
            ...
            ...
         }
}
The content of the payload would be created once the 
python object is converted to json format
'''
class D(object):
    '''
    The d property would help us hold the data we want to send to WatsonIoT

    You have to define your own object then assign
    an instance of that object to the "d" property
    
    my_watsonIoT_message = D()
    my_watsonIoT_message.d = payloadData() #Your own defined object
    
    my_watsonIoT_message.d.metric1 = 502
    my_watsonIoT_message.d.sensorA = 0.77415198
    my_watsonIoT_message.d.temperature = 17.822
     
    '''
    def __init__(self):
        self.d = {}
    
    '''
    The to_JSON method will convert the python object to the d variable
    This is the simplest json coverter
    
    json_for_WatsonIoT = my_watsonIoT_message.to_JSON
    '''
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)    
        #return json.dumps(self, cls=EasyEncoder)
'''
BluemixCnxHelper
'''
class WatsonIoTCnxHelper:
    # Suffix for the WatsonIoT Cloud endpoint
    BLUEMIX_URI_SUFFIX = ".messaging.internetofthings.ibmcloud.com"
    
    # Default command suffix 
    DEFAULT_CMD_ID = "cid"
    
    #Initialize variables
    def __init__(self):
        self.deviceId = ""
        self.deviceType = ""
        self.clientId = ""
        self.broker = ""
        self.organization = ""
        
        self.topic = "iot-2/evt/status/fmt/json"
        self.cmdSubject = "iot-2/cmd/" + self.DEFAULT_CMD_ID + "/fmt/json"
        self.port = 1883
        self.useSSL = False
    
    '''
    Initialize with your Watson IoT instance device information
    '''
    def setBluemixIoT(self, org, dtype, device ):
        self.organization = org
        self.deviceType = dtype
        self.deviceId = device
        self.broker = self.organization + self.BLUEMIX_URI_SUFFIX

    '''
    Token assiged to the device
    '''
    def setCredentials(self, u, p):
        self.userName = u
        self.password = p
    
    '''
    Change the topic to use to publish the information
    '''
    def setTopic(self, t):
        self.topic = t
    
    '''
    The ClientId that Watson IoT needs must follow this format
    d : <your-watsonIoT-org-name> : <device-type-for-the-device> : <device-identifier>
    The device variable must match the record on WatsonIoT
    '''
    def getClientId(self):
        self.clientId = "d:" + self.organization + ":" + self.deviceType + ":" + self.deviceId
        return self.clientId
    
    '''
    Getters / Setters for helper variables
    '''
    def getUser(self):
        return self.userName
    
    def getPassword(self):
        return self.password
    
    def getBroker(self):
        return self.broker
    
    def getPort(self):
        return self.port
    