from time import sleep
import RPi.GPIO as GPIO


class Buzzer:
    buzzerPIN = 26

    def __init__(self):
        GPIO.setup(self.buzzerPIN, GPIO.OUT)

    def buzzAlert(self, period):
        while True:
            GPIO.output(self.buzzerPIN, GPIO.HIGH)
            sleep(period)
            GPIO.output(self.buzzerPIN, GPIO.LOW)
            sleep(period)

    def buzzOff(self):
        while True:
            GPIO.output(self.buzzerPIN, GPIO.LOW)


class LED:
    ledPIN = None
    ledColour = ""

    def __init__(self, pin, colour):
        self.ledPIN = pin
        self.ledColour = colour
        GPIO.setup(self.ledPIN, GPIO.OUT)

    def ledAlert(self, period):
        while True:
            GPIO.output(self.ledPIN, GPIO.HIGH)
            sleep(period)
            GPIO.output(self.ledPIN, GPIO.LOW)
            sleep(period)

    def ledOn(self):
        while True:
            GPIO.output(self.ledPIN, GPIO.HIGH)

    def ledOff(self):
        while True:
            GPIO.output(self.ledPIN, GPIO.LOW)
