from factory.hcsr04 import HCSR04
from factory.z_uart import ZL_UART
from factory.z_beep import ZL_BEEP
from factory.z_kinematics import ZL_KINEMATICS
from machine import SoftI2C,Pin
from factory.ssd1306 import SSD1306_I2C  #I2C的oled选该方法
from factory import z_main
from machine import Pin
import time

dis = 0
dis_cur = 0
get_count = 0
carry_step = 0
systick_time_bak = 0    # 控制执行时间，即在指定时间内或超过指定时间时做一些操作

# oled初始化函数
def setup_oled():
    global oled
    i2c = SoftI2C(sda=Pin(21), scl=Pin(22))              # I2C初始化
    oled = SSD1306_I2C(128, 64, i2c)                     # 你的OLED分辨率，使用I2C
    oled.fill(0)                                         # 屏幕全黑
    oled.show()
    time.sleep(1)                                        # 延时1秒

# 传感器按键初始化
def setup_sensor():
    global chaoshengbo, uart, kms, beep
    
    beep = ZL_BEEP()                                     # 实例化蜂鸣器对象
    uart = ZL_UART()                                     # 实例化串口对象
    kms = ZL_KINEMATICS(170,105,75,185)                  # 实例化逆运动学
    setup_oled()                                         # oled初始化

'''
此函数实现测距夹取功能：
注意：此处会用到逆运动学，如果逆运动学有偏差，可以根据实际情况改变代码中kms.kinematics_move(0, dis*10+120, 100, 1000)函数中的对应参数
传感器接线说明：超声波模块接的是S3接口，oled显示屏接的是S6接口
操作说明：
    超声波模块检测到前方8-15厘米范围内的物体时，机械臂会执行 前抓 来抓取前方物体，然后将物体放置到左侧。
    oled模块可实时显示超声波模块测得的距离值，在此处仅为辅助观察作用。
'''
# 循环执行智能功能
def loop_sensor():
    global systick_time_bak, dis, dis_cur, get_count, carry_step
    if carry_step == 0 and millis() - systick_time_bak > 100:
        systick_time_bak = millis()
        dis = chaoshengbo.distance_cm()
        oled.text('hello world', 0, 0, 1)
        oled.text('ZL-TECH', 0, 16, 1)
        oled.text('Jibot', 0, 32, 1)
        oled.text('dis:', 0, 48, 1)
        oled.text(str(int(dis)), 33, 48, 1)
        oled.text('cm', 55, 48, 1)
        oled.show()
        time.sleep(0.1)
        for i in range(241):
            oled.text(str(i), 33, 48, 0)
        oled.show()
        time.sleep(0.1)
        if 8 < dis < 15:
            oled.text(str(int(dis)), 33, 48, 1)
            oled.show()
            dis_cur = chaoshengbo.distance_cm()
            if abs(dis_cur - dis) <= 2:
                get_count += 1
                if get_count > 5:
                    get_count = 0
                    carry_step = 1
                    beep.beep_on_times(1, 0.1)
            else:
                get_count = 0
        else:
            get_count = 0
    elif carry_step == 1:
        uart.uart_send_str('#005P1250T0500!')  # 爪子张开
        systick_time_bak = millis()
        carry_step = 2
        print('1 ok')
    elif carry_step == 2 and millis() - systick_time_bak > 1000:
        if kms.kinematics_move(0, dis*10+120, 100, 1000):
            text_str = kms.kinematics_move(0, dis*10+120, 100, 1000)  # 通过逆运动学获得机械臂各舵机需要运行到的pwm值
            uart.uart_send_str(text_str)                              # 串口发送对应pwm值使机械臂运行到目标点
            beep.beep_on_times(1, 0.1)
            systick_time_bak = millis()
            carry_step = 3
            print('2 ok')
    elif carry_step == 3 and millis() - systick_time_bak > 2000 and z_main.group_ok == 1:
        uart.uart_send_str('#005P1760T0500!') # 爪子闭合
        systick_time_bak = millis()
        carry_step = 4
        print('3 ok')
    elif carry_step == 4 and millis() - systick_time_bak > 1000:
        z_main.parse_cmd("$DGT:1-1,1!")       # 蜷缩
        carry_step = 5
        print('4 ok')
    elif carry_step == 5 and z_main.group_ok == 1:
        z_main.parse_cmd("$DGT:22-26,1!")     # 左放
        carry_step = 6
        print('5 ok')
    elif carry_step == 6 and z_main.group_ok == 1:
        carry_step = 0
        print('6 ok')
    #print('sensor group ok: ', z_main.group_ok)

#获取系统时间，毫秒为单位
def millis():
    return int(time.time_ns()//1000000)

# 程序入口
if __name__ == '__main__':
    setup_sensor()
    while 1:
        loop_sensor()
