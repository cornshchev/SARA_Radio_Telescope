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
        self.decimation = decimation = 8
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
        self.qtgui_histogram_sink_x_0.enable_grid(True)
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
            [-0.00010077140177600086,3.744094076378371e-18,0.00010225032747257501,0.0001928186829900369,0.0002597580896690488,0.00029382319189608097,0.000289677846012637,0.0002466746373102069,0.00016909977421164513,6.583039066754282e-05,-5.0583734264364466e-05,-0.00016533579037059098,-0.00026313215494155884,-0.00033012282801792026,-0.00035576397203840315,-0.0003343744028825313,-0.00026616855757310987,-0.00015759572852402925,-2.0890498490189202e-05,0.0001271671208087355,0.0002671798865776509,0.0003795491938944906,0.0004470957210287452,0.0004575501661747694,0.00040556868771091104,0.00029396190075203776,0.0001339077716693282,-5.5962584156077355e-05,-0.0002515707165002823,-0.0004262994334567338,-0.0005544746527448297,-0.0006149832624942064,-0.0005945363081991673,-0.0004900945932604373,-0.0003100538451690227,-7.392675615847111e-05,0.000189549449714832,0.0004457355826161802,0.0006584867369383574,0.0007950858562253416,0.0008310627308674157,0.0007542108069173992,0.0005671796971000731,0.00028817192651331425,-5.04916170029901e-05,-0.0004058895574416965,-0.000729755440261215,-0.0009748543961904943,-0.001101661822758615,-0.0010844252537935972,-0.0009157112799584866,-0.0006086961948312819,-0.00019672000780701637,0.0002700166078284383,0.0007303403108380735,0.0011199230793863535,0.0013800577726215124,0.0014662218745797873,0.0013552122982218862,0.0010497546754777431,0.0005797845660708845,-1.471207555619054e-17,-0.0006161980563774705,-0.0011857599020004272,-0.0016269513871520758,-0.0018708114512264729,-0.0018715295009315014,-0.0016142255626618862,-0.0011188883800059557,-0.0004396907170303166,0.0003404956660233438,0.0011199063155800104,0.0017908948939293623,0.0022545214742422104,0.002434777794405818,0.002290444914251566,0.001822799677029252,0.0010778607102110982,0.00014255345740821213,-0.0008650132222101092,-0.0018101362511515617,-0.0025592176243662834,-0.0029982891865074635,-0.003049836726859212,-0.0026855035685002804,-0.001932682585902512,-0.0008737613097764552,0.0003622721997089684,0.001615110319107771,0.002713544527068734,0.003498471574857831,0.0038454467430710793,0.0036836452782154083,0.0030084303580224514,0.0018854588270187378,0.0004453219298738986,-0.001131025841459632,-0.0026345201767981052,-0.0038552533369511366,-0.004611252341419458,-0.004774898290634155,-0.0042932238429784775,-0.0031990045681595802,-0.0016106439288705587,0.0002796905755531043,0.002228643512353301,0.003972405567765236,0.005261801183223724,0.00589714152738452,0.00575806200504303,0.0048240129835903645,0.003182128304615617,0.0010207775048911572,-0.0013910436537116766,-0.0037363660521805286,-0.005691098980605602,-0.006967911962419748,-0.0073573230765759945,-0.006760253105312586,-0.0052071912214159966,-0.002860687207430601,3.61133158806361e-17,0.0030109172221273184,0.005768586881458759,0.00788287352770567,0.009030761197209358,0.009003815241158009,0.007742572575807571,0.00535252969712019,0.0020986301824450493,-0.001622132956981659,-0.005327435210347176,-0.008510385639965534,-0.010706890374422073,-0.011560900136828423,-0.010878674685955048,-0.008664165623486042,-0.0051297699101269245,-0.000679649121593684,0.004133662208914757,0.008675052784383297,0.012307527475059032,0.014477899298071861,0.014796378090977669,0.013099155388772488,0.009484703652560711,0.004317425191402435,-0.0018037520349025726,-0.008109875954687595,-0.013753114268183708,-0.01791430450975895,-0.01991395093500614,-0.01931246928870678,-0.015986070036888123,-0.010166900232434273,-0.0024399636313319206,0.006305685732513666,0.014968391507863998,0.02235942706465721,0.02734929695725441,0.029018204659223557,0.02679256722331047,0.020550107583403587,0.01067889854311943,-0.0019196730572730303,-0.01588793843984604,-0.029526036232709885,-0.0409533753991127,-0.048301875591278076,-0.04992091655731201,-0.04457191005349159,-0.03159036487340927,-0.0109963184222579,0.016461091116070747,0.0493323989212513,0.0855695903301239,0.12269250303506851,0.1580045372247696,0.18883630633354187,0.21279296278953552,0.22797951102256775,0.23318113386631012,0.22797951102256775,0.21279296278953552,0.18883630633354187,0.1580045372247696,0.12269250303506851,0.0855695903301239,0.0493323989212513,0.016461091116070747,-0.0109963184222579,-0.03159036487340927,-0.04457191005349159,-0.04992091655731201,-0.048301875591278076,-0.0409533753991127,-0.029526036232709885,-0.01588793843984604,-0.0019196730572730303,0.01067889854311943,0.020550107583403587,0.02679256722331047,0.029018204659223557,0.02734929695725441,0.02235942706465721,0.014968391507863998,0.006305685732513666,-0.0024399636313319206,-0.010166900232434273,-0.015986070036888123,-0.01931246928870678,-0.01991395093500614,-0.01791430450975895,-0.013753114268183708,-0.008109875954687595,-0.0018037520349025726,0.004317425191402435,0.009484703652560711,0.013099155388772488,0.014796378090977669,0.014477899298071861,0.012307527475059032,0.008675052784383297,0.004133662208914757,-0.000679649121593684,-0.0051297699101269245,-0.008664165623486042,-0.010878674685955048,-0.011560900136828423,-0.010706890374422073,-0.008510385639965534,-0.005327435210347176,-0.001622132956981659,0.0020986301824450493,0.00535252969712019,0.007742572575807571,0.009003815241158009,0.009030761197209358,0.00788287352770567,0.005768586881458759,0.0030109172221273184,3.61133158806361e-17,-0.002860687207430601,-0.0052071912214159966,-0.006760253105312586,-0.0073573230765759945,-0.006967911962419748,-0.005691098980605602,-0.0037363660521805286,-0.0013910436537116766,0.0010207775048911572,0.003182128304615617,0.0048240129835903645,0.00575806200504303,0.00589714152738452,0.005261801183223724,0.003972405567765236,0.002228643512353301,0.0002796905755531043,-0.0016106439288705587,-0.0031990045681595802,-0.0042932238429784775,-0.004774898290634155,-0.004611252341419458,-0.0038552533369511366,-0.0026345201767981052,-0.001131025841459632,0.0004453219298738986,0.0018854588270187378,0.0030084303580224514,0.0036836452782154083,0.0038454467430710793,0.003498471574857831,0.002713544527068734,0.001615110319107771,0.0003622721997089684,-0.0008737613097764552,-0.001932682585902512,-0.0026855035685002804,-0.003049836726859212,-0.0029982891865074635,-0.0025592176243662834,-0.0018101362511515617,-0.0008650132222101092,0.00014255345740821213,0.0010778607102110982,0.001822799677029252,0.002290444914251566,0.002434777794405818,0.0022545214742422104,0.0017908948939293623,0.0011199063155800104,0.0003404956660233438,-0.0004396907170303166,-0.0011188883800059557,-0.0016142255626618862,-0.0018715295009315014,-0.0018708114512264729,-0.0016269513871520758,-0.0011857599020004272,-0.0006161980563774705,-1.471207555619054e-17,0.0005797845660708845,0.0010497546754777431,0.0013552122982218862,0.0014662218745797873,0.0013800577726215124,0.0011199230793863535,0.0007303403108380735,0.0002700166078284383,-0.00019672000780701637,-0.0006086961948312819,-0.0009157112799584866,-0.0010844252537935972,-0.001101661822758615,-0.0009748543961904943,-0.000729755440261215,-0.0004058895574416965,-5.04916170029901e-05,0.00028817192651331425,0.0005671796971000731,0.0007542108069173992,0.0008310627308674157,0.0007950858562253416,0.0006584867369383574,0.0004457355826161802,0.000189549449714832,-7.392675615847111e-05,-0.0003100538451690227,-0.0004900945932604373,-0.0005945363081991673,-0.0006149832624942064,-0.0005544746527448297,-0.0004262994334567338,-0.0002515707165002823,-5.5962584156077355e-05,0.0001339077716693282,0.00029396190075203776,0.00040556868771091104,0.0004575501661747694,0.0004470957210287452,0.0003795491938944906,0.0002671798865776509,0.0001271671208087355,-2.0890498490189202e-05,-0.00015759572852402925,-0.00026616855757310987,-0.0003343744028825313,-0.00035576397203840315,-0.00033012282801792026,-0.00026313215494155884,-0.00016533579037059098,-5.0583734264364466e-05,6.583039066754282e-05,0.00016909977421164513,0.0002466746373102069,0.000289677846012637,0.00029382319189608097,0.0002597580896690488,0.0001928186829900369,0.00010225032747257501,3.744094076378371e-18,-0.00010077140177600086],
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
