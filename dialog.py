import tkinter as tk
#from tkinter import simpledialog
from tkinter import filedialog, simpledialog
import pickle

# Function to load settings
def load_settings(filename='settings.pkl'):
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return {'num_channels': 6, 'channel_names': ['Servo #1', 'Servo #2', 'Servo #3', 'Servo #4', 'Servo #5', 'Servo #6']}

# Function to save settings
def save_settings(settings, filename='settings.pkl'):
    with open(filename, 'wb') as f:
        pickle.dump(settings, f, pickle.HIGHEST_PROTOCOL)

class SettingsDialog(simpledialog.Dialog):
    def __init__(self, parent, title=None, settings=None):
        self.settings = settings if settings else load_settings()
        super().__init__(parent, title=title)

    def body(self, frame):

        tk.Label(frame, text="Arm Image Path:").grid(row=2, column=0)
        self.image_path_var = tk.StringVar(value=self.settings.get('image_path', ''))
        self.image_path_entry = tk.Entry(frame, textvariable=self.image_path_var)
        self.image_path_entry.grid(row=2, column=1)
        
        self.browse_button = tk.Button(frame, text="Browse", command=self.browse_image)
        self.browse_button.grid(row=2, column=2)


        tk.Label(frame, text="Number of PWM Channels:").grid(row=0, column=0)
        self.num_channels_var = tk.StringVar(value=str(self.settings.get('num_channels', 6)))
        self.num_channels_entry = tk.Entry(frame, textvariable=self.num_channels_var)
        self.num_channels_entry.grid(row=0, column=1)

        tk.Label(frame, text="Channel Names (comma-separated):").grid(row=1, column=0)
        self.channel_names_var = tk.StringVar(value=','.join(self.settings.get('channel_names', [])))
        self.channel_names_entry = tk.Entry(frame, textvariable=self.channel_names_var)
        self.channel_names_entry.grid(row=1, column=1)

        return self.num_channels_entry  # initial focus
    
    def browse_image(self):
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=(("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*"))
        )
        if file_path:
            self.image_path_var.set(file_path)

    def apply(self):
        num_channels = int(self.num_channels_var.get())
        channel_names = self.channel_names_var.get().split(',')

        # Ensure that there is a name for each channel
        channel_names += [f"Servo #{i+1}" for i in range(len(channel_names), num_channels)]
        channel_names = channel_names[:num_channels]  # Ensure not to exceed the number of channels

        # Update settings
        self.settings['num_channels'] = num_channels
        self.settings['channel_names'] = channel_names


        self.settings['image_path'] = self.image_path_var.get()

        save_settings(self.settings)
