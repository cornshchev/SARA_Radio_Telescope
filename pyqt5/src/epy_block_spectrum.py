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

class SpectrumDisplayBlock(gr.sync_block, QtCore.QObject):
    """
    自定义Python Block，用于接收频谱数据并使用PyQtGraph显示
    """
    
    # 定义信号
    update_display_signal = QtCore.pyqtSignal(np.ndarray)
    
    def __init__(self, vec_length=1024, parent=None):
        # 分别调用两个父类的初始化
        gr.sync_block.__init__(
            self,
            name="Spectrum Display Block",
            in_sig=[(np.float32, vec_length)],
            out_sig=None
        )
        QtCore.QObject.__init__(self)
        
        self.vec_length = vec_length
        self.parent = parent
        self.data_queue = []
        self.max_queue_size = 10
        
        # 连接信号到槽
        self.update_display_signal.connect(self.update_display, QtCore.Qt.QueuedConnection)
        
        # 初始化PyQtGraph显示
        self.init_pyqtgraph()
    
    def init_pyqtgraph(self):
        """初始化PyQtGraph显示"""
        if self.parent and hasattr(self.parent, 'add_spectrum_widget'):
            # 创建PyQtGraph绘图窗口
            self.plot_widget = pg.PlotWidget()
            self.plot_widget.setWindowTitle("Spectrum Display")
            self.plot_widget.setLabel('left', 'Amplitude', 'dB')
            self.plot_widget.setLabel('bottom', 'Frequency', 'MHz')
            self.plot_widget.showGrid(True, True)
            
            # 创建曲线
            self.curve = self.plot_widget.plot(pen='y')
            
            # 添加到父窗口
            self.parent.add_spectrum_widget(self.plot_widget)
    
    def work(self, input_items, output_items):
        """处理输入数据"""
        in0 = input_items[0]
        
        if len(in0) > 0:
            # 获取最新的频谱数据
            spectrum_data = in0[0]
            
            # 将数据添加到队列
            self.data_queue.append(spectrum_data.copy())
            if len(self.data_queue) > self.max_queue_size:
                self.data_queue.pop(0)
            
            # 发射信号更新显示
            if hasattr(self, 'curve') and self.curve:
                self.update_display_signal.emit(spectrum_data.copy())
        
        return len(input_items[0])
    
    @QtCore.pyqtSlot(np.ndarray)
    def update_display(self, data):
        """更新显示（在主线程中执行）"""
        try:
            if hasattr(self, 'curve') and self.curve:
                x_data = np.arange(len(data))
                self.curve.setData(x_data, data)
        except Exception as e:
            print(f"Error updating display: {e}")