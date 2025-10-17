"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. All of them are required to have default values!
"""

import numpy as np
import os
import datetime
import struct
from gnuradio import gr

class stream_recorder(gr.sync_block):
    """
    时域流数据记录器
    输入: 复数或浮点流数据
    输出: 直通输入数据
    通过外部控制信号控制记录起停
    """
    
    def __init__(self, file_path="/tmp", samp_rate=1e6, max_length=32768, data_type="complex"):
        gr.sync_block.__init__(
            self,
            name="Time Domain Recorder",
            in_sig=[np.complex64 if data_type == "complex" else np.float32],
            out_sig=None
        )
        
        # 参数初始化
        self.file_path = file_path
        self.samp_rate = samp_rate
        self.max_length = max_length
        self.data_type = data_type
        
        # 状态变量
        self.recording = False
        self.current_file = None
        self.current_length = 0
        self.file_start_time = None
        self.filename = ""
        
        # 创建保存目录
        os.makedirs(self.file_path, exist_ok=True)
        
    def start_recording(self):
        """开始记录"""
        if self.recording:
            return
            
        self.recording = True
        self._create_new_file()
        print(f"开始记录: {self.filename}")
        
    def stop_recording(self):
        """停止记录"""
        if not self.recording:
            return
            
        self.recording = False
        if self.current_file:
            self.current_file.close()
            self.current_file = None
            
        # 写入文件头信息
        self._write_header_info()
        print(f"停止记录: {self.filename}")
        
    def _create_new_file(self):
        """创建新文件"""
        if self.current_file:
            self.current_file.close()
            
        # 生成唯一文件名
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        self.filename = f"td_record_{timestamp}.bin"
        file_full_path = os.path.join(self.file_path, self.filename)
        
        self.current_file = open(file_full_path, 'wb')
        self.current_length = 0
        self.file_start_time = datetime.datetime.now()
        
        # 先写入预留的文件头空间
        header_size = 256  # 预留256字节给文件头
        self.current_file.write(b'\x00' * header_size)
        
    def _write_header_info(self):
        """写入文件头信息"""
        if not self.filename:
            return
            
        file_full_path = os.path.join(self.file_path, self.filename)
        
        # 读取文件内容
        with open(file_full_path, 'rb') as f:
            data = f.read()
            
        # 构建文件头信息
        header_info = {
            'sampling_rate': self.samp_rate,
            'data_length': self.current_length,
            'data_type': self.data_type,
            'start_time': self.file_start_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
            'item_size': 8 if self.data_type == "complex" else 4  # complex64=8字节, float32=4字节
        }
        
        # 构建文件头字符串
        header_str = (
            f"GNU Radio Time Domain Recorder\n"
            f"Sampling Rate: {header_info['sampling_rate']} Hz\n"
            f"Data Length: {header_info['data_length']} samples\n"
            f"Data Type: {header_info['data_type']}\n"
            f"Start Time: {header_info['start_time']}\n"
            f"Item Size: {header_info['item_size']} bytes\n"
            f"End Header\n"
        )
        
        # 填充到256字节
        header_bytes = header_str.encode('utf-8')
        if len(header_bytes) > 256:
            header_bytes = header_bytes[:256]
        else:
            header_bytes = header_bytes.ljust(256, b'\x00')
            
        # 重新写入文件（头信息+数据）
        with open(file_full_path, 'wb') as f:
            f.write(header_bytes)
            f.write(data[256:])  # 写入原始数据（跳过最初的256字节预留空间）
            
    def work(self, input_items, output_items):
        in0 = input_items[0]
        
        n_samples = len(in0)
        
        
        # 如果正在记录，保存数据
        if self.recording and self.current_file:
            # 转换为字节并写入
            data_bytes = in0.tobytes()
            self.current_file.write(data_bytes)
            self.current_length += n_samples
            
            # 检查是否达到最大长度，需要创建新文件
            if self.current_length >= self.max_length:
                self.stop_recording()
                self.start_recording()  # 自动开始新文件记录
                
        return n_samples

    def set_recording_state(self, state):
        """设置记录状态（供外部调用）"""
        if state:
            self.start_recording()
        else:
            self.stop_recording()
            
    def set_file_path(self, file_path):
        """设置文件路径"""
        self.file_path = file_path
        os.makedirs(self.file_path, exist_ok=True)
        
    def set_samp_rate(self, samp_rate):
        """设置采样率"""
        self.samp_rate = samp_rate
        
    def set_max_length(self, max_length):
        """设置最大长度"""
        self.max_length = max_length