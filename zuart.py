from machine import UART

class ZUart:
    def __init__(self, pin=2, baud=115200):
        self.baud = baud
        self.uart2 = UART(pin, baud)  
    def open_port(self):
        self.uart2.init(self.baud, bits=8, parity=None, stop=1)
    def is_open(self): pass
    def close_port(self): pass
    def send_data(self,temp): 
        self.uart_send_flag = 1
        self.uart2.write(temp)                                      # 串口发送数据
    def read_data(self): pass
    def read_data_until(self,data): pass
    def read_data_until_timeout(self,data,timeout): pass

    # 串口接收数据，主要处理数据接受格式，主要格式为<...> {...} $...!  #...! 4种格式，...内容长度不限
    def recv_str(self):
        if self.uart2.any() > 0:
            self.uart_receive_str = self.uart_receive_str + self.uart2.read().decode("utf-8","ignore")
        
        if self.uart_send_flag:
            self.uart_receive_str = ''
            self.uart_send_flag = 0
            return
    
        if len(self.uart_receive_str) < 2:
            return
        
        self.mode = 0
        if self.mode == 0:
            if self.uart_receive_str.find('<') >= 0:
                self.mode = 1
                #print('mode1 start')
            elif self.uart_receive_str.find('{') >= 0:
                self.mode = 2
                #print('mode2 start')
            elif self.uart_receive_str.find('#') >= 0:
                self.mode = 3
                #print('mode3 start')
            elif self.uart_receive_str.find('$') >= 0:
                self.mode = 4
                #print('mode4 start')
        
        if self.mode == 1:
            if self.uart_receive_str.find('>') >= 0:
                self.uart_get_ok = 1
                self.mode = 0
                #print('mode1 end')
        elif self.mode == 2:
            if self.uart_receive_str.find('}') >= 0:
                self.uart_get_ok = 2
                self.mode = 0
                #print('mode2 end')
        elif self.mode == 3:
            if self.uart_receive_str.find('!') >= 0:
                self.uart_get_ok = 3
                self.mode = 0
                #print('mode3 end')
        elif self.mode == 4:
            if self.uart_receive_str.find('!') >= 0:
                self.uart_get_ok = 4
                self.mode = 0
                #print('mode4 end')
 