'''
颜色识别夹取木块
实验效果：
    将红绿蓝其中任意一种颜色的木块放置在机械臂正前方8厘米左右处，
    K210会根据识别到的木块颜色来将对应的木块放置到对应位置：
        如果识别到的是红色木块，则夹取红色模块放置到前方偏远位置；
        如果识别到的是绿色木块，则夹取绿色模块放置到左侧偏远位置；
        如果识别到的是蓝色木块，则夹取蓝色模块放置到右侧偏远位置；
        未识别到红绿蓝木块时，保持不动。
注意：环境光会对识别有影响，找比较合适的环境来运行此程序。
'''

'''
本次课程设计的引脚配置
SPI: SDA, SCL, GND, VCC
CN7: GP3, GP2, GND, VCC
     Pin5,Pin4,GND, 3V3

TXD1: Pin11 (机械臂 RXD)
RXD1: Pin12 (机械臂 TXD)
'''

# ------------------- 用户配置 -------------------
SENTRY_I2C_ADDR = 0x60      # Sentry2 的 I2C 地址
UART_NUM        = 1         # 机械臂接的串口号（ESP32-UART1）
UART_BAUD       = 115200
# ----------------------------------------------

from machine import I2C, UART, Pin
import time

i2c = I2C(0, scl=Pin(4), sda=Pin(5), freq=400_000)
uart = UART(UART_NUM, UART_BAUD, tx=Pin(11), rx=Pin(12))

# ---------- 动作组字符串 ----------
DETECT_POS      = "$DGT:2-2,1!"   # 识别位
CLAMP_GRAB      = "$DGT:3-7,1!"   # 夹取
RED_PLACE       = "$DGT:18-21,1!" # 红色放置
GREEN_PLACE     = "$DGT:22-26,1!" # 绿色放置
BLUE_PLACE      = "$DGT:27-31,1!" # 蓝色放置

# ---------- 全局变量 ----------
systick_ms_bak         = 0
target_color_appear_cnt = 0
detected_color         = ""        # "red" | "green" | "blue" | ""

# ---------- Sentry2 驱动 ----------
class Sentry2:
    def __init__(self, i2c, addr=0x60):
        self.i2c = i2c
        self.addr = addr
        # 初始化一次即可，Mixly 里 BEGIN + AWB + VisionBegin
        self._write(0x20, 0x01)          # CameraBegin
        time.sleep_ms(100)
        self._write(0x21, 0x01)          # SetAWB = Auto
        time.sleep_ms(100)
        self._write(0x34, 0x01)          # VisionBegin kVisionBlob
        time.sleep_ms(100)

    def _write(self, reg, dat):
        self.i2c.writeto_mem(self.addr, reg, bytes([dat]))

    def _read(self, reg):
        return self.i2c.readfrom_mem(self.addr, reg, 1)[0]

    def detected_count(self):
        return self._read(0xB0)          # 寄存器 0xB0 = 当前画面色块个数

    def color_label(self, idx=1):
        # 0xB1 开始是第 idx 个色块的颜色标签
        return self._read(0xB0 + idx)

sentry = Sentry2(i2c, SENTRY_I2C_ADDR)

# ---------- 业务逻辑 ----------
def loop_k210():
    global systick_ms_bak, target_color_appear_cnt, detected_color

    if time.ticks_diff(time.ticks_ms(), systick_ms_bak) < 50:
        return
    systick_ms_bak = time.ticks_ms()

    cnt = sentry.detected_count()
    if cnt != 1:
        return

    label = sentry.color_label(1)
    # Sentry2 颜色定义：1=红 2=绿 3=蓝
    if label not in (1, 2, 3):
        return

    target_color_appear_cnt += 1
    detected_color = ("red", "green", "blue")[label - 1]
    color_sort()

def color_sort():
    global target_color_appear_cnt, detected_color
    if target_color_appear_cnt < 6:
        return

    # 1. 夹取
    uart.write(CLAMP_GRAB + '\n')
    time.sleep_ms(8000)

    # 2. 按颜色放置
    if detected_color == "red":
        uart.write(RED_PLACE + '\n')
    elif detected_color == "green":
        uart.write(GREEN_PLACE + '\n')
    elif detected_color == "blue":
        uart.write(BLUE_PLACE + '\n')

    time.sleep_ms(8000)

    # 3. 回到识别位
    uart.write(DETECT_POS + '\n')
    time.sleep_ms(2000)

    # 4. 清零，准备下一轮
    target_color_appear_cnt = 0
    detected_color = ""

# ---------- 主循环 ----------
print("init ok!")
uart.write(DETECT_POS + '\n')
time.sleep_ms(2000)

while True:
    loop_k210()