"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from collections import deque
from gnuradio import gr

class spectrum_integrator(gr.sync_block):
    """
    频谱积分器块
    输入: 浮点向量 (频谱数据)
    输出: 积分后的复数向量
    """
    def __init__(self, vec_length=1024, integration_time=1.0, samp_rate=1.0):
        gr.sync_block.__init__(
            self,
            name="Spectrum Integrator",
            in_sig=[(np.float32, vec_length)],
            out_sig=[(np.float32, vec_length)]
        )
        
        # 参数初始化
        self.vec_length = vec_length
        self.integration_time = integration_time
        self.samp_rate = samp_rate
        
        # 状态变量
        self.reset_state()
        
        # 上一次的参数值，用于检测变化
        # self.last_integration_time = integration_time
        # self.last_vec_length = vec_length
        # self.last_samp_rate = samp_rate
        
    def reset_state(self):
        """重置积分器状态"""
        # 移动平均模式：使用队列存储历史帧
        self.n_frames = max(1, int(self.integration_time * self.samp_rate / self.vec_length))
        self.buffer_queue = deque(maxlen=self.n_frames)
        self.current_sum = np.zeros(self.vec_length, dtype=np.float32)
        self.buffer_count = 0
        
    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        
        # 检查参数是否发生变化
        # if (self.integration_time != self.last_integration_time or 
        #     self.vec_length != self.last_vec_length or
        #     self.samp_rate != self.last_samp_rate):
        #     self.reset_state()
        #     self.last_integration_time = self.integration_time
        #     self.last_vec_length = self.vec_length
        #     self.last_samp_rate = self.samp_rate
        
        nframes = len(in0)
        
        # 使用队列的移动平均实现
        for i in range(nframes):
            current_frame = in0[i].copy()

            if len(current_frame) != self.vec_length:
                self.vec_length = len(current_frame)
                self.reset_state()
            
            if self.buffer_count < self.n_frames:
                # 缓冲区未满，增量添加
                self.buffer_queue.append(current_frame)
                self.current_sum += current_frame
                self.buffer_count = len(self.buffer_queue)
                out[i] = self.current_sum / self.buffer_count
            else:
                # 缓冲区已满，滑动窗口平均
                oldest_frame = self.buffer_queue.popleft()
                self.buffer_queue.append(current_frame)
                
                # 更新总和：减去最旧的帧，加上最新的帧
                self.current_sum = self.current_sum - oldest_frame + current_frame
                out[i] = self.current_sum / self.n_frames
        
        return nframes

    def set_integration_time(self, integration_time):
        """设置积分时间"""
        self.integration_time = integration_time
        self.reset_state()
        
        
    def set_samp_rate(self, samp_rate):
        """设置采样率"""
        self.samp_rate = samp_rate
        self.reset_state


    def set_vector_length(self, vec_length):
        """设置向量长度"""
        self.vec_length = vec_length
        self.reset_state()