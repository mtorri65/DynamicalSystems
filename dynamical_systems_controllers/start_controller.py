import tkinter as tk
from tkinter import scrolledtext

from dynamical_systems_models.main_model import Model
from dynamical_systems_views.main_view import View

class StartController:
    def __init__(self, model: Model, view: View) -> None:
        self.model = model
        self.view = view
        self.frame = self.view.frames['start']
        self.selected_system = ''
        self._bind()

    def _bind(self) -> None:
        self.frame.create_new_system_button.config(command = self._switch_system_characteristics)
        self.frame.mechanical_systems_listbox.bind("<<ListboxSelect>>", self._select_system)

    def _switch_system_characteristics(self) -> None:
        self.model.system.selected_system = ''
        self.view.switch('system_characteristics', 'system description')

    def _select_system(self, event):
        system = self.frame.mechanical_systems_listbox.curselection()
        if system:
            index = system[0]
            self.selected_system = event.widget.get(index)    
            self.model.system.selected_system = self.selected_system
            self._switch_next_frame(self.selected_system)

    def _switch_next_frame(self, selected_system) -> None:
        system_simulations = self.model.system.get_list_of_simulations(selected_system)
        if system_simulations:
            self.view.switch('existing_simulations', 'existing simulations')
        else:
            self.view.switch('new_simulation', 'new simulation')

    def clear_systems_list(self):
        self.frame.mechanical_systems_listbox.delete(0,tk.END)        

    def populate_systems_list(self):
        for system in self.model.system.get_list_of_systems():
            self.frame.mechanical_systems_listbox.insert('end', system)    


