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
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import qtgui
from gnuradio import blocks
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.filter import pfb
# import pyqt5.epy_modules.epy_block_integration as spectrum_integration_block  # embedded python block
# import pyqt5.epy_modules.epy_block_spectrum as spectrum_display_block  # embedded python block
from grc_modules import epy_block_integration as spectrum_integration_block
from grc_modules import epy_block_spectrum as spectrum_display_block
import numpy
import osmosdr
import time
import sip
import threading
import os
from pathlib import Path
from PyQt5.QtCore import QFile
import numpy as np

import qdarkstyle
from qt_material import apply_stylesheet



class RadioTelescopeUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(RadioTelescopeUI, self).__init__(parent)


        file_path = os.fspath(Path(__file__).resolve().parent / "ui" / "main_win.ui")
        if os.path.exists(file_path):
           ui_file = QFile(file_path)
           ui_file.open(QFile.ReadOnly)
           uic.loadUi(ui_file,self)
           ui_file.close()
        
        # 存储UI中的控件引用
        self.histogram_widget = self.findChild(QtWidgets.QWidget, "widget_histogram")
        self.waterfall_widget = self.findChild(QtWidgets.QWidget, "widget_waterfall")
        self.spectrum_widget = self.findChild(QtWidgets.QWidget, "widget_integration")
        
        # 连接信号和槽
        self.setup_connections()
    
    def setup_connections(self):
        # 连接UI控件的信号到对应的槽函数
        self.slider_freq.valueChanged.connect(self.on_freq_changed)
        self.spinbox_freq.valueChanged.connect(self.on_freq_changed)
        self.slider_gain.valueChanged.connect(self.on_gain_changed)
        self.spinbox_gain.valueChanged.connect(self.on_gain_changed)
        self.slider_integration.valueChanged.connect(self.on_integration_time_changed)
        self.spinbox_integration.valueChanged.connect(self.on_integration_time_changed)
        self.spinbox_freqcorr.valueChanged.connect(self.on_freq_corr_changed)
        self.checkbox_enabledb.stateChanged.connect(self.on_db_enabled_changed)
        self.radio_movingaverage.toggled.connect(self.on_integration_mode_changed)
        self.radio_iiraverage.toggled.connect(self.on_integration_mode_changed)
        self.radio_calioff.toggled.connect(self.on_calibration_mode_changed)
        self.radio_staticcali.toggled.connect(self.on_calibration_mode_changed)
        self.radio_dynamiccali.toggled.connect(self.on_calibration_mode_changed)
        self.button_save.clicked.connect(self.on_save_spectrum)
    
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
    
    def on_save_spectrum(self):
        # 保存频谱信号
        if hasattr(self, 'main_block'):
            self.main_block.spectrum_save.set_pressed(True)

    def add_spectrum_widget(self, widget):
        """添加频谱显示控件到UI"""
        widget.setParent(self.spectrum_widget)
        self.spectrum_widget.layout().addWidget(widget)
        widget.show()

    

class RadioTelescope1420(gr.top_block):

    def __init__(self, ui):
        gr.top_block.__init__(self, "RadioTelescop1420", catch_exceptions=True)
        
        # 保存UI引用
        self.ui = ui
        self.ui.main_block = self
        
        ##################################################
        # Variables
        ##################################################
        self.source_freq = source_freq = 1420400000
        self.vec_length = vec_length = 1024
        self.samp_rate = samp_rate = 3000000
        self.rf_gain = rf_gain = 10
        self.integration_time = integration_time = 5
        self.integration_mode = integration_mode = 0
        self.freq_corr = freq_corr = 0
        self.freq = freq = source_freq
        self.decimation = decimation = 8
        self.db_enabled = db_enabled = True
        self.calibration_mode = calibration_mode = 0
        self.bit_max = bit_max = 4096

        ##################################################
        # Blocks
        ##################################################

        # 创建图像显示控件并添加到UI中
        # histogram sink
        self.qtgui_histogram_sink_x_0 = qtgui.histogram_sink_f(
            (int(samp_rate/8)),
            bit_max,
            0,
            0.5,
            "信号直方图",
            1,
            None
        )
        self.qtgui_histogram_sink_x_0.set_update_time(0.10)
        self.qtgui_histogram_sink_x_0.enable_autoscale(True)
        self.qtgui_histogram_sink_x_0.enable_accumulate(False)
        self.qtgui_histogram_sink_x_0.enable_grid(True)
        self.qtgui_histogram_sink_x_0.enable_axis_labels(False)
        self.qtgui_histogram_sink_x_0.disable_legend()
        hist_win = sip.wrapinstance(self.qtgui_histogram_sink_x_0.qwidget(), QtWidgets.QWidget)
        self.ui.histogram_widget.layout().addWidget(hist_win)
        hist_win.show()
        # waterfall sink
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            4096,
            window.WIN_BLACKMAN_hARRIS,
            freq,
            samp_rate,
            "频谱瀑布图",
            1,
            None
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)
        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)
        waterfall_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.qwidget(), QtWidgets.QWidget)
        self.ui.waterfall_widget.layout().addWidget(waterfall_win)
        waterfall_win.show()

        # def spectrum_update_callback(data):
        #     """频谱数据更新回调函数"""
        #     try:
        #         # 确保在主线程中更新UI
        #         if hasattr(self, 'spectrum_curve') and self.spectrum_curve:
        #             x_data = np.arange(len(data))
        #             self.spectrum_curve.setData(x_data, data)
        #     except Exception as e:
        #         print(f"Error updating spectrum: {e}")

        # 频谱显示
        self.spectrum_display_block = spectrum_display_block.SpectrumDisplayBlock(vec_length=vec_length, freq=freq, samp_rate=samp_rate/decimation, parent=ui)
        

        # 多相抽样滤波器
        file_path = os.fspath(Path(__file__).resolve().parent / "grc_modules" / "ph_decimator_taps.csv")
        taps = np.loadtxt(file_path, delimiter=',')
        self.pfb_decimator_ccf_0 = pfb.decimator_ccf(
            decimation,
            taps,
            False,
            False)
        self.pfb_decimator_ccf_0.declare_sample_delay(0)
        
        self.osmosdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + "airspy=0"
        )
        self.osmosdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(freq, 0)
        self.osmosdr_source_0.set_freq_corr(freq_corr, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(rf_gain, 0)
        self.osmosdr_source_0.set_if_gain(0, 0)
        self.osmosdr_source_0.set_bb_gain(0, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
        
        self.fft_vxx_0 = fft.fft_vcc(vec_length, True, window.rectangular(vec_length), True, 4)
        
        self.spectrum_integration_block = spectrum_integration_block.spectrum_integrator(vec_length=vec_length, integration_time=integration_time, mode=integration_mode, samp_rate=samp_rate/4)
        
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_float*1, vec_length)
        self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, vec_length)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_float*vec_length,db_enabled,0)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(10, vec_length, 0)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(vec_length)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)

        # # 保存频谱按钮
        # self.spectrum_save = blocks.message_strobe(gr.message().make_from_string("save"), 1000)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_0, 0), (self.qtgui_histogram_sink_x_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.spectrum_integration_block, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.blocks_selector_0, 1))
        # self.connect((self.blocks_selector_0, 0), (self.blocks_vector_to_stream_0, 0))
        # self.connect((self.blocks_selector_0, 0), (self.qtgui_vector_sink_f_0_0_1_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.spectrum_display_block, 0))
        self.connect((self.spectrum_integration_block, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.spectrum_integration_block, 0), (self.blocks_selector_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.pfb_decimator_ccf_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.pfb_decimator_ccf_0, 0), (self.blocks_stream_to_vector_0_0, 0))

    ##################################################
    '''# Getter and Setter methods'''
    ##################################################
    def get_source_freq(self):
        return self.source_freq

    def set_source_freq(self, source_freq):
        self.source_freq = source_freq
        self.set_freq(self.source_freq)

    def get_vec_length(self):
        return self.vec_length

    def set_vec_length(self, vec_length):
        self.vec_length = vec_length
        self.spectrum_integration_block.vec_length = self.vec_length
        self.spectrum_display_block.vec_length = self.vec_length
        # self.spectrum_display_block.x_axis_step_value = (self.samp_rate/self.decimation/self.vec_length)/1e6
        self.fft_vxx_0.set_window(window.rectangular(self.vec_length))
        # self.qtgui_vector_sink_f_0_0_1_0.set_x_axis(((self.freq-self.samp_rate/self.decimation/2)/1e6), ((self.samp_rate/self.decimation/self.vec_length)/1e6))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.spectrum_integration_block.samp_rate = self.samp_rate/self.decimation
        self.spectrum_display_block.samp_rate(self.samp_rate/self.decimation)
        # self.spectrum_display_block.x_axis_step_value = (self.samp_rate/self.decimation/self.vec_length)/1e6
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        # self.qtgui_vector_sink_f_0_0_1_0.set_x_axis(((self.freq-self.samp_rate/self.decimation/2)/1e6), ((self.samp_rate/self.decimation/self.vec_length)/1e6))
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.freq, self.samp_rate)

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self.osmosdr_source_0.set_gain(self.rf_gain, 0)

    def get_integration_time(self):
        return self.integration_time

    def set_integration_time(self, integration_time):
        self.integration_time = integration_time
        self.spectrum_integration_block.integration_time = self.integration_time

    def get_integration_mode(self):
        return self.integration_mode

    def set_integration_mode(self, integration_mode):
        self.integration_mode = integration_mode
        # self._integration_mode_callback(self.integration_mode)
        self.spectrum_integration_block.mode = self.integration_mode

    def get_freq_corr(self):
        return self.freq_corr

    def set_freq_corr(self, freq_corr):
        self.freq_corr = freq_corr
        self.osmosdr_source_0.set_freq_corr(self.freq_corr, 0)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.spectrum_display_block.freq = self.freq
        self.spectrum_display_block.update_freq_axis()
        self.osmosdr_source_0.set_center_freq(self.freq, 0)
        # self.qtgui_vector_sink_f_0_0_1_0.set_x_axis(((self.freq-self.samp_rate/self.decimation/2)/1e6), ((self.samp_rate/self.decimation/self.vec_length)/1e6))
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.freq, self.samp_rate)

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation
        # self.spectrum_display_block.x_axis_start_value = (self.freq-self.samp_rate/self.decimation/2)/1e6
        # self.spectrum_display_block.x_axis_step_value = (self.samp_rate/self.decimation/self.vec_length)/1e6
        # self.qtgui_vector_sink_f_0_0_1_0.set_x_axis(((self.freq-self.samp_rate/self.decimation/2)/1e6), ((self.samp_rate/self.decimation/self.vec_length)/1e6))

    def get_db_enabled(self):
        return self.db_enabled

    def set_db_enabled(self, db_enabled):
        self.db_enabled = db_enabled
        # self._db_enabled_callback(self.db_enabled)
        self.blocks_selector_0.set_input_index(self.db_enabled)

    def get_calibration_mode(self):
        return self.calibration_mode

    def set_calibration_mode(self, calibration_mode):
        self.calibration_mode = calibration_mode
        # self._calibration_mode_callback(self.calibration_mode)

    def get_bit_max(self):
        return self.bit_max

    def set_bit_max(self, bit_max):
        self.bit_max = bit_max
        self.qtgui_histogram_sink_x_0.set_bins(self.bit_max)

    # 其他setter方法...
    # [保留原有的所有setter方法]

def main(top_block_cls=RadioTelescope1420, options=None):
    qapp = QtWidgets.QApplication(sys.argv)

    # setup qdarkstylesheet
    light_stylesheet = qdarkstyle.load_stylesheet(qt_api='pyqt5', palette=qdarkstyle.LightPalette)
    qapp.setStyleSheet(light_stylesheet)

    # setup stylesheet
    # apply_stylesheet(qapp, theme='light_cyan.xml')



    # 创建UI
    ui = RadioTelescopeUI()
    
    # 创建GNU Radio主块
    tb = top_block_cls(ui)
    
    # 显示窗口
    ui.show()
    
    tb.start()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()
        QtWidgets.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = QtCore.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()