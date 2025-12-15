from zuart import ZUart
from hardware import Hardware
from robot import Robot
import time

from hcsr04 import HCSR04

def test_goto():
    z=ZUart('COM11',115200)
    hard = Hardware(z)
    robot = Robot(None, hard)

    time.sleep(4)
    robot.goto(150, -120, 100, 0, -90)
    time.sleep(4)
    robot.goto(150, 120, 100, 0, -90)

def test_ultrasonic():
    z=ZUart('COM11',115200)
    hard = Hardware(z)
    robot = Robot(None, hard)

    chaoshengbo = HCSR04(trigger_pin=2, echo_pin=4)      # 定义超声波模块Tring控制管脚及超声波模块Echo控制管脚,S6接口

if __name__ == '__main__':
    test_goto()