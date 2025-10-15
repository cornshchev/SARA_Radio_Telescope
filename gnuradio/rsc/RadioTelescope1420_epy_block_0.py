"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr

class spectrum_integrator(gr.sync_block):
    """
    频谱积分器块
    输入: 浮点向量 (频谱数据)
    输出: 积分后的复数向量
    """
    def __init__(self, vec_length=1024, integration_time=1.0, mode=0, samp_rate=1.0):
        gr.sync_block.__init__(
            self,
            name="Spectrum Integrator",
            in_sig=[(np.float32, vec_length)],
            out_sig=[(np.float32, vec_length)]
        )
        
        # 参数初始化
        self.vec_length = vec_length
        self.integration_time = integration_time
        self.mode = mode
        self.samp_rate = samp_rate
        
        # 状态变量
        self.reset_state()
        
        # 上一次的参数值，用于检测变化
        self.last_integration_time = integration_time
        self.last_mode = mode
        self.last_samp_rate = samp_rate
        
    def reset_state(self):
        """重置积分器状态"""
        if self.mode == 0:
            # 移动平均模式：需要存储多个历史帧
            self.n_frames = max(1, int(self.integration_time * self.samp_rate / self.vec_length))
            self.buffer = np.zeros((self.n_frames, self.vec_length), dtype=np.float32)
            self.buffer_index = 0
            self.buffer_count = 0
        else:  # IIR模式
            # IIR滤波器系数
            alpha = 1.0 / max(1.0, self.integration_time * self.samp_rate / self.vec_length)
            self.alpha = alpha
            self.state = np.zeros(self.vec_length, dtype=np.float32)
        
    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        
        # 检查参数是否发生变化
        if (self.integration_time != self.last_integration_time or 
            self.mode != self.last_mode or 
            self.samp_rate != self.last_samp_rate):
            self.reset_state()
            self.last_integration_time = self.integration_time
            self.last_mode = self.mode
            self.last_samp_rate = self.samp_rate
        
        nframes = len(in0)
        
        if self.mode == 0:
            # 更高效的移动平均实现
            for i in range(nframes):
                self.buffer[self.buffer_index] = in0[i]
                self.buffer_index = (self.buffer_index + 1) % self.n_frames
                
                if self.buffer_count < self.n_frames:
                    self.buffer_count += 1
                    # 增量更新平均值
                    if self.buffer_count == 0:
                        out[i] = in0[i]
                    else:
                        out[i] = out[i-1] + (in0[i] - out[i-1]) / self.buffer_count
                else:
                    # 缓冲区满，使用滑动窗口平均
                    out[i] = out[i-1] + (in0[i] - self.buffer[self.buffer_index]) / self.n_frames
        else:  # IIR模式
            # 使用NumPy的向量化操作
            alpha = self.alpha
            one_minus_alpha = 1.0 - alpha
            
            # 批量处理所有帧
            for i in range(nframes):
                out[i] = alpha * in0[i] + one_minus_alpha * (self.state if i == 0 else out[i-1])
            
            self.state = out[-1]  # 只更新一次状态
        
        return nframes

    def set_integration_time(self, integration_time):
        """设置积分时间"""
        self.integration_time = integration_time
        
    def set_mode(self, mode):
        """设置积分模式"""
        self.mode = mode
        
    def set_samp_rate(self, samp_rate):
        """设置采样率"""
        self.samp_rate = samp_rate