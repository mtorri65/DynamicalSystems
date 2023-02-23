import tkinter as tk

from . import views_constants as vc

class ExistingSimulationsView(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

#        global mechanical_system_library_path
#        global mechanical_system_path

#        master.title(title + ' - existing simulations')

#        mechanical_system_path = mechanical_system_library_path + system + '\\'
#        self.mechanical_system_characteristics_file = mechanical_system_path + 'mechanical_system_characteristics.txt'

        fontsize = str(18)    
        font_parameters = vc.font + fontsize
        self.mechanical_system_label = tk.Label(self, padx=10, pady=10, font= (font_parameters))
        self.mechanical_system_label.grid(row=0, column=0, padx=10, pady=10, columnspan=2 )

        fontsize = str(12)    
        font_parameters = vc.font + fontsize
        self.select_label = tk.Label(self, text= "Select an existing simulation", font= (font_parameters))
        self.select_label.grid(row=1, column=0, padx=10, pady=10, sticky='wn')

        self.create_button = tk.Button(self, text= "Create a new simulation", font= (font_parameters))
        self.create_button.grid(row=1, column=0, padx=10, pady=10, sticky='wn')
#        self.create_button.grid_forget()

        self.simulations_listbox = tk.Listbox(self, width=40, font= (font_parameters))
        self.simulations_listbox.grid(row=1, column=1, padx=10, pady=10)
        '''
        for file in os.listdir(mechanical_system_path + 'simulations\\'):
            if os.path.isfile(os.path.join(mechanical_system_path + 'simulations\\', file)) and os.path.splitext(file)[-1].lower() == '.json':
                self.simulations_listbox.insert('end', file)
        '''
        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.grid(row=2, column=0, padx=10, pady=10, columnspan = 2)
#        self.home_button = tk.Button(self.buttons_frame,text='Previous', font=(font_parameters), command = self.go_home)
        self.previous_button = tk.Button(self.buttons_frame,text='Previous', font=(font_parameters))
        self.previous_button.grid(row=0, column=0, padx = 10, pady=10)        
