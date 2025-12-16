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

import pandas as pd
# from calibration.handeye_clib.handeye_calibration import hangeye_calibration 
class JIBot:

    def __init__(self):
        # 从文件中加载UI定义

        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        self.ui = uic.loadUi('ui/mainWindow.ui')
        
        
        #*********************基础控制页***********************#
        self.robot=Robot()
        self.teach=Teach()
        # self.vision=Vision()
        self.interact=Interact()
        
        #更新全部位置标签
        self.update_all_lables()
        # 使用对象名称找到按钮并连接槽函数
        
        #######串口通信及仿真
        self.ui.pushButton_portUpdate.clicked.connect(self.portUpdate)
        self.ui.comboBox_baud.clear()
        self.ui.comboBox_baud.addItems(self.robot.baudrate_options)
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

    
        #*********************视觉控制页***********************#
        if self.vision.eye_to_end_existed==False:
            self.ui.textEdit_clibInfo.moveCursor(QTextCursor.End)
            self.ui.textEdit_clibInfo.insertPlainText('>>>注意：当前尚无手眼标定结果可用...' + '\n')
            self.ui.textEdit_clibInfo.moveCursor(QTextCursor.End)
        else:
            self.ui.textEdit_clibInfo.moveCursor(QTextCursor.End)
            self.ui.textEdit_clibInfo.insertPlainText('>>>已成功加载手眼标定结果...' + '\n')
            self.ui.textEdit_clibInfo.moveCursor(QTextCursor.End)
        self.vision.change_pixmap_signal.connect(self.update_liveVideo)
        self.ui.pushButton_camUpdate.clicked.connect(self.cameraUpdate)
        self.ui.pushButton_cameraOpen.clicked.connect(self.cameraOpen)
        self.ui.pushButton_snap.clicked.connect(self.snap)
        self.ui.pushButton_clibRun.clicked.connect(self.clibRun)
        #抓取
        self.ui.horizontalSlider_hl.valueChanged.connect(self.change_hl)
        self.ui.horizontalSlider_sl.valueChanged.connect(self.change_sl)
        self.ui.horizontalSlider_vl.valueChanged.connect(self.change_vl)
        self.ui.horizontalSlider_hu.valueChanged.connect(self.change_hu)
        self.ui.horizontalSlider_su.valueChanged.connect(self.change_su)
        self.ui.horizontalSlider_vu.valueChanged.connect(self.change_vu)
        self.ui.pushButton_savePickConfig.clicked.connect(self.savePickConfig)
        self.ui.lineEdit_targetLen.setPlaceholderText(str(self.vision.target_size[0]))
        self.ui.lineEdit_targetWid.setPlaceholderText(str(self.vision.target_size[1]))
        self.ui.lineEdit_placeX.setPlaceholderText(str(self.vision.place_pose[0]))
        self.ui.lineEdit_placeY.setPlaceholderText(str(self.vision.place_pose[1]))
        self.ui.pushButton_change_waitJoint.clicked.connect(self.change_waitJoint)
        self.ui.pushButton_pick.clicked.connect(self.pick)
        self.vision.grasp_info_signal.connect(self.update_grasp_info)
        self.ui.pushButton_roi.clicked.connect(self.roiView)
        #跟踪
        self.ui.horizontalSlider_hl_2.valueChanged.connect(self.change_hl_2)
        self.ui.horizontalSlider_sl_2.valueChanged.connect(self.change_sl_2)
        self.ui.horizontalSlider_vl_2.valueChanged.connect(self.change_vl_2)
        self.ui.horizontalSlider_hu_2.valueChanged.connect(self.change_hu_2)
        self.ui.horizontalSlider_su_2.valueChanged.connect(self.change_su_2)
        self.ui.horizontalSlider_vu_2.valueChanged.connect(self.change_vu_2)
        self.ui.pushButton_saveTrackConfig.clicked.connect(self.saveTrackConfig)
        self.ui.lineEdit_targetLen_2.setPlaceholderText(str(self.vision.target_size_2[0]))
        self.ui.lineEdit_targetWid_2.setPlaceholderText(str(self.vision.target_size_2[1]))
        self.ui.lineEdit_dis.setPlaceholderText(str(self.vision.hold_dis))
        self.ui.lineEdit_lamda.setPlaceholderText(str(self.vision.lamda))
        self.ui.pushButton_change_waitJoint_2.clicked.connect(self.change_waitJoint_2)
        self.ui.pushButton_track.clicked.connect(self.track)
        self.vision.track_info_signal.connect(self.update_track_info)
        self.ui.pushButton_roi_2.clicked.connect(self.roiView_2)
        
        #*********************交互控制页***********************#     
        # 加载图片
        pixmap = QPixmap('ui/stick_cartesian.png')
        self.ui.label_stick_cartesian.setPixmap(pixmap)
        pixmap = QPixmap('ui/stick_joint.png')
        self.ui.label_stick_joint.setPixmap(pixmap)
        self.ui.label_stick_joint.show()  
        self.ui.label_stick_cartesian.show()
        self.ui.label_stick_joint.setVisible(False)           
        self.ui.pushButton_stickUpdate.clicked.connect(self.stickUpdate)
        self.ui.pushButton_stickOpen.clicked.connect(self.stickOpen)
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
        port_list=self.robot.get_serial_port()
        self.ui.comboBox_port.clear()
        self.ui.comboBox_port.addItems(port_list)
        print('更新完毕')
        
    def portEstablish(self):
        if self.robot.ser.isOpen()==False:
            self.robot.port=self.ui.comboBox_port.currentText()
            self.robot.baudrate=int(self.ui.comboBox_baud.currentText())
            ret=self.robot.open_port()
            if ret == False:
                QMessageBox.warning(self.ui,'Warning','串口打开失败！')
            else:
                QMessageBox.information(self.ui,'Information','串口打开成功！')
                self.ui.pushButton_establish.setText('断开')
        else:
            self.robot.close_port()
            QMessageBox.information(self.ui,'Information','串口已断开！')
            self.ui.pushButton_establish.setText('连接')
    def portSend(self):
        # 将文本追加到QTextEdit中
        cur_text=self.ui.plainTextEdit_send.toPlainText()
        self.ui.textEdit_send.moveCursor(QTextCursor.End)
        self.ui.textEdit_send.insertPlainText('>>>'+cur_text + '\n')
        self.ui.textEdit_send.moveCursor(QTextCursor.End)
        #串口发送
        self.robot.ser.write(cur_text.encode('utf-8'))
    
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
        
    def update_liveVideo(self,frame):
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        self.ui.label_liveVideo.setPixmap(pixmap)

    def cameraUpdate(self):
        camera_list=self.vision.get_camera_list()
        self.ui.comboBox_camera.clear()
        self.ui.comboBox_camera.addItems(camera_list)
        print('相机列表更新完毕')        

    def cameraOpen(self):
        if not self.vision.is_running:
            self.vision.camera_index=int(self.ui.comboBox_camera.currentText())
            self.vision.start()
            self.vision.is_running=True
            self.ui.pushButton_cameraOpen.setText('关闭')
        else:
            self.vision.is_running=False
            self.ui.pushButton_cameraOpen.setText('打开')
    def snap(self):
        if self.vision.snap(self.teach.joint_cur_paras):
            self.ui.textEdit_clibInfo.moveCursor(QTextCursor.End)
            self.ui.textEdit_clibInfo.insertPlainText('>>>'+'成功保存第'+str(len(self.vision.handeye_joints))+'张图片及相应位姿!' + '\n')
            self.ui.textEdit_clibInfo.moveCursor(QTextCursor.End)
        else:
            self.ui.textEdit_clibInfo.moveCursor(QTextCursor.End)
            self.ui.textEdit_clibInfo.insertPlainText('>>>snap failed...' + '\n')
            self.ui.textEdit_clibInfo.moveCursor(QTextCursor.End)
            
    # def clibRun(self): 
    #     if not self.ui.pushButton_cameraOpen.text()=='关闭':
    #         QMessageBox.warning(self.ui, 'Warning', '请先打开相机！')
    #     else:
    #         if self.ui.checkBox_clibCheck.isChecked():
    #             print('已确认标定')
                
    #             if len(self.vision.handeye_joints)<2:
    #                 print('位姿少于两组,无法求解')
    #                 if os.path.isfile('calibration\handeye_clib\hand_eye\机械臂末端位姿.xlsx'):
    #                     reply = QMessageBox.question(self.ui, "询问", "没有进行新的拍照，确定要用以前的拍照进行标定吗？", QMessageBox.Yes | QMessageBox.No)
    #                     if reply == QMessageBox.Yes:
    #                         good_pictures,RT=hangeye_calibration()
    #                         if good_pictures<2:
    #                             QMessageBox.warning(self.ui, 'Warning', '有效标定位姿少于两个！标定失败！')
    #                             return 
    #                         else:
    #                             self.vision.eye_to_end=RT
    #                             # 保存NumPy数组到文件
    #                             np.save('calibration/handeye_clib/eye_to_end.npy', RT)
    #                             QMessageBox.information(self.ui, 'Information', '标定完成！'+'有效位姿数：'+str(good_pictures))
    #                             self.ui.textEdit_clibInfo.moveCursor(QTextCursor.End)
    #                             self.ui.textEdit_clibInfo.insertPlainText('>>>'+'手眼标定完成！' + '\n')
    #                             self.ui.textEdit_clibInfo.moveCursor(QTextCursor.End)
    #                             return 
    #                     else:
    #                         # 用户选择了“否”
    #                         return
    #                 else :       
    #                     QMessageBox.warning(self.ui, 'Warning', '位姿少于两组,无法求解！')
    #                     return 
    #             else:
                    
    #                 # 将数据转换为DataFrame
    #                 # print('self.vision.handeye_joints:',self.vision.handeye_joints)
    #                 df = pd.DataFrame(self.vision.handeye_joints, columns=["J1（度）", "J2（度）","J3（度）","J4（度）","J5（度）"])
    #                 # print('df:',df)
    #                 df.to_excel("calibration/handeye_clib/hand_eye/机械臂末端位姿.xlsx", index=False)
                
    #                 good_pictures,RT=hangeye_calibration()
    #                 if good_pictures<2:
    #                     QMessageBox.warning(self.ui, 'Warning', '有效标定位姿少于两个！标定失败！')
    #                 else:
    #                     self.vision.eye_to_end=RT
    #                     # 保存NumPy数组到文件
    #                     np.save('calibration/handeye_clib/eye_to_end.npy', RT)
    #                     QMessageBox.information(self.ui, 'Information', '标定完成！'+'有效位姿数：'+str(good_pictures))
    #                     self.ui.textEdit_clibInfo.moveCursor(QTextCursor.End)
    #                     self.ui.textEdit_clibInfo.insertPlainText('>>>'+'手眼标定完成！' + '\n')
    #                     self.ui.textEdit_clibInfo.moveCursor(QTextCursor.End)
    #         else:
    #             QMessageBox.warning(self.ui, 'Warning', '请先确认标定！')

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
        
    #抓取槽函数
    def change_hl(self):
        self.vision.hsv_lower[0]=int(self.ui.horizontalSlider_hl.value())
        print('hl改变为 ',self.vision.hsv_lower[0])
    def change_sl(self):
        self.vision.hsv_lower[1]=int(self.ui.horizontalSlider_sl.value())
        print('sl改变为 ',self.vision.hsv_lower[1])
    def change_vl(self):
        self.vision.hsv_lower[2]=int(self.ui.horizontalSlider_vl.value())
        print('vl改变为 ',self.vision.hsv_lower[2])
    def change_hu(self):
        self.vision.hsv_upper[0]=int(self.ui.horizontalSlider_hu.value())
        print('hu改变为 ',self.vision.hsv_upper[0])
    def change_su(self):
        self.vision.hsv_upper[1]=int(self.ui.horizontalSlider_su.value())
        print('su改变为 ',self.vision.hsv_upper[1])
    def change_vu(self):
        self.vision.hsv_upper[2]=int(self.ui.horizontalSlider_vu.value())
        print('vu改变为 ',self.vision.hsv_upper[2])
    def savePickConfig(self):
        if self.ui.lineEdit_targetLen.text():
            self.vision.target_size[0]=int(self.ui.lineEdit_targetLen.text())
        if self.ui.lineEdit_targetWid.text():
            self.vision.target_size[1]=int(self.ui.lineEdit_targetWid.text())
        if self.ui.lineEdit_placeX.text():
            self.vision.place_pose[0]=int(self.ui.lineEdit_placeX.text())
        if self.ui.lineEdit_placeY.text():
            self.vision.place_pose[1]=int(self.ui.lineEdit_placeY.text())
        print('成功修改夹取配置：',self.vision.target_size,'，',self.vision.place_pose)
    def change_waitJoint(self):
        # 创建一个询问对话框
        confirmation = QMessageBox.question(self.ui, 'Confirmation', '确认修改waitJoint?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirmation==QMessageBox.Yes:
            # 深拷贝
            deep_copy_of_one = copy.deepcopy(self.teach.joint_cur_paras)
            self.vision.waitJoint=deep_copy_of_one
            print('waitJoint改变为 ',self.vision.waitJoint)
    def pick(self):
        if self.vision.is_grasping==False:
            
            # 创建一个询问对话框
            confirmation = QMessageBox.question(self.ui, 'Confirmation', '确认启动抓取?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if confirmation==QMessageBox.Yes:
                self.ui.textEdit_pickInfo.moveCursor(QTextCursor.End)
                self.ui.textEdit_pickInfo.insertPlainText('>>>'+'启动视觉抓取程序...' + '\n')
                self.ui.textEdit_pickInfo.moveCursor(QTextCursor.End)
                #设置待命位置
                time.sleep(1)
                self.robot.send_command(self.vision.waitJoint,'1000')
                time.sleep(1)
                # uart.send_command(self.vision.waitJoint,'0500')
                # time.sleep(1)
                self.robot.set_grapper_pwm(1100)
                time.sleep(1)
                self.robot.set_grapper_pwm(1100)
                self.vision.uart=self.robot #引用传参
                self.vision.teach=self.teach#引用传参
                self.vision.is_grasping=True#启动抓取，多线程
                self.ui.pushButton_pick.setText('停止抓取')
        else:
            self.vision.is_grasping=False
            self.ui.pushButton_pick.setText('启动抓取')
            self.ui.textEdit_pickInfo.moveCursor(QTextCursor.End)
            self.ui.textEdit_pickInfo.insertPlainText('>>>'+'已停止视觉抓取程序...' + '\n')
            self.ui.textEdit_pickInfo.moveCursor(QTextCursor.End)
            #设置待命位置
            self.robot.send_command(self.vision.waitJoint,'0800')
            time.sleep(0.02)
            self.robot.send_command(self.vision.waitJoint,'0800')
            time.sleep(1)
            self.robot.set_grapper_pwm(1100)
            
    def update_grasp_info(self,info):
        self.ui.textEdit_pickInfo.moveCursor(QTextCursor.End)
        self.ui.textEdit_pickInfo.insertPlainText(info+ '\n')
        self.ui.textEdit_pickInfo.moveCursor(QTextCursor.End)
        self.update_all_lables()
    def roiView(self):
        if self.vision.is_roiViewing==False:
            self.vision.is_roiViewing=True
            self.ui.pushButton_roi.setText('关闭预览')
        else:
            self.vision.is_roiViewing=False
            self.ui.pushButton_roi.setText('开启预览')
            
    #跟踪槽函数
    def change_hl_2(self):
        self.vision.hsv_lower_2[0]=int(self.ui.horizontalSlider_hl_2.value())
        print('hl_2改变为 ',self.vision.hsv_lower_2[0])
    def change_sl_2(self):
        self.vision.hsv_lower_2[1]=int(self.ui.horizontalSlider_sl_2.value())
        print('sl_2改变为 ',self.vision.hsv_lower_2[1])
    def change_vl_2(self):
        self.vision.hsv_lower_2[2]=int(self.ui.horizontalSlider_vl_2.value())
        print('vl_2改变为 ',self.vision.hsv_lower_2[2])
    def change_hu_2(self):
        self.vision.hsv_upper_2[0]=int(self.ui.horizontalSlider_hu_2.value())
        print('hu_2改变为 ',self.vision.hsv_upper_2[0])
    def change_su_2(self):
        self.vision.hsv_upper_2[1]=int(self.ui.horizontalSlider_su_2.value())
        print('su_2改变为 ',self.vision.hsv_upper_2[1])
    def change_vu_2(self):
        self.vision.hsv_upper_2[2]=int(self.ui.horizontalSlider_vu_2.value())
        print('vu_2改变为 ',self.vision.hsv_upper_2[2])

    def saveTrackConfig(self):
        if self.ui.lineEdit_targetLen_2.text():
            self.vision.target_size_2[0]=int(self.ui.lineEdit_targetLen_2.text())
        if self.ui.lineEdit_targetWid_2.text():
            self.vision.target_size_2[1]=int(self.ui.lineEdit_targetWid_2.text())
        if self.ui.lineEdit_dis.text():
            self.vision.hold_dis=int(self.ui.lineEdit_dis.text())
        if self.ui.lineEdit_lamda.text():
            self.vision.lamda=float(self.ui.lineEdit_lamda.text())
        print('成功修改跟踪配置：',self.vision.target_size_2,'，',self.vision.hold_dis,'，',self.vision.lamda)
    
    def change_waitJoint_2(self):
        # 创建一个询问对话框
        confirmation = QMessageBox.question(self.ui, 'Confirmation', '确认修改waitJoint?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirmation==QMessageBox.Yes:
            # 深拷贝
            deep_copy_of_one = copy.deepcopy(self.teach.joint_cur_paras)
            self.vision.waitJoint_2=deep_copy_of_one
            print('waitJoint_2改变为 ',self.vision.waitJoint_2)
    def track(self):
        if self.vision.is_tracking ==False:
            confirmation = QMessageBox.question(self.ui, 'Confirmation', '确认开始追踪物体?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if confirmation==QMessageBox.Yes:
                self.vision.uart_2=self.robot
                self.vision.teach_2=self.teach
                #设置待命位置
                points=[self.teach.joint_cur_paras+[1100],self.vision.waitJoint_2+[1100]]
                print('points：',points)
                self.teach.joint_point_teach(self.robot,points)
                time.sleep(1)
                self.vision.is_tracking=True
                self.ui.pushButton_track.setText('停止跟踪')
                self.ui.textEdit_trackInfo.moveCursor(QTextCursor.End)
                self.ui.textEdit_trackInfo.insertPlainText('>>>'+'开始物体追踪...' + '\n')
                self.ui.textEdit_trackInfo.moveCursor(QTextCursor.End)
        else:
            confirmation = QMessageBox.question(self.ui, 'Confirmation', '确认停止追踪物体?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if confirmation==QMessageBox.Yes:
                self.vision.is_tracking=False
                self.ui.pushButton_track.setText('开始跟踪')
                self.ui.textEdit_trackInfo.moveCursor(QTextCursor.End)
                self.ui.textEdit_trackInfo.insertPlainText('>>>'+'终止物体追踪...' + '\n')
                self.ui.textEdit_trackInfo.moveCursor(QTextCursor.End)
    def update_track_info(self,info):
        self.ui.textEdit_trackInfo.moveCursor(QTextCursor.End)
        self.ui.textEdit_trackInfo.insertPlainText(info+ '\n')
        self.ui.textEdit_trackInfo.moveCursor(QTextCursor.End)
        self.update_all_lables()
        
    def roiView_2(self):
        if self.vision.is_roiViewing_2==False:
            self.vision.is_roiViewing_2=True
            self.ui.pushButton_roi_2.setText('关闭预览')
        else:
            self.vision.is_roiViewing_2=False
            self.ui.pushButton_roi_2.setText('开启预览')
    
        
if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)#这句可以解决ui加载后与designer中预览不一样的问题
    app = QtWidgets.QApplication([])
    app.setStyle('Fusion')  # Fusion风格是一种现代风格
    jibot = JIBot()
    jibot.ui.show()
    app.exec_()
