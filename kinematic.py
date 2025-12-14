import math
import numpy as np
from calculate import *
# import fprint
def jacobian(joint_angles):
    """返回一个6x5的jacobian矩阵
    参数:
   joint_angles -- 根据改进法建模得到的各个关节theta,但最后一个元素指的是第五个关节的alpha4
   注意要传弧度
    """
    #下面是DH参数，单位mm
    a1=-10
    d1=80
    a2=105
    a3=98
    a4=67+105
    theta = [joint_angles[0], joint_angles[1], joint_angles[2], joint_angles[3], 0]
    alpha4=joint_angles[4]
    J=np.zeros((6,5))
    
    J[0,0]=0
    J[0,1]=a2*math.sin(theta[2]+theta[3])+a3*math.sin(theta[3])
    J[0,2]=a3*math.sin(theta[3])
    J[0,3]=0
    J[0,4]=0
    J[1,0]=-math.sin(alpha4)*(a1+a2*math.cos(theta[1])+a3*math.cos(theta[1]+theta[2])+a4*math.cos(theta[1]+theta[2]+theta[3]))
    J[1,1]=math.cos(alpha4)*(a2*math.cos(theta[2]+theta[3])+a3*math.cos(theta[3])+a4)
    J[1,2]=math.cos(alpha4)*(a3*math.cos(theta[3])+a4)
    J[1,3]=math.cos(alpha4)*(a4)
    J[1,4]=0
    J[2,0]=-math.cos(alpha4)*(a1+a2*math.cos(theta[1])+a3*math.cos(theta[1]+theta[2])+a4*math.cos(theta[1]+theta[2]+theta[3]))
    J[2,1]=-math.sin(alpha4)*(a2*math.cos(theta[2]+theta[3])+a3*math.cos(theta[3])+a4)
    J[2,2]=-math.sin(alpha4)*(a3*math.cos(theta[3])+a4)
    J[2,3]=-math.sin(alpha4)*(a4)
    J[2,4]=0
    
    J[3,0]=math.sin(theta[1]+theta[2]+theta[3])
    J[3,1]=0
    J[3,2]=0
    J[3,3]=0
    J[3,4]=1
    J[4,0]=math.cos(alpha4)*math.cos(theta[1]+theta[2]+theta[3])
    J[4,1]=math.sin(alpha4)
    J[4,2]=math.sin(alpha4)
    J[4,3]=math.sin(alpha4)
    J[4,4]=0
    J[5,0]=-math.sin(alpha4)*math.cos(theta[1]+theta[2]+theta[3])
    J[5,1]=math.cos(alpha4)
    J[5,2]=math.cos(alpha4)
    J[5,3]=math.cos(alpha4)
    J[5,4]=0
    return J

def forward_kinematic(joint_angles):
    """
   功能 -- 机器人正运动学求解
   
   参数:
   joint_angles -- 根据改进法建模得到的各个关节theta,但最后一个元素指的是第五个关节的alpha4
   注意要传弧度
   返回:
   第五个关节坐标系的位姿
   """
    #下面是DH参数，单位mm
    a1=-10
    d1=80
    a2=105
    a3=98
    a4=67+105
    
    
    theta = [joint_angles[0], joint_angles[1], joint_angles[2], joint_angles[3], 0]
    alpha4=joint_angles[4]
    TF = np.zeros((4, 4))  # 正运动学矩阵
    TF[3, 3] = 1

    TF[0, 0] = math.cos(theta[0]) * math.cos(theta[1] + theta[2] + theta[3])
    TF[0, 1] = math.sin(theta[0]) * math.sin(alpha4) - math.cos(theta[0]) * math.sin(theta[1] + theta[2] + theta[3]) * math.cos(alpha4)
    TF[0, 2] = math.sin(theta[0]) * math.cos(alpha4) + math.cos(theta[0]) * math.sin(theta[1] + theta[2] + theta[3]) * math.sin(alpha4)
    TF[0, 3] = math.cos(theta[0]) * math.cos(theta[1] + theta[2] + theta[3]) * a4 + math.cos(theta[0]) * math.cos(theta[1] + theta[2]) * a3 + math.cos(theta[0]) * math.cos(theta[1]) * a2+math.cos(theta[0])*a1

    TF[1, 0] = math.sin(theta[0]) * math.cos(theta[1] + theta[2] + theta[3])
    TF[1, 1] = -math.cos(theta[0]) * math.sin(alpha4) - math.sin(theta[0]) * math.sin(theta[1] + theta[2] + theta[3]) * math.cos(alpha4)
    TF[1, 2] = -math.cos(theta[0]) * math.cos(alpha4) + math.sin(theta[0]) * math.sin(theta[1] + theta[2] + theta[3]) * math.sin(alpha4)
    TF[1, 3] = math.sin(theta[0]) * math.cos(theta[1] + theta[2] + theta[3]) * a4 + math.sin(theta[0]) * math.cos(theta[1] + theta[2]) * a3 + math.sin(theta[0]) * math.cos(theta[1]) * a2+math.sin(theta[0])*a1

    TF[2, 0] = math.sin(theta[1] + theta[2] + theta[3])
    TF[2, 1] = math.cos(theta[1] + theta[2] + theta[3]) * math.cos(alpha4)
    TF[2, 2] = -math.cos(theta[1] + theta[2] + theta[3]) * math.sin(alpha4)
    TF[2, 3] = math.sin(theta[1] + theta[2] + theta[3]) * a4 + math.sin(theta[1] + theta[2]) * a3 + math.sin(theta[1]) * a2 + d1
    return TF
def inverse_kinematic_analysis(x,y,z,Alpha):
    #参数设置
    l0 = 80
    l1 = 105
    l2 = 98
    l3 = 67+105
    offset=10
    #初始化定义关节角
    q1, q2, q3, q4=[0,0,0,0]
    #print("x:",x,"y:",y,"z:",z)
    # if np.abs(y) <= 1e-10:
    #     theta6 = 0.0
    # else:
    theta6 = math.atan2(y, x) * 180.0 / math.pi
    #print('原始theta6:',theta6)
    
    #修正theta6
    if x>=0:
        pass
    else:
        if y>=0:
            theta6=180-theta6
        else:
            theta6=180+theta6
    #print('修正theta6:',theta6)
    #修正xy
    x=x+offset*math.cos(theta6*math.pi/180.0)
    y=y+offset*math.sin(theta6*math.pi/180.0)
    
    y = math.sqrt(x * x + y * y)
    y = y - l3 * math.cos(Alpha * math.pi / 180.0)
    z = z - l0 - l3 * math.sin(Alpha * math.pi / 180.0)

    if z < -l0:
        result = 1
        #print(result)
        return result, q1, q2, q3, q4

    if math.sqrt(y * y + z * z) > (l1 + l2):
        result = 2
        #print(result)
        return result, q1, q2, q3, q4

    ccc = math.acos(y / math.sqrt(y * y + z * z))
    bbb = (y * y + z * z + l1 * l1 - l2 * l2) / (2 * l1 * math.sqrt(y * y + z * z))

    if bbb > 1 or bbb < -1:
        result = 3
        #print(result)
        return result, q1, q2, q3, q4

    if z < 0:
        zf_flag = -1
    else:
        zf_flag = 1

    theta5 = ccc * zf_flag + math.acos(bbb)
    theta5 = theta5 * 180.0 / math.pi

    if theta5 > 180.0 or theta5 < 0.0:
        result = 4
        #print(result)
        return result, q1, q2, q3, q4

    aaa = -(y * y + z * z - l1 * l1 - l2 * l2) / (2 * l1 * l2)

    if aaa > 1 or aaa < -1:
        result = 5
        #print(result)
        return result, q1, q2, q3, q4

    theta4 = math.acos(aaa)
    theta4 = 180.0 - theta4 * 180.0 / math.pi

    if theta4 > 135.0 or theta4 < -135.0:
        result = 6
        #print(result)
        return result, q1, q2, q3, q4

    theta3 = Alpha - theta5 + theta4

    if theta3 > 90.0 or theta3 < -90.0:
        result = 7
        #print(result)
        return result, q1, q2, q3, q4

    result=0
    q1 = theta6
    q2 = theta5
    q3 = -theta4
    q4 = theta3
    
    return result, q1, q2, q3, q4

def inverse_kinematic(x,y,z,roll,pitch,p_direction='bio',p_step=1):
    """
    功能 -- 机器人逆运动学求解
    注意 -- 事实上一般来说jibot机械臂有四组逆解,但是最后只算两组结构上省力的解
    
    参数:
    x,y,z,roll,pitch -- 末端的位姿
    p_direction --搜寻合适pitch的方向,'bio' 双向，'down'往下搜,'up'网上搜
    p_step --搜索步长
    
    返回:
    两组逆解,注意，用第一组解就够了，也就是
    ret,_joint_angles,best_alpha=inverse_kinematic(0, 360, 100, 0, 0)
    robot.send_command(_joint_angles[0],time='1000')

    坐标: 朝前为X, 朝左为Y, 朝上为Z, 右手定则
    角度: 执行器相对于机械臂末端, 如(0,0)代表直直地伸出去, 正为仰头, 负为俯头, 正为逆时针看, 负为顺时针看
    """
    alpha1=999
    alpha2=-999
    Alpha=-999
    [q1,q2,q3,q4,q5] =[0,0,0,0,0]
    [j1,j2,j3,j4,j5]=[0,0,0,0,0]
    q5 = roll      #第五个关节角就是roll角
     
    if p_direction=='bio':
        for offset in range(0, 360, p_step):
            if pitch-offset <= -180:
                break;
            ret,q1,q2,q3,q4=inverse_kinematic_analysis(x,y,z,pitch-offset)
            if ret == 0:
                alpha2=pitch-offset
                break
            
        if alpha2 == -999:
            for offset in range(p_step, 361, p_step):
                if pitch+offset > 180:
                    break;
                ret,q1,q2,q3,q4=inverse_kinematic_analysis(x,y,z,pitch+offset)
                if ret == 0:
                    alpha1=pitch+offset
                    break    
                
        #找不到就返回0
        if alpha1-alpha2>1500:
            #print("找不到合适的pitch")
            return 0,[[q1,q2,q3,q4,q5],[j1,j2,j3,j4,j5]],Alpha
        
        if abs(alpha1-pitch)<abs(alpha2-pitch):
            Alpha=alpha1
        else:
            Alpha=alpha2
        # #print("最适合的pitch:",Alpha)   
    elif p_direction=='up':
        for offset in range(0, 361, p_step):
                if pitch+offset > 180:
                    break;
                ret,q1,q2,q3,q4=inverse_kinematic_analysis(x,y,z,pitch+offset)
                if ret == 0:
                    alpha1=pitch+offset
                    break
        if alpha1 != 999:
            Alpha=alpha1
        else:
            #print("找不到合适的pitch")
            
            return 0,[[q1,q2,q3,q4,q5],[j1,j2,j3,j4,j5]],Alpha
    elif p_direction=='down':
        for offset in range(0, 361, p_step):
            if pitch-offset < -180:
                break;
            ret,q1,q2,q3,q4=inverse_kinematic_analysis(x,y,z,pitch-offset)
            if ret == 0:
                alpha2=pitch-offset
                break
        if alpha2 != -999:
            Alpha=alpha2
        else:
            #print("找不到合适的pitch")
            
            return 0,[[q1,q2,q3,q4,q5],[j1,j2,j3,j4,j5]],Alpha
        
    #最终的逆解
    ret,q1,q2,q3,q4=inverse_kinematic_analysis(x,y,z,Alpha)        
            
    #下面是验证q1和q2,3,4是不是在同一组解里面
    T =forward_kinematic([q1* math.pi / 180.0, q2* math.pi / 180.0, q3* math.pi / 180.0, q4* math.pi / 180.0, q5* math.pi / 180.0])
    #利用x,y,z约束判断
    # #print(T)
    if  (abs(T[0,3]-x)+ abs(T[1,3]-y)+ abs(T[2,3]-z)) < 1e-10:
        #print('满足xyz约束')
        pass
    else:
        q1 = q1 - 180
        #print('不满足xyz约束，修改q1')

    j1 = q1 + 180
    j2 = 180 - q2
    j3 = -q3
    j4 = -q4
    j5 = q5 + 180

    return 1,[[q1,q2,q3,q4,q5],[j1,j2,j3,j4,j5]],Alpha

if __name__ == '__main__':
    #测试逆解
    singularity=[]
    for i in range(455,99,-1):
        ret,angles,alpha=inverse_kinematic(0,0,i,0,90)
        if ret != 1:
            singularity.append(i)
            
    #print(singularity)

    T=forward_kinematic(np.deg2rad([10,80,30,-30,0]))
    print('正运动学：\n',T)
    ret=inverse_kinematic(T[0,3],T[1,3],T[2,3],0,90)
    print('逆解：\n',ret)

    ret=inverse_kinematic(-10,0,453,0,90)
    #print('逆解：',ret)
    TF=forward_kinematic(np.deg2rad(ret[1][0]))
    #print('逆解正解',TF)

    theta=[15*math.pi/180,80*math.pi/180,60*math.pi/180,50*math.pi/180,0]
    print(jacobian(theta))



    
    
    