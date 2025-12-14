from zlink import ZLink
from simulator import Simulator
from robot import Robot

import time


def test_reset():
    uart=ZLink('COM11',115200)
    sim = Simulator()
    robot = Robot(sim, uart)

    time.sleep(2)
    robot.send_command([0, 90, 0, 0, 0],time='2000')
    time.sleep(2)
    robot.send_command([30, 30, 30, 30, 30],time='2000')



def test_move():
    uart=ZLink('COM11',115200)
    sim = Simulator()
    robot = Robot(sim, uart)

    time.sleep(4)
    robot.send_command([0, 96,-36, -96, 0],time='1000')
    time.sleep(2)
    robot.set_grapper_pwm(1900,'1000')
    robot.send_command([0.0, 138.62230082742636, 15.828464537153678, -87.45076536458004, 180],time='2000')
    time.sleep(6)
    robot.send_command([0,90,30,60,0],time='1000')


def test_overlap():
    uart=ZLink('COM11',115200)
    sim = Simulator()
    robot = Robot(sim, uart)

    
    time.sleep(4)
    robot.send_command([0, 96,-36, -96, 0],time='1000')
    time.sleep(2)
    robot.set_grapper_pwm(1900,'1000')
    robot.send_command([0.0, 138.62230082742636, 15.828464537153678, -87.45076536458004, 180],time='2000')
    
    robot.send_command([0,90,60,30,0],time='1000')
    robot.send_command([90,90,30,30,0],time='0050')
    time.sleep(0.01)
    robot.send_command([0,90,30,60,0],time='0100')

    robot.send_command([0,90,60,30,0],time='1000')
    robot.send_command([0,90,30,30,0],time='1000')
    robot.send_command([0,90,30,60,0],time='1000')

    robot.send_command([0,90,60,30,0],time='1000')
    robot.send_command([0,90,30,30,0],time='1000')
    robot.send_command([0,90,30,60,0],time='1000')

    robot.send_command([0,90,60,30,0],time='1000')
    robot.send_command([0,90,30,30,0],time='1000')
    robot.send_command([0,90,30,60,0],time='1000')

    robot.send_command([0,90,60,30,0],time='1000')
    robot.send_command([0,90,30,30,0],time='1000')
    robot.send_command([0,90,30,60,0],time='1000')

    robot.send_command([0,90,60,30,0],time='1000')
    robot.send_command([0,90,30,30,0],time='1000')
    robot.send_command([0,90,30,60,0],time='1000')

    robot.send_command([0,90,60,30,0],time='1000')
    robot.send_command([0,90,30,30,0],time='1000')
    robot.send_command([0,90,30,60,0],time='1000')


if __name__ == '__main__':
    test_reset()
    
    while True:
        pass