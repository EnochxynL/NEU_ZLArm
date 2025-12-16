
import cv2
from PyQt5.QtCore import  QThread, pyqtSignal
import numpy as np
import pygame
import os
import time

class Interact(QThread):
    #关节空间信号
    signal_j1Neg = pyqtSignal()
    signal_j1Pos = pyqtSignal()
    signal_j2Neg = pyqtSignal()
    signal_j2Pos = pyqtSignal()
    signal_j3Neg = pyqtSignal()
    signal_j3Pos = pyqtSignal()
    signal_j4Neg = pyqtSignal()
    signal_j4Pos = pyqtSignal()
    signal_j5Neg = pyqtSignal()
    signal_j5Pos = pyqtSignal()
    signal_grapperNeg = pyqtSignal()
    signal_grapperPos = pyqtSignal()
    signal_shift_to_cartesian = pyqtSignal()
    
    #笛卡尔空间信号
    signal_xNeg = pyqtSignal()
    signal_xPos = pyqtSignal()
    signal_yNeg = pyqtSignal()
    signal_yPos = pyqtSignal()
    signal_zNeg = pyqtSignal()
    signal_zPos = pyqtSignal()
    signal_rollNeg = pyqtSignal()
    signal_rollPos = pyqtSignal()
    signal_pitchNeg = pyqtSignal()
    signal_pitchPos = pyqtSignal()
    signal_grapperNeg_2 = pyqtSignal()
    signal_grapperPos_2 = pyqtSignal()
    signal_shift_to_joint = pyqtSignal()
    
    
    def __init__(self, stick_index=0):
        super().__init__()
        self.stick_index = stick_index
        self.is_running=False
        self.cur_mode=0#  0--笛卡尔  1--关节
        # 初始化pygame
        pygame.init()
        
        
    def run(self):
        # 获取手柄
        joystick = pygame.joystick.Joystick(self.stick_index)
        joystick.init()

        # 主循环
        while True and self.is_running:

            # 获取手柄按键状态
            buttons = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]
            if buttons[7] ==True :#切换模式
                if self.cur_mode==0:#切换至关节空间控制
                    self.signal_shift_to_joint.emit()
                    self.cur_mode=1
                    #防止按键粘滞
                    time.sleep(0.15)
                else:
                    self.signal_shift_to_cartesian.emit()
                    self.cur_mode=0
                    #防止按键粘滞
                    time.sleep(0.15)
            elif buttons[0] == True:
                if self.cur_mode==0:
                    self.signal_zNeg.emit()
                    print('zNeg')
                else:
                    self.signal_j4Neg.emit()
                    print('j4Neg')
                #防止按键粘滞
                time.sleep(0.15)
            elif buttons[3] == True:
                if self.cur_mode==0:
                    self.signal_zPos.emit()
                    print('zPos')
                else:
                    self.signal_j4Pos.emit()
                    print('j4Pos')
                #防止按键粘滞
                time.sleep(0.15)
            elif buttons[2] == True:
                if self.cur_mode==0:
                    self.signal_pitchNeg.emit()
                else:
                    self.signal_j3Neg.emit()
                #防止按键粘滞
                time.sleep(0.15)
            elif buttons[1] == True:
                if self.cur_mode==0:
                    self.signal_pitchPos.emit()
                else:
                    self.signal_j3Pos.emit()
                #防止按键粘滞
                time.sleep(0.15)
            elif buttons[4] == True:
                if self.cur_mode==0:
                    self.signal_rollNeg.emit()
                else:
                    self.signal_j5Neg.emit()
                #防止按键粘滞
                time.sleep(0.15)
            elif buttons[5] == True:
                if self.cur_mode==0:
                    self.signal_rollPos.emit()
                else:                
                    self.signal_j5Pos.emit()
                #防止按键粘滞
                time.sleep(0.15)    
            # # 显示按键状态
            # for i, button_state in enumerate(buttons):
            #     button_text = f"Button {i}: {button_state}"
            #     print(button_text)    
                            
            # 获取手柄十字方向键状态
            hat = joystick.get_hat(0)
            if hat==(-1,0):
                if self.cur_mode==0:
                    self.signal_xNeg.emit()
                    print("xNeg")
                else:
                    self.signal_j1Neg.emit()
                    print('j1Neg')
                #防止按键粘滞
                time.sleep(0.15)                
            elif hat==(1,0):
                if self.cur_mode==0:
                    self.signal_xPos.emit()
                else:
                    self.signal_j1Pos.emit()
                #防止按键粘滞
                time.sleep(0.15)       
            elif hat==(0,-1):
                if self.cur_mode==0:
                    self.signal_yNeg.emit()
                    print("yNeg")
                else:
                    self.signal_j2Neg.emit()
                    print('j2Neg')
                #防止按键粘滞
                time.sleep(0.15)       
            elif hat==(0,1):
                if self.cur_mode==0:
                    self.signal_yPos.emit()
                else:
                    self.signal_j2Pos.emit()
                #防止按键粘滞
                time.sleep(0.15)       
                
            # 获取手柄轴状态
            axes = [joystick.get_axis(i) for i in range(joystick.get_numaxes())]
            if axes[4]>0.2:
                if self.cur_mode==0:
                    self.signal_grapperNeg.emit()
                    print('grap-')
                else:
                    self.signal_grapperNeg_2.emit()
                    print('grap-')
                #防止按键粘滞
                time.sleep(0.15) 
            elif axes[5]>0.2:
                if self.cur_mode==0:
                    self.signal_grapperPos.emit()
                    print('grap+')
                else:                
                    self.signal_grapperPos_2.emit()
                    print('grap+')
                #防止按键粘滞
                time.sleep(0.15)
                
                
                
            # # 显示轴状态
            # for i, axis_value in enumerate(axes):
            #     axis_text =f"Axis {i}: {axis_value:.2f}"
            #     print(axis_text)

            # # 调用函数清空终端输出
            # self.clear_terminal()
            # time.sleep(0.05)
    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_stick_list(self):
        stick_list=[]
        # 获取手柄数量
        joystick_count = pygame.joystick.get_count()
        for i in range(joystick_count): 
            stick_list.append(str(i))
        return stick_list
   
    def stop(self):
        self.is_running=False
