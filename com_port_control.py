import tkinter as tk
from tkinter import ttk
from arduino_manager import ArduinoManager

class COMPortControl(tk.Frame):
    def __init__(self, parent, arduino_manager, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.arduino_manager = arduino_manager

        self.com_ports_label = tk.Label(self, text="Select COM Port:")
        self.com_ports_label.pack(side="top", pady=5)

        self.com_ports = ttk.Combobox(self, values=self.arduino_manager.find_ports())
        self.com_ports.pack(side="top", pady=5)
        self.com_ports.bind('<<ComboboxSelected>>', self.on_com_port_selected)

        self.connect_button = tk.Button(self, text="Connect", command=self.connect_arduino)
        self.connect_button.pack(side="top", pady=5)

    def on_com_port_selected(self, event=None):
        selected_port = self.com_ports.get()
        if selected_port:
            self.connect_button.config(text="Connect", state="normal")

    def connect_arduino(self):
        if self.arduino_manager.is_connected():
            self.arduino_manager.disconnect()
            self.connect_button.config(text="Connect")
        else:
            selected_port = self.com_ports.get()
            if self.arduino_manager.connect(selected_port):
                self.connect_button.config(text="Disconnect")
            else:
                tk.messagebox.showerror("Connection Failed", f"Could not connect to {selected_port}")

    def refresh_ports(self):
        # Method to refresh the list of COM ports
        self.com_ports['values'] = self.arduino_manager.find_ports()
        if self.arduino_manager.current_port not in self.com_ports['values']:
            self.connect_button.config(text="Connect", state="disabled")
