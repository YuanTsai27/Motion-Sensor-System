class DatabaseLogger:
    databasePath = None

    def __init__(self, path):
        self.databasePath = path

    def addEntry(self, motionEvent):
        motTime = motionEvent.timeCode
        motLevel = motionEvent.alertLevel.value
        with open(self.databasePath + "/Motion_log.txt", "a") as f:
            f.write("Motion detected at " + motTime + ", ALERT " + motLevel + "\n")
