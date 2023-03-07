import tkinter as tk
import json

from dynamical_systems_models.main_model import Model
from dynamical_systems_views.main_view import View

class NewSimulationController:
    def __init__(self, model: Model, view: View) -> None:
        self.model = model
        self.view = view
        self.frame = self.view.frames["new_simulation"]
        self._bind()

    def _bind(self) -> None:
        self.frame.create_button.config(command=self.switch_system_characteristics)        
        self.frame.previous_button.config(command=self.switch_start)

    def switch_start(self) -> None:
        self.view.frames['start'].mechanical_systems_listbox.delete(0, tk.END)        
        self.view.switch('start', '')

    def switch_system_characteristics(self) -> None:
        self.clear_system_characteristics() 
        self.view.switch('system_characteristics', '')

#    def show_diagram(self):
#        # see: https://web.archive.org/web/20201111190625/http://effbot.org/pyfaq/why-do-my-tkinter-images-not-appear.htm
#        # as to why a reference to the image (diagram, in this case) must be kept
#        diagram = self.model.system.get_mechanical_system_diagram()
#        self.view.frames['system_characteristics'].label_diagram.config(image = diagram)
#        self.view.frames['system_characteristics'].label_diagram.image = diagram

#    def update_system_characteristics(self, simulation):
#        system_characteristics_frame = self.view.frames['system_characteristics']
#        self.clear_system_characteristics()
#        self.selected_system = self.model.system.selected_system
#        system_characteristics_frame.name_input.insert(tk.END, self.selected_system)

    def clear_system_characteristics(self):
        system_characteristics_frame = self.view.frames['system_characteristics']

        system_characteristics_frame.name_input.delete(0, tk.END)
        system_characteristics_frame.number_dimensions_input.delete(0, tk.END)
        system_characteristics_frame.number_particles_input.delete(0, tk.END)
        system_characteristics_frame.degrees_of_freedom_input.delete('1.0', tk.END)
        system_characteristics_frame.parameters_input.delete('1.0', tk.END)
        system_characteristics_frame.cartesian_coordinates_input.delete('1.0', tk.END)
        system_characteristics_frame.potential_energy_input.delete('1.0', tk.END)
        system_characteristics_frame.friction_coefficients_input.delete('1.0', tk.END)
        system_characteristics_frame.driving_force_coefficients_input.delete('1.0', tk.END)
        system_characteristics_frame.notes_input.delete('1.0', tk.END)
        system_characteristics_frame.initial_conditions_input.delete('1.0', tk.END)
        system_characteristics_frame.integration_parameters_input.delete('1.0', tk.END)
