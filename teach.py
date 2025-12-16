from trajectory import cartesian_planning, linearPlanning, joint_planning
import numpy as np
from kinematic import inverse_kinematic, forward_kinematic
import copy
import time

from hardware import convert_to_four_digit_string

class Teach:
    def __init__(self):
        #笛卡尔空间参数
        self.cartesian_old_paras=[-10,0,455,0,90]
        self.cartesian_cur_paras=[-10,0,455,0,90]
        self.cartesian_speed_opts=[0.5/50,0.5/10]
        self.cartesian_stepdis_opts=[2,6,10]
        self.cartesian_step_speed=0.5/50  #mm/ms,目前默认低速
        self.cartesian_step_dis =2     #mm默认短距离
        self.cartesian_sample_dis=0.5  #mm采样距离
        self.cartesian_plan_mode=1 #0代表直线规划，1代表一般曲线规划,默认曲线
        
        #关节空间参数
        self.joint_old_paras=[0,90,0,0,0]
        self.joint_cur_paras=[0,90,0,0,0]
        self.joint_speed_opts=[2/100,2/50]
        self.joint_stepdis_opts=[2,6,10]
        self.joint_step_speed=2/100  #度/ms,目前默认低速
        self.joint_step_dis =2     #默认短距离
        self.joint_ranges=[[-135,135],[0,180],[-135,135],[-135,135],[-135,135]]
        #关节空间下只能曲线规划
        
        self.cur_grapper_pwm=1300
        self.grapper_step=50#笛卡尔空间页设置
        self.grapper_step_2=50#关节空间页设置
    
    def check_angles(self,_joint_angles):
        if _joint_angles[0]>=self.joint_ranges[0][0] and _joint_angles[0]<=self.joint_ranges[0][1] and\
            _joint_angles[1]>=self.joint_ranges[1][0] and _joint_angles[1]<=self.joint_ranges[1][1] and\
            _joint_angles[2]>=self.joint_ranges[2][0] and _joint_angles[2]<=self.joint_ranges[2][1] and\
            _joint_angles[3]>=self.joint_ranges[3][0] and _joint_angles[3]<=self.joint_ranges[3][1] and\
            _joint_angles[4]>=self.joint_ranges[4][0] and _joint_angles[4]<=self.joint_ranges[4][1] :
            return True
        else:
            return False
            
    def cartesian_step_teach(self,ser):
        #默认采样点间隔0.5mm
        coordinate_traj=np.array(linearPlanning(self.cartesian_old_paras[0:3],self.cartesian_cur_paras[0:3],dotNum=self.cartesian_step_dis/self.cartesian_sample_dis))
        print(coordinate_traj)
        joint_angles=[]
        all_can_inverse=True
        best_alpha=-999
        for i in range(len(coordinate_traj)):
            ret,_joint_angles,best_alpha=inverse_kinematic(coordinate_traj[i,0],coordinate_traj[i,1],coordinate_traj[i,2],self.cartesian_cur_paras[3],self.cartesian_cur_paras[4])
            print(_joint_angles[0])
            if ret and self.check_angles(_joint_angles[0]):
                joint_angles.append(_joint_angles)         
            else:
                print("逆解求解失败或路径点角度超出范围，取消执行！")
                all_can_inverse=False
                self.cartesian_cur_paras=self.cartesian_old_paras
                return False
        if all_can_inverse:

            self.cartesian_old_paras[4]=self.cartesian_cur_paras[4]
            self.cartesian_cur_paras[4]=best_alpha
            t=convert_to_four_digit_string(int(self.cartesian_sample_dis/self.cartesian_step_speed))
            print(t)
            for i in range(len(joint_angles)):
                ser.send_command(np.array(joint_angles[i][0]),time=t)
                time.sleep(0.01)
            #更新对应关节空间参数
            self.joint_old_paras=self.joint_cur_paras
            self.joint_cur_paras=joint_angles[-1][0]
        return True
    
    def step_roll(self,ser):
        #更新对应关节空间参数
        self.joint_old_paras=self.joint_cur_paras
        self.joint_cur_paras[4]=self.cartesian_cur_paras[3]
        t=convert_to_four_digit_string(int(self.cartesian_step_dis/self.cartesian_step_speed))
        ser.send_command(np.array(self.joint_cur_paras),time=t)
    
    def step_pitch(self,ser,direction='up'):
        ret,_joint_angles,best_alpha=inverse_kinematic(self.cartesian_cur_paras[0],self.cartesian_cur_paras[1],self.cartesian_cur_paras[2],self.cartesian_cur_paras[3],self.cartesian_cur_paras[4],p_direction=direction,p_step=self.cartesian_step_dis)
        if ret:
            self.cartesian_old_paras[4]=self.cartesian_cur_paras[4]
            self.cartesian_cur_paras[4]=best_alpha
            print('当前alpha=',best_alpha)
            #更新对应关节空间参数
            self.joint_old_paras=self.joint_cur_paras
            self.joint_cur_paras=_joint_angles[0]
            t=convert_to_four_digit_string(int(self.cartesian_step_dis/self.cartesian_step_speed))
            ser.send_command(np.array(self.joint_cur_paras),time=t)
            return True
        else:
            self.cartesian_cur_paras=self.cartesian_old_paras
            return False
        
    def cartesian_point_teach(self,ser,points):
        #!!!!!!下面有点问题，在笛卡尔直线规划时，roll角也应该和xyz一样逐渐变化
        if self.cartesian_plan_mode==0:#直线规划,每两点之间直线运动
            for i in range(len(points)-1):
                dis=np.sqrt(sum((np.array(points[i][0:3])-np.array(points[i+1][0:3]))**2))
                if dis<=0.5:
                    print('两点间距离太小，直接动')
                t=dis/self.cartesian_step_speed
                coordinate_traj=np.array(linearPlanning(points[i][0:3],points[i+1][0:3],dotNum=t/100))
                # print("轨迹点数:",len(coordinate_traj))
                joint_angles=[]
                all_can_inverse=True
                best_alpha=-999
                for j in range(len(coordinate_traj)):
                    ret,_joint_angles,best_alpha=inverse_kinematic(coordinate_traj[j,0],coordinate_traj[j,1],coordinate_traj[j,2],points[i+1][3],points[i+1][4])
                    if ret and self.check_angles(_joint_angles[0]):
                        joint_angles.append(_joint_angles)         
                    else:
                        print("逆解求解失败或路径点角度超出范围，取消执行！")
                        all_can_inverse=False
                        break
                if all_can_inverse:
                    # t=convert_to_four_digit_string(int(self.cartesian_sample_dis/self.cartesian_step_speed))#用的还是步进示教时的时间
                    for j in range(len(joint_angles)):
                        ser.send_command(np.array(joint_angles[j][0]),time='0100')
                        time.sleep(0.01)
                    time.sleep(0.5)
                    ser.set_grapper_pwm(points[i+1][5])
                    time.sleep(1)
                    #更新笛卡尔空间参数
                    self.cartesian_cur_paras=points[i+1][0:5]
                    self.cartesian_cur_paras[4]=best_alpha
                    #更新夹具pwm
                    self.cur_grapper_pwm=points[i+1][5]
                    #更新关节空间参数
                    self.joint_old_paras=self.joint_cur_paras
                    self.joint_cur_paras=joint_angles[-1][0]
                else:#就返回最后一个可以到达的那个示教点
                    return i
            return len(points)-1
        else:#一般曲线规划
            if len(points)==0:
                return -1
            pieces=[]
            one={'via':[],'pwm':0,'startidx':0}
            one['via'].append(points[0][0:5])
            one['pwm']=points[0][5]
            one['startidx']=0
            for i in range(1,len(points)):
                if abs(points[i][5]-points[i-1][5])<=1:#pwm不变
                    if i!=len(points)-1:
                        one['via'].append(points[i][0:5])
                    else:
                        one['via'].append(points[i][0:5])
                        one['pwm']=points[i][5]
                        
                        # 深拷贝
                        deep_copy_of_one = copy.deepcopy(one)
                        # 将深拷贝对象添加到列表
                        pieces.append(deep_copy_of_one)
                else:
                    
                    one['via'].append(points[i][0:5])
                    one['pwm']=points[i][5]
                    # pieces.append(one)#截取完整的一个阶段
                    # 深拷贝
                    deep_copy_of_one = copy.deepcopy(one)
                    # 将深拷贝对象添加到列表
                    pieces.append(deep_copy_of_one)
                    one['via'].clear()
                    one['via'].append(points[i][0:5])#存入下一阶段的起始点
                    one['pwm']=points[i][5]
                    one['startidx']=i
            # print("轨迹分段:",len(pieces))       
            
            #下面进行笛卡尔曲线轨迹规划
            for j in range(len(pieces)):
                dt=self.cartesian_step_speed
                cartesian_traj=cartesian_planning(np.array(pieces[j]['via']),dt=0.1,tacc=0.5,qdmax=self.cartesian_step_speed*1000)
                # print(cartesian_traj)
                # print("分段",j,"轨迹点数:",len(cartesian_traj),'轨迹如下：',cartesian_traj)
                joint_angles=[]
                all_can_inverse=True
                best_alpha=0
                for i in range(len(cartesian_traj)):
                    ret,_joint_angles,best_alpha=inverse_kinematic(cartesian_traj[i,0],cartesian_traj[i,1],cartesian_traj[i,2],cartesian_traj[i,3],cartesian_traj[i,4])
                    if ret and self.check_angles(_joint_angles[0]):
                        joint_angles.append(_joint_angles)
                        # send_command(ser,np.array(joint_angles[0]))                
                    else:
                        print("逆解求解失败或路径点角度超出范围，取消执行！")
                        all_can_inverse=False
                        break
                if all_can_inverse:
                    # t=convert_to_four_digit_string(int(self.cartesian_sample_dis/self.cartesian_step_speed))#用的还是步进示教时的时间
                    for i in range(len(joint_angles)):
                        ser.send_command(np.array(joint_angles[i][0]),time='0100')
                        time.sleep(0.01)
                    # print('uart已发送',ser.count,'条指令')
                    #运动完就控制夹具
                    time.sleep(0.5)
                    ser.set_grapper_pwm(pieces[j]['pwm'])
                    time.sleep(1)
                    #更新笛卡尔空间参数
                    self.cartesian_cur_paras=pieces[j]['via'][-1]
                    self.cartesian_cur_paras[4]=best_alpha
                    #更新夹具pwm
                    self.cur_grapper_pwm=pieces[j]['pwm']
                    #更新关节空间参数
                    self.joint_old_paras=self.joint_cur_paras
                    self.joint_cur_paras=joint_angles[-1][0]
                else:#就返回最后一个可以到达的那个示教点
                    return pieces[j]['startidx']   
            return len(points)-1
    def joint_step_teach(self,ser):
        joints_traj=joint_planning(np.array([self.joint_old_paras,self.joint_cur_paras]),dt=0.02,tacc=0.1,tsegment=np.array([self.joint_step_dis/self.joint_step_speed/1000]))
        if all([self.check_angles(joints_traj[i]) for i in range(len(joints_traj))]):
            
            for i in range(len(joints_traj)):
                ser.send_command(np.array(joints_traj[i]),time='0020')
                time.sleep(0.01)
            T=forward_kinematic(np.deg2rad(self.joint_cur_paras))
            # print('joints:\n',self.joint_cur_paras)
            # print('T:\n',T)
            self.cartesian_cur_paras[0]=T[0,3]
            self.cartesian_cur_paras[1]=T[1,3]
            self.cartesian_cur_paras[2]=T[2,3]
            self.cartesian_cur_paras[3]=joints_traj[-1][4]
            self.cartesian_cur_paras[4]=joints_traj[-1][1]+joints_traj[-1][2]+joints_traj[-1][3]
            return True
        else:
            print('joints out of range')
            self.joint_cur_paras=self.joint_old_paras#恢复
            return False
        
    def joint_point_teach(self,ser,points):
        
        #一般曲线规划
        if len(points)==0:
            return -1
        pieces=[]
        one={'via':[],'pwm':0,'startidx':0}
        one['via'].append(points[0][0:5])
        one['pwm']=points[0][5]
        one['startidx']=0
        for i in range(1,len(points)):
            if abs(points[i][5]-points[i-1][5])<=1:#pwm不变
                if i!=len(points)-1:
                    one['via'].append(points[i][0:5])
                else:
                    one['via'].append(points[i][0:5])
                    one['pwm']=points[i][5]
                    
                    # 深拷贝
                    deep_copy_of_one = copy.deepcopy(one)
                    # 将深拷贝对象添加到列表
                    pieces.append(deep_copy_of_one)
            else:
                
                one['via'].append(points[i][0:5])
                one['pwm']=points[i][5]
                # pieces.append(one)#截取完整的一个阶段
                # 深拷贝
                deep_copy_of_one = copy.deepcopy(one)
                # 将深拷贝对象添加到列表
                pieces.append(deep_copy_of_one)
                one['via'].clear()
                one['via'].append(points[i][0:5])#存入下一阶段的起始点
                one['pwm']=points[i][5]
                one['startidx']=i
        # print("轨迹分段:",len(pieces))       
        for j in range(len(pieces)):
            
            joints_traj=joint_planning(np.array(pieces[j]['via']),dt=0.05,tacc=0.5,qdmax=self.joint_step_speed*1000)
            # print("分段",j,"轨迹点数:",len(joints_traj),'轨迹如下：',joints_traj)
            if all([self.check_angles(joints_traj[i]) for i in range(len(joints_traj))]):
                
                for i in range(len(joints_traj)):
                    ser.send_command(np.array(joints_traj[i]),time='0050')
                    time.sleep(0.01)
                #运动完就控制夹具
                # print('uart已发送',ser.count,'条指令')
                time.sleep(1)
                ser.set_grapper_pwm(pieces[j]['pwm'],_time='1000')
                time.sleep(1)
                #更新关节空间参数
                self.joint_old_paras=self.joint_cur_paras
                self.joint_cur_paras=pieces[j]['via'][-1]
                T=forward_kinematic(np.deg2rad(self.joint_cur_paras))
                self.cartesian_cur_paras[0]=T[0,3]
                self.cartesian_cur_paras[1]=T[1,3]
                self.cartesian_cur_paras[2]=T[2,3]
                self.cartesian_cur_paras[3]=joints_traj[-1][4]
                self.cartesian_cur_paras[4]=joints_traj[-1][1]+joints_traj[-1][2]+joints_traj[-1][3]
            else:#就返回最后一个可以到达的那个示教点
                return pieces[j]['startidx'] 
        return len(points)-1
        
       