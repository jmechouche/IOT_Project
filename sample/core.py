import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

class Maison:
    def __init__(self, Nom):
        self.nom = Nom

class Piece:
    def __init__(Nom):
        self.nom = Nom

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

## Test Bouton
bouton = Button('interrupteur', 15)
led_1 = Led('led', 14) 
while True:
    if bouton._checkstate_():
        led_1._changestate_()

gpio.cleanup()


