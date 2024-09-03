from PyQt5.QtCore import QThread, pyqtSignal
import serial

class SerialThread(QThread):
    data_received = pyqtSignal(str)

    def __init__(self, port='/dev/ttyS0', baudrate=9600, timeout=1):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
        self.running = True

    def run(self):
        while self.running:
            if self.ser.in_waiting > 0:
                data = self.ser.readline().decode().strip()
                self.data_received.emit(data)

    def stop(self):
        self.running = False
        self.ser.close()

    def send_data(self, data):
        self.ser.write(data.encode())
