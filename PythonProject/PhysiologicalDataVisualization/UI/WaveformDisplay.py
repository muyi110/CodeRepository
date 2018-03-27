#此模块为波形绘制模块，将matplotlib嵌入到tkinter中
import matplotlib
matplotlib.use('TkAgg')
#from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk

class WaveformDisplay():
    def __init__(self, master=None):
        self.root = master

    def creat_waveform_eeg(self, figure):
        """创建脑波波形"""
        canvas = FigureCanvasTkAgg(figure, master=self.root)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def creat_waveform_attention_meditation(self, figure):
        """创建注意力和冥想度波形"""
        canvas = FigureCanvasTkAgg(figure, master=self.root)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=0)

    def creat_waveform_ecg(self, figure):
        """创建心电波形"""
        #self.figure = Figure(figsize=(5,4),dpi=100)
        canvas = FigureCanvasTkAgg(figure, master=self.root)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=0)

    def creat_waveform_gsr(self, figure):
        """创建皮肤电波形"""
        canvas = FigureCanvasTkAgg(figure, master=self.root)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=0)
