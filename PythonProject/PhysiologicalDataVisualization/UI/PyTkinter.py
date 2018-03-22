#tkinter控件设置模块#
try:
    import Tkinter as tk
    import Tkinter.ttk as ttk
except ImportError:
    import tkinter as tk
    import tkinter.ttk as ttk

g_default_theme = "dark"

class PyButton(tk.Button):
    """Button"""
    def __init__(self, master, theme=g_default_theme, **kw):
        self.theme = theme
        self.kw = kw
        self.temp = dict()
        self.choose_theme()
        super().__init__(master, self.temp)

    def choose_theme(self):
        if self.theme == "dark":
            dark_theme_dict = {
                                "activebackground": "#00B2EE",
                                "activeforeground": "#E0EEEE",
                                "bg": "#008B8B",
                                "fg": "#FFFFFF"
                              }
            for key, value in dark_theme_dict.items():
                self.temp[key] = value
        for key, value in self.kw.items():
            self.temp[key] = value

class PyLabel(tk.Label):
    '''
    Label
    '''
    def __init__(self, master, theme=g_default_theme, **kw):
        self.theme = theme
        self.kw = kw
        self.temp = dict()
        self.choose_theme()
        super().__init__(master, self.temp)

    def choose_theme(self):
        if self.theme == "dark":
            dark_theme_dict = {
                                "bg": "#292929",
                                "fg": "#E0EEEE"
                              }
            for key,value in dark_theme_dict.items():
                self.temp[key] = value

        for key,value in self.kw.items():
            self.temp[key] = value

class PyFrame(tk.Frame):
    '''
    Frame
    '''
    def __init__(self, master, theme=g_default_theme, **kw):
        self.theme = theme
        self.kw = kw
        self.temp = dict()
        self.choose_theme()
        super().__init__(master, self.temp)

    def choose_theme(self):
        if self.theme == "dark":
            dark_theme_dict = {
                                "bg": "#292929"
                              }
            for key,value in dark_theme_dict.items():
                self.temp[key] = value

        for key,value in self.kw.items():
            self.temp[key] = value

class PyListbox(tk.Listbox):
    '''
    Listbox
    '''
    def __init__(self, master, theme=g_default_theme, **kw):
        self.theme = theme
        self.kw = kw
        self.temp = dict()
        self.choose_theme()
        super().__init__(master, self.temp)

    def choose_theme(self):
        if self.theme == "dark":
            dark_theme_dict = {
                                "bg": "#292929",
                                "fg": "#1E90FF",
                                "selectbackground": "#00B2EE"
                              }
            for key,value in dark_theme_dict.items():
                self.temp[key] = value

        for key,value in self.kw.items():
            self.temp[key] = value

class PyLabelFrame(tk.LabelFrame):
    '''
    LabelFrame
    '''
    def __init__(self, master, theme=g_default_theme, **kw):  #kw是一个空字典
        self.theme = theme
        self.kw = kw
        self.temp = dict()
        self.choose_theme()
        super().__init__(master, self.temp)

    def choose_theme(self):
        if self.theme == "dark":
            dark_theme_dict = {
                                "bg": "#292929",
                                "fg": "#1E90FF"
                              }
            for key,value in dark_theme_dict.items():
                self.temp[key] = value
        
        for key,value in self.kw.items():
            self.temp[key] = value

class PyCanvas(tk.Canvas):
    '''
    Canvas
    '''
    def __init__(self, master, theme=g_default_theme, **kw):
        self.theme = theme
        self.kw = kw
        self.temp = dict()
        self.choose_theme()
        super().__init__(master, self.temp)

    def choose_theme(self):
        if self.theme == "dark":
            dark_theme_dict = {
                                "bg": "lightgrey",
                                "height": 500,
                                "width": 700
                              }
            for key,value in dark_theme_dict.items():
                self.temp[key] = value

        for key,value in self.kw.items():
            self.temp[key] = value

#下面是此模块的测试部分#

if __name__ == "__main__":
    import PyTkinter as pytk
    import tkinter as tk

    root = tk.Tk()
    root.configure(bg = "#292929")
    root.title("Tkinter Test UI")
    root.geometry("1080x600")
    tabcontrol = ttk.Notebook(root)
    tab1 = pytk.PyFrame(tabcontrol)
    tab2 = pytk.PyFrame(tabcontrol)
    tabcontrol.add(tab1,text="tab1")
    tabcontrol.add(tab2, text="tab2")
    tabcontrol.pack(expand=1,fill = "both")
    pytk.PyButton(tab1, text="Button1", font=("Monaco",12)).grid(column=0,row=0,padx=10,pady=10)
    pytk.PyButton(tab2, text="Button2").grid(column=0,row=0,padx=100,pady=50)
    tabcontrol.select(tab2)

    root.mainloop()
