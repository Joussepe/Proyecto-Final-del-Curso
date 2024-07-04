import tkinter as tk
from tkinter import messagebox
import time
import threading
import winsound

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicación de Temporizadores")

        # Temporizador Estándar
        self.standard_minutes = tk.IntVar()
        self.standard_seconds = tk.IntVar()
        self.standard_timer_label = tk.Label(root, text="Temporizador Estándar")
        self.standard_timer_label.pack()
        self.standard_minutes_entry = tk.Entry(root, textvariable=self.standard_minutes, width=5)
        self.standard_minutes_entry.pack()
        self.standard_seconds_entry = tk.Entry(root, textvariable=self.standard_seconds, width=5)
        self.standard_seconds_entry.pack()
        self.standard_display = tk.Label(root, text="00:00")
        self.standard_display.pack()
        self.standard_start_button = tk.Button(root, text="Iniciar", command=self.start_standard_timer)
        self.standard_start_button.pack()
        self.standard_pause_button = tk.Button(root, text="Pausar", command=self.pause_standard_timer)
        self.standard_pause_button.pack()
        self.standard_reset_button = tk.Button(root, text="Reiniciar", command=self.reset_standard_timer)
        self.standard_reset_button.pack()

        # Alarma
        self.alarm_time = tk.StringVar()
        self.alarm_label = tk.Label(root, text="Alarma")
        self.alarm_label.pack()
        self.alarm_entry = tk.Entry(root, textvariable=self.alarm_time)
        self.alarm_entry.pack()
        self.set_alarm_button = tk.Button(root, text="Configurar Alarma", command=self.set_alarm)
        self.set_alarm_button.pack()
        self.stop_alarm_button = tk.Button(root, text="Detener Alarma", command=self.stop_alarm)
        self.stop_alarm_button.pack()

        # Temporizador Pomodoro
        self.pomodoro_work_minutes = tk.IntVar()
        self.pomodoro_break_minutes = tk.IntVar()
        self.pomodoro_label = tk.Label(root, text="Temporizador Pomodoro")
        self.pomodoro_label.pack()
        self.pomodoro_work_entry = tk.Entry(root, textvariable=self.pomodoro_work_minutes, width=5)
        self.pomodoro_work_entry.pack()
        self.pomodoro_break_entry = tk.Entry(root, textvariable=self.pomodoro_break_minutes, width=5)
        self.pomodoro_break_entry.pack()
        self.pomodoro_display = tk.Label(root, text="00:00")
        self.pomodoro_display.pack()
        self.pomodoro_start_button = tk.Button(root, text="Iniciar", command=self.start_pomodoro)
        self.pomodoro_start_button.pack()
        self.pomodoro_pause_button = tk.Button(root, text="Pausar", command=self.pause_pomodoro)
        self.pomodoro_pause_button.pack()
        self.pomodoro_reset_button = tk.Button(root, text="Reiniciar", command=self.reset_pomodoro)
        self.pomodoro_reset_button.pack()

        self.standard_timer_running = False
        self.pomodoro_running = False
        self.alarm_running = False
        self.is_work_time = True

    def update_display(self, label, time_left):
        minutes = time_left // 60
        seconds = time_left % 60
        label.config(text=f"{minutes:02}:{seconds:02}")

    def play_alarm(self):
        winsound.Beep(1000, 3000)  # Beep sound for 3 seconds

    def start_standard_timer(self):
        self.standard_timer_running = True
        self.standard_time_left = self.standard_minutes.get() * 60 + self.standard_seconds.get()
        self.run_standard_timer()

    def run_standard_timer(self):
        if self.standard_timer_running and self.standard_time_left > 0:
            self.standard_time_left -= 1
            self.update_display(self.standard_display, self.standard_time_left)
            self.root.after(1000, self.run_standard_timer)
        elif self.standard_time_left == 0:
            self.play_alarm()

    def pause_standard_timer(self):
        self.standard_timer_running = False

    def reset_standard_timer(self):
        self.standard_timer_running = False
        self.standard_time_left = 0
        self.update_display(self.standard_display, self.standard_time_left)

    def set_alarm(self):
        alarm_time_str = self.alarm_time.get()
        alarm_time = time.strptime(alarm_time_str, "%H:%M")
        current_time = time.localtime()
        alarm_seconds = (alarm_time.tm_hour * 3600 + alarm_time.tm_min * 60) - (current_time.tm_hour * 3600 + current_time.tm_min * 60 + current_time.tm_sec)
        if alarm_seconds < 0:
            alarm_seconds += 86400  # Add 24 hours in seconds
        self.alarm_running = True
        self.root.after(alarm_seconds * 1000, self.trigger_alarm)

    def trigger_alarm(self):
        if self.alarm_running:
            self.play_alarm()
            messagebox.showinfo("Alarma", "¡La alarma está sonando!")

    def stop_alarm(self):
        self.alarm_running = False

    def start_pomodoro(self):
        self.pomodoro_running = True
        self.pomodoro_work_time = self.pomodoro_work_minutes.get() * 60
        self.pomodoro_break_time = self.pomodoro_break_minutes.get() * 60
        self.is_work_time = True
        self.pomodoro_time_left = self.pomodoro_work_time
        self.run_pomodoro()

    def run_pomodoro(self):
        if self.pomodoro_running and self.pomodoro_time_left > 0:
            self.pomodoro_time_left -= 1
            self.update_display(self.pomodoro_display, self.pomodoro_time_left)
            self.root.after(1000, self.run_pomodoro)
        elif self.pomodoro_time_left == 0:
            self.play_alarm()
            if self.is_work_time:
                self.pomodoro_time_left = self.pomodoro_break_time
                self.is_work_time = False
            else:
                self.pomodoro_time_left = self.pomodoro_work_time
                self.is_work_time = True
            self.run_pomodoro()

    def pause_pomodoro(self):
        self.pomodoro_running = False

    def reset_pomodoro(self):
        self.pomodoro_running = False
        self.pomodoro_time_left = 0
        self.update_display(self.pomodoro_display, self.pomodoro_time_left)

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()