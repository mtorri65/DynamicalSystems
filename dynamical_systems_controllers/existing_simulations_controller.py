import tkinter as tk
from tkinter import scrolledtext
import json
from PIL import ImageTk, Image

from dynamical_systems_models.main_model import Model
from dynamical_systems_views.main_view import View

class ExistingSimulationsController:
    def __init__(self, model: Model, view: View) -> None:
        self.model = model
        self.view = view
        self.frame = self.view.frames['existing_simulations']
        self._bind()

    def _bind(self) -> None:
        self.frame.simulations_listbox.bind("<<ListboxSelect>>", self._select_simulation)
        self.frame.previous_button.config(command=self._switch_start)

    def _select_simulation(self, event):
        selection = event.widget.curselection()
        index = selection[0]
        selected_simulation = event.widget.get(index)    
        self.model.system.selected_simulation = selected_simulation

        self.model.system.set_mechanical_system_simulation_path()
        with open(self.model.system.mechanical_systems_simulation_path, 'r') as f:
            simulation_json = json.load(f)
            simulation = self.model.simulation
            simulation.mechanical_system = simulation_json['Mechanical System']
            simulation.initial_conditions = simulation_json['Initial Conditions']
            simulation.integration_parameters = simulation_json['Integration Parameters']
            simulation.equations_of_motion = simulation_json['Equations of Motion']
            simulation.output = simulation_json['Output']
        self.view.switch('system_characteristics', 'system description')

    def _switch_start(self) -> None:
        self.view.switch('start', '')

    def clear_simulations_list(self):
        self.frame.simulations_listbox.delete(0,tk.END)        

    def replace_system_label(self):
        self.frame.mechanical_system_label.config(text = self.model.system.selected_system.replace('_',' '))

    def populate_simulations_list(self):
        system_simulations = self.model.system.get_list_of_simulations(self.model.system.selected_system)
        for simulation in system_simulations:
            self.frame.simulations_listbox.insert('end', simulation)

