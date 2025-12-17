from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QFileDialog, QWidget,QComboBox,QMessageBox,QPlainTextEdit
from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtGui import QTextCursor,QPixmap,QImage
from PyQt5.QtCore import  *

from robot import Robot
from teach import Teach
# from vision import *
from interact import Interact
import time

from hardware import get_serial_port,baudrate_options

from simulator import Simulator
from hardware import Hardware
from zlink import ZLink

import pandas as pd
# from calibration.handeye_clib.handeye_calibration import hangeye_calibration 
class JIBot:

    def __init__(self):
        # 从文件中加载UI定义

        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        self.ui = uic.loadUi('ui/mainWindow.ui')
        
        
        #*********************基础控制页***********************#
        sim = Simulator()
        hard = Hardware(ZLink())
        self.robot=Robot(sim, hard)
        self.teach=Teach()
        # self.vision=Vision()
        self.interact=Interact()
        
        #更新全部位置标签
        self.update_all_lables()
        # 使用对象名称找到按钮并连接槽函数
        
        #######串口通信及仿真
        self.ui.pushButton_portUpdate.clicked.connect(self.portUpdate)
        self.ui.comboBox_baud.clear()
        self.ui.comboBox_baud.addItems(baudrate_options)
        self.ui.comboBox_baud.setCurrentIndex(2)
        self.ui.pushButton_establish.clicked.connect(self.portEstablish)
        self.ui.pushButton_send.clicked.connect(self.portSend)
        self.ui.pushButton_sim.clicked.connect(self.sim_start)
        self.ui.checkBox_trace.stateChanged.connect(self.draw_trace)
        #########步进示教########
        #####笛卡尔空间
        self.ui.radioButton_speedLow.toggled.connect(self.speed_low)
        self.ui.radioButton_speedHigh.toggled.connect(self.speed_high)
        self.ui.radioButton_disShort.toggled.connect(self.dis_short)
        self.ui.radioButton_disMid.toggled.connect(self.dis_mid)
        self.ui.radioButton_disLong.toggled.connect(self.dis_long)
        
        #连接步进按钮槽函数
        self.ui.pushButton_xNeg.clicked.connect(self.xNeg)
        self.ui.pushButton_xPos.clicked.connect(self.xPos)
        self.ui.pushButton_yNeg.clicked.connect(self.yNeg)
        self.ui.pushButton_yPos.clicked.connect(self.yPos)
        self.ui.pushButton_zNeg.clicked.connect(self.zNeg)
        self.ui.pushButton_zPos.clicked.connect(self.zPos)
        self.ui.pushButton_rollNeg.clicked.connect(self.rollNeg)
        self.ui.pushButton_rollPos.clicked.connect(self.rollPos)
        self.ui.pushButton_pitchNeg.clicked.connect(self.pitchNeg)
        self.ui.pushButton_pitchPos.clicked.connect(self.pitchPos)
        self.ui.pushButton_grapperNeg.clicked.connect(self.grapperNeg)
        self.ui.pushButton_grapperPos.clicked.connect(self.grapperPos)
        
        #点示教
        self.ui.radioButton_linearPlan.toggled.connect(self.linear_plan)
        self.ui.radioButton_nonlinearPlan.toggled.connect(self.nonlinear_plan)
        self.ui.pushButton_run.clicked.connect(self.point_run)
        self.ui.pushButton_save.clicked.connect(self.save_to_excel)
        self.ui.pushButton_open.clicked.connect(self.open_from_excel)
        self.ui.pushButton_delete.clicked.connect(self.delete_row)
        self.ui.pushButton_add.clicked.connect(self.add_row)
        self.ui.pushButton_remove.clicked.connect(self.remove_row)
        #####关节空间
        self.ui.radioButton_speedLow_2.toggled.connect(self.speed_low_2)
        self.ui.radioButton_speedHigh_2.toggled.connect(self.speed_high_2)
        self.ui.radioButton_disShort_2.toggled.connect(self.dis_short_2)
        self.ui.radioButton_disMid_2.toggled.connect(self.dis_mid_2)
        self.ui.radioButton_disLong_2.toggled.connect(self.dis_long_2)        

        self.ui.pushButton_j1Neg.clicked.connect(self.j1Neg)
        self.ui.pushButton_j1Pos.clicked.connect(self.j1Pos)
        self.ui.pushButton_j2Neg.clicked.connect(self.j2Neg)
        self.ui.pushButton_j2Pos.clicked.connect(self.j2Pos)
        self.ui.pushButton_j3Neg.clicked.connect(self.j3Neg)
        self.ui.pushButton_j3Pos.clicked.connect(self.j3Pos)
        self.ui.pushButton_j4Neg.clicked.connect(self.j4Neg)
        self.ui.pushButton_j4Pos.clicked.connect(self.j4Pos)
        self.ui.pushButton_j5Neg.clicked.connect(self.j5Neg)
        self.ui.pushButton_j5Pos.clicked.connect(self.j5Pos)
        self.ui.pushButton_grapperNeg_2.clicked.connect(self.grapperNeg_2)
        self.ui.pushButton_grapperPos_2.clicked.connect(self.grapperPos_2)
        
        self.ui.pushButton_run_2.clicked.connect(self.point_run_2)
        self.ui.pushButton_save_2.clicked.connect(self.save_to_excel_2)
        self.ui.pushButton_open_2.clicked.connect(self.open_from_excel_2)
        self.ui.pushButton_delete_2.clicked.connect(self.delete_row_2)

        
        #*********************交互控制页***********************#     
        self.interact.signal_shift_to_joint.connect(self.shift_to_joint)
        self.interact.signal_shift_to_cartesian.connect(self.shift_to_cartesian)
        self.interact.signal_xNeg.connect(self.xNeg)
        self.interact.signal_xPos.connect(self.xPos)
        self.interact.signal_yNeg.connect(self.yNeg)
        self.interact.signal_yPos.connect(self.yPos)
        self.interact.signal_zNeg.connect(self.zNeg)
        self.interact.signal_zPos.connect(self.zPos)
        self.interact.signal_rollNeg.connect(self.rollNeg)
        self.interact.signal_rollPos.connect(self.rollPos)
        self.interact.signal_pitchNeg.connect(self.pitchNeg)
        self.interact.signal_pitchPos.connect(self.pitchPos)
        self.interact.signal_grapperNeg.connect(self.grapperNeg)
        self.interact.signal_grapperPos.connect(self.grapperPos)
        self.interact.signal_j1Neg.connect(self.j1Neg)
        self.interact.signal_j1Pos.connect(self.j1Pos)
        self.interact.signal_j2Neg.connect(self.j2Neg)
        self.interact.signal_j2Pos.connect(self.j2Pos)
        self.interact.signal_j3Neg.connect(self.j3Neg)
        self.interact.signal_j3Pos.connect(self.j3Pos)
        self.interact.signal_j4Neg.connect(self.j4Neg)
        self.interact.signal_j4Pos.connect(self.j4Pos)
        self.interact.signal_j5Neg.connect(self.j5Neg)
        self.interact.signal_j5Pos.connect(self.j5Pos)
        self.interact.signal_grapperNeg_2.connect(self.grapperNeg_2)
        self.interact.signal_grapperPos_2.connect(self.grapperPos_2)
        
        # ********************* 键盘遥控补丁 *********************** #
        from PyQt5.QtCore import Qt

        # 记录当前按下的键（防止重复触发）
        self._key_pressed = set()

        # 用 QShortcut 捕获按键（好处：不需要焦点也能响应）
        self.key_map = {
            Qt.Key_W: 'xPos',
            Qt.Key_S: 'xNeg',
            Qt.Key_A: 'j1Pos',
            Qt.Key_D: 'j1Neg',
            Qt.Key_C: 'zNeg',
            Qt.Key_Z: 'zPos',
            Qt.Key_Up: 'j4Pos',
            Qt.Key_Down: 'j4Neg',
            Qt.Key_Left: 'rollNeg',
            Qt.Key_Right: 'rollPos',
            Qt.Key_F: 'grapperPos',
            Qt.Key_J: 'grapperNeg',
        }

        for key, func in self.key_map.items():
            sc = QtWidgets.QShortcut(QtGui.QKeySequence(key), self.ui)
            sc.setContext(Qt.ApplicationShortcut)          # 全局有效
            sc.activated.connect(lambda f=func: self._key_start(f))

        # 给主窗口挂 keyReleaseEvent
        self.ui.keyReleaseEvent = self._key_release       # 直接替换，简单粗暴

    # ---------- 按下 ----------
    def _key_start(self, func_name):
        if func_name in self._key_pressed:
            return
        self._key_pressed.add(func_name)
        getattr(self, func_name)()

    # ---------- 松开 ----------
    def _key_release(self, event):
        func = self.key_map.get(event.key())
        if func and func in self._key_pressed:
            self._key_pressed.discard(func)
        # 如果想让别的按键继续正常响应，就保留下面这句：
        event.accept()   

    def add_row(self):
        # 将新行添加到表格的末尾
        self.ui.table_cartesian.insertRow(self.ui.table_cartesian.rowCount())
        self.ui.table_cartesian.setItem(self.ui.table_cartesian.rowCount()-1, 0, QTableWidgetItem("{:.2f}".format(self.teach.cartesian_cur_paras[0])))
        self.ui.table_cartesian.setItem(self.ui.table_cartesian.rowCount()-1, 1, QTableWidgetItem("{:.2f}".format(self.teach.cartesian_cur_paras[1])))
        self.ui.table_cartesian.setItem(self.ui.table_cartesian.rowCount()-1, 2, QTableWidgetItem("{:.2f}".format(self.teach.cartesian_cur_paras[2])))
        self.ui.table_cartesian.setItem(self.ui.table_cartesian.rowCount()-1, 3, QTableWidgetItem("{:.2f}".format(self.teach.cartesian_cur_paras[3])))
        self.ui.table_cartesian.setItem(self.ui.table_cartesian.rowCount()-1, 4, QTableWidgetItem("{:.2f}".format(self.teach.cartesian_cur_paras[4])))
        self.ui.table_cartesian.setItem(self.ui.table_cartesian.rowCount()-1, 5, QTableWidgetItem("{:.2f}".format(self.teach.cur_grapper_pwm)))
        
    def remove_row(self):
        # 删除表格的最后一行
        if self.ui.table_cartesian.rowCount() > 0:
            self.ui.table_cartesian.removeRow(self.ui.table_cartesian.rowCount() - 1)

    def update_all_lables(self):
        #笛卡尔tab页
        self.ui.label_x.setText("{:.2f}".format(self.teach.cartesian_cur_paras[0]))
        self.ui.label_y.setText("{:.2f}".format(self.teach.cartesian_cur_paras[1]))
        self.ui.label_z.setText("{:.2f}".format(self.teach.cartesian_cur_paras[2]))
        self.ui.label_roll.setText("{:.2f}".format(self.teach.cartesian_cur_paras[3]))
        self.ui.label_pitch.setText("{:.2f}".format(self.teach.cartesian_cur_paras[4]))
        self.ui.label_grapper.setText("{:.2f}".format(self.teach.cur_grapper_pwm))
        #关节tab页
        self.ui.label_j1.setText("{:.2f}".format(self.teach.joint_cur_paras[0]))
        self.ui.label_j2.setText("{:.2f}".format(self.teach.joint_cur_paras[1]))
        self.ui.label_j3.setText("{:.2f}".format(self.teach.joint_cur_paras[2]))
        self.ui.label_j4.setText("{:.2f}".format(self.teach.joint_cur_paras[3]))
        self.ui.label_j5.setText("{:.2f}".format(self.teach.joint_cur_paras[4]))
        self.ui.label_grapper_2.setText("{:.2f}".format(self.teach.cur_grapper_pwm))          
        
        
            
    def portUpdate(self):
        port_list=get_serial_port()
        self.ui.comboBox_port.clear()
        self.ui.comboBox_port.addItems(port_list)
        print('更新完毕')
        
    def portEstablish(self):
        if self.robot.hard.z.ser.isOpen()==False:
            self.robot.hard.z.ser.port=self.ui.comboBox_port.currentText()
            self.robot.hard.z.ser.baudrate=int(self.ui.comboBox_baud.currentText())
            ret=self.robot.hard.z.open_port()
            if ret == False:
                QMessageBox.warning(self.ui,'Warning','串口打开失败！')
            else:
                QMessageBox.information(self.ui,'Information','串口打开成功！')
                self.ui.pushButton_establish.setText('断开')
        else:
            self.robot.hard.z.close_port()
            QMessageBox.information(self.ui,'Information','串口已断开！')
            self.ui.pushButton_establish.setText('连接')
    def portSend(self):
        # 将文本追加到QTextEdit中
        cur_text=self.ui.plainTextEdit_send.toPlainText()
        self.ui.textEdit_send.moveCursor(QTextCursor.End)
        self.ui.textEdit_send.insertPlainText('>>>'+cur_text + '\n')
        self.ui.textEdit_send.moveCursor(QTextCursor.End)
        #串口发送
        self.robot.hard.z.ser.write(cur_text.encode('utf-8'))
    
    def sim_start(self):
        if self.robot.sim.is_simulating ==False:
            if self.robot.sim.start_sim():
                self.ui.pushButton_sim.setText('停止仿真')
                self.robot.sim.is_simulating =True
                self.robot.sim.step_sim(self.teach.joint_cur_paras)#初始化位置
                time.sleep(0.01)
                self.robot.sim.set_grapper(self.teach.cur_grapper_pwm)#初始化夹具
                time.sleep(0.01)
                
            else:
                QMessageBox.warning(self.ui,'Warning','仿真启动失败！')
        else:
            if self.robot.sim.stop_sim():
                self.ui.pushButton_sim.setText('启动仿真')
                self.robot.sim.is_simulating =False
            else:
                QMessageBox.warning(self.ui,'Warning','仿真停止失败！')
    def draw_trace(self,state):
        if state == Qt.Checked:
            print(" trace Checkbox checked")
            self.robot.sim.draw_trace =True
        elif state == Qt.Unchecked:
            print(" trace Checkbox unchecked")
            self.robot.sim.draw_trace =False
            
    
    
    
    
    
    
    
    
    
    
    
    
    def xNeg(self):
        self.teach.cartesian_old_paras=self.teach.cartesian_cur_paras
        self.teach.cartesian_cur_paras[0]=self.teach.cartesian_old_paras[0]-self.teach.cartesian_step_dis
        if self.teach.cartesian_step_teach(self.robot):
            self.update_all_lables()
        else:
            QMessageBox.warning(self.ui,'Warning','无法到达，步进失败！')
            
    def xPos(self):
        self.teach.cartesian_old_paras=self.teach.cartesian_cur_paras
        self.teach.cartesian_cur_paras[0]=self.teach.cartesian_old_paras[0]+self.teach.cartesian_step_dis
        if self.teach.cartesian_step_teach(self.robot):
            self.update_all_lables()
        else:
            QMessageBox.warning(self.ui,'Warning','无法到达，步进失败！')
            
    def yNeg(self):
        self.teach.cartesian_old_paras=self.teach.cartesian_cur_paras
        self.teach.cartesian_cur_paras[1]=self.teach.cartesian_old_paras[1]-self.teach.cartesian_step_dis
        if self.teach.cartesian_step_teach(self.robot):
            self.update_all_lables()
        else:
            QMessageBox.warning(self.ui,'Warning','无法到达，步进失败！')
            
    def yPos(self):
        self.teach.cartesian_old_paras=self.teach.cartesian_cur_paras
        self.teach.cartesian_cur_paras[1]=self.teach.cartesian_old_paras[1]+self.teach.cartesian_step_dis
        if self.teach.cartesian_step_teach(self.robot):
            self.update_all_lables()
        else:
            QMessageBox.warning(self.ui,'Warning','无法到达，步进失败！')

    def zNeg(self):
        self.teach.cartesian_old_paras=self.teach.cartesian_cur_paras
        self.teach.cartesian_cur_paras[2]=self.teach.cartesian_old_paras[2]-self.teach.cartesian_step_dis
        if self.teach.cartesian_step_teach(self.robot):
            self.update_all_lables()
        else:
            QMessageBox.warning(self.ui,'Warning','无法到达，步进失败！')
            
    def zPos(self):
        self.teach.cartesian_old_paras=self.teach.cartesian_cur_paras
        self.teach.cartesian_cur_paras[2]=self.teach.cartesian_old_paras[2]+self.teach.cartesian_step_dis
        if self.teach.cartesian_step_teach(self.robot):
            self.update_all_lables()
        else:
            QMessageBox.warning(self.ui,'Warning','无法到达，步进失败！')
    
    def rollNeg(self):
        if abs(self.teach.cartesian_cur_paras[3]-self.teach.cartesian_step_dis)<=135:
            self.teach.cartesian_old_paras=self.teach.cartesian_cur_paras
            self.teach.cartesian_cur_paras[3]=self.teach.cartesian_old_paras[3]-self.teach.cartesian_step_dis
            self.teach.step_roll(self.robot)
            self.update_all_lables()
            
        else:
            QMessageBox.warning(self.ui,'Warning','旋转角度过大！')
    
    def rollPos(self):
        if abs(self.teach.cartesian_cur_paras[3]+self.teach.cartesian_step_dis)<=135:
            self.teach.cartesian_old_paras=self.teach.cartesian_cur_paras
            self.teach.cartesian_cur_paras[3]=self.teach.cartesian_old_paras[3]+self.teach.cartesian_step_dis
            self.teach.step_roll(self.robot)
            self.update_all_lables()
            
        else:
            QMessageBox.warning(self.ui,'Warning','旋转角度过大！')

    def pitchNeg(self):
        self.teach.cartesian_old_paras=self.teach.cartesian_cur_paras
        self.teach.cartesian_cur_paras[4]=self.teach.cartesian_old_paras[4]-self.teach.cartesian_step_dis
        if self.teach.step_pitch(self.robot,direction='down'):
            self.update_all_lables()
        else:
            QMessageBox.warning(self.ui,'Warning','俯仰角度过大或无合适俯仰角！')
    def pitchPos(self):
        self.teach.cartesian_old_paras=self.teach.cartesian_cur_paras
        self.teach.cartesian_cur_paras[4]=self.teach.cartesian_old_paras[4]+self.teach.cartesian_step_dis
        if self.teach.step_pitch(self.robot,direction='up'):
            self.update_all_lables()
        else:
            QMessageBox.warning(self.ui,'Warning','俯仰角度过大或无合适俯仰角！')
    def grapperNeg(self):
        if self.teach.cur_grapper_pwm-self.teach.grapper_step>=1100:
            self.teach.cur_grapper_pwm=self.teach.cur_grapper_pwm-self.teach.grapper_step
            self.robot.set_grapper_pwm(self.teach.cur_grapper_pwm)
            self.update_all_lables()
        else:
            QMessageBox.warning(self.ui,'Warning','夹爪PWM过小！')
    def grapperPos(self):
        if self.teach.cur_grapper_pwm+self.teach.grapper_step<=2100:
            self.teach.cur_grapper_pwm=self.teach.cur_grapper_pwm+self.teach.grapper_step
            self.robot.set_grapper_pwm(self.teach.cur_grapper_pwm)
            self.update_all_lables()
        else:
            QMessageBox.warning(self.ui,'Warning','夹爪PWM过大！')            
        
    def speed_low(self,checked):
        if checked:
            print("shift speed to low")
            self.teach.cartesian_step_speed=self.teach.cartesian_speed_opts[0]
    def speed_high(self,checked):
        if checked:
            print("shift speed to high")
            self.teach.cartesian_step_speed=self.teach.cartesian_speed_opts[1]
    def dis_short(self,checked):
        if checked:
            print("RadioButton state: Checked")
            self.teach.cartesian_step_dis=self.teach.cartesian_stepdis_opts[0]
            self.teach.grapper_step=50
    def dis_mid(self,checked):
        if checked:
            print("RadioButton state: Checked")
            self.teach.cartesian_step_dis=self.teach.cartesian_stepdis_opts[1]  
            self.teach.grapper_step=100
            
    def dis_long(self,checked):
        if checked:
            print("RadioButton state: Checked")
            self.teach.cartesian_step_dis=self.teach.cartesian_stepdis_opts[2]
            self.teach.grapper_step=200

        
    def point_run(self):
        #[1]获取和处理表格数据
        data = []
        row_data=self.teach.cartesian_cur_paras+[self.teach.cur_grapper_pwm]+['当前点']
        data.append(row_data)
        for i in range(self.ui.table_cartesian.rowCount()):
            row_data = []
            drop_row=False
            for j in range(self.ui.table_cartesian.columnCount()):
                item = self.ui.table_cartesian.item(i, j)
                if item is None:
                    print('none')
                    if j==6:
                        row_data.append('')
                    elif j==5:#夹取pwm为空时默认保持和之前一样
                        row_data.append(data[i][5])
                    else:
                        drop_row=True
                        break
                else:
                    if item.text() == ''  :
                        if j==5:
                            row_data.append(data[i][5])
                        elif j==6:
                            row_data.append('')
                        else:
                            drop_row=True
                            break
                    else:
                        if j!=6:
                            row_data.append(float(item.text()))
                        else:
                            row_data.append(item.text())
                            
            if drop_row:
                break#存在一行信息不完整，下面的行就不看了
            else:
                data.append(row_data)     
        # print("data",data)

        #[2]运动
        ret=self.teach.cartesian_point_teach(self.robot,[row[:6] for row in data])
        self.update_all_lables()
        if ret!=len(data)-1:
            QMessageBox.information(self.ui,'提示','由于运动限制只运动到第'+str(ret)+'点')
        else:
            QMessageBox.information(self.ui,'提示','运动完成')
        
    def linear_plan(self,checked):
        if checked:
            print("shift linear plan")
            self.teach.cartesian_plan_mode=0
    def nonlinear_plan(self,checked):
        if checked:
            print("shift nonlinear plan")
            self.teach.cartesian_plan_mode=1 
            
    def delete_row(self):
                # 获取选中的行号
        selected_row = self.ui.table_cartesian.currentRow()

        # 如果有行被选中
        if selected_row >= 0:
            # 移除选中的行
            self.ui.table_cartesian.removeRow(selected_row)
            
    def save_to_excel(self):
        #[1]获取和处理表格数据
        data = []
        row_data=self.teach.cartesian_cur_paras+[self.teach.cur_grapper_pwm]+['起始点']
        data.append(row_data)
        for i in range(self.ui.table_cartesian.rowCount()):
            row_data = []
            drop_row=False
            for j in range(self.ui.table_cartesian.columnCount()):
                item = self.ui.table_cartesian.item(i, j)
                if item is None:
                    # print('none')
                    if j==6:
                        row_data.append('')
                    elif j==5:#夹取pwm为空时默认保持和之前一样
                        row_data.append(data[i][5])
                    else:
                        drop_row=True
                        break
                else:
                    if item.text() == ''  :
                        if j==5:
                            row_data.append(data[i][5])
                        elif j==6:
                            row_data.append('')
                        else:
                            drop_row=True
                            break
                    else:
                        if j!=6:
                            row_data.append(float(item.text()))
                        else:
                            row_data.append(item.text())
                            
            if drop_row:
                break#存在一行信息不完整，下面的行就不看了
            else:
                data.append(row_data)     
        # print('table data:',data)

        # 将数据转换为DataFrame
        df = pd.DataFrame(data, columns=["X(mm)", "Y(mm)","Z(mm)","roll(度)","pitch(度)","夹具PWM","名称及描述"])
        # print('df:',df)
        # 使用文件对话框获取保存路径
        file_path, _ = QFileDialog.getSaveFileName(self.ui, "保存Excel文件", "", "Excel Files (*.xlsx)")

        # 如果用户选择了文件路径，保存DataFrame到Excel文件
        if file_path:
            df.to_excel(file_path, index=False)

    def open_from_excel(self):
        # 使用文件对话框获取打开路径
        file_path, _ = QFileDialog.getOpenFileName(self.ui, "打开Excel文件", "", "Excel Files (*.xlsx)")

        # 如果用户选择了文件路径，读取Excel文件到DataFrame
        if file_path:
            df = pd.read_excel(file_path)
            print(df)
            # 清空表格
            self.ui.table_cartesian.clearContents()

            # 将DataFrame数据加载到表格中
            for row in range(df.shape[0]):
                
                self.ui.table_cartesian.setItem(row, 0, QTableWidgetItem(str(df.iloc[row, 0])))
                self.ui.table_cartesian.setItem(row, 1, QTableWidgetItem(str(df.iloc[row, 1])))
                self.ui.table_cartesian.setItem(row, 2, QTableWidgetItem(str(df.iloc[row, 2])))
                self.ui.table_cartesian.setItem(row, 3, QTableWidgetItem(str(df.iloc[row, 3])))
                self.ui.table_cartesian.setItem(row, 4, QTableWidgetItem(str(df.iloc[row, 4])))
                self.ui.table_cartesian.setItem(row, 5, QTableWidgetItem(str(df.iloc[row, 5])))
                self.ui.table_cartesian.setItem(row, 6, QTableWidgetItem(str(df.iloc[row, 6])))
   
 ######################################################
    def speed_low_2(self,checked):
        if checked:
            print("shift speed to low")
            self.teach.joint_step_speed=self.teach.joint_speed_opts[0]
    def speed_high_2(self,checked):
        if checked:
            print("shift speed to high")
            self.teach.joint_step_speed=self.teach.joint_speed_opts[1]
    def dis_short_2(self,checked):
        if checked:
            print("RadioButton state: Checked")
            self.teach.joint_step_dis=self.teach.joint_stepdis_opts[0]
            self.teach.grapper_step_2=50
    def dis_mid_2(self,checked):
        if checked:
            print("RadioButton state: Checked")
            self.teach.joint_step_dis=self.teach.joint_stepdis_opts[1]  
            self.teach.grapper_step_2=100
            
    def dis_long_2(self,checked):
        if checked:
            print("RadioButton state: Checked")
            self.teach.joint_step_dis=self.teach.joint_stepdis_opts[2]
            self.teach.grapper_step_2=200
                
    def delete_row_2(self):
                # 获取选中的行号
        selected_row = self.ui.table_joint.currentRow()

        # 如果有行被选中
        if selected_row >= 0:
            # 移除选中的行
            self.ui.table_joint.removeRow(selected_row)
            
    def save_to_excel_2(self):
        #[1]获取和处理表格数据
        data = []
        row_data=self.teach.joint_cur_paras+[self.teach.cur_grapper_pwm]+['起始点']
        data.append(row_data)
        for i in range(self.ui.table_joint.rowCount()):
            row_data = []
            drop_row=False
            for j in range(self.ui.table_joint.columnCount()):
                item = self.ui.table_joint.item(i, j)
                if item is None:
                    # print('none')
                    if j==6:
                        row_data.append('')
                    elif j==5:#夹取pwm为空时默认保持和之前一样
                        row_data.append(data[i][5])
                    else:
                        drop_row=True
                        break
                else:
                    if item.text() == ''  :
                        if j==5:
                            row_data.append(data[i][5])
                        elif j==6:
                            row_data.append('')
                        else:
                            drop_row=True
                            break
                    else:
                        if j!=6:
                            row_data.append(float(item.text()))
                        else:
                            row_data.append(item.text())
                            
            if drop_row:
                break#存在一行信息不完整，下面的行就不看了
            else:
                data.append(row_data)     
        # print('table data:',data)

        # 将数据转换为DataFrame
        df = pd.DataFrame(data, columns=["J1（度）", "J2（度）","J3（度）","J4（度）","J5（度）","夹具PWM","名称及描述"])
        # print('df:',df)
        # 使用文件对话框获取保存路径
        file_path, _ = QFileDialog.getSaveFileName(self.ui, "保存Excel文件", "", "Excel Files (*.xlsx)")

        # 如果用户选择了文件路径，保存DataFrame到Excel文件
        if file_path:
            df.to_excel(file_path, index=False)

    def open_from_excel_2(self):
        # 使用文件对话框获取打开路径
        file_path, _ = QFileDialog.getOpenFileName(self.ui, "打开Excel文件", "", "Excel Files (*.xlsx)")

        # 如果用户选择了文件路径，读取Excel文件到DataFrame
        if file_path:
            df = pd.read_excel(file_path)
            print(df)
            # 清空表格
            self.ui.table_joint.clearContents()

            # 将DataFrame数据加载到表格中
            for row in range(df.shape[0]):
                
                self.ui.table_joint.setItem(row, 0, QTableWidgetItem(str(df.iloc[row, 0])))
                self.ui.table_joint.setItem(row, 1, QTableWidgetItem(str(df.iloc[row, 1])))
                self.ui.table_joint.setItem(row, 2, QTableWidgetItem(str(df.iloc[row, 2])))
                self.ui.table_joint.setItem(row, 3, QTableWidgetItem(str(df.iloc[row, 3])))
                self.ui.table_joint.setItem(row, 4, QTableWidgetItem(str(df.iloc[row, 4])))
                self.ui.table_joint.setItem(row, 5, QTableWidgetItem(str(df.iloc[row, 5])))
                self.ui.table_joint.setItem(row, 6, QTableWidgetItem(str(df.iloc[row, 6])))    
                
    def j1Neg(self):#-135--135
        new=self.teach.joint_cur_paras[0]-self.teach.joint_step_dis
        if new>=self.teach.joint_ranges[0][0] and new<=self.teach.joint_ranges[0][1]:
            
            self.teach.joint_old_paras=self.teach.joint_cur_paras
            self.teach.joint_cur_paras[0]=new
            if self.teach.joint_step_teach(self.robot):
                self.update_all_lables()
            else:
                QMessageBox.warning(self.ui,'Warning','无法到达，步进失败！')
        else:
            QMessageBox.warning(self.ui,'Warning','无法到达，步进失败！')
            
    def j1Pos(self):
        new=self.teach.joint_cur_paras[0]+self.teach.joint_step_dis
        if new>=self.teach.joint_ranges[0][0] and new<=self.teach.joint_ranges[0][1]:
            
            self.teach.joint_old_paras=self.teach.joint_cur_paras
            self.teach.joint_cur_paras[0]=new
            if self.teach.joint_step_teach(self.robot):
                self.update_all_lables()
            else:
                QMessageBox.warning(self.ui,'Warning','无法到达，步进失败！')
        else:
            QMessageBox.warning(self.ui,'Warning','无法到达，步进失败！')
    def j2Neg(self):
        new=self.teach.joint_cur_paras[1]-self.teach.joint_step_dis
        if new>=self.teach.joint_ranges[1][0] and new<=self.teach.joint_ranges[1][1]:
            
            self.teach.joint_old_paras=self.teach.joint_cur_paras
            self.teach.joint_cur_paras[1]=new
            if self.teach.joint_step_teach(self.robot):
                self.update_all_lables()
            else:
                QMessageBox.warning(self.ui,'Warning','无法到达，步进失败！')
        else:
            QMessageBox.warning(self.ui,'Warning','无法到达，步进失败！')
    def j2Pos(self):
        new=self.teach.joint_cur_paras[1]+self.teach.joint_step_dis
        if new>=self.teach.joint_ranges[1][0] and new<=self.teach.joint_ranges[1][1]:
            
            self.teach.joint_old_paras=self.teach.joint_cur_paras
            self.teach.joint_cur_paras[1]=new
            if self.teach.joint_step_teach(self.robot):
                self.update_all_lables()
            else:
                QMessageBox.warning(self.ui,'Warning','无法到达，步进失败！')
        else:
            QMessageBox.warning(self.ui,'Warning','无法到达，步进失败！')
    def j3Neg(self):
        new=self.teach.joint_cur_paras[2]-self.teach.joint_step_dis
        if new>=self.teach.joint_ranges[2][0] and new<=self.teach.joint_ranges[2][1]:
            
            self.teach.joint_old_paras=self.teach.joint_cur_paras
            self.teach.joint_cur_paras[2]=new
            if self.teach.joint_step_teach(self.robot):
                self.update_all_lables()
            else:
                QMessageBox.warning(self.ui,'Warning','无法到达，步进失败！')
        else:
            QMessageBox.warning(self.ui,'Warning','无法到达，步进失败！')
    def j3Pos(self):
        new=self.teach.joint_cur_paras[2]+self.teach.joint_step_dis
        if new>=self.teach.joint_ranges[2][0] and new<=self.teach.joint_ranges[2][1]:
            
            self.teach.joint_old_paras=self.teach.joint_cur_paras
            self.teach.joint_cur_paras[2]=new
            if self.teach.joint_step_teach(self.robot):
                self.update_all_lables()
            else:
                QMessageBox.warning(self.ui,'Warning','无法到达，步进失败！')
        else:
            QMessageBox.warning(self.ui,'Warning','无法到达，步进失败！')        
    def j4Neg(self):
        new=self.teach.joint_cur_paras[3]-self.teach.joint_step_dis
        if new>=self.teach.joint_ranges[3][0] and new<=self.teach.joint_ranges[3][1]:
            
            self.teach.joint_old_paras=self.teach.joint_cur_paras
            self.teach.joint_cur_paras[3]=new
            if self.teach.joint_step_teach(self.robot):
                self.update_all_lables()
            else:
                QMessageBox.warning(self.ui,'Warning','无法到达，步进失败！')
        else:
            QMessageBox.warning(self.ui,'Warning','无法到达，步进失败！')
    def j4Pos(self):
        new=self.teach.joint_cur_paras[3]+self.teach.joint_step_dis
        if new>=self.teach.joint_ranges[3][0] and new<=self.teach.joint_ranges[3][1]:
            
            self.teach.joint_old_paras=self.teach.joint_cur_paras
            self.teach.joint_cur_paras[3]=new
            if self.teach.joint_step_teach(self.robot):
                self.update_all_lables()
            else:
                QMessageBox.warning(self.ui,'Warning','无法到达，步进失败！')
        else:
            QMessageBox.warning(self.ui,'Warning','无法到达，步进失败！')
    def j5Neg(self):
        new=self.teach.joint_cur_paras[4]-self.teach.joint_step_dis
        if new>=self.teach.joint_ranges[4][0] and new<=self.teach.joint_ranges[4][1]:
            
            self.teach.joint_old_paras=self.teach.joint_cur_paras
            self.teach.joint_cur_paras[4]=new
            if self.teach.joint_step_teach(self.robot):
                self.update_all_lables()
            else:
                QMessageBox.warning(self.ui,'Warning','无法到达，步进失败！')
        else:
            QMessageBox.warning(self.ui,'Warning','无法到达，步进失败！')
    def j5Pos(self):
        new=self.teach.joint_cur_paras[4]+self.teach.joint_step_dis
        if new>=self.teach.joint_ranges[4][0] and new<=self.teach.joint_ranges[4][1]:
            
            self.teach.joint_old_paras=self.teach.joint_cur_paras
            self.teach.joint_cur_paras[4]=new
            if self.teach.joint_step_teach(self.robot):
                self.update_all_lables()
            else:
                QMessageBox.warning(self.ui,'Warning','无法到达，步进失败！')
        else:
            QMessageBox.warning(self.ui,'Warning','无法到达，步进失败！')
    def grapperNeg_2(self):
        if self.teach.cur_grapper_pwm-self.teach.grapper_step_2>=1100:
            self.teach.cur_grapper_pwm=self.teach.cur_grapper_pwm-self.teach.grapper_step_2
            self.robot.set_grapper_pwm(self.teach.cur_grapper_pwm)
            self.update_all_lables()
        else:
            QMessageBox.warning(self.ui,'Warning','夹爪PWM过小！')
    def grapperPos_2(self):
        if self.teach.cur_grapper_pwm+self.teach.grapper_step_2<=2100:
            self.teach.cur_grapper_pwm=self.teach.cur_grapper_pwm+self.teach.grapper_step_2
            self.robot.set_grapper_pwm(self.teach.cur_grapper_pwm)
            self.update_all_lables()
        else:
            QMessageBox.warning(self.ui,'Warning','夹爪PWM过大！')
                  
    def point_run_2(self):
        #[1]获取和处理表格数据
        data = []
        row_data=self.teach.joint_cur_paras+[self.teach.cur_grapper_pwm]+['当前点']
        data.append(row_data)
        for i in range(self.ui.table_joint.rowCount()):
            row_data = []
            drop_row=False
            for j in range(self.ui.table_joint.columnCount()):
                item = self.ui.table_joint.item(i, j)
                if item is None:
                    # print('none')
                    if j==6:
                        row_data.append('')
                    elif j==5:#夹取pwm为空时默认保持和之前一样
                        row_data.append(data[i][5])
                    else:
                        drop_row=True
                        break
                else:
                    if item.text() == ''  :
                        if j==5:
                            row_data.append(data[i][5])
                        elif j==6:
                            row_data.append('')
                        else:
                            drop_row=True
                            break
                    else:
                        if j!=6:
                            row_data.append(float(item.text()))
                        else:
                            row_data.append(item.text())
                            
            if drop_row:
                break#存在一行信息不完整，下面的行就不看了
            else:
                data.append(row_data)     
        # print('table data:',data)

        #[2]运动
        ret=self.teach.joint_point_teach(self.robot,[row[:6] for row in data])
        self.update_all_lables()
        if ret!=len(data)-1:
            QMessageBox.information(self.ui,'提示','由于运动限制只运动到第'+str(ret)+'点')
        else:
            QMessageBox.information(self.ui,'提示','运动完成')
        

    def stickUpdate(self):
        stick_list=self.interact.get_stick_list()
        self.ui.comboBox_stick.clear()
        self.ui.comboBox_stick.addItems(stick_list)
        print('手柄列表更新完毕')        

    def stickOpen(self):
        if not self.interact.is_running:
            self.interact.stick_index=int(self.ui.comboBox_stick.currentText())
            self.interact.start()
            self.interact.is_running=True
            self.ui.pushButton_stickOpen.setText('关闭')
        else:
            self.interact.is_running=False
            self.ui.pushButton_stickOpen.setText('打开')
    def shift_to_joint(self):
        self.ui.label_stickMode.setText('Joint模式')
        self.ui.label_stick_joint.setVisible(True)
        self.ui.label_stick_cartesian.setVisible(False)
    def shift_to_cartesian(self):
        self.ui.label_stickMode.setText('Cartesian模式')
        self.ui.label_stick_joint.setVisible(False)
        self.ui.label_stick_cartesian.setVisible(True)
        
if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)#这句可以解决ui加载后与designer中预览不一样的问题
    app = QtWidgets.QApplication([])
    app.setStyle('Fusion')  # Fusion风格是一种现代风格
    jibot = JIBot()
    jibot.ui.show()
    app.exec_()
