import tkinter as tk

from . import views_constants as vc

class NewSimulationView(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        fontsize = str(18)    
        font_parameters = vc.font + fontsize
        self.mechanical_system_label = tk.Label(self, padx=10, pady=10, font= (font_parameters))
        self.mechanical_system_label.grid(row=0, column=0, padx=10, pady=10, columnspan=2 )

        fontsize = str(12)    
        font_parameters = vc.font + fontsize
        self.create_button = tk.Button(self, text= "Create a new simulation", font= (font_parameters))
        self.create_button.grid(row=1, column=0, padx=10, pady=10, sticky='wn')

        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.grid(row=2, column=0, padx=10, pady=10, columnspan = 2)
        self.previous_button = tk.Button(self.buttons_frame,text='Previous', font=(font_parameters))
        self.previous_button.grid(row=0, column=0, padx = 10, pady=10)        
