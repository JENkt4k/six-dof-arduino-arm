import tkinter as tk
from tkinter import ttk
import serial

class ServoControl:
    def __init__(self, root):
        self.root = root
        self.root.title("Servo Control")

        self.arduino = serial.Serial('COM6', 9600, timeout=1)  # Replace 'COM3' with your Arduino's COM port

        self.servo_sliders = []

        for i in range(6):  # 6 servos
            label = ttk.Label(root, text=f"Servo {i+1}")
            label.grid(row=i, column=0, padx=10, pady=10)

            slider = ttk.Scale(root, from_=0, to=180, orient=tk.HORIZONTAL, command=self.update_servo)
            slider.grid(row=i, column=1, padx=10, pady=10)
            self.servo_sliders.append(slider)

    def update_servo(self, _):
        for i, slider in enumerate(self.servo_sliders):
            angle = int(slider.get())
            command = f"S{i},{angle}\n"
            self.arduino.write(command.encode())

    def on_closing(self):
        self.arduino.close()
        self.root.destroy()

root = tk.Tk()
app = ServoControl(root)
root.protocol("WM_DELETE_WINDOW", app.on_closing)
root.mainloop()
