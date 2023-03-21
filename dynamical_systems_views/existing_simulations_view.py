import tkinter as tk

from . import views_constants as vc

class ExistingSimulationsView(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        fontsize = str(18)    
        font_parameters = vc.font + fontsize
        self.mechanical_system_label = tk.Label(self, padx=10, pady=10, font= (font_parameters))

        fontsize = str(12)    
        font_parameters = vc.font + fontsize
        self.select_label = tk.Label(self, text= 'Select an existing simulation', font= (font_parameters))
        self.simulations_listbox = tk.Listbox(self, width=40, font= (font_parameters))
        self.buttons_frame = tk.Frame(self)
        self.previous_button = tk.Button(self.buttons_frame,text='Previous', font=(font_parameters))

        self.mechanical_system_label.grid(row=0, column=0, padx=10, pady=10, columnspan=2 )
        self.select_label.grid(row=1, column=0, padx=10, pady=10, sticky='wn')
        self.simulations_listbox.grid(row=1, column=1, padx=10, pady=10)
        self.buttons_frame.grid(row=2, column=0, padx=10, pady=10, columnspan = 2)
        self.previous_button.grid(row=0, column=0, padx = 10, pady=10)        
