from enum import Enum
from time import time, sleep
from datetime import datetime
import RPi.GPIO as GPIO
import grove_rgb_lcd
import cv2

class AlertLevel(Enum):
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class Motion:
    timeCode = None
    alertLevel = None
    motPhoto = None
    def __init__(self, time, level, photo):
        self.timeCode = time
        self.alertLevel = level
        self.photo = photo

class PIRSensor:
    pirPIN = 17
    def __init__(self):
        GPIO.setup(self.pirPIN, GPIO.IN)
    def isMotion(self):
        if GPIO.input(self.pirPIN):
            return True
        else:
            return False

class Webcam:
    def savePhoto(self, photo, path):
        fileID = f"/snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        cv2.imwrite(path + fileID, photo)
    def capturePhoto(self, path):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            self.savePhoto(frame, path)
            cap.release()
            return frame
        else:
            cap.release()
            return None

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

class PushButton:
    buttPIN = None
    buttAction = ""
    def __init__(self, pin, action):
        self.buttPIN = pin
        self.buttAction = action
        GPIO.setup(self.buttPIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    def isSelect(self):
        if GPIO.input(self.buttPIN) == GPIO.LOW:
            return True
        else:
            return False

class LCD:
    def __init__(self):
        grove_rgb_lcd.setRGB((255, 255, 255))
    def displayText(self, text):
        grove_rgb_lcd.setText(text)
    def displayColour(self, colour):
        grove_rgb_lcd.setRGB(colour)
    def clear(self):
        grove_rgb_lcd.setRGB((0, 0, 0))
        grove_rgb_lcd.clear()

class DisplayController:
    deviceDisplay = LCD()
    leftButton = PushButton(23, "Left")
    rightButton = PushButton(24, "Right")
    selectButton = PushButton(25, "Select")
    def displayMain(self):
        self.deviceDisplay.displayText("Main Menu\nSet Alert Level")
    def displayMenu(self, title, options):
        self.deviceDisplay.displayText(title + "\n" + options)

class DatabaseLogger:
    databasePath = None
    def __init__(self, path):
        self.databasePath = path
    def addEntry(self, motionEvent):
        motTime = motionEvent.timeCode
        motLevel = motionEvent.alertLevel.value
        with open(self.databasePath + "/Motion_log.txt", "a") as f:
            f.write("Motion detected at " + motTime + ", ALERT " + motLevel + "\n")

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

MotionSensorController = SystemControl()
MotionSensorController.activeDevice()
