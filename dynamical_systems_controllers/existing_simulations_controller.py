import tkinter as tk
import json
from PIL import ImageTk, Image


from models.main_model import Model
from models.auth_model import User
from views.main import View


class ExistingSimulationsController:
    def __init__(self, model: Model, view: View) -> None:
        self.model = model
        self.view = view
        self.frame = self.view.frames["existing_simulations"]
#        self.selection = self.model.system.selected_system
        self._bind()

    def _bind(self) -> None:
        self.frame.simulations_listbox.bind("<<ListboxSelect>>", self._select_simulation)
        self.frame.previous_button.config(command=self.switch_start)

    def update_view(self):
        selected_system = self.model.system.selected_system
        self.frame.mechanical_system_label.config(text=selected_system.replace('_',' '))

    def _update_list_of_systems(self):
        self.view.frames["start"].mechanical_systems_listbox.delete(0,tk.END)        
        systems_list = self.model.system.get_list_of_systems()
        for system in systems_list:
            self.view.frames["start"].mechanical_systems_listbox.insert('end', system)

    def switch_start(self) -> None:
        self._update_list_of_systems()
        self.view.switch('start', '')

    def _select_simulation(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            selected_simulation = event.widget.get(index)    
            self.model.system.selected_simulation = selected_simulation
        else:
            self.model.system.selected_simulation = ''

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

                    self.show_diagram()
                    self.update_system_characteristics(simulation)

                self.view.switch('system_characteristics', 'system description')

    def show_diagram(self):
        # see: https://web.archive.org/web/20201111190625/http://effbot.org/pyfaq/why-do-my-tkinter-images-not-appear.htm
        # as to why a reference to the image (diagram, in this case) must be kept
        diagram = self.model.system.get_mechanical_system_diagram()
        self.view.frames['system_characteristics'].label_diagram.config(image = diagram)
        self.view.frames['system_characteristics'].label_diagram.image = diagram

    def update_system_characteristics(self, simulation):
        system_characteristics_frame = self.view.frames['system_characteristics']

        self.clear_system_characteristics()

        system_characteristics_frame.name_input.insert(tk.END, simulation.mechanical_system['Name'])
        system_characteristics_frame.number_dimensions_input.insert(tk.END, simulation.mechanical_system['Dimensions'])
        system_characteristics_frame.number_particles_input.insert(tk.END, simulation.mechanical_system['Particles'])
        for degree_of_freedom in simulation.mechanical_system['Degrees of Freedom'].values():
            system_characteristics_frame.degrees_of_freedom_input.insert(tk.END, degree_of_freedom + '\n')
        for parameter_name, parameter_value in simulation.mechanical_system['Parameters'].items():
            system_characteristics_frame.parameters_input.insert(tk.END, parameter_name + '= ' + str(parameter_value) + '\n')
        for cartesian_coordinate_name, cartesian_coordinate_value in simulation.mechanical_system['Cartesian Coordinates'].items():
            system_characteristics_frame.cartesian_coordinates_input.insert(tk.END, cartesian_coordinate_name + '= ' + cartesian_coordinate_value + '\n')
        for potential_energy_name, potential_energy_value in simulation.mechanical_system['Potential Energy'].items():
            system_characteristics_frame.potential_energy_input.insert(tk.END, potential_energy_name + '= ' + potential_energy_value + '\n')
        for friction_coefficient_name, friction_coefficient_value in simulation.mechanical_system['Friction Coefficients'].items():
            system_characteristics_frame.friction_coefficients_input.insert(tk.END, friction_coefficient_name + '= ' + str(friction_coefficient_value) + '\n')
        for driving_force_coefficient_name, driving_force_coefficient_value in simulation.mechanical_system['Driving Force Coefficients'].items():
            system_characteristics_frame.driving_force_coefficients_input.insert(tk.END, driving_force_coefficient_name + '= ' + str(driving_force_coefficient_value) + '\n')
        system_characteristics_frame.notes_input.insert(tk.END, simulation.mechanical_system['Notes'])
        for initial_condition_name, initial_condition_value in simulation.initial_conditions.items():
            system_characteristics_frame.initial_conditions_input.insert(tk.END, initial_condition_name + '= ' + str(initial_condition_value) + '\n')
        for integration_parameters_name, integration_parameters_value in simulation.integration_parameters.items():
            system_characteristics_frame.integration_parameters_input.insert(tk.END, integration_parameters_name + '= ' + str(integration_parameters_value) + '\n')

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
