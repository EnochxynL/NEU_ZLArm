import serial

class ZLink:
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
        try :
            self.ser.write(data)
        except Exception as e:
            print(f"Error sending data to serial port: {e}")
    def read_data(self):
        return self.ser.readline()
    def read_data_until(self,data):
        return self.ser.read_until(data)
    def read_data_until_timeout(self,data,timeout):
        return self.ser.read_until(data,timeout)
        