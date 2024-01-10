import time
import serial

class BarcodeScanner:
    def __init__(self, port, baudrate, timeout):
        self.ser = None
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

    def open_serial(self):
        if self.ser is None or not self.ser.is_open:
            try:
                self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            except serial.SerialException as e:
                print(f"Error opening the serial port: {e}")
                time.sleep(5)

    def close_serial(self):
        if self.ser and self.ser.is_open:
            self.ser.close()

    def read_barcode(self):
        self.open_serial()
        if self.ser and self.ser.is_open:
            try:
                barcode = self.ser.readline().decode('utf-8').rstrip()
                return barcode
            except Exception as e:
                print(str(e))
                return None
        return None