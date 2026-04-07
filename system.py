from time import time, sleep
from datetime import datetime
import RPi.GPIO as GPIO

from models import AlertLevel, Motion
from sensors import PIRSensor, Webcam
from actuators import Buzzer, LED
from display import DisplayController
from database import DatabaseLogger


class SystemControl:
    pinNumber = [1, 0, 2]
    currAlert = AlertLevel.NONE
    currMotion = None
    motionDatabase = DatabaseLogger("/home/pi/motionsense")
    devicePIR = PIRSensor()
    deviceWebcam = Webcam()
    lcdControl = DisplayController()
    deviceBuzzer = Buzzer()
    redLED = LED(22, "Red")
    greenLED = LED(27, "Green")

    def __int__(self):
        GPIO.setmode(GPIO.BCM)

    def triggerAlert(self):
        self.greenLED.ledOff()
        self.redLED.ledAlert(0.4)
        self.deviceBuzzer.buzzAlert(0.4)
        self.lcdControl.deviceDisplay.displayColour((255, 0, 0))
        self.motionDatabase.addEntry(self.currMotion)

    def stopAlert(self):
        self.redLED.ledOff()
        self.greenLED.ledOn()
        self.deviceBuzzer.buzzOff()
        self.lcdControl.deviceDisplay.displayColour((255, 255, 255))

    def monitorAlert(self):
        while True:
            if self.devicePIR.isMotion():
                motPhoto = self.deviceWebcam.capturePhoto("/home/pi/motionsense/captures")
                self.currMotion = Motion(datetime.now(), self.currAlert, motPhoto)
                if self.currAlert == AlertLevel.HIGH:
                    self.triggerAlert()
                if self.currAlert == AlertLevel.MEDIUM:
                    self.motionDatabase.addEntry(self.currMotion)
            sleep(2)

    def requirePIN(self, pin):
        self.lcdControl.displayMenu("Enter PIN Number", "   1 - 2 - 3   ")
        timer = time()
        pinState = 0
        while True:
            if pinState == 3:
                return True
            if self.lcdControl.leftButton.isSelect() & pinState == pin[1]:
                pinState += 1
            elif self.lcdControl.selectButton.isSelect() & pinState == pin[2]:
                pinState += 1
            elif self.lcdControl.rightButton.isSelect() & pinState == pin[3]:
                pinState += 1
            elif (time() - timer) > 60:
                return False

    def changeAlert(self):
        self.lcdControl.displayMenu("Set Alert Level", "Green-Yellow-Red")
        while True:
            if self.lcdControl.leftButton.isSelect():
                self.currAlert = AlertLevel.LOW
                break
            if self.lcdControl.selectButton.isSelect():
                self.currAlert = AlertLevel.MEDIUM
                break
            if self.lcdControl.rightButton.isSelect():
                self.currAlert = AlertLevel.HIGH
                break

    def deactiveDevice(self):
        self.lcdControl.deviceDisplay.clear()
        GPIO.cleanup()

    def activeDevice(self):
        self.lcdControl.displayMain()
        self.monitorAlert()
        while True:
            if self.lcdControl.selectButton.isSelect():
                if self.requirePIN(self.pinNumber):
                    self.changeAlert()
                else:
                    self.lcdControl.displayMain()
            elif self.lcdControl.rightButton.isSelect():
                self.deactiveDevice()
