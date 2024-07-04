# alarm.py

import threading
import time
import pygame
from tkinter import messagebox

class Alarm(threading.Thread):
    def __init__(self, label, time, sound_file):
        super().__init__()
        self.label = label
        self.time = time
        self.sound_file = sound_file
        self.is_playing = False
        self.is_running = True

    def run(self):
        while self.is_running:
            now = time.strftime('%H:%M', time.localtime())
            if now == self.time:
                self.play_alarm()
                break
            time.sleep(1)

    def play_alarm(self):
        if not self.is_playing:
            pygame.init()
            pygame.mixer.music.load(self.sound_file)
            pygame.mixer.music.play(loops=-1)
            self.is_playing = True
            messagebox.showinfo("Alarm", f"Time's up! Alarm: {self.label}")

            # Mostrar opciones de posponer o cancelar
            choice = messagebox.askyesno("Alarm", f"Would you like to snooze for 1 minute?")
            if choice:
                time.sleep(60)  # Pausar durante 1 minuto y luego detener el sonido
            pygame.mixer.music.stop()
            self.is_playing = False

    def stop(self):
        self.is_running = False
