from simulator import Simulator
from zlink import Hardware

class Robot:
    def __init__(self, sim: Simulator, hard: Hardware):
        self.sim = sim
        self.hard = hard
        # 启动仿真
        self.sim.start_sim()
        # 运行串口通信
        self.hard.start_hard()

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

        [-180, 180]
        [0, 180]
        []
        []
        []

        '''
        self.sim.step_sim(joint_angles)
        self.hard.send_command(joint_angles, time)

    def set_grapper_pwm(self, pwm: int, time: str = '0500'):
        '''
        设置夹爪舵机PWM值
        '''
        self.sim.set_grapper(pwm)
        self.hard.set_grapper_pwm(pwm, time)
