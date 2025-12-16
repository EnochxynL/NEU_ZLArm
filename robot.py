from simulator import Simulator
from hardware import Hardware
from kinematic import inverse_kinematic

import time

class Robot:
    def __init__(self, sim: Simulator, hard: Hardware):
        self.sim = sim
        self.hard = hard
        # 启动仿真
        if self.sim is not None: self.sim.start_sim()
        # 运行串口通信
        if self.hard is not None: self.hard.start_hard()

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
        if self.sim is not None: self.sim.step_sim(joint_angles)
        if self.hard is not None: self.hard.send_command(joint_angles, time)

    def set_grapper_pwm(self, pwm: int, time: str = '0500'):
        '''
        设置夹爪舵机PWM值
        '''
        if self.sim is not None: self.sim.set_grapper(pwm)
        if self.hard is not None: self.hard.set_grapper_pwm(pwm, time)
        
    def servo_reset(self):
        self.send_command([0,90,0,0,0],time='1000')
        time.sleep(1)
        self.set_grapper_pwm(1300)
        time.sleep(0.01)

    def goto(self,x,y,z,roll,pitch,p_direction='bio',p_step=1):
        ret,_joint_angles,best_alpha=inverse_kinematic(x,y,z,roll,pitch,p_direction,p_step)
        if not ret:
            print('无法到达指定位置')
            return False
        else:
            print('逆解关节角：',_joint_angles[0])
            self.send_command(_joint_angles[0],time='1000')
            return True
