import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

from . import views_constants as vc

class OutputView(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        fontsize = str(18)    
        font_parameters = vc.font + fontsize
        self.mechanical_system_label = tk.Label(self, text='system', padx=10, pady=10, font= (font_parameters))
        self.simulation_label = tk.Label(self, text='simulation', padx=10, pady=10, font= (font_parameters))

        fontsize = str(12)    
        font_parameters = vc.font + fontsize
        self.graph_type_label = tk.Label(self, text='graph type: ', padx=10, pady=10, font= (font_parameters))
        self.graph_type_combo = ttk.Combobox(self, state='readonly')
        self.x_axis_label = tk.Label(self, text='x_axis: ', padx=10, pady=10, font= (font_parameters))
        self.x_axis_combo = ttk.Combobox(self, state='readonly', exportselection=False)
        self.y_axis_label = tk.Label(self, text='y_axis: ', padx=10, pady=10, font= (font_parameters))
        self.y_axis_combo = ttk.Combobox(self, state='readonly', exportselection=False)
        self.z_axis_label = tk.Label(self, text='z_axis: ', padx=10, pady=10, font= (font_parameters))
        self.z_axis_combo = ttk.Combobox(self, state='readonly')

        self.mechanical_system_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.simulation_label.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        self.graph_type_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.graph_type_combo.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        self.x_axis_label.grid(row=1, column=2, padx=10, pady=10, sticky='e')
        self.x_axis_combo.grid(row=1, column=3, padx=10, pady=10, sticky='w')
        self.y_axis_label.grid(row=1, column=4, padx=10, pady=10, sticky='e')
        self.y_axis_combo.grid(row=1, column=5, padx=10, pady=10, sticky='w')
        self.z_axis_label.grid(row=1, column=6, padx=10, pady=10, sticky='e')
        self.z_axis_combo.grid(row=1, column=7, padx=10, pady=10, sticky='w')

        self.plot_frame = tk.Frame(self)
        self.plot_frame.grid(row = 2, column = 0, padx=10, pady=10, sticky='we', columnspan=8)

        plt.style.use(['science', 'notebook', 'grid'])
        height = self.winfo_screenheight()
        width = self.winfo_screenmmwidth()
        self.fig = Figure(figsize=(height/96, width/96), dpi=100)
        self.ax = self.fig.add_subplot()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)  
        self.canvas.get_tk_widget().pack()        

#        self.buttons_frame = tk.Frame(self)
#        self.buttons_frame.grid(row = 3, column = 0, padx=10, pady=10, sticky='we', columnspan=2)
#        self.start_button = tk.Button(self.buttons_frame, text= 'Systems', font= (font_parameters))
#        self.simulations_button = tk.Button(self.buttons_frame, text= 'Simulations', font= (font_parameters))
#        self.start_button.grid(row=0, column=0, padx=10, pady=10, sticky='wn')
#        self.simulations_button.grid(row=0, column=1, padx = 10, pady=10, sticky='wn')

#        self.close_button = tk.Button(self.buttons_frame, text = 'Close Window', font = (font_parameters))
#        self.close_button.grid(row=0, column=2, padx=10, pady=10, sticky='wn')




'''
        self.graphtype_combo.bind('<<ComboboxSelected>>', comboFunction)

    def comboFunction(self, event):
        print(self.graphtype_combo.get())
'''

'''
        fontsize = str(18)    
        font_parameters = vc.font + fontsize
        self.mechanical_system_label = tk.Label(self, padx=10, pady=10, font= (font_parameters))

        fontsize = str(12)    
        font_parameters = vc.font + fontsize
        self.create_button = tk.Button(self, text= 'Create a new simulation', font= (font_parameters))

        self.buttons_frame = tk.Frame(self)
        self.previous_button = tk.Button(self.buttons_frame,text='Previous', font=(font_parameters))

        self.mechanical_system_label.grid(row=0, column=0, padx=10, pady=10, columnspan=2 )
        self.create_button.grid(row=1, column=0, padx=10, pady=10, sticky='wn')
        self.buttons_frame.grid(row=2, column=0, padx=10, pady=10, columnspan = 2)
        self.previous_button.grid(row=0, column=0, padx = 10, pady=10)        
'''        
