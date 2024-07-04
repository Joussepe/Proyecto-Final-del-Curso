# alarm.py

import time
import threading
from playsound import playsound
from config import ALARM_SOUND

class Alarm:
    def __init__(self, alarm_time, callback):
        self.alarm_time = alarm_time
        self.callback = callback
        self.thread = threading.Thread(target=self.run)

    def run(self):
        while True:
            current_time = time.strftime("%H:%M")
            if current_time == self.alarm_time:
                self.callback()
                break
            time.sleep(1)

    def start(self):
        self.thread.start()

    def stop(self):
        if self.thread.is_alive():
            self.thread.join()
