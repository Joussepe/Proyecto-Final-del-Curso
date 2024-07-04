# pomodoro.py

from timer import Timer
from config import DEFAULT_POMODORO_WORK_TIME, DEFAULT_POMODORO_BREAK_TIME

class Pomodoro:
    def __init__(self, work_time, break_time, work_callback, break_callback):
        self.work_timer = Timer(work_time, work_callback)
        self.break_timer = Timer(break_time, break_callback)

    def start_work(self):
        self.work_timer.start()

    def start_break(self):
        self.break_timer.start()

    def stop(self):
        self.work_timer.stop()
        self.break_timer.stop()
