"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pyqtgraph as pg
from PyQt5 import QtCore, QtWidgets

class spectrum_display(gr.sync_block, QtCore.QObject):
    """
    自定义Python Block，用于接收频谱数据并使用PyQtGraph显示
    """
    
    # 定义信号
    update_display_signal = QtCore.pyqtSignal(np.ndarray)
    
    def __init__(self, vec_length=1024, freq = 1420400000, samp_rate = 6000000000, cat_ratio = 1.0, parent=None):
        # 分别调用两个父类的初始化
        gr.sync_block.__init__(
            self,
            name="Spectrum Display Block",
            in_sig=[(np.float32, vec_length)],
            out_sig=None
        )
        QtCore.QObject.__init__(self)
        
        self.vec_length = vec_length
        self.freq = freq
        self.samp_rate = samp_rate
        self.cat_ratio = min(1, abs(cat_ratio))
        self.parent = parent

        # self.data_queue = []
        # self.max_queue_size = 10

        self.freq_axis = None  # 预分配频率轴
        self.update_freq_axis()  # 初始化频率轴
        self.frame_count = 0  # 帧计数器
        
        # 连接信号到槽
        self.update_display_signal.connect(self.update_display, QtCore.Qt.QueuedConnection)
        
        # 初始化PyQtGraph显示
        self.init_pyqtgraph()
    
    def init_pyqtgraph(self):
        """初始化PyQtGraph显示"""
        if self.parent and hasattr(self.parent, 'add_spectrum_widget'):
            # 创建PyQtGraph绘图窗口
            self.plot_widget = pg.PlotWidget()
            self.plot_widget.setWindowTitle("平均功率谱")
            self.plot_widget.setBackground('#f0f0f0')
            self.plot_widget.setLabel('left', '功率', 'dB')
            self.plot_widget.setLabel('bottom', '频率', 'MHz')
            self.plot_widget.showGrid(True, True)
            
            # 创建曲线
            self.curve = self.plot_widget.plot(pen={'color': 'b', 'width': 2})
            
            # 添加到父窗口
            self.parent.add_spectrum_widget(self.plot_widget)
    
    def work(self, input_items, output_items):
        """处理输入数据"""
        in0 = input_items[0]
        
        if len(in0) > 0:
            # 获取最新的频谱数据
            spectrum_data = in0[0][self.spectrum_indices]
            
            if hasattr(self, 'curve') and self.curve:
                # 只在必要时发射信号，比如每N帧发射一次
                if self.frame_count % 10 == 0:  # 每5帧更新一次显示
                    self.update_display_signal.emit(spectrum_data.copy())
            self.frame_count += 1
        
        return len(input_items[0])
    
    @QtCore.pyqtSlot(np.ndarray)
    def update_display(self, data):
        """更新显示（在主线程中执行）"""
        try:
            if hasattr(self, 'curve') and self.curve:
                # 使用预分配的频率轴
                self.curve.setData(self.freq_axis, data)
        except Exception as e:
            print(f"epy_block_spectrum.py更新频谱数据错误: {e}")


    def update_freq_axis(self):
        """更新频率轴，只在频率参数变化时调用"""
        n = self.vec_length
        # 计算截取索引
        start_idx = int((0.5 - self.cat_ratio/2) * n)
        end_idx = int((0.5 + self.cat_ratio/2) * n)
        self.spectrum_indices = slice(start_idx, end_idx)
        # 计算频率轴
        self.freq_axis = np.linspace(
            (self.freq - self.samp_rate*self.cat_ratio/2) / 1e6,
            (self.freq + self.samp_rate*self.cat_ratio/2) / 1e6,
            end_idx - start_idx
        )