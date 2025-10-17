#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import argparse
import os
from matplotlib.ticker import EngFormatter

def read_spectrum_data(filename, fft_size=1024, dtype=np.float32):
    """
    读取GNU Radio File Sink保存的频谱数据
    
    参数:
        filename: 输入文件名
        fft_size: FFT长度
        dtype: 数据类型 (默认float32)
    
    返回:
        numpy数组包含频谱数据
    """
    try:
        # 读取二进制文件
        data = np.fromfile(filename, dtype=dtype)
        
        # 检查数据长度是否匹配FFT大小
        if len(data) % fft_size != 0:
            print(f"警告: 数据长度({len(data)})不是FFT大小({fft_size})的整数倍")
            print(f"将截断数据以适应FFT大小")
            data = data[:len(data)//fft_size * fft_size]
        
        # 重塑数据为二维数组 [帧数, FFT大小]
        frames = len(data) // fft_size
        spectrum_data = data.reshape((frames, fft_size))
        
        return spectrum_data
    
    except FileNotFoundError:
        print(f"错误: 文件 '{filename}' 未找到")
        return None
    except Exception as e:
        print(f"读取文件时发生错误: {e}")
        return None

def plot_spectrum(spectrum_data, sample_rate=3e6, center_freq=1420.4e6, 
                 fft_size=1024, db_range=80, avg_frames=None, output_file=None):
    """
    绘制频谱图
    
    参数:
        spectrum_data: 频谱数据数组
        sample_rate: 采样率 (Hz)
        center_freq: 中心频率 (Hz)
        fft_size: FFT长度
        db_range: 显示的动态范围 (dB)
        avg_frames: 平均的帧数 (None表示所有帧平均)
        output_file: 输出图像文件名
    """
    if spectrum_data is None or len(spectrum_data) == 0:
        print("错误: 无有效数据可绘制")
        return
    
    # 计算频率轴
    freq_resolution = sample_rate / fft_size
    freq_axis = np.fft.fftshift(np.fft.fftfreq(fft_size, 1/sample_rate)) + center_freq
    
    # 处理数据：转换为dB尺度并平均
    if avg_frames is None:
        # 平均所有帧
        avg_spectrum = np.mean(spectrum_data, axis=0)
    else:
        # 平均指定数量的帧
        avg_spectrum = np.mean(spectrum_data[:min(avg_frames, len(spectrum_data))], axis=0)
    
    # 转换为dB尺度
    avg_spectrum_db = 10 * np.log10(avg_spectrum + 1e-12)  # 加上小值避免log10(0)
    
    # 应用FFT移位以正确显示频率
    avg_spectrum_db_shifted = np.fft.fftshift(avg_spectrum_db)
    
    # 设置动态范围
    max_power = np.max(avg_spectrum_db_shifted)
    min_power = max_power - db_range
    
    # 创建图形
    plt.figure(figsize=(12, 8))
    
    # 绘制频谱
    plt.plot(freq_axis / 1e6, avg_spectrum_db_shifted, linewidth=1)
    plt.ylim(min_power, max_power)
    
    # 设置标签和标题
    plt.xlabel('频率 (MHz)')
    plt.ylabel('功率 (dB)')
    plt.title(f'频谱图 - 中心频率: {center_freq/1e6:.1f} MHz, 采样率: {sample_rate/1e6:.1f} MS/s')
    plt.grid(True, alpha=0.3)
    
    # 使用工程格式器美化频率轴
    formatter = EngFormatter(unit='Hz')
    plt.gca().xaxis.set_major_formatter(formatter)
    
    # 添加文本信息
    info_text = f'FFT长度: {fft_size}\n频率分辨率: {freq_resolution/1e3:.2f} kHz\n帧数: {len(spectrum_data)}'
    plt.text(0.02, 0.98, info_text, transform=plt.gca().transAxes, 
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    
    # 保存或显示图像
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"图像已保存到: {output_file}")
    
    plt.show()

def main():
    parser = argparse.ArgumentParser(description='绘制GNU Radio File Sink保存的频谱数据')
    parser.add_argument('filename', help='输入文件名')
    parser.add_argument('--fft-size', type=int, default=1024, help='FFT长度 (默认: 1024)')
    parser.add_argument('--sample-rate', type=float, default=3e6, help='采样率 (Hz) (默认: 3e6)')
    parser.add_argument('--center-freq', type=float, default=1420.4e6, help='中心频率 (Hz) (默认: 1420.4e6)')
    parser.add_argument('--db-range', type=int, default=80, help='显示的动态范围 (dB) (默认: 80)')
    parser.add_argument('--avg-frames', type=int, default=None, help='平均的帧数 (默认: 所有帧)')
    parser.add_argument('--output', '-o', help='输出图像文件名')
    
    args = parser.parse_args()
    
    # 检查文件是否存在
    if not os.path.exists(args.filename):
        print(f"错误: 文件 '{args.filename}' 不存在")
        return
    
    # 读取数据
    print(f"正在读取文件: {args.filename}")
    spectrum_data = read_spectrum_data(args.filename, args.fft_size)
    
    if spectrum_data is not None:
        print(f"成功读取 {len(spectrum_data)} 帧数据, 每帧 {args.fft_size} 个点")
        print(f"总数据点: {len(spectrum_data) * args.fft_size}")
        
        # 绘制频谱
        plot_spectrum(spectrum_data, args.sample_rate, args.center_freq, 
                     args.fft_size, args.db_range, args.avg_frames, args.output)

if __name__ == "__main__":
    main()