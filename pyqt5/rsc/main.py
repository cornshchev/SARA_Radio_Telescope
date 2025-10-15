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

project_root = Path(__file__).parent
sys.path.append(str(project_root))

from grc_modules.grc_blocks import RadioTelescope1420

try:
    from ui.main_window import Ui_MainWindow
    from ui.spectrum_page import Ui_spectrum_page
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
            spectrum_widget = QtWidgets.QWidget()
            self.ui_spectrum = Ui_spectrum_page()
            self.ui_spectrum.setupUi(spectrum_widget)
            
            record_page = QtWidgets.QWidget()
            direction_page = QtWidgets.QWidget()
            calibration_page = QtWidgets.QWidget()
            about_page = QtWidgets.QWidget()
            
            # 设置页面到stacked_widget
            self.ui.add_external_ui(spectrum_widget, 0)
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
        self.histogram_widget = spectrum_widget.findChild(QtWidgets.QWidget, "widget_histogram")
        self.waterfall_widget = spectrum_widget.findChild(QtWidgets.QWidget, "widget_waterfall")
        self.spectrum_widget = spectrum_widget.findChild(QtWidgets.QWidget, "widget_integration")
        
        # 初始化控件引用
        # 连接信号和槽
        self.setup_connections()
    
    def setup_connections(self):
        # 连接UI控件的信号到对应的槽函数
        self.ui_spectrum.slider_freq.valueChanged.connect(self.on_freq_changed)
        self.ui_spectrum.spinbox_freq.valueChanged.connect(self.on_freq_changed)
        self.ui_spectrum.slider_gain.valueChanged.connect(self.on_gain_changed)
        self.ui_spectrum.spinbox_gain.valueChanged.connect(self.on_gain_changed)
        self.ui_spectrum.slider_integration.valueChanged.connect(self.on_integration_time_changed)
        self.ui_spectrum.spinbox_integration.valueChanged.connect(self.on_integration_time_changed)
        self.ui_spectrum.spinbox_freqcorr.valueChanged.connect(self.on_freq_corr_changed)
        self.ui_spectrum.checkbox_enabledb.stateChanged.connect(self.on_db_enabled_changed)
        self.ui_spectrum.radio_movingaverage.toggled.connect(self.on_integration_mode_changed)
        self.ui_spectrum.radio_iiraverage.toggled.connect(self.on_integration_mode_changed)
        self.ui_spectrum.radio_calioff.toggled.connect(self.on_calibration_mode_changed)
        self.ui_spectrum.radio_staticcali.toggled.connect(self.on_calibration_mode_changed)
        self.ui_spectrum.radio_dynamiccali.toggled.connect(self.on_calibration_mode_changed)
        # self.ui_spectrum.button_save.clicked.connect(self.on_save_spectrum)
    
    def on_freq_changed(self, value):
        # 频率改变信号
        if hasattr(self, 'main_block'):
            self.main_block.set_freq(value)
    
    def on_gain_changed(self, value):
        # 增益改变信号
        if hasattr(self, 'main_block'):
            self.main_block.set_rf_gain(value)
    
    def on_integration_time_changed(self, value):
        # 积分时间改变信号
        if hasattr(self, 'main_block'):
            self.main_block.set_integration_time(value)
    
    def on_freq_corr_changed(self, value):
        # 频率校正改变信号
        if hasattr(self, 'main_block'):
            self.main_block.set_freq_corr(value)
    
    def on_db_enabled_changed(self, state):
        # dB模式改变信号
        if hasattr(self, 'main_block'):
            self.main_block.set_db_enabled(state == QtCore.Qt.Checked)
    
    def on_integration_mode_changed(self, checked):
        # 积分模式改变信号
        if checked and hasattr(self, 'main_block'):
            if self.radio_movingaverage.isChecked():
                self.main_block.set_integration_mode(0)
            elif self.radio_iiraverage.isChecked():
                self.main_block.set_integration_mode(1)
    
    def on_calibration_mode_changed(self, checked):
        # 校准模式改变信号
        if checked and hasattr(self, 'main_block'):
            if self.radio_calioff.isChecked():
                self.main_block.set_calibration_mode(0)
            elif self.radio_staticcali.isChecked():
                self.main_block.set_calibration_mode(1)
            elif self.radio_dynamiccali.isChecked():
                self.main_block.set_calibration_mode(2)
    

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
        if self.main_block:
            self.main_block.stop()
            self.main_block.wait()
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
    try:
        tb = RadioTelescope1420(ui=ui)
        # ui.set_main_block(tb)
    except Exception as e:
        print(f"main.py创建GNU Radio块错误: {e}")
        QtWidgets.QMessageBox.critical(None, "错误", f"无法初始化无线电接收器: {e}")
        return 1
    
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