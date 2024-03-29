## Serveur Mqtt
## 
import paho.mqtt.client as mqtt

IP_BROKER="localhost"
PORT_BROKER=1883

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("Maison/#")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if msg.topic == "Maison/Chambre1/lumiere":
        if str(msg.payload) == b'on':
            print("On")
        if msg.payload == b'off':
            print("Off")
    if msg.topic == "Maison/Salon/lumiere":
        if msg.payload == b'on':
            print("On")
        if msg.payload == b'off':
            print("Off")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(IP_BROKER, PORT_BROKER, 60)

client.loop_forever()