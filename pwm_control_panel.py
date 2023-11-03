import tkinter as tk
from tkinter import ttk
from servo_slider import ServoSlider
from dialog import load_settings, save_settings
from PIL import Image, ImageTk

class PWMControlPanel(tk.Frame):
    def __init__(self, parent, settings, arduino_manager, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.settings = settings
        self.arm_image_path = settings.get('arm_image', 'Arduino-Robot-Arm-3D-Model.png')
        self.arduino_manager = arduino_manager
        self.servo_sliders = []
        self.last_positions = [-1] * 6  # Initialize with invalid positions
        self.last_command_time = [0] * 6  # Initialize last command times
        self.debounce_delay = 0.015  # Debounce delay in seconds
        self.create_widgets()
        self.set_state('disabled')  # Initially disable all widgets

    def create_widgets(self):
        # Create and layout servo sliders based on settings
        for i in range(self.settings['num_channels']):
            servo_name = self.settings['channel_names'][i]
            servo_slider = ServoSlider(self, i, servo_name, self.arduino_manager)
            servo_slider.grid(row=i, column=0, padx=10, pady=5, sticky="ew")
            self.servo_sliders.append(servo_slider)

        # # Settings button
        # self.settings_button = ttk.Button(self, text="Settings", command=self.open_settings_dialog)
        # self.settings_button.grid(row=self.settings['num_channels'], column=0, padx=10, pady=5)

    def set_state(self, state):
        # Enable or disable all slider controls
        for servo_slider in self.servo_sliders:
            servo_slider.set_state(state)

        # Enable or disable the settings button
        #self.settings_button['state'] = state

    # def open_settings_dialog(self):
    #     dialog = SettingsDialog(self, title="Settings", settings=self.settings)
    #     self.update_settings()

    def update_settings(self):
        # Reload the settings after they've potentially been changed
        self.settings = load_settings()
        # Reinitialize the PWM control panel with new settings
        self.reinitialize_servo_sliders()

    def reinitialize_servo_sliders(self):
        # Destroy all current servo sliders
        for slider in self.servo_sliders:
            slider.destroy()
        self.servo_sliders.clear()

        # Create new servo sliders based on updated settings
        for i in range(self.settings['num_channels']):
            servo_name = self.settings['channel_names'][i]
            servo_slider = ServoSlider(self, i, servo_name, self.arduino_manager)
            servo_slider.grid(row=i, column=0, padx=10, pady=5, sticky="ew")
            self.servo_sliders.append(servo_slider)

    def load_arm_image(self):
        try:
            arm_image = Image.open(self.arm_image_path)
            arm_image.thumbnail((200, 200))  # Resize to fit the GUI
            arm_photo = ImageTk.PhotoImage(arm_image)
            self.arm_label = tk.Label(self, image=arm_photo)
            self.arm_label.image = arm_photo  # Keep a reference!
            self.arm_label.grid(row=0, column=1, rowspan=self.settings['num_channels'], padx=10, pady=10, sticky='ns')
        except FileNotFoundError:
            self.arm_label = tk.Label(self, text="Image not found")
            self.arm_label.grid(row=0, column=1, rowspan=self.settings['num_channels'], padx=10, pady=10, sticky='ns')
