import tkinter as tk
from tkinter import ttk
import serial
import serial.tools.list_ports

class ServoControl:
    def __init__(self, root):
        self.root = root
        self.root.title("Servo Control")

        # Dropdown for COM port selection
        self.port_label = ttk.Label(root, text="Select COM Port:")
        self.port_label.grid(row=0, column=0, padx=10, pady=10)

        self.available_ports = [port.device for port in serial.tools.list_ports.comports()]
        self.port_var = tk.StringVar()
        self.port_dropdown = ttk.Combobox(root, textvariable=self.port_var, values=self.available_ports)
        if self.available_ports:
            self.port_var.set(self.available_ports[0])
        self.port_dropdown.grid(row=0, column=1, padx=10, pady=10)

        self.connect_btn = ttk.Button(root, text="Connect", command=self.connect_to_arduino)
        self.connect_btn.grid(row=0, column=2, padx=10, pady=10)

        self.servo_sliders = []

        # Text widget for logging
        self.log_text = tk.Text(root, height=10, width=50)
        self.log_text.grid(row=7, column=0, columnspan=3, padx=10, pady=10)

    def connect_to_arduino(self):
        selected_port = self.port_var.get()
        self.arduino = serial.Serial(selected_port, 9600, timeout=1)

        for i in range(6):  # 6 servos
            label = ttk.Label(self.root, text=f"Servo {i+1}")
            label.grid(row=i+1, column=0, padx=10, pady=10)

            slider = ttk.Scale(self.root, from_=0, to=180, orient=tk.HORIZONTAL, command=self.update_servo)
            slider.grid(row=i+1, column=1, padx=10, pady=10)
            self.servo_sliders.append(slider)

    def update_servo(self, _):
        for i, slider in enumerate(self.servo_sliders):
            angle = int(slider.get())
            command = f"S{i},{angle}\n"
            self.arduino.write(command.encode())

            # Log the command
            self.log_text.insert(tk.END, f"Sent: {command}")
            self.log_text.see(tk.END)  # Scroll to the latest message

    def on_closing(self):
        self.arduino.close()
        self.root.destroy()

root = tk.Tk()
app = ServoControl(root)
root.protocol("WM_DELETE_WINDOW", app.on_closing)
root.mainloop()
