# app.py

import tkinter as tk
from tkinter import messagebox, simpledialog
import time
from math import pi, cos, sin
from alarm import Alarm
from config import ALARM_SOUND, DEFAULT_POMODORO_WORK_TIME, DEFAULT_POMODORO_BREAK_TIME
from timer import Timer
from pomodoro import Pomodoro

class ClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Clock App")
        self.root.configure(bg="#2E2E2E")
        self.alarms = []
        self.timer_app = None  # Mantener una referencia al objeto Timer
        self.create_main_interface()
        self.update_clock()

    def create_main_interface(self):
        self.clear_frame()
        self.main_frame = tk.Frame(self.root, bg="#2E2E2E")
        self.main_frame.pack(pady=20)

        self.canvas = tk.Canvas(self.main_frame, width=200, height=200, bg='#1E1E1E', highlightthickness=0)
        self.canvas.pack()

        button_style = {"bg": "#4A4A4A", "fg": "#FFFFFF", "activebackground": "#6E6E6E", "activeforeground": "#FFFFFF",
                        "bd": 0, "width": 20, "font": ("Helvetica", 12)}

        tk.Button(self.main_frame, text="Set Alarm", command=self.open_alarm_interface, **button_style).pack(pady=5)
        tk.Button(self.main_frame, text="Start Timer", command=self.open_timer_interface, **button_style).pack(pady=5)
        tk.Button(self.main_frame, text="Start Pomodoro", command=self.open_pomodoro_interface, **button_style).pack(pady=5)

        self.update_clock()

    def open_alarm_interface(self):
        self.clear_frame()
        self.alarm_frame = tk.Frame(self.root, bg="#2E2E2E")
        self.alarm_frame.pack(pady=10)

        tk.Label(self.alarm_frame, text="Set Alarm:", bg="#2E2E2E", fg="#FFFFFF", font=("Helvetica", 12)).pack(pady=5)

        entry_style = {"bg": "#4A4A4A", "fg": "#FFFFFF", "insertbackground": "#FFFFFF", "font": ("Helvetica", 12)}

        tk.Label(self.alarm_frame, text="Label:", bg="#2E2E2E", fg="#FFFFFF", font=("Helvetica", 12)).pack(pady=5)
        self.alarm_label_entry = tk.Entry(self.alarm_frame, **entry_style)
        self.alarm_label_entry.pack(pady=5)

        tk.Label(self.alarm_frame, text="Time (HH:MM):", bg="#2E2E2E", fg="#FFFFFF", font=("Helvetica", 12)).pack(pady=5)
        self.alarm_time_entry = tk.Entry(self.alarm_frame, width=5, **entry_style)
        self.alarm_time_entry.pack(side=tk.LEFT, padx=5)
        tk.Label(self.alarm_frame, text=":", bg="#2E2E2E", fg="#FFFFFF", font=("Helvetica", 12)).pack(side=tk.LEFT)
        self.alarm_minute_entry = tk.Entry(self.alarm_frame, width=5, **entry_style)
        self.alarm_minute_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(self.alarm_frame, text="Alarm Sound File:", bg="#2E2E2E", fg="#FFFFFF", font=("Helvetica", 12)).pack(pady=5)
        self.alarm_sound_entry = tk.Entry(self.alarm_frame, **entry_style)
        self.alarm_sound_entry.pack(pady=5)

        button_style = {"bg": "#4A4A4A", "fg": "#FFFFFF", "activebackground": "#6E6E6E", "activeforeground": "#FFFFFF",
                        "bd": 0, "width": 20, "font": ("Helvetica", 12)}
        tk.Button(self.alarm_frame, text="Set Alarm", command=self.set_alarm, **button_style).pack(pady=5)
        tk.Button(self.alarm_frame, text="Back", command=self.create_main_interface, **button_style).pack(pady=5)

        # Mostrar historial de alarmas con opción de editar y eliminar
        tk.Label(self.alarm_frame, text="Alarm History:", bg="#2E2E2E", fg="#FFFFFF", font=("Helvetica", 12)).pack(pady=10)
        for idx, alarm in enumerate(self.alarms):
            label_text = f"{alarm['label']} - {alarm['time']} - {alarm['sound']}"
            tk.Label(self.alarm_frame, text=label_text, bg="#2E2E2E", fg="#FFFFFF", font=("Helvetica", 10)).pack()

            # Botones para editar y eliminar
            edit_button = tk.Button(self.alarm_frame, text="Edit", command=lambda idx=idx: self.edit_alarm(idx), **button_style)
            edit_button.pack(side=tk.LEFT, padx=5)
            delete_button = tk.Button(self.alarm_frame, text="Delete", command=lambda idx=idx: self.delete_alarm(idx), **button_style)
            delete_button.pack(side=tk.LEFT, padx=5)

    def open_timer_interface(self):
        self.clear_frame()
        self.timer_frame = tk.Frame(self.root, bg="#2E2E2E")
        self.timer_frame.pack(pady=10)

        tk.Label(self.timer_frame, text="Set Timer:", bg="#2E2E2E", fg="#FFFFFF", font=("Helvetica", 12)).pack(pady=5)

        # Entry fields for time input
        self.timer_hour_entry = tk.Entry(self.timer_frame, width=5, bg="#4A4A4A", fg="#FFFFFF", insertbackground="#FFFFFF", font=("Helvetica", 12))
        self.timer_hour_entry.pack(side=tk.LEFT, padx=5)
        tk.Label(self.timer_frame, text="HH", bg="#2E2E2E", fg="#FFFFFF", font=("Helvetica", 12)).pack(side=tk.LEFT)

        self.timer_minute_entry = tk.Entry(self.timer_frame, width=5, bg="#4A4A4A", fg="#FFFFFF", insertbackground="#FFFFFF", font=("Helvetica", 12))
        self.timer_minute_entry.pack(side=tk.LEFT, padx=5)
        tk.Label(self.timer_frame, text="MM", bg="#2E2E2E", fg="#FFFFFF", font=("Helvetica", 12)).pack(side=tk.LEFT)

        self.timer_second_entry = tk.Entry(self.timer_frame, width=5, bg="#4A4A4A", fg="#FFFFFF", insertbackground="#FFFFFF", font=("Helvetica", 12))
        self.timer_second_entry.pack(side=tk.LEFT, padx=5)
        tk.Label(self.timer_frame, text="SS", bg="#2E2E2E", fg="#FFFFFF", font=("Helvetica", 12)).pack(side=tk.LEFT)

        button_style = {"bg": "#4A4A4A", "fg": "#FFFFFF", "activebackground": "#6E6E6E", "activeforeground": "#FFFFFF",
                        "bd": 0, "width": 20, "font": ("Helvetica", 12)}
        tk.Button(self.timer_frame, text="Start Timer", command=self.start_timer, **button_style).pack(pady=5)
        tk.Button(self.timer_frame, text="Stop Timer", command=self.stop_timer, **button_style).pack(pady=5)
        tk.Button(self.timer_frame, text="Back", command=self.create_main_interface, **button_style).pack(pady=5)

    def open_pomodoro_interface(self):
        self.clear_frame()
        self.pomodoro_frame = tk.Frame(self.root, bg="#2E2E2E")
        self.pomodoro_frame.pack(pady=10)

        tk.Label(self.pomodoro_frame, text="Work Time (minutes):", bg="#2E2E2E", fg="#FFFFFF", font=("Helvetica", 12)).pack(pady=5)
        self.pomodoro_work_entry = tk.Entry(self.pomodoro_frame, bg="#4A4A4A", fg="#FFFFFF", insertbackground="#FFFFFF", font=("Helvetica", 12))
        self.pomodoro_work_entry.insert(0, str(DEFAULT_POMODORO_WORK_TIME // 60))
        self.pomodoro_work_entry.pack(pady=5)

        tk.Label(self.pomodoro_frame, text="Break Time (minutes):", bg="#2E2E2E", fg="#FFFFFF", font=("Helvetica", 12)).pack(pady=5)
        self.pomodoro_break_entry = tk.Entry(self.pomodoro_frame, bg="#4A4A4A", fg="#FFFFFF", insertbackground="#FFFFFF", font=("Helvetica", 12))
        self.pomodoro_break_entry.insert(0, str(DEFAULT_POMODORO_BREAK_TIME // 60))
        self.pomodoro_break_entry.pack(pady=5)

        button_style = {"bg": "#4A4A4A", "fg": "#FFFFFF", "activebackground": "#6E6E6E", "activeforeground": "#FFFFFF",
                        "bd": 0, "width": 20, "font": ("Helvetica", 12)}
        tk.Button(self.pomodoro_frame, text="Start Pomodoro", command=self.start_pomodoro, **button_style).pack(pady=5)
        tk.Button(self.pomodoro_frame, text="Stop Pomodoro", command=self.stop_pomodoro, **button_style).pack(pady=5)
        tk.Button(self.pomodoro_frame, text="Back", command=self.create_main_interface, **button_style).pack(pady=5)
        tk.Button(self.timer_frame, text="Back", command=self.close_timer_interface, **button_style).pack(pady=5)

    def close_timer_interface(self):
        # Detener y destruir la instancia del temporizador si existe
        if self.timer_app:
            self.timer_app.stop_timer()
            self.timer_app = None

        # Volver a la interfaz principal
        self.create_main_interface()

    def clear_frame(self):
        if hasattr(self, 'main_frame'):
            self.main_frame.destroy()
        if hasattr(self, 'alarm_frame'):
            self.alarm_frame.destroy()
        if hasattr(self, 'timer_frame'):
            self.timer_frame.destroy()
        if hasattr(self, 'pomodoro_frame'):
            self.pomodoro_frame.destroy()

    def set_alarm(self):
        label = self.alarm_label_entry.get()
        time = f"{self.alarm_time_entry.get()}:{self.alarm_minute_entry.get()}"
        sound = "beep.wav"

        alarm = Alarm(label, time, sound)
        alarm.start()

        self.alarms.append({
            'label': label,
            'time': time,
            'sound': sound
        })

        messagebox.showinfo("Alarm Set", f"Alarm set for {label} - {time}")

        self.create_main_interface()

    def edit_alarm(self, idx):
        alarm = self.alarms[idx]
        new_label = simpledialog.askstring("Edit Alarm Label", "Enter new label:", initialvalue=alarm['label'])
        if new_label:
            alarm['label'] = new_label
        new_time = simpledialog.askstring("Edit Alarm Time", "Enter new time (HH:MM):", initialvalue=alarm['time'])
        if new_time:
            alarm['time'] = new_time
        new_sound = simpledialog.askstring("Edit Alarm Sound", "Enter new sound file:", initialvalue=alarm['sound'])
        if new_sound:
            alarm['sound'] = new_sound
        self.create_main_interface()

    def delete_alarm(self, idx):
        confirmed = messagebox.askyesno("Delete Alarm", "Are you sure you want to delete this alarm?")
        if confirmed:
            del self.alarms[idx]
            messagebox.showinfo("Alarm Deleted", "Alarm deleted successfully.")
            self.create_main_interface()

    def start_timer(self):
        try:
            duration = int(self.timer_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for seconds.")
            return

        self.timer_app = Timer(self.timer_frame)  # Inicializar el temporizador
        self.timer_app.remaining_time = duration  # Establecer la duración del temporizador
        self.timer_app.start_timer()

    def timer_callback(self):
        messagebox.showinfo("Timer", "Time's up!")
        sound = "beep.wav"

    def stop_timer(self):
        if hasattr(self, 'timer_app') and self.timer_app:
            self.timer_app.stop_timer()

    def start_pomodoro(self):
        work_time = int(self.pomodoro_work_entry.get()) * 60
        break_time = int(self.pomodoro_break_entry.get()) * 60
        self.pomodoro = Pomodoro(work_time, break_time, self.pomodoro_work_callback, self.pomodoro_break_callback)
        self.pomodoro.start_work()

    def stop_pomodoro(self):
        if hasattr(self, 'pomodoro'):
            self.pomodoro.stop()

    def update_clock(self):
        now = time.localtime()
        self.draw_clock(now)
        self.root.after(1000, self.update_clock)

    def draw_clock(self, now):
        self.canvas.delete("all")

        center_x, center_y = 100, 100
        radius = 80

        self.canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, fill="#1E1E1E")

        for i in range(12):
            angle = pi/6 * i
            x = center_x + radius * 0.85 * sin(angle)
            y = center_y - radius * 0.85 * cos(angle)
            self.canvas.create_text(x, y, text=str(i if i != 0 else 12), fill="#FFFFFF", font=("Helvetica", 10))

        hour = now.tm_hour % 12 + now.tm_min / 60.0
        minute = now.tm_min + now.tm_sec / 60.0
        second = now.tm_sec

        self.draw_hand(center_x, center_y, radius * 0.5, pi/6 * hour, "#FFFFFF")
        self.draw_hand(center_x, center_y, radius * 0.7, pi/30 * minute, "#FFFFFF")
        self.draw_hand(center_x, center_y, radius * 0.9, pi/30 * second, "#FF0000")

    def draw_hand(self, x, y, length, angle, color):
        end_x = x + length * sin(angle)
        end_y = y - length * cos(angle)
        self.canvas.create_line(x, y, end_x, end_y, width=2, fill=color)

    def clear_frame(self):
        if hasattr(self, 'main_frame'):
            self.main_frame.destroy()
        if hasattr(self, 'alarm_frame'):
            self.alarm_frame.destroy()
        if hasattr(self, 'timer_frame'):
            self.timer_frame.destroy()
        if hasattr(self, 'pomodoro_frame'):
            self.pomodoro_frame.destroy()
            
if __name__ == "__main__":
    root = tk.Tk()
    clock_app = ClockApp(root)
    root.mainloop()
