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
        self.frame = self.view.frames["existing_simulations"]
        self._bind()

    def _bind(self) -> None:
        self.frame.simulations_listbox.bind("<<ListboxSelect>>", self._select_simulation)
        self.frame.previous_button.config(command=self._switch_start)

    def _select_simulation(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            selected_simulation = event.widget.get(index)    
            self.model.system.selected_simulation = selected_simulation
        selected_system = self.model.system.selected_system

        if selected_system != '':
            if self.model.system.selected_simulation:
                mechanical_system_simulation_path = self.model.system.mechanical_system_simulation_path
                if mechanical_system_simulation_path != '':
                    with open(mechanical_system_simulation_path, 'r') as f:
                        simulation_json = json.load(f)
                        simulation = self.model.simulation
                        simulation.mechanical_system = simulation_json['Mechanical System']
                        simulation.initial_conditions = simulation_json['Initial Conditions']
                        simulation.integration_parameters = simulation_json['Integration Parameters']
                        simulation.equations_of_motion = simulation_json['Equations of Motion']
                        simulation.output = simulation_json['Output']
                    self._update_system_characteristics(simulation)
            self._show_diagram()
            self.view.switch('system_characteristics', 'system description')

    def _switch_start(self) -> None:
        self.view.frames["start"].mechanical_systems_listbox.delete(0,tk.END)        
        self.view.switch('start', '')

    def _update_system_characteristics(self, simulation):
        system_characteristics_frame = self.view.frames['system_characteristics']
        self._clear_system_characteristics()

        self.fields = {'name': simulation.mechanical_system['Name'],
                        'dimensions' : simulation.mechanical_system['Dimensions'],
                        'particles' : simulation.mechanical_system['Particles'],
                        'degrees_of_freedom' : simulation.mechanical_system['Degrees of Freedom'],
                        'parameters' : simulation.mechanical_system['Parameters'],
                        'cartesian_coordinates' : simulation.mechanical_system['Cartesian Coordinates'],
                        'potential_energy' : simulation.mechanical_system['Potential Energy'],
                        'friction_coefficients' : simulation.mechanical_system['Friction Coefficients'],
                        'driving_force_coefficients' : simulation.mechanical_system['Driving Force Coefficients'],
                        'notes' : simulation.mechanical_system['Notes'],
                        'initial_conditions' : simulation.initial_conditions,
                        'integration_parameters' : simulation.integration_parameters}


        for field_name, field in self.fields.items():
            if field_name in ['name', 'dimensions', 'particles', 'notes']:
                system_characteristics_frame.fields[field_name].insert(tk.END, field)
            else:
                if field_name == 'degrees_of_freedom':
                    for field_item_value in field.values():
                        system_characteristics_frame.fields[field_name].insert(tk.END, field_item_value + '\n')
                else:
                    for field_item_name, field_item_value in field.items():
                        system_characteristics_frame.fields[field_name].insert(tk.END, field_item_name + '= ' + str(field_item_value) + '\n')

    def _show_diagram(self):
        # see: https://web.archive.org/web/20201111190625/http://effbot.org/pyfaq/why-do-my-tkinter-images-not-appear.htm
        # as to why a reference to the image (diagram, in this case) must be kept
        diagram = self.model.system.get_mechanical_system_diagram()
        self.view.frames['system_characteristics'].label_diagram.config(image = diagram)
        self.view.frames['system_characteristics'].label_diagram.image = diagram

    def _clear_system_characteristics(self):
        system_characteristics_frame = self.view.frames['system_characteristics']

        for field in system_characteristics_frame.fields.values():
            if type(field) == tk.Entry:
                start = 0
            elif type(field) == scrolledtext.ScrolledText:
                start = '1.0'
            else:
                print("Unknown type")
            field.delete(start, tk.END)
