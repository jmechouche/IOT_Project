import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
from time import sleep

IP_BROKER="localhost"
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

    def _AddRgbLed_(self,Nom,Red,Green,Blue):
        self.led.append(RgbLed(Nom, Red, Green, Blue))

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

class RgbLed:
    def __init__(self, Nom, Red, Green, Blue):
        """Rouge, Vert, Bleu """
        self.nom = Nom
        self.red = Red
        self.green = Green
        self.blue = Blue
        GPIO.setup(self.red, GPIO.OUT)
        GPIO.setup(self.blue, GPIO.OUT)
        GPIO.setup(self.green, GPIO.OUT)

    def _turnon_(self, color):
        if color == "green":
            gpio = self.green
        elif color == "blue":
            gpio = self.blue
        elif color == "red":
            gpio = self.red
        else:
            return -1
        try:
            GPIO.output(gpio, GPIO.HIGH)
        except:
            return -1
        return 0

    def _turnoff_(self, color):
        if color == "green":
            gpio = self.green
        elif color == "blue":
            gpio = self.blue
        elif color == "red":
            gpio = self.red
        else:
            return -1
        try:
            GPIO.output(gpio, GPIO.LOW)
        except:
            return -1
        return 0

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
Maison.room[0]._AddLed_("L1", 7)
Maison.room[0]._AddLed_("L2", 17)
Maison.room[0]._AddButton_("I1", 12)
Maison.room[0]._AddButton_("I2", 27)

Maison._AddRoom_("Chambre2")
Maison.room[1]._AddLed_("L1", 16)
Maison.room[1]._AddLed_("L2", 2)
Maison.room[1]._AddButton_("I1", 20)
Maison.room[1]._AddButton_("I2", 3)

Maison._AddRoom_("Salon")
Maison.room[2]._AddRgbLed_("lumiere", 26, 19, 13)
Maison.room[2]._AddButton_("I1", 24)

Maison._AddRoom_("Salledebain")
Maison.room[3]._AddLed_("L1", 25)
Maison.room[3]._AddButton_("I1", 8)

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if msg.topic == "Maison/Chambre1/lumiere1":
        if msg.payload == b'on':
            Maison.room[0].led[0]._turnon_()
        if msg.payload == b'off':
            Maison.room[0].led[0]._turnoff_()
        if msg.payload == b'changeState':
            Maison.room[0].led[0]._changestate_()
    if msg.topic == "Maison/Chambre1/lumiere2":
        if msg.payload == b'on':
            Maison.room[0].led[1]._turnon_()
        if msg.payload == b'off':
            Maison.room[0].led[1]._turnoff_()
        if msg.payload == b'changeState':
            Maison.room[0].led[1]._changestate_()

    if msg.topic == "Maison/Chambre2/lumiere1":
        if msg.payload == b'on':
            Maison.room[1].led[0]._turnon_()
        if msg.payload == b'off':
            Maison.room[1].led[0]._turnoff_()    
        if msg.payload == b'changeState':
            Maison.room[1].led[0]._changestate_()
    if msg.topic == "Maison/Chambre2/lumiere2":
        if msg.payload == b'on':
            Maison.room[1].led[1]._turnon_()
        if msg.payload == b'off':
            Maison.room[1].led[1]._turnoff_()    
        if msg.payload == b'changeState':
            Maison.room[1].led[1]._changestate_()

    if msg.topic == "Maison/Salon/lumiere/red":
        if msg.payload == b'on':
            Maison.room[2].led[0]._turnon_("red")
        if msg.payload == b'off':
            Maison.room[2].led[0]._turnoff_("red")
        if msg.payload == b'changeState':
            Maison.room[2].led[0]._changestate_("red")

    if msg.topic == "Maison/Salon/lumiere/green":
        if msg.payload == b'on':
            Maison.room[2].led[0]._turnon_("green")
        if msg.payload == b'off':
            Maison.room[2].led[0]._turnoff_("green")
        if msg.payload == b'changeState':
            Maison.room[2].led[0]._changestate_("green")

    if msg.topic == "Maison/Salon/lumiere/blue":
        if msg.payload == b'on':
            Maison.room[2].led[0]._turnon_("blue")
        if msg.payload == b'off':
            Maison.room[2].led[0]._turnoff_("blue")
        if msg.payload == b'changeState':
            Maison.room[2].led[0]._changestate_("blue")

    if msg.topic == "Maison/Sdb/lumiere":
        if msg.payload == b'on':
            Maison.room[3].led[0]._turnon_()
        if msg.payload == b'off':
            Maison.room[3].led[0]._turnoff_()
        if msg.payload == b'changeState':
            Maison.room[3].led[0]._changestate_()

    if msg.topic == "Maison/lumieres":
        if msg.payload == b'on':
            Maison.room[0].led[0]._turnon_()
            Maison.room[0].led[1]._turnon_()
            Maison.room[1].led[0]._turnon_()
            Maison.room[1].led[1]._turnon_()
            Maison.room[2].led[0]._turnon_("green")
            Maison.room[2].led[0]._turnon_("blue")
            Maison.room[2].led[0]._turnon_("red")
            Maison.room[3].led[0]._turnon_()
        if msg.payload == b'off':
            Maison.room[0].led[0]._turnoff_()
            Maison.room[0].led[1]._turnoff_()
            Maison.room[1].led[0]._turnoff_()
            Maison.room[1].led[1]._turnoff_()
            Maison.room[2].led[0]._turnoff_("green")
            Maison.room[2].led[0]._turnoff_("blue")
            Maison.room[2].led[0]._turnoff_("red")
            Maison.room[3].led[0]._turnoff_()

    if msg.topic == "Maison/scenario1":
        Maison.room[2].led[0]._turnon_("blue")
        sleep(3)
        Maison.room[3].led[0]._turnon_()
        sleep(3)
        Maison.room[2].led[0]._turnon_("green")
        Maison.room[3].led[0]._turnoff_()
        sleep(3)
        Maison.room[2].led[0]._turnoff_("blue")
        Maison.room[0].led[1]._turnon_()
        sleep(3)
        Maison.room[2].led[0]._turnoff_("green")
        Maison.room[0].led[0]._turnon_()
        sleep(3)
        Maison.room[0].led[1]._turnoff_()
        sleep(3)
        Maison.room[0].led[0]._turnoff_()

    if msg.topic == "Maison/scenario2":
        Maison.room[2].led[0]._turnon_("red")
        sleep(3)
        Maison.room[3].led[0]._turnon_()
        sleep(3)
        Maison.room[2].led[0]._turnon_("blue")
        Maison.room[3].led[0]._turnoff_()
        sleep(3)
        Maison.room[2].led[0]._turnoff_("red")
        Maison.room[1].led[1]._turnon_()
        sleep(3)
        Maison.room[2].led[0]._turnoff_("blue")
        Maison.room[1].led[0]._turnon_()
        sleep(3)
        Maison.room[1].led[1]._turnoff_()
        sleep(3)
        Maison.room[1].led[0]._turnoff_()

try:
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(IP_BROKER, PORT_BROKER, 60)
    client.loop_forever()

except KeyboardInterrupt:
    GPIO.cleanup()
