import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt

IP_BROKER="192.168.1.15"
PORT_BROKER=1883
GPIO.setmode(GPIO.BCM)

class Home:
    def __init__(self, Nom):
        self.nom = Nom
        self.room = []

    def _AddRoom_(self, Nom):
        self.room.append(Room(Nom))

class Room:
    def __init__(self, Nom):
        self.nom = Nom
        self.led = []
        self.button = []

    def _AddLed_(self,Nom,Gpio):
        self.led.append(Led(Nom, Gpio))

    def _DelLed_(self,Nom):
        self.led.remove(Nom)

    def _AddButton_(self,Nom,Gpio):
        self.button.append(Button(Nom, Gpio))
    
    def _DelButton_(self, Nom):
        self.button.remove(Nom)

class Led:
    def __init__(self, Nom, Gpio):
        self.nom = Nom
        self.gpio = Gpio
        GPIO.setup(self.gpio, GPIO.OUT)

    def _turnon_(self):
        try:
            GPIO.output(self.gpio, GPIO.HIGH)
        except:
            return -1
        return 0
    
    def _turnoff_(self):
        try:
            GPIO.output(self.gpio, GPIO.LOW)
        except:
            return -1
        return 0

    def _checkstate_(self):
        ## Return 1 when led is on
        ## Return 0 when led is off
        GPIO.setup(self.gpio, GPIO.OUT)
        try:
            return GPIO.input(self.gpio)
        except:
            return -1
    
    def _changestate_(self):
        if self._checkstate_():
            self._turnoff_()
        else:
            self._turnon_()

class Button:
    def __init__(self, Nom, Gpio):
        self.nom = Nom
        self.gpio = Gpio
        GPIO.setup(self.gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def _checkstate_(self):
        self.state = GPIO.input(self.gpio)
        if self.state == False:
            # Appuie Boutton
            time.sleep(0.25)
            return True
        else:
            return False

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("Maison/#")

Maison = Home("Maison")
Maison._AddRoom_("Chambre1")
Maison.room[0]._AddLed_("L1",12)
Maison.room[0]._AddButton_("I1",13)

Maison._AddRoom_("Chambre2")
Maison.room[1]._AddLed_("L1",14)
Maison.room[1]._AddButton_("I1", 15)

Maison._AddRoom_("Chambre3")
Maison.room[2]._AddLed_("L1",16)
Maison.room[2]._AddButton_("I1", 17)

Maison._AddRoom_("Salon")
Maison.room[3]._AddLed_("L1", 18)
Maison.room[3]._AddButton_("I1", 19)
Maison.room[3]._AddLed_("L2", 20)
Maison.room[3]._AddButton_("I2", 21)

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if msg.topic == "Maison/Chambre1/lumiere":
        if msg.payload == 'on':
            Maison.room[0].led[0]._turnon_()
        if msg.payload == 'off':
            Maison.room[0].led[0]._turnoff_()

    if msg.topic == "Maison/Chambre2/lumiere":
        if msg.payload == 'on':
            Maison.room[1].led[0]._turnon_()
        if msg.payload == 'off':
            Maison.room[1].led[0]._turnoff_()    

    if msg.topic == "Maison/Salon/lumiere":
        if msg.payload == 'on':
            Maison.room[2].led[0]._turnon_()
        if msg.payload == 'off':
            Maison.room[2].led[0]._turnoff_()

try:
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(IP_BROKER, PORT_BROKER, 60)
    client.loop_forever()

except KeyboardInterrupt:
    GPIO.cleanup()