"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QFileDialog
from gnuradio import gr
import os

class save_spectrum_image(gr.sync_block):
    """
    Block to save spectrum image when triggered by a Qt GUI Push Button.
    """
    def __init__(self, vec_length=1024, x_axis_start_value=0, x_axis_step_value=1,
                 x_axis_label="Frequency", y_axis_label="Magnitude",
                 x_axis_units="Hz", y_axis_units="dB",
                 y_min=-120, y_max=0):
        gr.sync_block.__init__(
            self,
            name="Save Spectrum Image",
            in_sig=[np.float32],
            out_sig=None
        )
        
        self.vec_length = vec_length
        self.x_axis_start_value = x_axis_start_value
        self.x_axis_step_value = x_axis_step_value
        self.x_axis_label = x_axis_label
        self.y_axis_label = y_axis_label
        self.x_axis_units = x_axis_units
        self.y_axis_units = y_axis_units
        self.y_min = y_min
        self.y_max = y_max
        
        self.message_port_register_in(gr.pmt.intern("save"))
        self.set_msg_handler(gr.pmt.intern("save"), self.handle_save_msg)
        
        self.data_buffer = np.zeros(vec_length)
        self.buffer_ready = False
        
    def work(self, input_items, output_items):
        in_data = input_items[0]
        
        # Only store the most recent data
        if len(in_data) >= self.vec_length:
            self.data_buffer = in_data[-self.vec_length:]
            self.buffer_ready = True
        elif len(in_data) > 0:
            # Handle case where we get partial data (shouldn't happen with sync block)
            self.data_buffer = np.roll(self.data_buffer, -len(in_data))
            self.data_buffer[-len(in_data):] = in_data
            self.buffer_ready = True
            
        return len(input_items[0])
    
    def handle_save_msg(self, msg):
        if not self.buffer_ready:
            print("No data available to save yet.")
            return
            
        # Get save path from user
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            None,
            "Save Spectrum Image",
            "",
            "PNG Files (*.png);;All Files (*)",
            options=options
        )
        
        if not file_path:
            return  # User cancelled
            
        # Add .png extension if not present
        if not file_path.lower().endswith('.png'):
            file_path += '.png'
            
        # Generate x-axis values
        x_values = np.arange(
            self.x_axis_start_value,
            self.x_axis_start_value + self.vec_length * self.x_axis_step_value,
            self.x_axis_step_value
        )
        
        # Create and save plot
        plt.figure(figsize=(10, 6))
        plt.plot(x_values, self.data_buffer)
        plt.xlabel(f"{self.x_axis_label} ({self.x_axis_units})")
        plt.ylabel(f"{self.y_axis_label} ({self.y_axis_units})")
        plt.title("Spectrum")
        plt.grid(True)
        
        # Set axis limits if specified
        if self.y_min is not None:
            plt.ylim(bottom=self.y_min)
        if self.y_max is not None:
            plt.ylim(top=self.y_max)
            
        plt.tight_layout()
        plt.savefig(file_path, dpi=300)
        plt.close()
        
        print(f"Spectrum image saved to: {file_path}")