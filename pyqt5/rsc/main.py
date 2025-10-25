#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: RadioTelescop1420
# GNU Radio version: 3.10.11.0

from PyQt5 import Qt
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import QObject, pyqtSlot, QFile

import sys
import signal
import osmosdr
import time
import threading
import os
from pathlib import Path
import pmt

project_root = Path(__file__).parent
sys.path.append(str(project_root))

from grc_modules.grc_blocks import RadioTelescope1420

try:
    from ui.main_window import Ui_MainWindow
    from ui.spectrum_page import Ui_spectrum_page
    from ui.record_page import Ui_record_page
except ImportError as e:
    print(f"main.py导入错误: {e}")
    print("请确保所有依赖的UI文件都存在")

# import qdarkstyle
# from qt_material import apply_stylesheet



class RadioTelescopeUI(QtWidgets.QMainWindow):
    def __init__(self, ui_class=None, parent=None):
        super(RadioTelescopeUI, self).__init__(parent)
        
        # if ui_class is None:
        #     try:
        #         from ui.main_window import Ui_MainWindow as ui_class
        #     except ImportError:
        #         print("错误：无法导入UI类，请检查ui/main_window.py文件是否存在")
        #         sys.exit(1)
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        try:     
            spectrum_page = QtWidgets.QWidget()
            self.ui_spectrum = Ui_spectrum_page()
            self.ui_spectrum.setupUi(spectrum_page)
            
            record_page = QtWidgets.QWidget()
            self.ui_record = Ui_record_page()
            self.ui_record.setupUi(record_page)
            direction_page = QtWidgets.QWidget()
            calibration_page = QtWidgets.QWidget()
            about_page = QtWidgets.QWidget()
            
            # 设置页面到stacked_widget
            self.ui.add_external_ui(spectrum_page, 0)
            self.ui.add_external_ui(record_page, 1)
            self.ui.add_external_ui(direction_page, 2)
            self.ui.add_external_ui(calibration_page, 3)
            self.ui.add_external_ui(about_page, 4)
            
            # 默认显示第一个页面
            self.ui.stacked_widget.setCurrentIndex(0)
            
        except ImportError as e:
            print(f"main.py导入错误: {e}")
            print("请确保所有依赖的UI文件都存在")
        
        # 存储UI中的控件引用
        self.histogram_widget = spectrum_page.findChild(QtWidgets.QWidget, "widget_histogram")
        self.waterfall_widget = spectrum_page.findChild(QtWidgets.QWidget, "widget_waterfall")
        self.spectrum_widget = spectrum_page.findChild(QtWidgets.QWidget, "widget_integration")
        
        # 初始化控件引用
        # 连接信号和槽
        self.setup_connections()
    
    def setup_connections(self):
        # 连接UI控件的信号到对应的槽函数

        #################################################################################################################
        # ui_spectrum控件
        #################################################################################################################
        self.ui_spectrum.slider_freq.valueChanged.connect(self.on_freq_changed)
        self.ui_spectrum.spinbox_freq.valueChanged.connect(self.on_freq_changed)
        self.ui_spectrum.slider_gain.valueChanged.connect(self.on_gain_changed)
        self.ui_spectrum.spinbox_gain.valueChanged.connect(self.on_gain_changed)
        self.ui_spectrum.slider_integration.valueChanged.connect(self.on_integration_time_changed)
        self.ui_spectrum.spinbox_integration.valueChanged.connect(self.on_integration_time_changed)
        self.ui_spectrum.spinbox_freqcorr.valueChanged.connect(self.on_freq_corr_changed)
        self.ui_spectrum.checkbox_enabledb.stateChanged.connect(self.on_db_enabled_changed)
        self.ui_spectrum.combo_veclength.currentIndexChanged.connect(self.on_vector_length_changed)
        # self.ui_spectrum.radio_movingaverage.toggled.connect(self.on_integration_mode_changed)
        # self.ui_spectrum.radio_iiraverage.toggled.connect(self.on_integration_mode_changed)
        self.ui_spectrum.radio_calioff.toggled.connect(self.on_calibration_mode_changed)
        self.ui_spectrum.radio_staticcali.toggled.connect(self.on_calibration_mode_changed)
        self.ui_spectrum.radio_dynamiccali.toggled.connect(self.on_calibration_mode_changed)
        self.ui_spectrum.button_toggle.clicked.connect(self.on_toggle_action)

        #################################################################################################################
        # ui_record控件
        self.ui_record.button_recording.clicked.connect(self.on_start_recording)
        self.ui_record.button_browse.clicked.connect(self.on_browse_file)
        self.ui_record.lineEdit_filepath.textChanged.connect(self.update_file_path)
        self.ui_record.lineEdit_filename.textChanged.connect(self.update_file_name)
        self.ui_record.lineEdit_filename.setText("td_record")
        # self.ui_record.list_record.

    #################################################################################################################
    # ui.spectrum槽函数定义
    #################################################################################################################
    def on_toggle_action(self):
        # 启动/停止按钮
        if hasattr(self, 'gr_block'):
            if self.ui_spectrum.button_toggle.isChecked():
                self.ui_spectrum.button_toggle.setText("停止")
                self.gr_block.start()
                

            else:
                self.ui_spectrum.button_toggle.setText("启动")
                self.gr_block.stop()
                self.gr_block.wait()
    
    def on_freq_changed(self, value):
        # 频率改变信号
        if hasattr(self, 'gr_block'):
            self.gr_block.set_freq(value)
    
    def on_gain_changed(self, value):
        # 增益改变信号
        if hasattr(self, 'gr_block'):
            self.gr_block.set_rf_gain(value)
    
    def on_integration_time_changed(self, value):
        # 积分时间改变信号
        if hasattr(self, 'gr_block'):
            self.gr_block.set_integration_time(value)
    
    def on_freq_corr_changed(self, value):
        # 频率校正改变信号
        if hasattr(self, 'gr_block'):
            self.gr_block.set_freq_corr(value)
    
    def on_db_enabled_changed(self, state):
        # dB模式改变信号
        if hasattr(self, 'gr_block'):
            self.gr_block.set_db_enabled(state == QtCore.Qt.Checked)

    def on_vector_length_changed(self, index):
        # 向量长度改变信号
        pass
        # vec_length = int(self.ui_spectrum.combo_veclength.currentText())
        # if hasattr(self, 'gr_block'):
        #     self.gr_block.set_vector_length(vec_length)
    
    
    def on_calibration_mode_changed(self, checked):
        # 校准模式改变信号
        if checked and hasattr(self, 'gr_block'):
            if self.radio_calioff.isChecked():
                self.gr_block.set_calibration_mode(0)
            elif self.radio_staticcali.isChecked():
                self.gr_block.set_calibration_mode(1)
            elif self.radio_dynamiccali.isChecked():
                self.gr_block.set_calibration_mode(2)

    #################################################################################################################
    # ui.record槽函数定义
    #################################################################################################################
    def on_start_recording(self):
        # 开始录制按钮
        if hasattr(self, 'gr_block'):
            """切换录制状态"""
            if self.ui_record.button_recording.isChecked():
                self.ui_record.button_recording.setText("停止记录")
                self.gr_block.stream_recorder_block.set_recording_state(True)
            else:
                self.ui_record.button_recording.setText("开始记录")
                self.gr_block.stream_recorder_block.set_recording_state(False)

    def on_browse_file(self):
        # 浏览文件保存位置（目录）
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        directory = QtWidgets.QFileDialog.getExistingDirectory(
            self, 
            "选择保存位置", 
            "",  # 默认路径
            options=options
        )
        if directory:
            self.ui_record.lineEdit_filepath.setText(directory)
            if hasattr(self, 'gr_block'):
                self.update_file_path(directory)

    # def start_recording(self):
    #     """发送开始录制消息"""
    #     msg = pmt.from_bool(True)
    #     self.gr_block.message_port_pub(pmt.intern("recording_control"), msg)
    
    # def stop_recording(self):
    #     """发送停止录制消息"""
    #     msg = pmt.from_bool(False)
    #     self.gr_block.message_port_pub(pmt.intern("recording_control"), msg)

    def update_file_path(self, path):
        # 更新文件保存路径
        if hasattr(self, 'gr_block'):
            self.gr_block.set_file_path(path)

    def update_file_name(self, filename):
        # 更新文件名前缀
        if hasattr(self, 'gr_block'):
            self.gr_block.set_file_name(filename)
    
    #################################################################################################################
    

    def add_histogram_widget(self, widget):
        """添加直方图显示控件到UI"""
        widget.setParent(self.histogram_widget)
        self.histogram_widget.layout().addWidget(widget)
        widget.show()

    def add_spectrum_widget(self, widget):
        """添加频谱显示控件到UI"""
        widget.setParent(self.spectrum_widget)
        self.spectrum_widget.layout().addWidget(widget)
        widget.show()

    def closeEvent(self, event):
        """重写关闭事件，确保GNU Radio块正确停止"""
        if self.gr_block:
            self.gr_block.stop()
            self.gr_block.wait()
        event.accept()



def main(top_block_cls=RadioTelescope1420, options=None):
    # 创建QApplication
    if QtWidgets.QApplication.instance() is None:
        qapp = QtWidgets.QApplication(sys.argv)
    else:
        qapp = QtWidgets.QApplication.instance()
    
    # 设置CSS样式
    # light_stylesheet = qdarkstyle.load_stylesheet(qt_api='pyqt5', palette=qdarkstyle.LightPalette)
    # qapp.setStyleSheet(light_stylesheet)
    # apply_stylesheet(qapp, theme='light_cyan.xml')
    
    # 创建UI
    try:
        ui = RadioTelescopeUI()
    except Exception as e:
        print(f"main.py创建UI错误: {e}")
        return 1
    
    # 创建GNU Radio主块
    # try:
    tb = RadioTelescope1420(ui=ui)
        # ui.set_gr_block(tb)
    # except Exception as e:
    #     print(f"main.py创建GNU Radio块错误: {e}")
    #     QtWidgets.QMessageBox.critical(None, "错误", f"无法初始化无线电接收器: {e}")
    #     return 1
    
    # 显示窗口
    ui.show()
    
    # 启动GNU Radio流图
    try:
        tb.start()
    except Exception as e:
        print(f"启动GNU Radio错误: {e}")
        QtWidgets.QMessageBox.critical(ui, "错误", f"无法启动无线电接收: {e}")
        return 1
    
    def sig_handler(sig=None, frame=None):
        """信号处理函数"""
        print("接收到关闭信号，正在停止...")
        tb.stop()
        tb.wait()
        qapp.quit()
    
    # 设置信号处理
    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)
    
    # 定时器用于处理Python信号
    timer = QtCore.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)
    
    # 运行应用
    return qapp.exec_()

if __name__ == '__main__':
    sys.exit(main())