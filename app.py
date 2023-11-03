import tkinter as tk
from tkinter import ttk, messagebox
from pwm_control_panel import PWMControlPanel
from arduino_manager import ArduinoManager
from dialog import SettingsDialog, load_settings, save_settings
import serial.tools.list_ports
import logging

#handles log display
class TextHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)
        self.text_widget.configure(state='normal')
        self.text_widget.insert(tk.END, msg + '\n')
        self.text_widget.configure(state='disabled')
        self.text_widget.see(tk.END)

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Servo Control Panel")

        self.settings = load_settings()

        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        self.add_menus()

        self.arduino_manager = None

        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(side=tk.TOP, fill=tk.X)
        self.create_com_port_dropdown(self.top_frame)

        self.slider_panel = tk.Frame(self.root)
        self.slider_panel.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.pwm_control_panel = None

        self.setup_logging()
        
    def setup_logging(self):
        self.log_text = tk.Text(self.root, height=10, state='disabled')
        self.log_text.pack()

        # Configure logging
        text_handler = TextHandler(self.log_text)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        text_handler.setFormatter(formatter)
        logging.getLogger().addHandler(text_handler)
        logging.getLogger().setLevel(logging.INFO)

    def add_menus(self):
        settings_menu = tk.Menu(self.menu_bar, tearoff=0)
        settings_menu.add_command(label="Settings", command=self.open_settings_dialog)
        self.menu_bar.add_cascade(label="Options", menu=settings_menu)

    def open_settings_dialog(self):
        dialog = SettingsDialog(self.root, title="Settings", settings=self.settings)
        try:
            self.pwm_control_panel.update_settings()
        except AttributeError:
            print('pwm_control_panel not yet defined')

    def create_com_port_dropdown(self, parent):
        ttk.Label(self.top_frame, text="Select COM Port:").pack(side=tk.LEFT)
        self.com_port_var = tk.StringVar()
        self.com_port_dropdown = ttk.Combobox(self.top_frame, textvariable=self.com_port_var, state="readonly")

        self.com_port_list = [port.device for port in serial.tools.list_ports.comports()]
        self.com_port_dropdown['values'] = self.com_port_list

        current_com_port = self.settings.get('com_port', '')
        if current_com_port in self.com_port_list:
            self.com_port_var.set(current_com_port)
        elif self.com_port_list:
            self.com_port_var.set(self.com_port_list[0])

        self.com_port_dropdown.pack(side=tk.LEFT)

        self.connect_button = tk.Button(self.top_frame, text="Connect", command=self.connect_to_arduino)
        self.connect_button.pack(side=tk.LEFT)

    def connect_to_arduino(self):
        selected_com_port = self.com_port_var.get()
        if selected_com_port:
            try:
                self.arduino_manager = ArduinoManager(port=selected_com_port)
                self.arduino_manager.connect()
                self.initialize_pwm_control_panel()
                self.connect_button['text'] = 'Disconnect'
                self.connect_button['command'] = self.disconnect_from_arduino
                self.settings['com_port'] = selected_com_port
                save_settings(self.settings)
            except serial.SerialException as e:
                messagebox.showerror("Connection Error", f"Failed to connect to {selected_com_port}.\n{e}")
        else:
            messagebox.showwarning("COM Port Selection", "Please select a COM port to connect.")

    def disconnect_from_arduino(self):
        if self.arduino_manager:
            self.arduino_manager.disconnect()
        self.connect_button['text'] = 'Connect'
        self.connect_button['command'] = self.connect_to_arduino
        if self.pwm_control_panel:
            self.pwm_control_panel.destroy()
            self.pwm_control_panel = None

    def initialize_pwm_control_panel(self):
        if self.pwm_control_panel:  # If already created, destroy the old one
            self.pwm_control_panel.destroy()

        self.pwm_control_panel = PWMControlPanel(
            #self.root,
            self.slider_panel,
            settings=self.settings,
            arduino_manager=self.arduino_manager
        )
        self.pwm_control_panel.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.pwm_control_panel.set_state('enabled')


    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    app.run()

