import tkinter as tk

from . import views_constants as vc


class StartView(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        '''        
        self.grid_columnconfigure(0, weight=1)

        self.header = Label(self, text="Home")
        self.header.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.greeting = Label(self, text="")
        self.greeting.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.signout_btn = Button(self, text="Sign Out")
        self.signout_btn.grid(row=2, column=0, padx=10, pady=10)
        '''
#        global mechanical_system_library_path
#        global mechanical_system_path

        fontsize = str(12)    
        font_parameters = vc.font + fontsize

        self.create_new_system_button = tk.Button(self, text="Create a new system", width=20, font= (font_parameters)) 
        self.create_new_system_button.grid(row=0, column=0, padx=10, pady=10, sticky='wn')
        select_label = tk.Label(self, text= "Select an existing system", font= (font_parameters)).grid(row=1, column=0, padx=10, pady=10, sticky='wn')

        # scan the Mechanical System Library to find out which systems are available and populate the list box
#        systems = [ f.name for f in os.scandir(mechanical_system_library_path) if f.is_dir() ]
        self.mechanical_systems_listbox = tk.Listbox(self, width=30, font= (font_parameters))
        self.mechanical_systems_listbox.grid(row=1, column=1, padx=10, pady=10)
#        for system in systems:
#            self.mechanical_systems_listbox.insert('end', system)
        
        # by clicking on an item in the listbox will trigger moving to the next pages
#        self.mechanical_systems_listbox.bind("<<ListboxSelect>>", self.select_item)
