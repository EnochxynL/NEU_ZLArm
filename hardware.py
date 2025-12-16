import time
from zlink import ZLink

DEFAULT_CMD = '#000P1500T1000!#001P2150T1000!#002P2300T1000!#003P1000T1000!#004P1500T1000!#005P1500T1000!'

def convert_to_four_digit_string(number):
    '''
    功能：使用字符串格式化，其中"{:04d}"表示使用4位数字，不足的地方用0填充
    参数: number -- 需要格式化的数字
    返回: 结果字符串
    '''
    # 使用字符串格式化，其中"{:04d}"表示使用4位数字，不足的地方用0填充
    result = "{:04d}".format(number)
    return result

class Hardware:
    DEBUG: bool = True

    def __init__(self, z: ZLink):
        '''z可以是ZLink类也可以是ZUart类'''
        # 串口部分
        self.pwm=[0,0,0,0,0]
        self.old_pwm=[0,0,0,0,0]
        self.count=int(0)
        self.z=z
        self.servo_reset()

    def start_hard(self):
        return self.z.open_port()
        
    def send_command(self,joint_angles: list,time: str):
        '''
        发送舵机指令
        
        :param joint_angles: 5个舵机的目标角度，单位为度
        :param time: 运动时间，单位为毫秒，字符串格式，如'0500'
        
        串口格式：#000P1500T1000!
        #: 舵机ID，000-006
        P: PWM脉宽，0500-2500
        T: 时间（毫秒），0000-9999
        !: 断句
        '''
        # 生成串口指令
        self.pwm[0]=(int)(1500+1400*joint_angles[0]/180)
        self.pwm[1]=(int)( 800+1400*joint_angles[1]/180)
        self.pwm[2]=(int)(1500-1400*joint_angles[2]/180)
        # self.pwm[3]=(int)(1500-1000*joint_angles[3]/135)
        self.pwm[3]=(int)(1500+1000*joint_angles[3]/135) # [x]
        self.pwm[4]=(int)(1500+1400*joint_angles[4]/180)
        command=[]
        for i in range(5):
            if abs(self.pwm[i]-self.old_pwm[i])>=2:#pwm差值太小就别法信息了，防止引起抖动
                command.append('#00'+str(i)+'P'+convert_to_four_digit_string(self.pwm[i])+'T'+time+'!')
                self.old_pwm[i]=self.pwm[i]
        command_string='{'
        for i in range(len(command)):
            command_string+=command[i]
        command_string+='}'
        # 指令打印
        if self.DEBUG:
            print(command_string)
        # 串口发送控制
        if self.z.is_open():
            self.count+=1
            self.z.send_data(command_string.encode('utf-8'))
    
    def set_grapper_pwm(self,pwm,_time='0500'):
        time.sleep(0.01)
        command_string='#005P'+convert_to_four_digit_string(int(pwm))+'T'+_time+'!'
        # 指令打印
        if self.DEBUG:
            print(command_string)
        # 串口发送控制
        if self.z.is_open():
            self.z.send_data(command_string.encode('utf-8'))

baudrate_options=["9600","19200","115200"]
import serial.tools.list_ports  
def get_serial_port():
    port_list = []
    portlist  = list(serial.tools.list_ports.comports())
    for port in portlist:
        port_list.append(port.device)
    return port_list 
