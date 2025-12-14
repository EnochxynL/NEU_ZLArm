import numpy as np



def extract_cartesian(input_string):
    try:
        # 使用逗号分隔字符串，然后将提取的部分转换为浮点数
        x, y, z, roll, pitch = map(float, input_string.split(','))
        # 返回提取的数字
        return [x, y, z, roll, pitch]

    except ValueError:
        # 处理转换失败的情况
        print("输入格式不正确，请确保输入为 'x, y, z, roll, pitch' 形式的字符串。")
        return None

def extract_joints(input_string):
    try:
        # 使用逗号分隔字符串，然后将提取的部分转换为浮点数
        j1,j2,j3,j4,j5 = map(float, input_string.split(','))
        # 返回提取的数字
        return [j1,j2,j3,j4,j5]

    except ValueError:
        # 处理转换失败的情况
        print("输入格式不正确，请确保输入为 'j1,j2,j3,j4,j5 ' 形式的字符串。")
        return None

def extract_coordinate(input_string):
    try:
        # 使用逗号分隔字符串，然后将提取的部分转换为浮点数
        x, y, z = map(float, input_string.split(','))
        # 返回提取的数字
        return [x, y, z]

    except ValueError:
        # 处理转换失败的情况
        print("输入格式不正确，请确保输入为 'x, y, z' 形式的字符串。")
        return None
    
def euler_to_rotation_matrix(roll, pitch, yaw):
    '''
    功能： x-y-z欧拉角求旋转矩阵
    
    参数：
        roll  -- 绕x
        pitch -- 绕y
        yaw   -- 绕z
    返回: 4x4旋转矩阵
    '''
    R_x = np.array([[1, 0, 0,0],
                    [0, np.cos(roll), -np.sin(roll),0],
                    [0, np.sin(roll), np.cos(roll),0],
                    [0,0,0,1]])
    R_y = np.array([[np.cos(pitch), 0, np.sin(pitch),0],
                    [0, 1, 0,0],
                    [-np.sin(pitch), 0, np.cos(pitch),0],
                    [0,0,0,1]])
    R_z = np.array([[np.cos(yaw), -np.sin(yaw), 0,0],
                    [np.sin(yaw), np.cos(yaw), 0,0],
                    [0, 0, 1,0],
                    [0,0,0,1]])
    R = np.dot(np.dot(R_x, R_y),R_z)
    return R

def rotation_matrix_to_euler(R):
    sy = np.sqrt(R[0,0]**2 + R[1,0]**2)
    singular = sy < 1e-6
    if not singular:
        x = np.arctan2(R[2,1], R[2,2])
        y = np.arctan2(-R[2,0], sy)
        z = np.arctan2(R[1,0], R[0,0])
    else:
        x = np.arctan2(-R[1,2], R[1,1])
        y = np.arctan2(-R[2,0], sy)
        z = 0
    return np.array([x, y, z])

def cal_Transform_matrix(x,y,z,roll,pitch,yaw):
    '''
    功能： 求变换矩阵

    参数：
        x,y,z  -- 相机坐标系下的相机中心点
        roll   -- 绕x
        pitch  -- 绕y
        yaw    -- 绕z
    返回: 4x4变换矩阵
    '''
    
    T=euler_to_rotation_matrix(roll, pitch, yaw)
    T[0,3]=x
    T[1,3]=y
    T[2,3]=z
    return  T


