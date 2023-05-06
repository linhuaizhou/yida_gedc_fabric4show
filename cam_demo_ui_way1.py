# Copyright (c) OpenMMLab. All rights reserved.

"""开发日志：
修改image.py中的展现形式为cv2.show,源码中提示可能会有部分小错误，但是实际运行除了帧数低其他都还好
"""
import datetime
import os
import re
import sys
import time

import cv2
import mmcv
import torch
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, QBasicTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsScene, QMessageBox, QApplication
from matplotlib import pyplot as plt
from mmdet.apis import init_detector, inference_detector
import threading
import show4fabric
from show4fabric import Ui_fabric4showby1hz
from show4fabric_en import Ui_fabric4showby1hz

import pandas as pd
from collections import Counter
import serial
from fabric_t_i import create_rgb_hist, hist_compare, handle_img
from frame_processing import frame2video, frame2gif


class mywindow(QtWidgets.QWidget, Ui_fabric4showby1hz):

    def __init__(self):
        super(mywindow, self).__init__()
        self.work_5 = WorkThread_5()
        global pv
        pv = 0
        self.defect_treatment_flag = defect_treatment
        self.setupUi(self)

        self.cap = camera  # 视频流
        # self.CAM_NUM = 0 # 为0时表示视频流来自笔记本内置摄像头
        self.work = WorkThread()
        self.work_1 = WorkThread_1()
        self.work_2 = WorkThread_2()
        self.work_3 = WorkThread_3()
        self.work_4 = WorkThread_4()
        # self.work_5 = WorkThread_5()
        self.R = 255
        self.G = 255
        self.B = 255
        # self.timer1 = QBasicTimer()
        self.slot_init()  # 初始化槽函数

    def slot_init(self):
        self.pushButton.clicked.connect(self.button_open_camera_clicked)  # 若该按键被点击，则调用button_open_camera_clicked()
        self.timer_camera.timeout.connect(self.show_camera)  # 若定时器结束，则调用show_camera()
        self.pushButton_2.clicked.connect(self.show_camera_1)
        self.pushButton_3.clicked.connect(self.ColorAdjust)
        self.pushButton_4.clicked.connect(self.serial_listener)
        self.pushButton_5.clicked.connect(self.ColorInit)
        self.pushButton_6.clicked.connect(self.serial_listener_close)
        self.pushButton_7.clicked.connect(self.serial_send_1)  # 底层传送带手动
        self.pushButton_8.clicked.connect(self.serial_send_0)  # 底层传送带手动
        self.pushButton_9.clicked.connect(self.defect_rating_enable)  # 缺陷评分使能
        self.pushButton_10.clicked.connect(self.defect_rating_disable)  # 缺陷评分关闭
        self.pushButton_11.clicked.connect(self.serial_send_auto)  # 底层传送带自动
        self.pushButton_12.clicked.connect(self.serial_send_auto_close)  # 底层传送带自动
        self.pushButton_13.clicked.connect(self.defect_treatment_enable)
        self.pushButton_14.clicked.connect(self.defect_treatment_disable)
        self.pushButton_15.clicked.connect(self.cloth_supplement_enable)
        self.pushButton_16.clicked.connect(self.cloth_supplement_disable)
        self.pushButton_17.clicked.connect(self.track_changing_enable)
        self.pushButton_18.clicked.connect(self.track_changing_disable)

        self.pushButton_19.clicked.connect(self.classification_self_check)
        self.pushButton_20.clicked.connect(self.classification_stop)
        self.pushButton_21.clicked.connect(self.serial_1_listener)
        self.pushButton_22.clicked.connect(self.serial_1_listener_close)
        self.pushButton_23.clicked.connect(self.slide_control_move2center)
        # self.pushButton_23.clicked.connect(self.myTimerState)
        # self.pushButton_24.clicked.connect(self.slide_control_stop)
        # self.pushButton_25.clicked.connect(self.slide_control_return_location)
        self.pushButton_26.clicked.connect(self.slide_control_back2zero)
        # self.pushButton_26.clicked.connect(self.myTimerState)
        self.pushButton_27.clicked.connect(self.slide_control_forward)
        self.pushButton_28.clicked.connect(self.slide_control_backward)
        self.pushButton_29.clicked.connect(self.slide_control_left)
        self.pushButton_30.clicked.connect(self.slide_control_right)
        self.pushButton_31.clicked.connect(self.detection_with_process)
        self.pushButton_32.clicked.connect(self.detection_with_process_disable)
        self.pushButton_33.clicked.connect(self.detection_not_process)
        self.pushButton_34.clicked.connect(self.detection_not_process_disable)
        self.pushButton_35.clicked.connect(self.set_pr_value)
        self.pushButton_36.clicked.connect(self.slide_control_up)
        self.pushButton_37.clicked.connect(self.slide_control_down)
        self.pushButton_38.clicked.connect(self.defect_video_save)
        self.pushButton_39.clicked.connect(self.defect_gif_save)
        self.pushButton_40.clicked.connect(self.pic_save)
        self.pushButton_41.clicked.connect(self.log_save)
        self.pushButton_42.clicked.connect(self.warning_selfcheck)
        self.pushButton_43.clicked.connect(self.auto_all_stop_enable)
        self.pushButton_44.clicked.connect(self.auto_all_stop_disable)
        self.pushButton_2.setEnabled(False)
        self.pushButton_31.setEnabled(False)
        self.pushButton_33.setEnabled(False)
        self.pushButton_43.setEnabled(False)
        self.pushButton_44.setEnabled(False)

        self.horizontalSlider.valueChanged.connect(self.SetR)
        self.horizontalSlider_2.valueChanged.connect(self.SetG)
        self.horizontalSlider_3.valueChanged.connect(self.SetB)
        # progressBar
        # self.progressBar.setGeometry(QtCore.QRect(20, 20, 450, 50))

        self.progressBar.setMinimum(0)
        self.progressBar.setMinimum(100)
        # self.progressBar.setValue(pv)

    def myTimerState(self):
        if self.timer1.isActive():
            self.timer1.stop()
        else:
            self.timer1.start(100, self)

    def timerEvent(self, e):
        if self.pv == 100:
            self.timer1.stop()
            self.printf("当前控制已完成")
        else:
            self.pv += 10 / 20
            print(self.pv)
            self.progressBar.setValue(self.pv)

    def copy_file(self, i):
        # print(type(i))

        self.progressBar.setValue(i)
        QtWidgets.QApplication.processEvents()
        if i == 85:
            self.printf("当前移动操作已完成！")
            self.work_5.disconnect()

    def template_signal_read(self, t):
        self.lcdNumber_4.display(int(t))

    def printf(self, mypstr):

        if mypstr == "show_result_fps":
            self.lcdNumber_2.display(fps_1)
            self.lcdNumber_5.display(defect_score)

        else:
            self.textBrowser.append(mypstr)  # 在指定的区域显示提示信息
            self.cursot = self.textBrowser.textCursor()
            self.textBrowser.moveCursor(self.cursot.End)
            QtWidgets.QApplication.processEvents()  # 一定加上这个功能  ，不然有卡顿

    def printf_1(self, mypstr):
        self.textBrowser_2.append(mypstr)  # 在指定的区域显示提示信息
        self.cursot = self.textBrowser_2.textCursor()
        self.textBrowser_2.moveCursor(self.cursot.End)
        QtWidgets.QApplication.processEvents()  # 一定加上这个功能  ，不然有卡顿
        self.lcdNumber_3.display(run_distance)

    def printf_2(self, mypstr):
        global cloth_supplement_flag
        if mypstr == "hist_ok":
            cloth_supplement_flag = True
            #self.textBrowser.append("补充模块使能完成")  # 在指定的区域显示提示信息
            self.textBrowser.append("Supplement Part is Enable!")
            self.cursot = self.textBrowser.textCursor()
            self.textBrowser.moveCursor(self.cursot.End)
            QtWidgets.QApplication.processEvents()  # 一定加上这个功能  ，不然有卡顿
        else:
            self.textBrowser_3.append(mypstr)  # 在指定的区域显示提示信息
            self.cursot = self.textBrowser_3.textCursor()
            self.textBrowser_3.moveCursor(self.cursot.End)
            QtWidgets.QApplication.processEvents()  # 一定加上这个功能  ，不然有卡顿

    def closeEvent(self, event):  # 关闭所有窗口
        reply = QMessageBox.question(self, '提示', "是否要关闭所有窗口?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # ser_1.write("b")
            event.accept()
            sys.exit(0)  # 退出程序
        else:
            event.ignore()

    def show_camera_1(self):

        self.work.signal.connect(self.printf)
        self.work.start()

    def button_open_camera_clicked(self):
        if not self.timer_camera.isActive():  # 若定时器未启动
            self.show_camera()
            self.pushButton.setText('关闭相机')
        else:
            self.timer_camera.stop()  # 关闭定时器
            self.cap.release()  # 释放视频流
            self.label.clear()  # 清空视频显示区域
            self.pushButton.setText('打开相机')

    def show_camera(self):
        try:
            # self.work_4.start()
            while True:
                fps = camera.get(cv2.CAP_PROP_FPS)
                # print(fps)
                self.lcdNumber.display(fps)
                # self.lcdNumber_2.display(fps_1)
                flag, self.image = self.cap.read()  # 从视频流中读取

                show = cv2.resize(self.image, (640, 480))  # 把读到的帧的大小重新设置为 640x480
                # R, G, B = cv2.split(show)
                if change_rgb_flag:

                    R_1 = show[:, :, 0]
                    G_1 = show[:, :, 1]
                    B_1 = show[:, :, 2]
                    R_2 = R_1 * R / 255
                    G_2 = G_1 * G / 255
                    B_2 = B_1 * B / 255

                    img1 = show
                    show = img1
                    show[:, :, 0] = R_2
                    show[:, :, 1] = G_2
                    show[:, :, 2] = B_2

                else:
                    show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
                showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0],
                                         QtGui.QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
                self.label.setPixmap(QtGui.QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage
                # self.label_2.setPixmap(QtGui.QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage
                # self.work_4.start()
                c = cv2.waitKey(30) & 0xff
                if c == 27:
                    self.cap.release()
                    break

        except:
            self.rintf("工业相机输入中断！")

    def SetR(self):
        R = self.horizontalSlider.value()
        self.R = R / 100 * 255
        # print(self.R)
        self.spinBox.setValue(self.R)

    def SetG(self):
        G = self.horizontalSlider_2.value()
        self.G = G / 100 * 255
        # print(self.G)
        self.spinBox_2.setValue(self.G)

    def SetB(self):
        B = self.horizontalSlider_3.value()
        self.B = B / 100 * 255
        # print(self.B)
        self.spinBox_3.setValue(self.B)

    def ColorAdjust(self):
        global R
        global G
        global B
        global change_rgb_flag
        R = self.R
        G = self.G
        B = self.B
        change_rgb_flag = True

    def ColorInit(self):
        global change_rgb_flag
        change_rgb_flag = False
        self.horizontalSlider.setValue(0)
        self.horizontalSlider_2.setValue(0)
        self.horizontalSlider_3.setValue(0)
        self.spinBox.setValue(0)
        self.spinBox_2.setValue(0)
        self.spinBox_3.setValue(0)

    def serial_listener(self):
        self.work_1.signal.connect(self.printf_1)
        self.work_1.start()

    def serial_listener_close(self):
        self.work_1.disconnect()
        self.printf_1("串口已关闭！")
        # 这里就算串口关闭了 也算占用着的 因为串口的打开在最前面 所以这里后续需要改进

    def serial_1_listener(self):
        self.work_2.signal.connect(self.printf_2)
        self.work_2.start()

    def serial_1_listener_close(self):
        self.work_2.disconnect()
        self.printf_2("串口已关闭！")
        # 这里就算串口关闭了 也算占用着的 因为串口的打开在最前面 所以这里后续需要改进

    def serial_send_1(self):  # 正反取决于摆放方向
        try:
            self.pushButton_7.setEnabled(False)
            choose_1 = self.comboBox.currentText()
            if choose_1 == "0.01":
                ser.write("1+0.01".encode('utf-8'))
            if choose_1 == "0.1":
                ser.write("1+0.1".encode('utf-8'))
            if choose_1 == "1":
                # ser.write("1+1".encode('utf-8'))
                ser.write("1".encode('utf-8'))
            if choose_1 == "10":
                ser.write("1+10".encode('utf-8'))
            if choose_1 == "100":
                ser.write("1+100".encode('utf-8'))

            self.pushButton_7.setEnabled(True)
        except:
            self.printf("底层传送带手动控制反转失败，请检查设置和硬件")

    def serial_send_0(self):
        try:
            self.pushButton_8.setEnabled(False)
            choose_2 = self.comboBox.currentText()
            if choose_2 == "0.01":
                ser.write("0+0.01".encode('utf-8'))
            if choose_2 == "0.1":
                ser.write("0+0.1".encode('utf-8'))
            if choose_2 == "1":
                # ser.write("0+1".encode('utf-8'))
                ser.write("0".encode('utf-8'))
            if choose_2 == "10":
                ser.write("0+10".encode('utf-8'))
            if choose_2 == "100":
                ser.write("0+100".encode('utf-8'))
            # ser.write("0".encode('utf-8'))
            self.pushButton_8.setEnabled(True)
        except:
            self.printf("底层传送带手动控制正转失败，请检查设置和硬件")

    def serial_send_auto(self):  # 底层传送带自动控制 开始 按钮
        try:
            self.pushButton_11.setEnabled(False)
            choose_3 = self.comboBox_2.currentText()
            if choose_3 == "Level 1":
                ser.write("2+1".encode('utf-8'))
            if choose_3 == "Level 2":
                ser.write("2+2".encode('utf-8'))
            if choose_3 == "Level 3":
                # ser.write("2+3".encode('utf-8'))
                ser.write("2".encode('utf-8'))
            if choose_3 == "Level 4":
                ser.write("2+4".encode('utf-8'))
            if choose_3 == "Level 5":
                ser.write("2+5".encode('utf-8'))
            # ser.write("0".encode('utf-8'))
            self.pushButton_11.setEnabled(True)
        except:
            self.printf("底层传送带自动控制失败，请检查设置和硬件")

    def serial_send_auto_close(self):  # 底层传送带自动控制 停止 按钮
        try:
            ser.write("3".encode('utf-8'))
        except:
            self.printf("底层传送带自动控制失败，请检查设置和硬件")

    def defect_treatment_enable(self):
        try:
            global defect_treatment
            global defect_ranking
            defect_treatment = True
            defect_ranking_text = self.comboBox_3.currentText()
            defect_ranking = int(defect_ranking_text)
            print(defect_ranking)
            self.printf("缺陷处理已使能，缺陷预处理等级为" + defect_ranking_text)
        except:
            self.printf("error!")

    def defect_treatment_disable(self):
        global defect_treatment
        global defect_ranking
        defect_treatment = False
        defect_ranking = 3

        self.printf("缺陷处理已关闭")

    def track_changing_enable(self):
        global track_changing_flag
        track_changing_flag = True
        try:
            ser_1.write("s".encode('utf-8'))
            # ser_1.write("a".encode('utf-8'))
            # ser_1.write("d".encode('utf-8'))
            self.printf("变轨装置使能自检")

        except:
            self.printf("变轨装置使能自检失败，请检查设置和硬件")

    def track_changing_disable(self):
        global track_changing_flag
        track_changing_flag = False
        self.printf("变轨装置关闭")

    def defect_rating_enable(self):
        global defect_rating_flag
        defect_rating_flag = True
        self.printf("缺陷评分功能使能")

    def defect_rating_disable(self):
        global defect_rating_flag
        defect_rating_flag = False
        self.printf("缺陷评分功能关闭")

    def cloth_supplement_enable(self):
        global cloth_supplement_flag
        self.work_4.signal.connect(self.printf_2)
        self.work_4.start()
        # self.printf("布匹补充功能正在使能,请等待！")
        self.printf("Fabric supplement is initializing,please wait...")
        self.pushButton_2.setEnabled(True)

    def cloth_supplement_disable(self):
        global cloth_supplement_flag
        cloth_supplement_flag = False
        self.printf("布匹补充功能关闭")
        self.work_4.disconnect()

    def classification_self_check(self):
        self.printf("分类传送带自检")
        ser.write("4".encode('utf-8'))
        global classification_flag
        classification_flag = True

    def classification_stop(self):
        self.printf("分类传送带关闭")
        global classification_flag
        classification_flag = False

    def slide_control_move2center(self):
        try:
            ser_1.write("c".encode('utf-8'))
            # self.work_5.progressBarValue.connect(self.copy_file)
            self.work_5.progressBarValue.connect(self.copy_file)
            self.work_5.start()
            self.printf("工业相机进行自动中心")

        except:
            self.printf("工业相机二维滑台运动失败，请检查设置和硬件")

    def slide_control_back2zero(self):
        try:
            ser_1.write("b".encode('utf-8'))
            self.work_5.progressBarValue.connect(self.copy_file)
            self.work_5.start()
            self.printf("工业相机进行自动归零")
        except:
            self.printf("工业相机二维滑台运动失败，请检查设置和硬件")

    def slide_control_forward(self):
        try:
            ser_1.write("2".encode('utf-8'))
            self.printf("工业相机二维滑台向前移动")

        except:
            self.printf("工业相机二维滑台运动失败，请检查设置和硬件")

    def slide_control_backward(self):
        try:
            ser_1.write("3".encode('utf-8'))
            self.printf("工业相机二维滑台向后移动")

        except:
            self.printf("工业相机二维滑台运动失败，请检查设置和硬件")

    def slide_control_up(self):
        try:
            ser_1.write("4".encode('utf-8'))
            self.printf("工业相机二维滑台向上移动")

        except:
            self.printf("工业相机二维滑台运动失败，请检查设置和硬件")

    def slide_control_down(self):
        try:
            ser_1.write("5".encode('utf-8'))
            self.printf("工业相机二维滑台向下移动")
        except:
            self.printf("工业相机二维滑台运动失败，请检查设置和硬件")

    def slide_control_left(self):
        try:
            ser_1.write("0".encode('utf-8'))
            self.printf("工业相机二维滑台向左移动")

        except:
            self.printf("工业相机二维滑台运动失败，请检查设置和硬件")

    def slide_control_right(self):
        try:
            ser_1.write("1".encode('utf-8'))
            self.printf("工业相机二维滑台向右移动")

        except:
            self.printf("工业相机二维滑台运动失败，请检查设置和硬件")

    def detection_not_process(self):
        ser.write("2".encode('utf-8'))  # 使能底层传送带

    def detection_not_process_disable(self):
        ser.write("3".encode('utf-8'))  # 使能底层传送带

    def detection_with_process(self):
        global auto_start_flag
        auto_start_flag = True
        self.work_3.signal.connect(self.printf)
        self.work_3.template_signal.connect(self.template_signal_read)
        self.work_3.start()
        # self.work_4.signal.connect(self.printf)
        # self.work_4.start()

    def detection_with_process_disable(self):
        global auto_start_flag
        auto_start_flag = False
        try:

            ser.write("3".encode('utf-8'))
            # ser_1.write("a".encode('utf-8'))  # 变轨装置归位
            ser.write("Q".encode('utf-8'))  # 缺陷传送带关闭
            self.work_3.disconnect()
            # self.work_4.disconnect()


        except:
            self.printf("缺陷检测关闭失败")

    def set_pr_value(self):
        global env_PR_value
        print(int(self.lineEdit_2.text()))

        # print(type(int(self.lineEdit_2.text())))
        s = int(self.lineEdit_2.text())
        env_PR_value = s
        # self.printf("光敏传感器环境值已设置为" + self.lineEdit_2.text())
        self.printf("The environment value of the photosensitive sensor has been set to" + self.lineEdit_2.text())
        self.pushButton_31.setEnabled(True)
        self.pushButton_33.setEnabled(True)

    def warning_selfcheck(self):
        try:
            ser_1.write("w".encode('utf-8'))
            time.sleep(1)
            ser_1.write("m".encode('utf-8'))
            self.pushButton_43.setEnabled(True)
            self.pushButton_44.setEnabled(True)
            # self.printf("报警模块自检完成！")
            self.printf("Alarm module self-check completed!")

        except:
            self.printf("报警模块自检失败！")

    def auto_all_stop_enable(self):
        global auto_all_stop_flag
        auto_all_stop_flag = True
        self.printf("大面积缺陷自动停机模块使能成功！")

    def auto_all_stop_disable(self):
        global auto_all_stop_flag
        auto_all_stop_flag = False
        self.printf("大面积缺陷自动停机模块已关闭！")
        global warning_flag
        warning_flag = False
        ser_1.write("m".encode('utf-8'))

    def defect_video_save(self):
        try:  # meifayong
            # fv = frame2video.frame2video(raw_path=r"/running_saved/fabric_shortcut",
                                         # save_path=r"/running_saved/fabric_video/frames",
                                         # save2format_path=r"D:\1_related_documents\fabric4show\frames",
                                         # video_path=r"D:\1_related_documents\fabric4show\frames\save.avi", fps=5)
            # fv.rename()
            # fv.rename2format()
            # fv.frame2video()
            self.printf("检测视频输出完成！")
        except:
            self.printf("检测视频输出失败，请检查路径！")

    def defect_gif_save(self):
        try:
            # keyi  danshi  dei fang xiancheng
            # fg = frame2gif.frame2gif(r"D:\1_related_documents\30_研究生电赛\server_lhz\running_saved\fabric_shortcut",
                                     # r"D:\1_related_documents\30_研究生电赛\server_lhz\running_saved\fabric_result_gif"
                                     # r"\save.gif", 5)
            # fg.do()
            self.printf("检测GIF输出完成！")
        except:
            self.printf("检测GIF输出失败，请检查路径！")

    def pic_save(self):
        self.printf("缺陷截图模块已开启！")

    def log_save(self):
        self.printf("日志输出模块已开启！")


class __Autonomy__(object):
    def __init__(self):
        self._buff = ""

    def write(self, out_stream):
        self._buff += out_stream


class WorkThread(QThread):
    # 定义一个信号
    signal = pyqtSignal(str)

    # label_2 =
    def __int__(self):
        # 初始化函数，默认
        super(WorkThread, self).__init__()

    def run(self):
        try:
            # self.signal.emit('正在打开摄像头')
            self.signal.emit('Opening Camera...')
            device = torch.device('cuda:0')
            config = r"D:\1_related_documents\30_研究生电赛\server_lhz\mmdetection-master\configs/faster_rcnn/demo_faster_rcnn_r50_fpn_2x_coco.py "
            checkpoint = r"D:\1_related_documents\30_研究生电赛\server_lhz\mmdetection-master\tools\work_dirs\20220425_epoch_25\11\latest.pth"
            model = init_detector(config, checkpoint, device=device)
            # camera = cv2.VideoCapture(0)
            self.signal.emit('Press "Esc", "q" or "Q" to exit show4fabric window.')
            start_time = time.time()
            counter = 0
            global fps_1
            fps_1 = 0
            score_time_count = 0
            global defect_score_list_1

            global defect_score
            defect_score = 0
            # self.signal.emit('请设置好光敏传感器环境值！')
            self.signal.emit('Please set the environment value of the photosensitive sensor！')

            while True:
                global img
                ret_val, img = camera.read()

                # result = inference_detector(model, img)
                result = inference_detector(model, img)
                ch = cv2.waitKey(1)
                if ch == 27 or ch == ord('q') or ch == ord('Q'):
                    # format_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
                    # file_save = r"D:\1_related_documents\30_研究生电赛\server_lhz\running_saved\fabric_video"
                    # filename = file_save + "/" + str(format_time) + "_video_detection.avi"
                    # mmcv.frames2video(r'D:\1_related_documents\30_研究生电赛\server_lhz\running_saved\fabric_video', filename)
                    mmcv.frames2video(r'D:\1_related_documents\30_研究生电赛\server_lhz\running_saved\fabric_video',
                                      "test.avi")
                    break
                current = sys.stdout
                a = __Autonomy__()
                sys.stdout = a
                model.show_result(img, result, score_thr=0.5, wait_time=0.1, show=True)
                sys.stdout = current
                # print(a._buff)
                # print(type(a._buff))
                # global defect_score_list
                defect_score_list = list(a._buff)
                # print(str(defect_score_list))
                # file_save = r"D:\1_related_documents\30_研究生电赛\server_lhz\running_saved\fabric_video"
                # format_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
                # filename = file_save+"/"+str(format_time)+"_viedo_detection_pic.jpg"
                # pic_filename =r"D:\1_related_documents\30_研究生电赛\server_lhz\running_saved\fabric_video\video_detection_pic.jpg"
                # os.rename(pic_filename,str(num+1)+'.jpg')
                value_list = ["[", "]", "\n", " "]
                for value in value_list:
                    j = 0
                    for i in range(len(defect_score_list)):
                        if defect_score_list[j] == value:
                            defect_score_list.pop(j)
                        else:
                            j += 1
                print(defect_score_list)  # 当前帧识别到的缺陷及对应缺陷类型 编号0-13

                if score_time_count == 0:
                    defect_score_list_1 = defect_score_list
                if len(defect_score_list) > len(defect_score_list_1):
                    defect_score_list_1 = defect_score_list
                if score_time_count == 10:
                    # print(defect_score_list_1)
                    score_dict = {}
                    score_dict["0"] = 0
                    score_dict["1"] = 0
                    score_dict["2"] = 0
                    score_dict["3"] = 0
                    score_dict["4"] = 0
                    score_dict["5"] = 0
                    score_dict["6"] = 0
                    score_dict["7"] = 0
                    score_dict["8"] = 0
                    score_dict["9"] = 0
                    score_dict["10"] = 0
                    score_dict["11"] = 0
                    score_dict["12"] = 0
                    score_dict["13"] = 0

                    for i in defect_score_list_1:
                        if defect_score_list_1.count(i) >= 1:
                            score_dict[i] = defect_score_list_1.count(i)
                    # print(score_dict)
                    # defect_score = 0.1 * int(score_dict["0"])
                    defect_score_1 = 0.15 * int(score_dict["0"]) + 0.15 * int(score_dict["1"]) + 0.1 * int(
                        score_dict["2"]) + 0.1 * int(score_dict["3"]) + 0.1 * int(score_dict["4"]) + 0.1 * int(
                        score_dict["5"]) + 0.1 * int(score_dict["6"]) + 0.1 * int(score_dict["7"]) + 0.1 * int(
                        score_dict["8"]) + 0.1 * int(score_dict["9"]) + 0.1 * int(score_dict["10"]) + 0.1 * int(
                        score_dict["11"]) + 0.05 * int(score_dict["12"]) + 0.05 * int(score_dict["13"])
                    defect_score = 100 * defect_score_1
                    print(defect_score)  # 字典声明有问题 应该补充其他的0-13 都要补充成类别
                    score_time_count = 0
                    defect_score_list_1 = []

                self.signal.emit('show_result_fps')
                counter += 1
                score_time_count += 1
                fps_1 = counter / (time.time() - start_time)
                self.signal.emit('show_result_fps')


        except:
            self.signal.emit('目标检测输出失败')


class WorkThread_1(QThread):
    # 定义一个信号
    signal = pyqtSignal(str)

    # label_2 =
    def __int__(self):
        # 初始化函数，默认
        super(WorkThread_1, self).__init__()

    def run(self):
        try:

            global run_distance
            run_distance = 0
            self.signal.emit("正在打开串口....")
            # 这里可以加一个步进电机自检XXX之类 加一个进度条
            while True:
                data = ser.readline()  # 按行读取串口数据进来
                data = data.decode()  # 读进来的数据是bytes形式，需要转化为字符串格式
                try:
                    data_1 = data[data.index("|run_distance="):]
                    # self.signal.emit(data_1.replace("|run_distance=", ""))
                    run_distance = data_1.replace("|run_distance=", "")
                    # print(run_distance)
                    self.signal.emit(data)
                except:
                    self.signal.emit(data)
        except:
            self.signal.emit("请检查串口是否被占用！")


class WorkThread_2(QThread):
    # 定义一个信号
    signal = pyqtSignal(str)

    # 此线程监听工业相机二维滑台的串口 Arduino（2）  负责控制二维滑台+变轨装置
    # label_2 =
    def __int__(self):
        # 初始化函数，默认
        super(WorkThread_2, self).__init__()

    def run(self):
        try:

            global camera_x
            global camera_y
            global data_guangmin
            self.signal.emit("正在打开串口....")
            # 这里可以加一个步进电机自检XXX之类 加一个进度条
            while True:
                data = ser_1.readline()  # 按行读取串口数据进来
                data = data.decode()  # 读进来的数据是bytes形式，需要转化为字符串格式
                # print(data)
                try:
                    # Arduino部分代码向外传当前X轴Y轴的坐标，上位机下发XY轴需要移动的步长
                    data_1 = data[data.index("guangmin="):]  # 数据切片
                    # self.signal.emit(data_1.replace("|run_distance=", ""))
                    data_guangmin = data_1.replace("guangmin=", "")  # replace 参考一下 原来的内容
                    # print(run_distance)
                    # print(data)
                    # print(data_guangmin)
                    # print(type(data_guangmin))
                    # print(type(int(data_guangmin)))
                    print((int(data_guangmin)))
                    self.signal.emit(data)
                except:
                    self.signal.emit(data)
        except:
            self.signal.emit("请检查串口是否被占用！")


class WorkThread_3(QThread):
    # 定义一个信号
    signal = pyqtSignal(str)
    template_signal = pyqtSignal(str)

    # 此线程监听做缺陷检测+处理的工作流程
    # label_2 =
    def __int__(self):
        # 初始化函数，默认
        super(WorkThread_3, self).__init__()

    def run(self):
        global env_PR_value
        global auto_start_flag
        global fabric_template_identification_flag
        global warning_flag

        # print(type(env_PR_value))
        ser.write("2".encode('utf-8'))  # 使能底层传送带
        track_changing_flag_1 = False
        warning_flag = False
        while auto_start_flag is True:
            if defect_score > 230:
                ser_1.write("w".encode('utf-8'))
                ser.write("3".encode('utf-8'))
                ser.write("Q".encode('utf-8'))  # 缺陷传送带关闭
                warning_flag = True
                self.signal.emit("Waring！大面积缺陷报警！！！")
            if defect_score > 70 and int(
                    data_guangmin) > env_PR_value + 20 and not warning_flag:  # 0911 将这里面的光敏组织判断做嵌套 不要同时判断 但是这样会增加运算量
                ser.write("3".encode('utf-8'))  # auto run 底层传送带
                image = img
                cv2.imwrite("running_saved/fabric_template_running_saved/saved_pic.jpg", image)
                fabric_template_identification_flag = True

                if track_changing_flag_1 is False:
                    ser_1.write("d".encode('utf-8'))  # 变轨装置变轨
                    track_changing_flag_1 = True
                    ser.write("q".encode('utf-8'))  # 缺陷传送带使能
                if fabric_template_identification_flag:
                    img_template_8 = cv2.imread("running_saved/fabric_template_running_saved/saved_pic.jpg")
                    img_template_8 = handle_img(img_template_8)
                    hist6 = create_rgb_hist(img_template_8)
                    com1 = hist_compare(hist1, hist6)
                    com2 = hist_compare(hist2, hist6)
                    com3 = hist_compare(hist3, hist6)
                    com4 = hist_compare(hist4, hist6)
                    com5 = hist_compare(hist5, hist6)
                    # com7 = hist_compare(hist7, hist6)
                    list_compare = ["red", "yellow", "green", "blue", "deepred"]
                    list_com = [com1, com2, com3, com4, com5]
                    # print(list_com)
                    # self.signal.emit(str(list_com))

                    dic_compare = dict(zip(list_compare, list_com))
                    result = max(dic_compare, key=lambda x: dic_compare[x])
                    print(result)
                    self.signal.emit(str(result))
                    self.template_signal.emit(str(list_compare.index(result)))
                    if result == "yellow":
                        ser_1.write("l".encode('utf-8'))  # 变轨装置变轨  kazhu le zheli
                        time.sleep(6)
                        ser_1.write("L".encode('utf-8'))  # 变轨装置变轨
                    if result == "green":
                        ser_1.write("n".encode('utf-8'))  # 变轨装置变轨
                        time.sleep(6)
                        ser_1.write("N".encode('utf-8'))  # 变轨装置变轨
                    if result == "deepred" or result == "red":
                        ser_1.write("o".encode('utf-8'))  # 变轨装置变轨
                        time.sleep(6)
                        ser_1.write("O".encode('utf-8'))  # 变轨装置变轨
                    fabric_template_identification_flag = False

            if int(data_guangmin) < env_PR_value + 20 and defect_score <= 70 and not warning_flag:
                if track_changing_flag_1:
                    ser_1.write("a".encode('utf-8'))  # 变轨装置归位
                    track_changing_flag_1 = False
                    time.sleep(2)

                # ser.write("Q".encode('utf-8'))  # 缺陷传送带关闭
                # ser.write("2".encode('utf-8'))  # 使能底层传送带

            self.signal.emit("正常")
            time.sleep(2)


class WorkThread_4(QThread):
    # 定义一个信号
    signal = pyqtSignal(str)

    # 此线程监听做缺陷检测+处理的工作流程
    # label_2 =
    def __int__(self):
        # 初始化函数，默认
        super(WorkThread_4, self).__init__()

    def run(self):
        global hist1
        global hist2
        global hist3
        global hist4
        global hist5
        global hist7
        # global hist_ok_flag
        img_template_1 = cv2.imread(r"running_saved\fabric_template_pre_saved\new\red.jpg")
        img_template_1 = handle_img(img_template_1)
        img_template_2 = cv2.imread(r"running_saved\fabric_template_pre_saved\new\yellow.jpg")
        img_template_2 = handle_img(img_template_2)
        img_template_3 = cv2.imread(r"running_saved\fabric_template_pre_saved\new\green.jpg")
        img_template_3 = handle_img(img_template_3)
        img_template_4 = cv2.imread(r"running_saved\fabric_template_pre_saved\new\blue.jpg")
        img_template_4 = handle_img(img_template_4)
        img_template_5 = cv2.imread(r"running_saved\fabric_template_pre_saved\new\deepred.jpg")
        img_template_5 = handle_img(img_template_5)
        img_template_7 = cv2.imread(r"running_saved\fabric_template_pre_saved\new\empty.jpg")
        img_template_7 = handle_img(img_template_7)
        hist1 = create_rgb_hist(img_template_1)
        hist2 = create_rgb_hist(img_template_2)
        hist3 = create_rgb_hist(img_template_3)
        hist4 = create_rgb_hist(img_template_4)
        hist5 = create_rgb_hist(img_template_5)
        hist7 = create_rgb_hist(img_template_7)
        # hist_ok_flag = True
        self.signal.emit("hist_ok")


class WorkThread_5(QThread):
    # 定义一个信号
    progressBarValue = pyqtSignal(int)

    def __int__(self):
        # 初始化函数，默认
        super(WorkThread_5, self).__init__()

    def run(self):
        for i in range(101):
            time.sleep(0.2)
            self.progressBarValue.emit(i)


if __name__ == '__main__':
    # main()
    global camera
    # global camera_template
    global camera_x
    global camera_y
    global fps_1
    global R
    global G
    global B
    global change_rgb_flag
    global run_distance
    global ser
    global defect_treatment
    global defect_ranking
    global track_changing_flag
    global defect_rating_flag
    global cloth_supplement_flag
    global classification_flag
    global defect_score
    global defect_score_reset_flag
    global defect_score_list_1
    global data_guangmin
    global env_PR_value
    global auto_start_flag
    global img
    global fabric_template_identification_flag
    global auto_all_stop_flag
    global pv
    global hist1
    global hist2
    global hist3
    global hist4
    global hist5
    global hist7
    global hist_ok_flag
    global warning_flag
    # 用来循环选择最佳的当前布匹所有缺陷类型
    change_rgb_flag = False
    defect_treatment = False
    defect_ranking = 3
    track_changing_flag = False
    defect_rating_flag = False
    cloth_supplement_flag = False
    classification_flag = False
    defect_score_reset_flag = False
    auto_start_flag = False
    fabric_template_identification_flag = False
    auto_all_stop_flag = False
    hist_ok_flag = False

    try:
        camera = cv2.VideoCapture(1)
        # camera_template = cv2.VideoCapture(1)
        ser_1 = serial.Serial('com4', 9600)
        ser = serial.Serial('com3', 9600)



    except:
        print("com or camera unusable!")
    app = QtWidgets.QApplication(sys.argv)
    myshow = mywindow()
    myshow.show()  # 显示
    sys.exit(app.exec_())
