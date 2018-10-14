import RPi.GPIO as GPIO
import time

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

Maison = Home("Maison")
Maison._AddRoom_("Chambre1")
Maison.room[0]._AddLed_("L1",12)
Maison.room[0].led[0]._turnon_()

GPIO.cleanup()
