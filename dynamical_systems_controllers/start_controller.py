import tkinter as tk
from tkinter import scrolledtext

from dynamical_systems_models.main_model import Model
from dynamical_systems_views.main_view import View

class StartController:
    def __init__(self, model: Model, view: View) -> None:
        self.model = model
        self.view = view
        self.frame_start = self.view.frames['start']
        self.frame_existing_simulation = self.view.frames['existing_simulations']
        self.frame_characteristics = self.view.frames['system_characteristics']
        self.frame_new_simulation = self.view.frames['new_simulation']
        self.selected_system = ''
        self._bind()

    def _bind(self) -> None:
        self.frame_start.create_new_system_button.config(command = self._switch_system_characteristics)
        self.frame_start.mechanical_systems_listbox.bind("<<ListboxSelect>>", self._select_system)

    def _switch_system_characteristics(self) -> None:
        self.model.system.selected_system = ''
        self._clear_system_characteristics()
        self.view.switch('system_characteristics', 'system description')

    def _select_system(self, event):
        system = self.frame_start.mechanical_systems_listbox.curselection()
        if system:
            index = system[0]
            self.selected_system = event.widget.get(index)    
            self.model.system.selected_system = self.selected_system
            self._switch_next_frame(self.selected_system)

    def _clear_system_characteristics(self):
        for field in self.frame_characteristics.fields.values():
            if type(field) == tk.Entry:
                start = 0
            elif type(field) == scrolledtext.ScrolledText:
                start = '1.0'
            else:
                print("Unknown type")
            field.delete(start, tk.END)

    def _switch_next_frame(self, selected_system) -> None:
        system_simulations = self.model.system.get_list_of_simulations(selected_system)
        if system_simulations:
            self.frame_existing_simulation.simulations_listbox.delete(0, tk.END)
            self.frame_existing_simulation.mechanical_system_label.config(text = '')
            self.view.switch('existing_simulations', 'existing simulations')
        else:
            self.frame_start.mechanical_systems_listbox.delete(0, tk.END)        
            self.frame_new_simulation.mechanical_system_label.config(text = '')
            self.view.switch('new_simulation', 'new simulation')

