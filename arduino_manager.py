import serial
import logging

class ArduinoManager:
    def __init__(self, port):
        self.port = port
        self.connection = None
        self.logger = logging.getLogger(__name__)

    def connect(self):
        if self.connection is None:
            #self.connection = serial.Serial(self.port, 9600, timeout=1)
            try:
                # Assume self.serial is a serial.Serial instance
                self.connection = serial.Serial(self.port, 9600, timeout=1)
                #self.serial.open()
                self.logger.info("Connected to Arduino")
            except Exception as e:
                self.logger.error(f"Failed to connect to Arduino: {e}")

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def send_servo_position(self, channel, position):
        if self.connection is not None:
            command = f"S{channel},{position}\n".encode()
            self.logger.info(command)
            self.connection.write(command)

    def is_connected(self):
        return self.connection is not None and self.connection.isOpen()

    def send_command(self, command):
        if self.serial_connection and self.serial_connection.isOpen():
            #self.logger.info(command.encode()) not here
            self.serial_connection.write(command.encode())
