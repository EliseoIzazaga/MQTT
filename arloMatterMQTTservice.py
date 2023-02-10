
#Eliseo Izazaga
#This application is meant to run as a service on a chiptool/MATTER device, 
#this service will receive subscribe as a "listener" to an MQTT broker (already on then arlo cloud) 
#this service will receive MQTT messages as JSON and parse them to send corresponding CLI to the MATTER system, 
#messages to be sent
'''
1.	Updated Arlo Secure App to send MQTT messages to Matter Hub (Linux) for the following operations
a.	Commission
b.	Turn On
c.	Turn Off
2.	Setup MQTT Server
a.	Host: 198.199.107.70
b.	Port: 1883
c.	User ID: arlo
d.	Password: matter
e.	Topic: arlomatter
3.	The Matter Hub (Linux) should do the following:
a.	Subscribe to the above topic on the MQTT Server
b.	Parse and process the following MQTT messages
•	Commission: mattertool ble
o	["device-id": "12345", "op-type": "comm", "op-value": ""]
•	Turn On: mattertool on
o	["device-id": "12345", "op-type": "admin", "op-value": "on"]
•	Turn Off: matter tool off
o	["device-id": "12345", "op-type": "admin", "op-value": "off"]
4.	Example Command-line
a.	Subscribe
•	mosquitto_sub -h 198.199.107.70 -p 1883 -u arlo -P matter -t arlomatter
b.	Publish
•	mosquitto_pub -h 198.199.107.70 -p 1883  -u arlo -P matter -t arlomatter -m "{'device-id':'1234', 'op-type':'comm', op-value:''}"
'''
import time 
import random
import subprocess

from paho.mqtt import client as mqtt_client


broker = '198.199.107.70'
port = 1883
topic = "arlomatter"
# generate client ID with pub prefix randomly
client_id = "1234"
username = 'arlo'
password = 'matter'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        inMessage = str(msg.payload.decode())
        print("DECODING MESSAGE: ")
        if "on" in inMessage:
            print(inMessage)
            x = subprocess.run(['/home/ubuntu/connectedhomeip/out/standalone/chip-tool onoff on 1122 1'], shell=True) #This command works. 
            print(x)
            print(x.args)
            print(x.returncode)
            print(x.stdout)
            print(x.stderr)
        if "off" in inMessage:
            print(inMessage)
            x = subprocess.run(['/home/ubuntu/connectedhomeip/out/standalone/chip-tool onoff off 1122 1'], shell=True) #This command works. 
            print(x)
            print(x.args)
            print(x.returncode)
            print(x.stdout)
        if "" in inMessage:
            x = subprocess.run(['/home/ubuntu/connectedhomeip/out/standalone/chip-tool pairing ble-wifi 1122 HOMENW 305995135 20202021 3840'], shell=True) #This command works. 
            print(x)
            print(x.args)
            print(x.returncode)
            print(x.stdout)
            
        
        

            


    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
