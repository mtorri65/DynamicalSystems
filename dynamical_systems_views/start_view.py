import tkinter as tk

from . import views_constants as vc


class StartView(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        fontsize = str(12)    
        font_parameters = vc.font + fontsize

        self.create_new_system_button = tk.Button(self, text='Create a new system', width=20, font= (font_parameters)) 
        self.select_label = tk.Label(self, text= 'Select an existing system', font= (font_parameters))
        self.mechanical_systems_listbox = tk.Listbox(self, width=30, font= (font_parameters), exportselection=0)

        self.create_new_system_button.grid(row=0, column=0, padx=10, pady=10, sticky='wn')
        self.select_label.grid(row=1, column=0, padx=10, pady=10, sticky='wn')
        self.mechanical_systems_listbox.grid(row=1, column=1, padx=10, pady=10)
