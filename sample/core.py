from gpiozero import LED
import RPi.GPIO as GPIO

class Maison:
    def __init__(Nom):
        self.nom = Nom

class Piece:
    def __init__(self):
        self.nom = "Piece"

class Led:
    def __init__(self, Nom, Gpio):
        self.nom = Nom
        self.gpio = Gpio

    def _turnon_(self):
        try:
            LED(self.gpio).on()
        except:
            return -1
        return 0
    
    def _turnoff_(self):
        try:
            LED(self.gpio).off()
        except:
            return -1
        return 0

    def _checkstate_(self):
        try:
            return GPIO.input(self.gpio)
        except:
            return -1

Led_test = Led("Chambre1", 4)
Led_test._turnon_()

