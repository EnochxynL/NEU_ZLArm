class Z:
    def is_open(self): pass
    def close_port(self): pass
    def send_data(self,data): pass
    def read_data(self): pass
    def read_data_until(self,data): pass
    def read_data_until_timeout(self,data,timeout): pass

# from machine import UART

# class ZUart:
#     def __init__(self, pin=2, baud=115200):
#         self.baud = baud
#         self.uart2 = UART(pin, baud)  
#     def open_port(self):
#         self.uart2.init(self.baud, bits=8, parity=None, stop=1)

import serial

class ZLink(Z):
    def __init__(self, port='COM11', baud=115200, timeout = 0.1):
        self.ser = serial.Serial()
        self.ser.port=port
        self.ser.baudrate=baud
        self.ser.timeout=timeout

    def open_port(self):
        try:
            self.ser.open()
        except Exception as e:
            print(f"Error opening the serial port: {e}")
        if self.ser.isOpen():
            print("串口已成功打开")
            return True
        else:
            print("串口未成功打开")
            return False

    def is_open(self):
        return self.ser.isOpen()
    def close_port(self):
        self.ser.close()
    def send_data(self,data):
        self.ser.write(data)
    def read_data(self):
        return self.ser.readline()
    def read_data_until(self,data):
        return self.ser.read_until(data)
    def read_data_until_timeout(self,data,timeout):
        return self.ser.read_until(data,timeout)
        