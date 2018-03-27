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
        self.canvas_eeg = None
        self.canvas_raweeg = None
        self.canvas_ecg = None
        self.canvas_gsr = None

    def creat_waveform_eeg(self, figure):
        """创建脑波波形"""
        self.canvas_eeg = FigureCanvasTkAgg(figure, master=self.root)
        self.canvas_eeg.show()
        self.canvas_eeg.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def creat_waveform_attention_meditation(self, figure):
        """创建注意力和冥想度波形"""
        self.canvas_raweeg = FigureCanvasTkAgg(figure, master=self.root)
        self.canvas_raweeg.show()
        self.canvas_raweeg.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=0)

    def creat_waveform_ecg(self, figure):
        """创建心电波形"""
        self.canvas_ecg = FigureCanvasTkAgg(figure, master=self.root)
        self.canvas_ecg.show()
        self.canvas_ecg.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=0)

    def creat_waveform_gsr(self, figure):
        """创建皮肤电波形"""
        self.canvas_gsr = FigureCanvasTkAgg(figure, master=self.root)
        self.canvas_gsr.show()
        self.canvas_gsr.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=0)
