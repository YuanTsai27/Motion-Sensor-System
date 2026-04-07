import RPi.GPIO as GPIO
import grove_rgb_lcd


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


class DisplayController:
    deviceDisplay = LCD()
    leftButton = PushButton(23, "Left")
    rightButton = PushButton(24, "Right")
    selectButton = PushButton(25, "Select")

    def displayMain(self):
        self.deviceDisplay.displayText("Main Menu\nSet Alert Level")

    def displayMenu(self, title, options):
        self.deviceDisplay.displayText(title + "\n" + options)
