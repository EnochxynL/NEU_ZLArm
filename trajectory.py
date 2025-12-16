import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from roboticstoolbox import mstraj
import numpy as np
from kinematic import *

def linearPlanning(p1f, p2f, dotNum,patience=0.5):
    '''
    *@brief:   笛卡尔空间直线规划函数
    *@date:    2021.9.12
    *@param:   p1f：起始点坐标，元组形式输入
    *@param:   p2f：终止点坐标，元组形式输入
    *@param:   dotNum：插值点数，以int形式输入
    *@returnParam:   pointf：规划后的点坐标list
    '''
    if not (isinstance(p1f, list) and isinstance(p2f, list)):
        print('两个路径点需要以列表的形式输入')
        return
    if len(p1f) != 3 or len(p2f) != 3:
        print('p1,p2中存在某点列表长度不为3，请检查')
        return
    pointf = []  # 存储路径点
    
    dis=np.sqrt(sum((np.array(p1f[0:3])-np.array(p2f[0:3]))**2))
    if dis<=0.5:
        pointf.append(p1f)
        pointf.append(p2f)
        return pointf
    
    deltax = (p2f[0] - p1f[0]) / dotNum
    deltay = (p2f[1] - p1f[1]) / dotNum
    deltaz = (p2f[2] - p1f[2]) / dotNum
    
    currentIndex = 0
    while currentIndex <= dotNum:
        x = p1f[0] + deltax * currentIndex
        y = p1f[1] + deltay * currentIndex
        z = p1f[2] + deltaz * currentIndex
        pointf.append([x, y, z])
        currentIndex += 1
    return pointf

def joint_planning(via,dt,tacc,qdmax=None,tsegment=None):
    if qdmax is not None:
        traj = mstraj(via, dt=dt, tacc=tacc, qdmax=qdmax)
    else:
        traj = mstraj(via, dt=dt, tacc=tacc, tsegment=tsegment)
    return traj.q

def cartesian_planning(via,dt,tacc,qdmax):
    """笛卡尔多段轨迹规划，多项式融合方案

    Args:
        via (_type_): 经过点
        dt (_type_): 采样时间间隔
        tacc (_type_): 各段加速时间
        qdmax (_type_): 各段的最大速度，即线性处速度

    Returns:
        _type_: 空间轨迹
    """
    traj = mstraj(via, dt=dt, tacc=tacc, qdmax=qdmax)
    return traj.q

