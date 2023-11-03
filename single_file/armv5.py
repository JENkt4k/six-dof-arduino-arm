import tkinter as tk
from tkinter import ttk
import serial
import serial.tools.list_ports
import time

class ServoControl:
    def __init__(self, root):
        self.root = root
        self.root.title("Servo Control")

        self.available_ports = [port.device for port in serial.tools.list_ports.comports()]
        self.port_var = tk.StringVar(value=self.available_ports[0] if self.available_ports else '')
        self.port_dropdown = ttk.Combobox(root, textvariable=self.port_var, values=self.available_ports)
        self.port_dropdown.grid(row=0, column=1, padx=10, pady=10)

        self.connect_btn = ttk.Button(root, text="Connect", command=self.connect_to_arduino)
        self.connect_btn.grid(row=0, column=2, padx=10, pady=10)

        self.servo_sliders = []
        self.last_positions = [-1] * 6  # Initialize with invalid positions
        self.last_command_time = [0] * 6  # Initialize last command times
        self.debounce_delay = 0.05  # 0.5 second debounce delay

        for i in range(6):  # Create sliders for 6 servos
            slider = ttk.Scale(root, from_=0, to=180, orient=tk.HORIZONTAL, command=lambda v, idx=i: self.update_servo(idx))
            slider.grid(row=i+1, column=1, padx=10, pady=10)
            self.servo_sliders.append(slider)

        self.log_text = tk.Text(root, height=10, width=50)
        self.log_text.grid(row=7, column=0, columnspan=3, padx=10, pady=10)

    def connect_to_arduino(self):
        selected_port = self.port_var.get()
        try:
            self.arduino = serial.Serial(selected_port, 9600, timeout=1)
            self.log_text.insert(tk.END, f"Connected to {selected_port}\n")
            self.log_text.see(tk.END)
        except serial.SerialException as e:
            self.log_text.insert(tk.END, f"Failed to connect to {selected_port}: {e}\n")
            self.log_text.see(tk.END)

    def update_servo(self, index):
        current_time = time.time()
        if current_time - self.last_command_time[index] > self.debounce_delay:
            angle = int(self.servo_sliders[index].get())
            if angle != self.last_positions[index]:
                self.last_positions[index] = angle
                self.last_command_time[index] = current_time
                command = f"S{index},{angle}\n"
                if self.arduino and self.arduino.isOpen():
                    self.arduino.write(command.encode())
                    self.log_text.insert(tk.END, f"Sent: {command}")
                    self.log_text.see(tk.END)

    def on_closing(self):
        if self.arduino:
            self.arduino.close()
        self.root.destroy()

root = tk.Tk()
app = ServoControl(root)
root.protocol("WM_DELETE_WINDOW", app.on_closing)
root.mainloop()
