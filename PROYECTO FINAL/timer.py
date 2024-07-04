# timer.py

import time
import threading

class Timer:
    def __init__(self, duration, callback):
        self.duration = duration
        self.callback = callback
        self.running = False
        self.thread = threading.Thread(target=self.run)

    def run(self):
        end_time = time.time() + self.duration
        while self.running and time.time() < end_time:
            time.sleep(1)
        if self.running:
            self.callback()

    def start(self):
        self.running = True
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread.is_alive():
            self.thread.join()