#界面主体框架模块#
import tkinter.ttk as ttk
import tkinter.font as tkFont
import tkinter as tk
import datetime
import threading

try:
    from UI import PyTkinter as pytk
except ImportError:
    import PyTkinter as pytk
g_font = ("Monaco", 16)

class MainFrame():
    """main frame"""
    def __init__(self, master=None):
        self.root = master
        self.create_frame()
        #self.state = True

    def create_frame(self):
        self.tabcontrol = ttk.Notebook(self.root)
        self.tabcontrol.pack(fill="both",expand=1)
        self.eeg_tab = pytk.PyFrame(self.tabcontrol) #脑电
        self.ecg_tab = pytk.PyFrame(self.tabcontrol) #心电
        self.gsr_tab = pytk.PyFrame(self.tabcontrol) #皮肤电
        self.tabcontrol.add(self.eeg_tab, text="脑电信号可视化")
        self.tabcontrol.add(self.ecg_tab, text="心电信号可视化")
        self.tabcontrol.add(self.gsr_tab, text="皮肤电信号可视化")
        self.tabcontrol.select(self.eeg_tab)
        #将每种数据的tab页分成左右两个部分，左边是设置及状态
        #右边是对应数据波形
        self.creat_eeg_frame()
        self.creat_ecg_frame()
        self.creat_gsr_frame()

    def creat_eeg_frame(self):
        """脑电tab"""
        self.eeg_frame_left = pytk.PyLabelFrame(self.eeg_tab) #左部分
        self.eeg_frame_right = pytk.PyLabelFrame(self.eeg_tab)#右部分
        self.eeg_frame_left.pack(fill="both", expand=0, padx=2, pady=5, side=tk.LEFT)
        self.eeg_frame_right.pack(fill="both", expand=1, padx=2, pady=5, side=tk.RIGHT)
        #左部分分成上下两个部分
        self.eeg_frame_left_top = pytk.PyLabelFrame(self.eeg_frame_left)
        self.eeg_frame_left_under = pytk.PyLabelFrame(self.eeg_frame_left)
        self.eeg_frame_left_top.pack(fill="both", expand=0)
        self.eeg_frame_left_under.pack(fill="both",expand=1)
        self.creat_eeg_frame_left_top()
        self.creat_eeg_frame_left_under()
        self.creat_eeg_frame_right()  #创建脑波Tab右边

    def creat_eeg_frame_right(self):
        self.eeg_frame_right_top = pytk.PyLabelFrame(self.eeg_frame_right)
        self.eeg_frame_right_under = pytk.PyLabelFrame(self.eeg_frame_right)
        self.eeg_frame_right_top.pack(fill="both", expand=1)
        self.eeg_frame_right_under.pack(fill="both",expand=0)

        self.eight_eeg = pytk.PyCanvas(self.eeg_frame_right_top)
        self.attention_mentation = pytk.PyCanvas(self.eeg_frame_right_under)
        self.eight_eeg.grid(row=0, column=0, padx=5, pady=5, sticky="wesn")
        self.attention_mentation.grid(row=0, column=0, padx=5, pady=5, sticky="wesn")

    def creat_eeg_frame_left_top(self):        

        self.eeg_frm_l_label = pytk.PyLabel(self.eeg_frame_left_top,
                                            text="Serial Ports",
                                            font=g_font,
                                            anchor="w")
        self.eeg_frm_l_listbox = pytk.PyListbox(self.eeg_frame_left_top,
                                                font=g_font)
        self.eeg_left_serial_set = pytk.PyLabelFrame(self.eeg_frame_left_top)
        self.eeg_left_btn = pytk.PyButton(self.eeg_frame_left_top,
                                          text = "Open",
                                          font=g_font,
                                          command=self.Toggle)

        self.eeg_frm_l_label.pack(fill="both",expand=0,padx=5,pady=5)
        self.eeg_frm_l_listbox.pack(fill="both",expand=1,padx=5,pady=5)
        self.eeg_left_serial_set.pack(fill="both",expand=0,padx=5,pady=5)
        self.eeg_left_btn.pack(fill="both",expand=0,padx=5,pady=10)
        self.eeg_frm_l_listbox.bind("<Double-Button-1>", self.open)

        eeg_baudrate_list = ["9600", "38400", "57600", "115200"]

        self.eeg_frm_left_left = pytk.PyFrame(self.eeg_left_serial_set)  #左边区域显示标签
        self.eeg_frm_left_right = pytk.PyFrame(self.eeg_left_serial_set) #右边区域显示波特率
        self.eeg_frm_left_left.pack(fill="both", expand=1, side=tk.LEFT)
        self.eeg_frm_left_right.pack(fill="both", expand=1, side=tk.RIGHT)

        self.eeg_frm_left_label_temp = pytk.PyLabel(self.eeg_frm_left_left, 
                                               text="Baudrate:",
                                               font=g_font)
        self.eeg_frm_left_label_temp.pack(fill="both", expand=1, padx=5, pady=5)

        self.eeg_frm_left_combobox_baudrate = ttk.Combobox(self.eeg_frm_left_right,
                                                       width=10,
                                                       font=g_font,
                                                       values=eeg_baudrate_list)
        self.eeg_frm_left_combobox_baudrate.pack(fill="both", expand=1, padx=5, pady=5)
        self.eeg_frm_left_combobox_baudrate.current(2)

    def creat_eeg_frame_left_under(self):
        self.eeg_status_label = pytk.PyLabel(self.eeg_frame_left_under,
                                             text="Ready",
                                             font=g_font)
        self.eeg_status_label.grid(row=0, column=0, padx=5, pady=5, sticky="wesn")

    def creat_ecg_frame(self):
        """心电tab"""
        self.ecg_frame_left = pytk.PyLabelFrame(self.ecg_tab)
        self.ecg_frame_right = pytk.PyLabelFrame(self.ecg_tab)
        self.ecg_frame_left.pack(fill="both", expand=0, padx=2, pady=5, side=tk.LEFT)
        self.ecg_frame_right.pack(fill="both", expand=1, padx=2, pady=5, side=tk.RIGHT)
        #左部分分成上下两个部分
        self.ecg_frame_left_top = pytk.PyLabelFrame(self.ecg_frame_left)
        self.ecg_frame_left_under = pytk.PyLabelFrame(self.ecg_frame_left)
        self.ecg_frame_left_top.pack(fill="both", expand=0)
        self.ecg_frame_left_under.pack(fill="both",expand=1)
        self.creat_ecg_frame_left_top()
        self.creat_ecg_frame_left_under()
        self.creat_ecg_frame_right()

    def creat_ecg_frame_right(self):
        self.ecg_wave = pytk.PyCanvas(self.ecg_frame_right)
        self.ecg_wave.grid(row=0, column=0, padx=5, pady=5, sticky="wesn")

    def creat_ecg_frame_left_top(self):
        self.ecg_frm_l_label = pytk.PyLabel(self.ecg_frame_left_top,
                                            text="Serial Ports",
                                            font=g_font,
                                            anchor="w")
        self.ecg_frm_l_listbox = pytk.PyListbox(self.ecg_frame_left_top,
                                                font=g_font)
        self.ecg_left_serial_set = pytk.PyLabelFrame(self.ecg_frame_left_top)
        self.ecg_left_btn = pytk.PyButton(self.ecg_frame_left_top,
                                          text = "Open",
                                          font=g_font,
                                          command=self.Toggle)

        self.ecg_frm_l_label.pack(fill="both",expand=0,padx=5,pady=5)
        self.ecg_frm_l_listbox.pack(fill="both",expand=1,padx=5,pady=5)
        self.ecg_left_serial_set.pack(fill="both",expand=0,padx=5,pady=5)
        self.ecg_left_btn.pack(fill="both",expand=0,padx=5,pady=5)
        self.ecg_frm_l_listbox.bind("<Double-Button-1>", self.open)

        ecg_baudrate_list = ["9600", "38400", "57600", "115200"]

        self.ecg_frm_left_left = pytk.PyFrame(self.ecg_left_serial_set)  #左边区域显示标签
        self.ecg_frm_left_right = pytk.PyFrame(self.ecg_left_serial_set) #右边区域显示波特率
        self.ecg_frm_left_left.pack(fill="both", expand=1, side=tk.LEFT)
        self.ecg_frm_left_right.pack(fill="both", expand=1, side=tk.RIGHT)

        self.ecg_frm_left_label_temp = pytk.PyLabel(self.ecg_frm_left_left, 
                                               text="Baudrate:",
                                               font=g_font)
        self.ecg_frm_left_label_temp.pack(fill="both", expand=1, padx=5, pady=5)

        self.ecg_frm_left_combobox_baudrate = ttk.Combobox(self.ecg_frm_left_right,
                                                       width=10,
                                                       font=g_font,
                                                       values=ecg_baudrate_list)
        self.ecg_frm_left_combobox_baudrate.pack(fill="both", expand=1, padx=5, pady=5)
        self.ecg_frm_left_combobox_baudrate.current(2)

    def creat_ecg_frame_left_under(self):
        self.ecg_status_label = pytk.PyLabel(self.ecg_frame_left_under,
                                             text="Ready",
                                             font=g_font)
        self.ecg_status_label.grid(row=0, column=0, padx=5, pady=5, sticky="wesn")


    def creat_gsr_frame(self):
        """皮肤电tab"""
        self.gsr_frame_left = pytk.PyLabelFrame(self.gsr_tab)
        self.gsr_frame_right = pytk.PyLabelFrame(self.gsr_tab)
        self.gsr_frame_left.pack(fill="both", expand=0, padx=2, pady=5, side=tk.LEFT)
        self.gsr_frame_right.pack(fill="both", expand=1, padx=2, pady=5, side=tk.RIGHT)
        #左部分分成上下两个部分
        self.gsr_frame_left_top = pytk.PyLabelFrame(self.gsr_frame_left)
        self.gsr_frame_left_under = pytk.PyLabelFrame(self.gsr_frame_left)
        self.gsr_frame_left_top.pack(fill="both", expand=0)
        self.gsr_frame_left_under.pack(fill="both",expand=1)
        self.creat_gsr_frame_left_top()
        self.creat_gsr_frame_left_under()
        self.creat_gsr_frame_right()

    def creat_gsr_frame_right(self):
        self.gsr_wave = pytk.PyCanvas(self.gsr_frame_right)
        self.gsr_wave.grid(row=0, column=0, padx=5, pady=5, sticky="wesn")

    def creat_gsr_frame_left_top(self):
        self.gsr_frm_l_label = pytk.PyLabel(self.gsr_frame_left_top,
                                            text="Serial Ports",
                                            font=g_font,
                                            anchor="w")
        self.gsr_frm_l_listbox = pytk.PyListbox(self.gsr_frame_left_top,
                                                font=g_font)
        self.gsr_left_serial_set = pytk.PyLabelFrame(self.gsr_frame_left_top)
        self.gsr_left_btn = pytk.PyButton(self.gsr_frame_left_top,
                                          text = "Open",
                                          font=g_font,
                                          command=self.Toggle)

        self.gsr_frm_l_label.pack(fill="both",expand=0,padx=5,pady=5)
        self.gsr_frm_l_listbox.pack(fill="both",expand=1,padx=5,pady=5)
        self.gsr_left_serial_set.pack(fill="both",expand=0,padx=5,pady=5)
        self.gsr_left_btn.pack(fill="both",expand=0,padx=5,pady=5)
        self.gsr_frm_l_listbox.bind("<Double-Button-1>", self.open)

        gsr_baudrate_list = ["9600", "38400", "57600", "115200"]

        self.gsr_frm_left_left = pytk.PyFrame(self.gsr_left_serial_set)  #左边区域显示标签
        self.gsr_frm_left_right = pytk.PyFrame(self.gsr_left_serial_set) #右边区域显示波特率
        self.gsr_frm_left_left.pack(fill="both", expand=1, side=tk.LEFT)
        self.gsr_frm_left_right.pack(fill="both", expand=1, side=tk.RIGHT)

        self.gsr_frm_left_label_temp = pytk.PyLabel(self.gsr_frm_left_left, 
                                               text="Baudrate:",
                                               font=g_font)
        self.gsr_frm_left_label_temp.pack(fill="both", expand=1, padx=5, pady=5)

        self.gsr_frm_left_combobox_baudrate = ttk.Combobox(self.gsr_frm_left_right,
                                                       width=10,
                                                       font=g_font,
                                                       values=gsr_baudrate_list)
        self.gsr_frm_left_combobox_baudrate.pack(fill="both", expand=1, padx=5, pady=5)
        self.gsr_frm_left_combobox_baudrate.current(2)

    def creat_gsr_frame_left_under(self):
        self.gsr_status_label = pytk.PyLabel(self.gsr_frame_left_under,
                                             text="Ready",
                                             font=g_font)
        self.gsr_status_label.grid(row=0, column=0, padx=5, pady=5, sticky="wesn")

    def open(self, event):
        pass

    def Toggle(self, event):
        pass

#下面为此模块测试代码
if __name__ == '__main__':
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.geometry()
    MainFrame(root)

    root.mainloop()


