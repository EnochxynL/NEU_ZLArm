from zlink import ZLink
from hardware import Hardware
from simulator import Simulator
from robot import Robot

import numpy as np

import time


def test_reset():
    z=ZLink('COM11',115200)
    hard = Hardware(z)
    sim = Simulator()
    robot = Robot(sim, hard)

    time.sleep(3)
    robot.send_command([0, 90, 0, 0, 0],time='2000')
    time.sleep(3)
    robot.send_command([30, 30, 30, 30, 30],time='2000')
    time.sleep(3)
    robot.send_command([-38.65980825409009, 124.17268651474643, -133.91521244290925, -7.25747407183718, 0],time='2000')
    time.sleep(3)
    robot.send_command([-38.65980825409009, 124.17268651474643, -30.91521244290925, -7.25747407183718, 0],time='2000')
    time.sleep(3)
    robot.send_command([-38.65980825409009, 124.17268651474643, -100.91521244290925, -7.25747407183718, 0],time='2000')
    time.sleep(3)
    robot.send_command([-38.65980825409009, 124.17268651474643, -110.91521244290925, -7.25747407183718, 0],time='2000')
    time.sleep(3)
    robot.send_command([-38.65980825409009, 124.17268651474643, -120.91521244290925, -7.25747407183718, 0],time='2000')
    time.sleep(3)
    robot.send_command([-38.65980825409009, 124.17268651474643, -130.91521244290925, -7.25747407183718, 0],time='2000')
    time.sleep(3)
    robot.send_command([-38.65980825409009, 124.17268651474643, -130.91521244290925, -7.25747407183718, 0],time='2000')
    time.sleep(3)
    robot.send_command([-38.65980825409009, 124.17268651474643, 120.91521244290925, -7.25747407183718, 0],time='2000')



def test_move():
    z=ZLink('COM11',115200)
    hard = Hardware(z)
    sim = Simulator()
    robot = Robot(sim, hard)

    time.sleep(4)
    robot.send_command([0, 96,-36, -96, 0],time='1000')
    time.sleep(2)
    robot.set_grapper_pwm(1900,'1000')
    robot.send_command([0.0, 138.62230082742636, 15.828464537153678, -87.45076536458004, 180],time='2000')
    time.sleep(6)
    robot.send_command([0,90,30,60,0],time='1000')


def test_overlap():
    z=ZLink('COM11',115200)
    hard = Hardware(z)
    sim = Simulator()
    robot = Robot(sim, hard)
    
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

from kinematic import inverse_kinematic

def test_ik():
    z=ZLink('COM11',115200)
    hard = Hardware(z)
    sim = Simulator()
    robot = Robot(sim, hard)

    time.sleep(2)
    ret,_joint_angles,best_alpha=inverse_kinematic(120, 120, 100, 90, -90)
    print(_joint_angles)
    if ret:
        robot.send_command(_joint_angles[0],time='1000')
    else:
        print('not ret')

def test_goto():
    z=ZLink('COM11',115200)
    hard = Hardware(z)
    sim = Simulator()
    robot = Robot(sim, hard)

    time.sleep(4)
    robot.goto(150, -120, 100, 0, -90)
    time.sleep(4)
    robot.goto(150, 120, 100, 0, -90)

if __name__ == '__main__':
    test_goto()
    
    while True:
        pass