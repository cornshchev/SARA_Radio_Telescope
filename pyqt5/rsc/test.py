import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
import pyqtgraph as pg


class HistogramWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        # 创建布局
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # 创建 pyqtgraph 的 PlotWidget
        self.plot_widget = pg.PlotWidget()
        self.layout.addWidget(self.plot_widget)
        
        # 生成随机数据（示例）
        data = np.random.normal(size=1000)  # 正态分布数据
        
        # 计算直方图
        y, x = np.histogram(data, bins=30)  # y: 频数, x: bin 边界
        
        # 绘制直方图
        self.bar_item = pg.BarGraphItem(
            x=x[:-1],  # 使用 bin 的左边界作为 x 坐标
            height=y,  # 高度 = 频数
            width=x[1] - x[0],  # 宽度 = bin 的宽度
            brush='b',  # 蓝色填充
            pen='k'  # 黑色边框
        )
        
        self.plot_widget.addItem(self.bar_item)
        
        # 设置图表标题和坐标轴标签
        self.plot_widget.setTitle("数据直方图")
        self.plot_widget.setLabel("left", "频数")
        self.plot_widget.setLabel("bottom", "数值")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("PyQtGraph 直方图示例")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建主 Widget 并设置布局
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        
        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)
        
        # 添加 HistogramWidget
        self.hist_widget = HistogramWidget()
        self.layout.addWidget(self.hist_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())