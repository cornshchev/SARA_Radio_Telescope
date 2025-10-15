"""
Embedded Python Block: Histogram Display for Dynamic Range Observation

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. All parameters are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pyqtgraph as pg
from PyQt5 import QtCore, QtWidgets
from pyqtgraph import HistogramLUTItem

class histogram_display(gr.sync_block, QtCore.QObject):
    """
    自定义Python Block，用于接收信号数据并使用PyQtGraph显示直方图来观测接收机动态范围
    """
    
    # 定义信号
    update_display_signal = QtCore.pyqtSignal(np.ndarray)
    
    def __init__(self, bins=100, samples_need=1000, x0=0, x1=0.5, parent=None):
        # 分别调用两个父类的初始化
        gr.sync_block.__init__(
            self,
            name="Histogram Display Block",
            in_sig=[np.float32],
            out_sig=None
        )
        QtCore.QObject.__init__(self)
        
        self.bins = bins
        self.samples_need = samples_need
        self.x0 = x0
        self.x1 = x1
        self.parent = parent
        
        # 数据缓冲区
        self.data_buffer = np.array([], dtype=np.float32)
        self.update_time = 0.10  # 更新间隔（秒）
        self.last_update_time = 0
        
        # 直方图参数
        self.enable_autoscale = True
        self.enable_accumulate = False
        self.enable_grid = False
        self.enable_axis_labels = False
        
        # 连接信号到槽
        self.update_display_signal.connect(self.update_display, QtCore.Qt.QueuedConnection)
        
        # 初始化PyQtGraph显示
        self.init_pyqtgraph()
        
        # 初始化直方图数据
        self.hist_data = None
        self.bin_centers = None
    
    def init_pyqtgraph(self):
        """初始化PyQtGraph直方图显示"""
        if self.parent and hasattr(self.parent, 'add_histogram_widget'):
            # 创建主窗口
            self.main_widget = QtWidgets.QWidget()
            self.main_widget.setWindowTitle("信号直方图 - 接收机动态范围")
            
            # 创建布局
            layout = QtWidgets.QVBoxLayout()
            self.main_widget.setLayout(layout)
            
            # 创建PlotWidget用于显示直方图
            self.plot_widget = pg.PlotWidget()
            self.plot_widget.setBackground('#f0f0f0')
            
            if self.enable_axis_labels:
                self.plot_widget.setLabel('left', '计数')
                self.plot_widget.setLabel('bottom', '幅度')
            else:
                # 隐藏坐标轴标签
                self.plot_widget.getAxis('left').setLabel('')
                self.plot_widget.getAxis('bottom').setLabel('')
            
            self.plot_widget.showGrid(self.enable_grid, self.enable_grid)
            
            # 创建直方图曲线
            self.histogram_curve = self.plot_widget.plot(pen={'color': 'b', 'width': 1}, stepMode=True)
            
            # 添加统计信息文本
            self.text_item = pg.TextItem("", color='k', anchor=(0, 1))
            self.plot_widget.addItem(self.text_item)
            
            layout.addWidget(self.plot_widget)
            
            # 添加到父窗口
            self.parent.add_histogram_widget(self.main_widget)
            
            # 显示窗口
            self.main_widget.show()
    
    def work(self, input_items, output_items):
        """处理输入数据"""
        in0 = input_items[0]
        
        if len(in0) > 0:
            # 将新数据添加到缓冲区
            self.data_buffer = np.concatenate([self.data_buffer, in0])
            
            # 如果缓冲区数据足够，处理并更新显示
            if len(self.data_buffer) >= self.samples_need:
                # 截取需要的数据量
                process_data = self.data_buffer[:self.samples_need]
                self.data_buffer = self.data_buffer[self.samples_need:]
                
                # 计算直方图
                hist, bin_edges = np.histogram(process_data, bins=self.bins, 
                                             range=(self.x0, self.x1), density=False)
                
                # 计算bin中心点
                bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
                
                # 发射信号更新显示（在主线程中执行）
                self.update_display_signal.emit(np.column_stack((bin_centers, hist)))
        
        return len(in0)
    
    @QtCore.pyqtSlot(np.ndarray)
    def update_display(self, data):
        """更新直方图显示（在主线程中执行）"""
        try:
            if hasattr(self, 'histogram_curve') and self.histogram_curve:
                # 获取bin边界和计数
                bin_edges = data[:, 0]  # 这里应该是bin边界，不是中心点
                hist_values = data[:, 1]
                
                # 修正：使用bin边界作为X，长度为bins+1
                # 但我们需要重新计算正确的边界
                if len(hist_values) > 0:
                    # 重新计算bin边界（假设均匀分布）
                    n_bins = len(hist_values)
                    if n_bins > 1:
                        # 计算bin宽度
                        bin_width = (self.x1 - self.x0) / n_bins
                        # 创建bin边界数组（长度为n_bins+1）
                        bin_edges = np.linspace(self.x0, self.x1, n_bins + 1)
                        
                        # 更新直方图曲线
                        self.histogram_curve.setData(bin_edges, hist_values, stepMode=True)
                        
                        # 自动调整Y轴范围
                        if self.enable_autoscale and len(hist_values) > 0:
                            max_count = np.max(hist_values)
                            self.plot_widget.setYRange(0, max_count * 1.1)
                        
                        # 更新统计信息
                        non_zero_indices = hist_values > 0
                        if np.any(non_zero_indices):
                            # 计算bin中心点用于统计
                            bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
                            
                            max_bin_idx = np.argmax(hist_values)
                            max_bin_center = bin_centers[max_bin_idx]
                            max_count = hist_values[max_bin_idx]
                            
                            min_amplitude = np.min(bin_centers[non_zero_indices])
                            max_amplitude = np.max(bin_centers[non_zero_indices])
                            dynamic_range_db = 20 * np.log10(max_amplitude / min_amplitude) if min_amplitude > 0 else 0
                            
                            stats_text = f"峰值: {max_bin_center:.3f}\n计数: {max_count}\n动态范围: {dynamic_range_db:.1f} dB"
                            self.text_item.setText(stats_text)
                            self.text_item.setPos(bin_edges[0], np.max(hist_values) * 0.9)
                    
        except Exception as e:
            print(f"直方图更新错误: {e}")
    
    def set_update_time(self, time):
        """设置更新间隔"""
        self.update_time = time
    
    def enable_autoscale(self, enable):
        """启用/禁用自动缩放"""
        self.enable_autoscale = enable
    
    def enable_accumulate(self, enable):
        """启用/禁用累积模式"""
        self.enable_accumulate = enable
        # 注意：累积模式需要特殊处理，这里需要修改数据缓冲区管理
    
    def enable_grid(self, enable):
        """启用/禁用网格"""
        self.enable_grid = enable
        if hasattr(self, 'plot_widget'):
            self.plot_widget.showGrid(enable, enable)
    
    def enable_axis_labels(self, enable):
        """启用/禁用坐标轴标签"""
        self.enable_axis_labels = enable
        if hasattr(self, 'plot_widget'):
            if enable:
                self.plot_widget.setLabel('left', '计数')
                self.plot_widget.setLabel('bottom', '幅度')
            else:
                self.plot_widget.getAxis('left').setLabel('')
                self.plot_widget.getAxis('bottom').setLabel('')
    
    def disable_legend(self):
        """禁用图例（pyqtgraph默认不显示图例，此方法为兼容性保留）"""
        pass