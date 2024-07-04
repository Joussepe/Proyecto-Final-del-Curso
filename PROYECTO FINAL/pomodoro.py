# pomodoro.py

from timer import Timer
from config import POMODORO_WORK_TIME, POMODORO_BREAK_TIME

class Pomodoro:
    def __init__(self, work_callback, break_callback):
        self.work_timer = Timer(POMODORO_WORK_TIME, work_callback)
        self.break_timer = Timer(POMODORO_BREAK_TIME, break_callback)

    def start_work(self):
        self.work_timer.start()

    def start_break(self):
        self.break_timer.start()

    def stop(self):
        self.work_timer.stop()
        self.break_timer.stop()