from datetime import datetime
import RPi.GPIO as GPIO
import cv2


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
