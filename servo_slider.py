import time
import tkinter as tk
from tkinter import ttk
import logging


class ServoSlider(tk.Frame):
    def __init__(self, parent, channel, name, arduino_manager, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.logger = logging.getLogger(__name__)
        self.channel = channel
        self.name = name
        self.arduino_manager = arduino_manager
        self.last_positions = -1  # Initialize with invalid positions
        self.last_command_time = 0  # Initialize last command times
        self.debounce_delay = 0.015  # Debounce delay in seconds
        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self, text=f"{self.name} (Ch {self.channel}):")
        self.label.grid(row=0, column=0, padx=10, pady=5)

        self.slider = ttk.Scale(self,
          from_=0, 
          to=180, 
          orient=tk.HORIZONTAL,
          command=lambda value, ch=self.channel: self.on_slider_update(ch, value))
        self.slider.grid(row=0, column=1, padx=10, pady=5)

        self.enable_var = tk.BooleanVar(value=True)
        self.enable_check = ttk.Checkbutton(self, variable=self.enable_var, command=self.toggle_enable)
        self.enable_check.grid(row=0, column=2, padx=10, pady=5)

    def set_state(self, state):
        self.slider['state'] = state
        self.enable_check['state'] = state

    def toggle_enable(self):
        if self.enable_var.get():
            self.slider['state'] = 'normal'
        else:
            self.slider['state'] = 'disabled'

    def on_slider_update(self, channel, value):
      position = int(float(value))  # Convert the value to an integer
      # Add any debouncing or rate-limiting logic here if necessary
      #self.arduino_manager.send_servo_position(channel, position)
      self.update_servo(channel, position)
    
    def update_servo(self, channel, position):
        current_time = time.time()
        if current_time - self.last_command_time > self.debounce_delay:
            angle = int(self.slider.get())
            if angle != self.last_positions:
                self.last_position = angle
                self.last_command_time = current_time
                #self.logger.info('{channel}, {position}') # this works but we can drop down into am
                self.arduino_manager.send_servo_position(channel, position)
