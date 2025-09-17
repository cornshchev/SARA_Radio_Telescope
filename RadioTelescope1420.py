#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: RadioTelescop1420
# GNU Radio version: 3.10.11.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import blocks
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.filter import pfb
import RadioTelescope1420_epy_block_0 as epy_block_0  # embedded python block
import RadioTelescope1420_epy_block_1 as epy_block_1  # embedded python block
import numpy
import osmosdr
import time
import sip
import threading



class RadioTelescope1420(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "RadioTelescop1420", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("RadioTelescop1420")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "RadioTelescope1420")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.source_freq = source_freq = 1420400000
        self.yzoom = yzoom = 10
        self.yroll = yroll = 0
        self.vec_length = vec_length = 1024
        self.samp_rate = samp_rate = 6000000
        self.rf_gain = rf_gain = 10
        self.integration_time = integration_time = 5
        self.integration_mode = integration_mode = 0
        self.freq_corr = freq_corr = 0
        self.freq = freq = source_freq
        self.decimation = decimation = 4
        self.db_enabled = db_enabled = True
        self.calibration_mode = calibration_mode = 0
        self.bit_max = bit_max = 4096

        ##################################################
        # Blocks
        ##################################################

        self.gui_tab = Qt.QTabWidget()
        self.gui_tab_widget_0 = Qt.QWidget()
        self.gui_tab_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.gui_tab_widget_0)
        self.gui_tab_grid_layout_0 = Qt.QGridLayout()
        self.gui_tab_layout_0.addLayout(self.gui_tab_grid_layout_0)
        self.gui_tab.addTab(self.gui_tab_widget_0, 'Spectrum')
        self.gui_tab_widget_1 = Qt.QWidget()
        self.gui_tab_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.gui_tab_widget_1)
        self.gui_tab_grid_layout_1 = Qt.QGridLayout()
        self.gui_tab_layout_1.addLayout(self.gui_tab_grid_layout_1)
        self.gui_tab.addTab(self.gui_tab_widget_1, 'Record')
        self.gui_tab_widget_2 = Qt.QWidget()
        self.gui_tab_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.gui_tab_widget_2)
        self.gui_tab_grid_layout_2 = Qt.QGridLayout()
        self.gui_tab_layout_2.addLayout(self.gui_tab_grid_layout_2)
        self.gui_tab.addTab(self.gui_tab_widget_2, 'Calibration')
        self.top_layout.addWidget(self.gui_tab)
        self._yzoom_range = qtgui.Range(1, 1000, 1, 10, 5)
        self._yzoom_win = qtgui.RangeWidget(self._yzoom_range, self.set_yzoom, "zoom", "slider", float, QtCore.Qt.Horizontal)
        self.gui_tab_grid_layout_0.addWidget(self._yzoom_win, 10, 0, 1, 7)
        for r in range(10, 11):
            self.gui_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 7):
            self.gui_tab_grid_layout_0.setColumnStretch(c, 1)
        self._yroll_range = qtgui.Range(-1000, 1000, 0.05*yzoom, 0, 5)
        self._yroll_win = qtgui.RangeWidget(self._yroll_range, self.set_yroll, "roll", "slider", float, QtCore.Qt.Horizontal)
        self.gui_tab_grid_layout_0.addWidget(self._yroll_win, 10, 7, 1, 7)
        for r in range(10, 11):
            self.gui_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(7, 14):
            self.gui_tab_grid_layout_0.setColumnStretch(c, 1)
        self._rf_gain_range = qtgui.Range(0, 21, 1, 10, 200)
        self._rf_gain_win = qtgui.RangeWidget(self._rf_gain_range, self.set_rf_gain, "RF Gain(dB)", "counter_slider", float, QtCore.Qt.Horizontal)
        self.gui_tab_grid_layout_0.addWidget(self._rf_gain_win, 1, 10, 1, 6)
        for r in range(1, 2):
            self.gui_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(10, 16):
            self.gui_tab_grid_layout_0.setColumnStretch(c, 1)
        self._integration_time_range = qtgui.Range(1, 20, 1, 5, 200)
        self._integration_time_win = qtgui.RangeWidget(self._integration_time_range, self.set_integration_time, "Interation Time(s)", "counter_slider", float, QtCore.Qt.Horizontal)
        self.gui_tab_grid_layout_0.addWidget(self._integration_time_win, 2, 12, 1, 4)
        for r in range(2, 3):
            self.gui_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(12, 16):
            self.gui_tab_grid_layout_0.setColumnStretch(c, 1)
        # Create the options list
        self._integration_mode_options = [0, 1]
        # Create the labels list
        self._integration_mode_labels = ['Moving Average', 'IIR Average']
        # Create the combo box
        # Create the radio buttons
        self._integration_mode_group_box = Qt.QGroupBox("Integration Mode" + ": ")
        self._integration_mode_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._integration_mode_button_group = variable_chooser_button_group()
        self._integration_mode_group_box.setLayout(self._integration_mode_box)
        for i, _label in enumerate(self._integration_mode_labels):
            radio_button = Qt.QRadioButton(_label)
            self._integration_mode_box.addWidget(radio_button)
            self._integration_mode_button_group.addButton(radio_button, i)
        self._integration_mode_callback = lambda i: Qt.QMetaObject.invokeMethod(self._integration_mode_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._integration_mode_options.index(i)))
        self._integration_mode_callback(self.integration_mode)
        self._integration_mode_button_group.buttonClicked[int].connect(
            lambda i: self.set_integration_mode(self._integration_mode_options[i]))
        self.gui_tab_grid_layout_0.addWidget(self._integration_mode_group_box, 2, 10, 2, 2)
        for r in range(2, 4):
            self.gui_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(10, 12):
            self.gui_tab_grid_layout_0.setColumnStretch(c, 1)
        self._freq_corr_range = qtgui.Range(-10, 10, 0.1, 0, 200)
        self._freq_corr_win = qtgui.RangeWidget(self._freq_corr_range, self.set_freq_corr, "Frequence Correction", "counter_slider", float, QtCore.Qt.Horizontal)
        self.gui_tab_grid_layout_0.addWidget(self._freq_corr_win, 3, 12, 1, 4)
        for r in range(3, 4):
            self.gui_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(12, 16):
            self.gui_tab_grid_layout_0.setColumnStretch(c, 1)
        self._freq_range = qtgui.Range(1418000000, 1445000000, 1000, source_freq, 200)
        self._freq_win = qtgui.RangeWidget(self._freq_range, self.set_freq, "freq", "counter_slider", int, QtCore.Qt.Horizontal)
        self.gui_tab_grid_layout_0.addWidget(self._freq_win, 0, 10, 1, 6)
        for r in range(0, 1):
            self.gui_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(10, 16):
            self.gui_tab_grid_layout_0.setColumnStretch(c, 1)
        _db_enabled_check_box = Qt.QCheckBox("Enable dB")
        self._db_enabled_choices = {True: True, False: False}
        self._db_enabled_choices_inv = dict((v,k) for k,v in self._db_enabled_choices.items())
        self._db_enabled_callback = lambda i: Qt.QMetaObject.invokeMethod(_db_enabled_check_box, "setChecked", Qt.Q_ARG("bool", self._db_enabled_choices_inv[i]))
        self._db_enabled_callback(self.db_enabled)
        _db_enabled_check_box.stateChanged.connect(lambda i: self.set_db_enabled(self._db_enabled_choices[bool(i)]))
        self.gui_tab_grid_layout_0.addWidget(_db_enabled_check_box, 10, 15, 1, 1)
        for r in range(10, 11):
            self.gui_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(15, 16):
            self.gui_tab_grid_layout_0.setColumnStretch(c, 1)
        self.spectrum_save = _spectrum_save_toggle_button = qtgui.MsgPushButton('Save Spectum', 'pressed',1,"default","default")
        self.spectrum_save = _spectrum_save_toggle_button

        self.gui_tab_grid_layout_0.addWidget(_spectrum_save_toggle_button, 0, 6, 1, 4)
        for r in range(0, 1):
            self.gui_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(6, 10):
            self.gui_tab_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            4096, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            freq, #fc
            samp_rate, #bw
            "Waterfall Spectrum", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.qwidget(), Qt.QWidget)

        self.gui_tab_grid_layout_0.addWidget(self._qtgui_waterfall_sink_x_0_win, 4, 0, 6, 16)
        for r in range(4, 10):
            self.gui_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 16):
            self.gui_tab_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_vector_sink_f_0_0_1_0 = qtgui.vector_sink_f(
            vec_length,
            ((freq-samp_rate/decimation/2)/1e6),
            ((samp_rate/decimation/vec_length)/1e6),
            "Frequency",
            "Average Signal",
            "Average Spectrum",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0_0_1_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0_0_1_0.set_y_axis((yroll-1000/yzoom), (yroll+1000/yzoom))
        self.qtgui_vector_sink_f_0_0_1_0.enable_autoscale(False)
        self.qtgui_vector_sink_f_0_0_1_0.enable_grid(True)
        self.qtgui_vector_sink_f_0_0_1_0.set_x_axis_units("MHz")
        self.qtgui_vector_sink_f_0_0_1_0.set_y_axis_units("Amp/dB")
        self.qtgui_vector_sink_f_0_0_1_0.set_ref_level(0)


        labels = ['Spectrum', '', '', '', '',
            '', '', '', '', '']
        widths = [2, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0_0_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_0_1_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_0_1_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_0_1_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_0_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_0_1_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_0_1_0.qwidget(), Qt.QWidget)
        self.gui_tab_grid_layout_0.addWidget(self._qtgui_vector_sink_f_0_0_1_0_win, 11, 0, 10, 16)
        for r in range(11, 21):
            self.gui_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 16):
            self.gui_tab_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_histogram_sink_x_0 = qtgui.histogram_sink_f(
            (int(samp_rate/8)),
            bit_max,
            0,
            0.5,
            "Signal Histogram",
            1,
            None # parent
        )

        self.qtgui_histogram_sink_x_0.set_update_time(0.10)
        self.qtgui_histogram_sink_x_0.enable_autoscale(True)
        self.qtgui_histogram_sink_x_0.enable_accumulate(False)
        self.qtgui_histogram_sink_x_0.enable_grid(False)
        self.qtgui_histogram_sink_x_0.enable_axis_labels(True)

        self.qtgui_histogram_sink_x_0.disable_legend()

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers= [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_histogram_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_histogram_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_histogram_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_histogram_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_histogram_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_histogram_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_histogram_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_histogram_sink_x_0_win = sip.wrapinstance(self.qtgui_histogram_sink_x_0.qwidget(), Qt.QWidget)
        self.gui_tab_grid_layout_0.addWidget(self._qtgui_histogram_sink_x_0_win, 0, 0, 4, 4)
        for r in range(0, 4):
            self.gui_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 4):
            self.gui_tab_grid_layout_0.setColumnStretch(c, 1)
        self.pfb_decimator_ccf_0 = pfb.decimator_ccf(
            decimation,
            [-1.6253957381987094e-18,-0.0003171409189235419,0.0005596519913524389,-2.0325000178946184e-18,-0.0013553404714912176,0.001955647487193346,-5.3988564840815144e-18,-0.0037004761397838593,0.004910294432193041,-1.0851606266612696e-17,-0.008197451941668987,0.010367341339588165,-7.150374208034986e-17,-0.016049886122345924,0.019715232774615288,-2.7224212988098325e-17,-0.0292399600148201,0.03543321043252945,-3.641610038077746e-17,-0.05211251974105835,0.06365709006786346,-4.4479314716879014e-17,-0.0990009754896164,0.1286739856004715,-5.000909321241236e-17,-0.2709931433200836,0.5489985346794128,1.333391785621643,0.5489985346794128,-0.2709931433200836,-5.000909321241236e-17,0.1286739856004715,-0.0990009754896164,-4.4479314716879014e-17,0.06365709006786346,-0.05211251974105835,-3.641610038077746e-17,0.03543321043252945,-0.0292399600148201,-2.7224212988098325e-17,0.019715232774615288,-0.016049886122345924,-7.150374208034986e-17,0.010367341339588165,-0.008197451941668987,-1.0851606266612696e-17,0.004910294432193041,-0.0037004761397838593,-5.3988564840815144e-18,0.001955647487193346,-0.0013553404714912176,-2.0325000178946184e-18,0.0005596519913524389,-0.0003171409189235419,-1.6253957381987094e-18],
            0,
            40,
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
        self.epy_block_1 = epy_block_1.save_spectrum_image(vec_length=vec_length, x_axis_start_value=(freq-samp_rate/decimation/2)/1e6, x_axis_step_value=(samp_rate/decimation/vec_length)/1e6, x_axis_label="Frequency", y_axis_label="Average Signal", x_axis_units="MHz", y_axis_units='dB', y_min=yroll-1000/yzoom, y_max=yroll+1000/yzoom)
        self.epy_block_0 = epy_block_0.spectrum_integrator(vec_length=vec_length, integration_time=integration_time, mode=integration_mode, samp_rate=samp_rate/4)
        # Create the options list
        self._calibration_mode_options = [0, 1, 2]
        # Create the labels list
        self._calibration_mode_labels = ['Calibration off', 'Static Calibration', 'Dynamic Calibration']
        # Create the combo box
        # Create the radio buttons
        self._calibration_mode_group_box = Qt.QGroupBox("Calibration Mode" + ": ")
        self._calibration_mode_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._calibration_mode_button_group = variable_chooser_button_group()
        self._calibration_mode_group_box.setLayout(self._calibration_mode_box)
        for i, _label in enumerate(self._calibration_mode_labels):
            radio_button = Qt.QRadioButton(_label)
            self._calibration_mode_box.addWidget(radio_button)
            self._calibration_mode_button_group.addButton(radio_button, i)
        self._calibration_mode_callback = lambda i: Qt.QMetaObject.invokeMethod(self._calibration_mode_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._calibration_mode_options.index(i)))
        self._calibration_mode_callback(self.calibration_mode)
        self._calibration_mode_button_group.buttonClicked[int].connect(
            lambda i: self.set_calibration_mode(self._calibration_mode_options[i]))
        self.gui_tab_grid_layout_0.addWidget(self._calibration_mode_group_box, 1, 6, 3, 4)
        for r in range(1, 4):
            self.gui_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(6, 10):
            self.gui_tab_grid_layout_0.setColumnStretch(c, 1)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_float*1, vec_length)
        self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, vec_length)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_float*vec_length,db_enabled,0)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(10, vec_length, 0)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(vec_length)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.spectrum_save, 'pressed'), (self.epy_block_1, 'save'))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.qtgui_histogram_sink_x_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.epy_block_0, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.blocks_selector_0, 1))
        self.connect((self.blocks_selector_0, 0), (self.blocks_vector_to_stream_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.qtgui_vector_sink_f_0_0_1_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.epy_block_1, 0))
        self.connect((self.epy_block_0, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.epy_block_0, 0), (self.blocks_selector_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.pfb_decimator_ccf_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.pfb_decimator_ccf_0, 0), (self.blocks_stream_to_vector_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "RadioTelescope1420")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_source_freq(self):
        return self.source_freq

    def set_source_freq(self, source_freq):
        self.source_freq = source_freq
        self.set_freq(self.source_freq)

    def get_yzoom(self):
        return self.yzoom

    def set_yzoom(self, yzoom):
        self.yzoom = yzoom
        self.epy_block_1.y_max = self.yroll+1000/self.yzoom
        self.epy_block_1.y_min = self.yroll-1000/self.yzoom
        self.qtgui_vector_sink_f_0_0_1_0.set_y_axis((self.yroll-1000/self.yzoom), (self.yroll+1000/self.yzoom))

    def get_yroll(self):
        return self.yroll

    def set_yroll(self, yroll):
        self.yroll = yroll
        self.epy_block_1.y_max = self.yroll+1000/self.yzoom
        self.epy_block_1.y_min = self.yroll-1000/self.yzoom
        self.qtgui_vector_sink_f_0_0_1_0.set_y_axis((self.yroll-1000/self.yzoom), (self.yroll+1000/self.yzoom))

    def get_vec_length(self):
        return self.vec_length

    def set_vec_length(self, vec_length):
        self.vec_length = vec_length
        self.epy_block_0.vec_length = self.vec_length
        self.epy_block_1.vec_length = self.vec_length
        self.epy_block_1.x_axis_step_value = (self.samp_rate/self.decimation/self.vec_length)/1e6
        self.fft_vxx_0.set_window(window.rectangular(self.vec_length))
        self.qtgui_vector_sink_f_0_0_1_0.set_x_axis(((self.freq-self.samp_rate/self.decimation/2)/1e6), ((self.samp_rate/self.decimation/self.vec_length)/1e6))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.epy_block_0.samp_rate = self.samp_rate/4
        self.epy_block_1.x_axis_start_value = (self.freq-self.samp_rate/self.decimation/2)/1e6
        self.epy_block_1.x_axis_step_value = (self.samp_rate/self.decimation/self.vec_length)/1e6
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.qtgui_vector_sink_f_0_0_1_0.set_x_axis(((self.freq-self.samp_rate/self.decimation/2)/1e6), ((self.samp_rate/self.decimation/self.vec_length)/1e6))
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
        self.epy_block_0.integration_time = self.integration_time

    def get_integration_mode(self):
        return self.integration_mode

    def set_integration_mode(self, integration_mode):
        self.integration_mode = integration_mode
        self._integration_mode_callback(self.integration_mode)
        self.epy_block_0.mode = self.integration_mode

    def get_freq_corr(self):
        return self.freq_corr

    def set_freq_corr(self, freq_corr):
        self.freq_corr = freq_corr
        self.osmosdr_source_0.set_freq_corr(self.freq_corr, 0)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.epy_block_1.x_axis_start_value = (self.freq-self.samp_rate/self.decimation/2)/1e6
        self.osmosdr_source_0.set_center_freq(self.freq, 0)
        self.qtgui_vector_sink_f_0_0_1_0.set_x_axis(((self.freq-self.samp_rate/self.decimation/2)/1e6), ((self.samp_rate/self.decimation/self.vec_length)/1e6))
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.freq, self.samp_rate)

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation
        self.epy_block_1.x_axis_start_value = (self.freq-self.samp_rate/self.decimation/2)/1e6
        self.epy_block_1.x_axis_step_value = (self.samp_rate/self.decimation/self.vec_length)/1e6
        self.qtgui_vector_sink_f_0_0_1_0.set_x_axis(((self.freq-self.samp_rate/self.decimation/2)/1e6), ((self.samp_rate/self.decimation/self.vec_length)/1e6))

    def get_db_enabled(self):
        return self.db_enabled

    def set_db_enabled(self, db_enabled):
        self.db_enabled = db_enabled
        self._db_enabled_callback(self.db_enabled)
        self.blocks_selector_0.set_input_index(self.db_enabled)

    def get_calibration_mode(self):
        return self.calibration_mode

    def set_calibration_mode(self, calibration_mode):
        self.calibration_mode = calibration_mode
        self._calibration_mode_callback(self.calibration_mode)

    def get_bit_max(self):
        return self.bit_max

    def set_bit_max(self, bit_max):
        self.bit_max = bit_max
        self.qtgui_histogram_sink_x_0.set_bins(self.bit_max)




def main(top_block_cls=RadioTelescope1420, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    tb.flowgraph_started.set()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
