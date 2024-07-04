# timer.py

import tkinter as tk
from tkinter import messagebox

class Timer:
    def __init__(self, root):
        self.root = root
        self.root.title("Timer")
        self.root.configure(bg="#2E2E2E")

        self.duration = 0
        self.remaining_time = 0
        self.running = False

        self.timer_label = None
        self.start_button = None
        self.stop_button = None

        self.create_timer_interface()

    def create_timer_interface(self):
        timer_frame = tk.Frame(self.root, bg="#2E2E2E")
        timer_frame.pack(pady=20)

        label_style = {"bg": "#2E2E2E", "fg": "#FFFFFF", "font": ("Helvetica", 24)}
        self.timer_label = tk.Label(timer_frame, text="00:00:00", **label_style)
        self.timer_label.pack(pady=10)

        button_style = {"bg": "#4A4A4A", "fg": "#FFFFFF", "activebackground": "#6E6E6E", "activeforeground": "#FFFFFF",
                        "bd": 0, "width": 20, "font": ("Helvetica", 12)}
        self.start_button = tk.Button(timer_frame, text="Start", command=self.start_timer, **button_style)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(timer_frame, text="Stop", command=self.stop_timer, **button_style)
        self.stop_button.pack(pady=5)
        self.stop_button.config(state=tk.DISABLED)

    def start_timer(self):
        if not self.running:
            self.running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.update_timer()

    def stop_timer(self):
        if self.running:
            self.running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

    def update_timer(self):
        if self.running:
            self.remaining_time -= 1
            formatted_time = self.format_time(self.remaining_time)
            self.timer_label.config(text=formatted_time)
            self.root.after(1000, self.update_timer)

    def format_time(self, seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"

# Entry point for standalone usage
if __name__ == "__main__":
    root = tk.Tk()
    timer_app = Timer(root)
    root.mainloop()
