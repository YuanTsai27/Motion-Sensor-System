# Motion-Sensor-System
A Raspberry Pi–based motion sensor that triggers an alert of varying intensity.  It integrates a PIR motion sensor, webcam, buzzer, LCD display and LEDs within the processes of detecting motion, capturing images, triggering alerts and logging motion events.

# Device explained more in-depth

The embedded system developed in this project focuses on motion detection and image 
capturing using a Raspberry Pi. The system integrates a Passive Infrared (PIR) sensor to 
detect motion, a camera for visual data capture, an LED indicator, a buzzer for alerts, and 
an LCD display. The PIR sensor detects infrared radiation from moving objects to trigger 
specific software events. 

When motion is detected, the Raspberry Pi executes a timed routine that activates the 
LED and buzzer, records the event in a log file stored locally, and captures a still image 
through the camera. Images are timestamped to ensure organized data storage. The 
software runs under real-time constraints to process each sensor event accurately, 
avoiding missed detections or duplicated captures. 

Data collected from the sensors are displayed on the LCD for immediate feedback, while 
long-term data are stored locally. This setup demonstrates real-time sensing, data 
acquisition, and simple human-machine interaction. From a software design perspective, 
the program follows an event-driven structure written in Python, where each component 
(sensor input, output display, and storage) runs sequentially within a loop, optimized for 
low latency and efficient I/O handling.


# Contents of each sub-file
- main.py:	Entry point 
- models.py: AlertLevel enum, Motion dataclass
- sensors.py: PIRSensor, Webcam
- actuators.py: Buzzer, LED
- display.py: LCD, PushButton, DisplayController
- database.py: DatabaseLogger
- system.py: SystemControl (imports from all modules above)
