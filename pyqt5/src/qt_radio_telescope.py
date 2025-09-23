#!/usr/bin/env gnuradio_env
# -*- coding: utf-8 -*-

#
# pyqt5 GUI for a simple radio telescope application
# GNU Radio version: 3.10.11.0

from PyQt5 import QtWidgets
from PyQt5 import uic
from gnuradio import qtgui
from PyQt5 import Qt, QtCore
from PyQt5.QtCore import QObject, pyqtSlot
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
import RadioTelescope1420_epy_block_0 as epy_block_0  # embedded python block
import pyqt5.src.epy_block_spectrum as epy_block_1  # embedded python block
import numpy
import osmosdr
import time
import sip
import threading



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # 建中央部件
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

            
        uic.loadUi('pyqt5/src/ui/main_win.ui', self.central_widget)

        ##################################################
        # Variables
        ##################################################
        self.freq = 1420400000
        self.vec_length = vec_length = 1024
        self.samp_rate = samp_rate = 6000000
        self.decimation = decimation = 4
        self.bit_max = bit_max = 4096
        # self.yzoom = yzoom = 10
        # self.yroll = yroll = 0
        
        self.rf_gain = rf_gain = self.findChild(QtWidgets.QSlider, "slider_gain")
        self.integration_time = integration_time = self.findChild(QtWidgets.QSlider, "slider_gain")
        # self.integration_mode = integration_mode = self.findchild(QtWidgets.QRadioButton, "radio_movingaverage")
        self.freq_corr = freq_corr = self.findChild(QtWidgets.QDoubleSpinBox, "spinbox_freqcorr")
        self.freq = freq = source_freq = self.findChild(QtWidgets.QSlider, "sllider_freq")
        
        self.db_enabled = db_enabled = self.findChild(QtWidgets.QCheckBox, "checkbox_enabledb")
        # self.calibration_mode = calibration_mode = self.findChild(QtWidgets.QRadioButton, "radio_calibration")
        

        ##################################################
        # Blocks
        ##################################################

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

        # self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.qwidget(), Qt.QWidget)

        # self.gui_tab_grid_layout_0.addWidget(self._qtgui_waterfall_sink_x_0_win, 4, 0, 6, 16)
        # for r in range(4, 10):
        #     self.gui_tab_grid_layout_0.setRowStretch(r, 1)
        # for c in range(0, 16):
        #     self.gui_tab_grid_layout_0.setColumnStretch(c, 1)
        # self.qtgui_vector_sink_f_0_0_1_0 = qtgui.vector_sink_f(
        #     vec_length,
        #     ((freq-samp_rate/decimation/2)/1e6),
        #     ((samp_rate/decimation/vec_length)/1e6),
        #     "Frequency",
        #     "Average Signal",
        #     "Average Spectrum",
        #     1, # Number of inputs
        #     None # parent
        # )
        # self.qtgui_vector_sink_f_0_0_1_0.set_update_time(0.10)
        # self.qtgui_vector_sink_f_0_0_1_0.set_y_axis((yroll-1000/yzoom), (yroll+1000/yzoom))
        # self.qtgui_vector_sink_f_0_0_1_0.enable_autoscale(False)
        # self.qtgui_vector_sink_f_0_0_1_0.enable_grid(True)
        # self.qtgui_vector_sink_f_0_0_1_0.set_x_axis_units("MHz")
        # self.qtgui_vector_sink_f_0_0_1_0.set_y_axis_units("Amp/dB")
        # self.qtgui_vector_sink_f_0_0_1_0.set_ref_level(0)


        # labels = ['Spectrum', '', '', '', '',
        #     '', '', '', '', '']
        # widths = [2, 1, 1, 1, 1,
        #     1, 1, 1, 1, 1]
        # colors = ["blue", "red", "green", "black", "cyan",
        #     "magenta", "yellow", "dark red", "dark green", "dark blue"]
        # alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
        #     1.0, 1.0, 1.0, 1.0, 1.0]

        # for i in range(1):
        #     if len(labels[i]) == 0:
        #         self.qtgui_vector_sink_f_0_0_1_0.set_line_label(i, "Data {0}".format(i))
        #     else:
        #         self.qtgui_vector_sink_f_0_0_1_0.set_line_label(i, labels[i])
        #     self.qtgui_vector_sink_f_0_0_1_0.set_line_width(i, widths[i])
        #     self.qtgui_vector_sink_f_0_0_1_0.set_line_color(i, colors[i])
        #     self.qtgui_vector_sink_f_0_0_1_0.set_line_alpha(i, alphas[i])

        # self._qtgui_vector_sink_f_0_0_1_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_0_1_0.qwidget(), Qt.QWidget)
        # self.gui_tab_grid_layout_0.addWidget(self._qtgui_vector_sink_f_0_0_1_0_win, 11, 0, 10, 16)
        # for r in range(11, 21):
        #     self.gui_tab_grid_layout_0.setRowStretch(r, 1)
        # for c in range(0, 16):
        #     self.gui_tab_grid_layout_0.setColumnStretch(c, 1)
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

        # 获取 QWidget
        histogram_win = self.qtgui_histogram_sink_x_0.qwidget()
        self.central_widget.findChild(QtWidgets.QWidget, "widget_histogram").layout().addWidget(histogram_win)

        # self._qtgui_histogram_sink_x_0_win = sip.wrapinstance(self.qtgui_histogram_sink_x_0.qwidget(), Qt.QWidget)
        # self.gui_tab_grid_layout_0.addWidget(self._qtgui_histogram_sink_x_0_win, 0, 0, 4, 4)
        # for r in range(0, 4):
        #     self.gui_tab_grid_layout_0.setRowStretch(r, 1)
        # for c in range(0, 4):
        #     self.gui_tab_grid_layout_0.setColumnStretch(c, 1)
        self.pfb_decimator_ccf_0 = pfb.decimator_ccf(
            decimation,
            [-1.72349809872685e-05,-1.2635308848985005e-05,5.224483605630463e-19,1.4853208085696679e-05,2.3831502403481863e-05,2.0874309484497644e-05,5.762801265518647e-06,-1.4855566405458376e-05,-3.0229126423364505e-05,-3.1006173230707645e-05,-1.4715826182509772e-05,1.1899030141648836e-05,3.5437817132333294e-05,4.2475381633266807e-05,2.705041151784826e-05,-5.091793354949914e-06,-3.827183900284581e-05,-5.438654261524789e-05,-4.263747177901678e-05,-6.320377906376962e-06,3.741988984984346e-05,6.550404941663146e-05,6.095322532928549e-05,2.2839672965346836e-05,-3.154400837956928e-05,-7.428459502989426e-05,-8.102563151624054e-05,-4.459935371414758e-05,1.9403796613914892e-05,7.894639566075057e-05,0.00010141074017155915,7.12546388967894e-05,-3.921092529491243e-18,-7.757605635561049e-05,-0.00012020699796266854,-0.00010189267050009221,-2.7271727958577685e-05,6.827121251262724e-05,0.00013511384895537049,0.00013497326290234923,6.246820703381673e-05,-4.9313508498016745e-05,-0.00014353806909639388,-0.00016831152606755495,-0.00010496056347619742,1.9362872990313917e-05,0.00014274813293013722,0.00019911186245735735,0.0001533250615466386,2.233897066616919e-05,-0.00013007273082621396,-0.00022406013158615679,-0.00020527711603790522,-7.577090582344681e-05,0.00010313526581740007,0.00023947743466123939,0.0002576623228378594,0.00013995783228892833,-6.0112397477496415e-05,-0.00024153420235961676,-0.0003065149358008057,-0.00021283715614117682,5.4672353694182105e-18,0.00022651886683888733,0.00034719222458079457,0.00029118405655026436,7.713247032370418e-05,-0.00019114943279419094,-0.00037458655424416065,-0.0003706115821842104,-0.00016992099699564278,0.0001329122023889795,0.0003834134840872139,0.00044565898133441806,0.0002755417372100055,-5.040622636443004e-05,-0.00036856677616015077,-0.0005099756526760757,-0.00038962316466495395,-5.633059481624514e-05,0.00032552541233599186,0.0005566042382270098,0.0005062550189904869,0.00018554097914602607,-0.0002507915487512946,-0.0005783576052635908,-0.0006181093049235642,-0.00033354051993228495,0.00014233298134058714,0.0005682790651917458,0.0007166816503740847,0.0004946094704791903,-2.005905540815579e-17,-0.0005201649037189782,-0.0007926575490273535,-0.0006610067212022841,-0.000174116954440251,0.0004291251243557781,0.0008363942033611238,0.0008231242536567152,0.00037542215432040393,-0.0002921474224422127,-0.0008385056862607598,-0.0009697929490357637,-0.0005966737517155707,0.00010862800263566896,0.0007905253442004323,0.0010887406533583999,0.0008279953617602587,0.00011917019583052024,-0.0006856143590994179,-0.0011671968968585134,-0.001057060551829636,-0.0003857740666717291,0.0005192758399061859,0.001192621304653585,0.0012694646138697863,0.0006823089206591249,-0.00029002971132285893,-0.0011535336961969733,-0.0014492832124233246,-0.0009964924538508058,3.3554545152266615e-17,0.0010403975611552596,0.0015798115637153387,0.0013128406135365367,0.00034463408519513905,-0.0008465187856927514,-0.0016444595530629158,-0.0016130991280078888,-0.0007333690882660449,0.0005688991514034569,0.0016277696704491973,0.0018769066082313657,0.0011513307690620422,-0.0002089907939080149,-0.001516512013040483,-0.0020826749969273806,-0.0015794800128787756,-0.00022670712496619672,0.0013008004752919078,0.0022086657118052244,0.0019950910937041044,0.0007262639701366425,-0.0009751687757670879,-0.002234220737591386,-0.0023725065402686596,-0.0012721923412755132,0.0005395361222326756,0.0021410961635410786,0.0026841601356863976,0.0018416200764477253,-4.950621041337197e-17,-0.0019148358842357993,-0.0029018374625593424,-0.002406783401966095,-0.0006306119612418115,0.0015461135189980268,0.0029981317929923534,0.002935847034677863,0.0013324839528650045,-0.001031962689012289,-0.00294804060831666,-0.003394045401364565,-0.002078894292935729,0.00037682504625990987,0.0027306245174258947,0.003745111171156168,0.0028366653714329004,0.0004066622641403228,-0.0023306573275476694,-0.003952948842197657,-0.0035669931676238775,-0.0012972023105248809,0.001740171923302114,0.003983487840741873,0.004226649645715952,0.0022647471632808447,-0.0009598266333341599,-0.0038066357374191284,-0.004769519902765751,-0.0032708144281059504,6.591672599515029e-17,0.0033982463646680117,0.005148435011506081,0.004269224591553211,0.001118447515182197,-0.0027420069091022015,-0.005317220464348793,-0.005207243375480175,-0.0023638049606233835,0.0018311510793864727,0.005232877563685179,0.006027106195688248,0.0036935671232640743,-0.0006699076620861888,-0.004857794381678104,-0.006667840760201216,-0.005054924171417952,-0.0007253880612552166,0.0041618854738771915,0.0070673199370503426,0.006385659333318472,0.0023255764972418547,-0.0031245388090610504,-0.007164420560002327,-0.007615393493324518,-0.004088378045707941,0.0017362736398354173,0.006901151966303587,0.008667081594467163,0.005958509631454945,-8.026712510030815e-17,-0.006224585231393576,-0.009458595886826515,-0.007868153043091297,-0.002068196190521121,0.005088386591523886,0.009904180653393269,0.00973766390234232,0.004438807722181082,-0.003453710814937949,-0.009915470145642757,-0.011476289480924606,-0.007069242652505636,0.0012891283258795738,0.00940158125013113,0.0129825659096241,0.009904749691486359,0.001430871314369142,-0.008267566561698914,-0.01414375752210617,-0.012879917398095131,-0.0047295596450567245,0.0064099617302417755,0.014833353459835052,0.01592070795595646,0.008635164238512516,-0.0037071595434099436,-0.014904596842825413,-0.018946925178170204,-0.013194232247769833,9.00891007809873e-17,0.014176110737025738,0.021875064820051193,0.018496885895729065,0.0049474891275167465,-0.012400717474520206,-0.024621374905109406,-0.024727657437324524,-0.01153181679546833,0.009195168502628803,0.027105027809739113,0.032278675585985184,0.020506424829363823,-0.0038669754285365343,-0.029251251369714737,-0.04204052314162254,-0.033514782786369324,-0.00508249644190073,0.030994273722171783,0.0563218854367733,0.05490107089281082,0.021784022450447083,-0.032279957085847855,-0.08291181921958923,-0.10075752437114716,-0.06359513103961945,0.0330679714679718,0.17161419987678528,0.3165138363838196,0.42596524953842163,0.4666682183742523,0.42596524953842163,0.3165138363838196,0.17161419987678528,0.0330679714679718,-0.06359513103961945,-0.10075752437114716,-0.08291181921958923,-0.032279957085847855,0.021784022450447083,0.05490107089281082,0.0563218854367733,0.030994273722171783,-0.00508249644190073,-0.033514782786369324,-0.04204052314162254,-0.029251251369714737,-0.0038669754285365343,0.020506424829363823,0.032278675585985184,0.027105027809739113,0.009195168502628803,-0.01153181679546833,-0.024727657437324524,-0.024621374905109406,-0.012400717474520206,0.0049474891275167465,0.018496885895729065,0.021875064820051193,0.014176110737025738,9.00891007809873e-17,-0.013194232247769833,-0.018946925178170204,-0.014904596842825413,-0.0037071595434099436,0.008635164238512516,0.01592070795595646,0.014833353459835052,0.0064099617302417755,-0.0047295596450567245,-0.012879917398095131,-0.01414375752210617,-0.008267566561698914,0.001430871314369142,0.009904749691486359,0.0129825659096241,0.00940158125013113,0.0012891283258795738,-0.007069242652505636,-0.011476289480924606,-0.009915470145642757,-0.003453710814937949,0.004438807722181082,0.00973766390234232,0.009904180653393269,0.005088386591523886,-0.002068196190521121,-0.007868153043091297,-0.009458595886826515,-0.006224585231393576,-8.026712510030815e-17,0.005958509631454945,0.008667081594467163,0.006901151966303587,0.0017362736398354173,-0.004088378045707941,-0.007615393493324518,-0.007164420560002327,-0.0031245388090610504,0.0023255764972418547,0.006385659333318472,0.0070673199370503426,0.0041618854738771915,-0.0007253880612552166,-0.005054924171417952,-0.006667840760201216,-0.004857794381678104,-0.0006699076620861888,0.0036935671232640743,0.006027106195688248,0.005232877563685179,0.0018311510793864727,-0.0023638049606233835,-0.005207243375480175,-0.005317220464348793,-0.0027420069091022015,0.001118447515182197,0.004269224591553211,0.005148435011506081,0.0033982463646680117,6.591672599515029e-17,-0.0032708144281059504,-0.004769519902765751,-0.0038066357374191284,-0.0009598266333341599,0.0022647471632808447,0.004226649645715952,0.003983487840741873,0.001740171923302114,-0.0012972023105248809,-0.0035669931676238775,-0.003952948842197657,-0.0023306573275476694,0.0004066622641403228,0.0028366653714329004,0.003745111171156168,0.0027306245174258947,0.00037682504625990987,-0.002078894292935729,-0.003394045401364565,-0.00294804060831666,-0.001031962689012289,0.0013324839528650045,0.002935847034677863,0.0029981317929923534,0.0015461135189980268,-0.0006306119612418115,-0.002406783401966095,-0.0029018374625593424,-0.0019148358842357993,-4.950621041337197e-17,0.0018416200764477253,0.0026841601356863976,0.0021410961635410786,0.0005395361222326756,-0.0012721923412755132,-0.0023725065402686596,-0.002234220737591386,-0.0009751687757670879,0.0007262639701366425,0.0019950910937041044,0.0022086657118052244,0.0013008004752919078,-0.00022670712496619672,-0.0015794800128787756,-0.0020826749969273806,-0.001516512013040483,-0.0002089907939080149,0.0011513307690620422,0.0018769066082313657,0.0016277696704491973,0.0005688991514034569,-0.0007333690882660449,-0.0016130991280078888,-0.0016444595530629158,-0.0008465187856927514,0.00034463408519513905,0.0013128406135365367,0.0015798115637153387,0.0010403975611552596,3.3554545152266615e-17,-0.0009964924538508058,-0.0014492832124233246,-0.0011535336961969733,-0.00029002971132285893,0.0006823089206591249,0.0012694646138697863,0.001192621304653585,0.0005192758399061859,-0.0003857740666717291,-0.001057060551829636,-0.0011671968968585134,-0.0006856143590994179,0.00011917019583052024,0.0008279953617602587,0.0010887406533583999,0.0007905253442004323,0.00010862800263566896,-0.0005966737517155707,-0.0009697929490357637,-0.0008385056862607598,-0.0002921474224422127,0.00037542215432040393,0.0008231242536567152,0.0008363942033611238,0.0004291251243557781,-0.000174116954440251,-0.0006610067212022841,-0.0007926575490273535,-0.0005201649037189782,-2.005905540815579e-17,0.0004946094704791903,0.0007166816503740847,0.0005682790651917458,0.00014233298134058714,-0.00033354051993228495,-0.0006181093049235642,-0.0005783576052635908,-0.0002507915487512946,0.00018554097914602607,0.0005062550189904869,0.0005566042382270098,0.00032552541233599186,-5.633059481624514e-05,-0.00038962316466495395,-0.0005099756526760757,-0.00036856677616015077,-5.040622636443004e-05,0.0002755417372100055,0.00044565898133441806,0.0003834134840872139,0.0001329122023889795,-0.00016992099699564278,-0.0003706115821842104,-0.00037458655424416065,-0.00019114943279419094,7.713247032370418e-05,0.00029118405655026436,0.00034719222458079457,0.00022651886683888733,5.4672353694182105e-18,-0.00021283715614117682,-0.0003065149358008057,-0.00024153420235961676,-6.0112397477496415e-05,0.00013995783228892833,0.0002576623228378594,0.00023947743466123939,0.00010313526581740007,-7.577090582344681e-05,-0.00020527711603790522,-0.00022406013158615679,-0.00013007273082621396,2.233897066616919e-05,0.0001533250615466386,0.00019911186245735735,0.00014274813293013722,1.9362872990313917e-05,-0.00010496056347619742,-0.00016831152606755495,-0.00014353806909639388,-4.9313508498016745e-05,6.246820703381673e-05,0.00013497326290234923,0.00013511384895537049,6.827121251262724e-05,-2.7271727958577685e-05,-0.00010189267050009221,-0.00012020699796266854,-7.757605635561049e-05,-3.921092529491243e-18,7.12546388967894e-05,0.00010141074017155915,7.894639566075057e-05,1.9403796613914892e-05,-4.459935371414758e-05,-8.102563151624054e-05,-7.428459502989426e-05,-3.154400837956928e-05,2.2839672965346836e-05,6.095322532928549e-05,6.550404941663146e-05,3.741988984984346e-05,-6.320377906376962e-06,-4.263747177901678e-05,-5.438654261524789e-05,-3.827183900284581e-05,-5.091793354949914e-06,2.705041151784826e-05,4.2475381633266807e-05,3.5437817132333294e-05,1.1899030141648836e-05,-1.4715826182509772e-05,-3.1006173230707645e-05,-3.0229126423364505e-05,-1.4855566405458376e-05,5.762801265518647e-06,2.0874309484497644e-05,2.3831502403481863e-05,1.4853208085696679e-05,5.224483605630463e-19,-1.2635308848985005e-05,-1.72349809872685e-05],
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
        self.epy_block_1 = epy_block_1.save_spectrum_image(vec_length=vec_length, x_axis_start_value=(freq-samp_rate/decimation/2)/1e6, x_axis_step_value=(samp_rate/decimation/vec_length)/1e6, x_axis_label="Frequency", y_axis_label="Average Signal", x_axis_units="MHz", y_axis_units='dB', y_min=0, y_max=10)
        self.epy_block_0 = epy_block_0.spectrum_integrator(vec_length=vec_length, integration_time=integration_time, mode=0, samp_rate=samp_rate/4)
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
        # self.connect((self.blocks_selector_0, 0), (self.blocks_vector_to_stream_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.qtgui_vector_sink_f_0_0_1_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.fft_vxx_0, 0))
        # self.connect((self.blocks_vector_to_stream_0, 0), (self.epy_block_1, 0))
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

        
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())