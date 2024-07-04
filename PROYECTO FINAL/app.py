# app.py

import tkinter as tk
from tkinter import messagebox
from timer import Timer
from pomodoro import Pomodoro
from alarm import Alarm
from config import ALARM_SOUND

class ClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Clock App")
        self.create_main_interface()

    def create_main_interface(self):
        self.clear_frame()
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=20)

        tk.Button(self.main_frame, text="Set Alarm", command=self.open_alarm_interface, width=20).pack(pady=5)
        tk.Button(self.main_frame, text="Start Timer", command=self.open_timer_interface, width=20).pack(pady=5)
        tk.Button(self.main_frame, text="Start Pomodoro", command=self.open_pomodoro_interface, width=20).pack(pady=5)

    def open_alarm_interface(self):
        self.clear_frame()
        self.alarm_frame = tk.Frame(self.root)
        self.alarm_frame.pack(pady=10)

        tk.Label(self.alarm_frame, text="Set Alarm (HH:MM):").pack(side=tk.LEFT)
        self.alarm_time_entry = tk.Entry(self.alarm_frame)
        self.alarm_time_entry.pack(side=tk.LEFT)
        tk.Button(self.alarm_frame, text="Set Alarm", command=self.set_alarm).pack(side=tk.LEFT)
        tk.Button(self.alarm_frame, text="Back", command=self.create_main_interface).pack(pady=5)

    def open_timer_interface(self):
        self.clear_frame()
        self.timer_frame = tk.Frame(self.root)
        self.timer_frame.pack(pady=10)

        tk.Label(self.timer_frame, text="Set Timer (seconds):").pack(side=tk.LEFT)
        self.timer_entry = tk.Entry(self.timer_frame)
        self.timer_entry.pack(side=tk.LEFT)
        tk.Button(self.timer_frame, text="Start Timer", command=self.start_timer).pack(side=tk.LEFT)
        tk.Button(self.timer_frame, text="Stop Timer", command=self.stop_timer).pack(side=tk.LEFT)
        tk.Button(self.timer_frame, text="Back", command=self.create_main_interface).pack(pady=5)

    def open_pomodoro_interface(self):
        self.clear_frame()
        self.pomodoro_frame = tk.Frame(self.root)
        self.pomodoro_frame.pack(pady=10)

        tk.Button(self.pomodoro_frame, text="Start Pomodoro", command=self.start_pomodoro).pack(side=tk.LEFT, pady=5)
        tk.Button(self.pomodoro_frame, text="Stop Pomodoro", command=self.stop_pomodoro).pack(side=tk.LEFT, pady=5)
        tk.Button(self.pomodoro_frame, text="Back", command=self.create_main_interface).pack(pady=5)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def set_alarm(self):
        alarm_time = self.alarm_time_entry.get()
        self.alarm = Alarm(alarm_time, self.alarm_callback)
        self.alarm.start()
        messagebox.showinfo("Alarm Set", f"Alarm set for {alarm_time}")

    def start_timer(self):
        duration = int(self.timer_entry.get())
        self.timer = Timer(duration, self.timer_callback)
        self.timer.start()

    def stop_timer(self):
        if hasattr(self, 'timer'):
            self.timer.stop()

    def start_pomodoro(self):
        self.pomodoro = Pomodoro(self.pomodoro_work_callback, self.pomodoro_break_callback)
        self.pomodoro.start_work()

    def stop_pomodoro(self):
        if hasattr(self, 'pomodoro'):
            self.pomodoro.stop()

    def alarm_callback(self):
        playsound(ALARM_SOUND)
        messagebox.showinfo("Alarm", "Time's up!")

    def timer_callback(self):
        messagebox.showinfo("Timer", "Time's up!")

    def pomodoro_work_callback(self):
        messagebox.showinfo("Pomodoro", "Work time is over! Take a break.")
        self.pomodoro.start_break()

    def pomodoro_break_callback(self):
        messagebox.showinfo("Pomodoro", "Break time is over! Back to work.")
        self.pomodoro.start_work()

if __name__ == "__main__":
    root = tk.Tk()
    app = ClockApp(root)
    root.mainloop()