import pybullet as p
import time
import pybullet_data
import numpy as np

class Simulator:
    def __init__(self,timeStep=1./60.):
        self.urdf_path='urdf6\\urdf\\urdf6.urdf'
        self.is_simulating=False
        self.time_step=timeStep#控制更新频率
        self.prev_pos=None
        self.draw_trace=False
        
    def start_sim(self):
        try:
            self.client=p.connect(p.GUI)
            p.removeAllUserDebugItems()
            p.resetDebugVisualizerCamera( cameraDistance=1, cameraYaw=50,
                                        cameraPitch=-35, cameraTargetPosition=[-0.15,0.13,-0.14])
            self.jibot=p.loadURDF(self.urdf_path,useFixedBase=True)#加载模型并固定基座
            self.is_simulating=True
            p.setTimeStep(self.time_step)
            # 开始记录
            # self.logging_id = p.startStateLogging(p.STATE_LOGGING_VIDEO_MP4, "sim.mp4")
            # 停止记录
           
        except Exception as e:
            print(f"Error start the simulator: {e}")
        if self.is_simulating:
            print("成功启动仿真！")
            # self.servo_reset()
            return True
        else:
            print("启动仿真失败！")
            return False
    
    def stop_sim(self):
        if self.is_simulating:
            if p.isConnected(self.client):
                # p.stopStateLogging(self.logging_id)
                p.disconnect()
                
            self.is_simulating=False
            print("成功停止仿真！")
            return True
        else:
            print("仿真已经停止！")
            return False

    def step_sim(self,_joint_angles=None):
    
        if self.is_simulating:

            if _joint_angles is not None:
                if len(_joint_angles)>=4:
                    #转换
                    #注意时弧度制
                    _joint_angles=np.deg2rad(_joint_angles)
                    print('仿真角度（弧度制）：',_joint_angles)
                    joint_angles=[0,0,0,0,0]
                    joint_angles[0]=-_joint_angles[0]
                    joint_angles[1]=-_joint_angles[1]
                    joint_angles[2]=_joint_angles[2]
                    joint_angles[3]=-_joint_angles[3]
                    joint_angles[4]=-_joint_angles[4]
                    #仿真
                    p.setJointMotorControlArray(self.jibot,jointIndices=range(0,5),controlMode=p.POSITION_CONTROL,targetPositions=joint_angles)
                else:
                    print("警告：关节角度列表长度不为5，不更新关节角")
            else:
                print("警告：关节角度列表为空，不更新关节角")
            
            count=60
            #注意一定要多次执行simulate,不然到不了想要的位置，pid控制是需要时间收敛的
            for i in range(int(count)):
                p.stepSimulation()
            
            end_link0=p.getLinkState(self.jibot, 5)[0]
            end_link1=p.getLinkState(self.jibot, 6)[0]
            cur_pos=[(e0+e1)/2 for e0,e1 in zip(end_link0,end_link1)]
            if self.prev_pos is not None  and self.draw_trace ==True:   
                p.addUserDebugLine(self.prev_pos, cur_pos, lineColorRGB=[1, 0, 0], lifeTime=10, lineWidth=3)
            self.prev_pos=cur_pos
            return True
        else:
            print("仿真未启动！")
            return False
    def set_grapper(self,pwm):

        if self.is_simulating:
        
            joint67=[0,0]
            joint67[0]=-0.6/1000*pwm+2100*0.6/1000#转换一下
            joint67[1]=joint67[0]
            p.setJointMotorControlArray(self.jibot,jointIndices=range(5,7),controlMode=p.POSITION_CONTROL,targetPositions=joint67)
            #注意一定要多次执行simulate,不然到不了想要的位置，pid控制是需要时间收敛的
            count=60
            for i in range(int(count)):
                p.stepSimulation()
                
            return True
        else:
            print("仿真未启动！")
            return False
        
    def get_obs(self):
        if self.is_simulating:
            joint_pos=p.getJointStates(self.jibot,jointIndices=range(1,8))
            joint_pos=np.array([state[0] for state in joint_pos])
            return joint_pos
        else:
            print("仿真未启动！")
            return False

    def get_reward(self):   
        if self.is_simulating:
            joint_pos=p.getJointStates(self.jibot,jointIndices=range(1,8))
            joint_pos=np.array([state[0] for state in joint_pos])
            return -np.sum(np.square(joint_pos))
        else:
            print("仿真未启动！")
            return False

    def get_done(self):
        if self.is_simulating:
            joint_pos=p.getJointStates(self.jibot,jointIndices=range(1,8))
            joint_pos=np.array([state[0] for state in joint_pos])
            if np.sum(np.square(joint_pos))<0.01:
                return True
            else:
                return False
        else:
            print("仿真未启动！")
            return False