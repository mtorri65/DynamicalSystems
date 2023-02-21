import tkinter as tk
from tkinter import messagebox

from dynamical_systems_models.main_model import Model
from dynamical_systems_models.simulation_model import Simulation
from dynamical_systems_views.main_view import View

class SystemCharacteristicsController:
    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view
        self.frame = self.view.frames["system_characteristics"]
        self._bind()

    def _bind(self) -> None:
        """Binds controller functions with respective buttons in the view"""
        self.frame.previous_button.config(command=self.switch_previous)
        self.frame.save_button.config(command=self.save)

    def _update_list_of_systems(self):
        self.view.frames['start'].mechanical_systems_listbox.delete(0, tk.END)        
        systems_list = self.model.system.get_list_of_systems()
        for system in systems_list:
            self.view.frames['start'].mechanical_systems_listbox.insert('end', system)

    def _update_list_of_simulations(self, selected_system):
        self.view.frames['existing_simulations'].simulations_listbox.delete(0, tk.END)        
        selected_system_simulations = self.model.system.get_list_of_simulations(selected_system)
        for simulation in selected_system_simulations:
            self.view.frames['existing_simulations'].simulations_listbox.insert('end', simulation)

    def switch_previous(self) -> None:
        if self.model.system.selected_simulation:
            self._update_list_of_simulations(self.model.system.selected_system)
            self.view.switch('existing_simulations', '')
        else:
            self._update_list_of_systems()
            self.view.switch('start', '')

    def save(self) -> None:
        '''
        data = {
            "fullname": self.frame.fullname_input.get(),
            "username": self.frame.username_input.get(),
            "password": self.frame.password_input.get(),
            "has_agreed": self.frame.has_agreed.get(),
        }
        print(data)
        user: User = {"username": data["username"]}
        self.model.auth.login(user)
        self.clear_form()
        '''        
#        global mechanical_system_path
#        global selected_simulation

        self.simulation = Simulation()
        mechanical_system = {}
        
        mechanical_system['Name'] = self.frame.name_input.get().rstrip('\n')
        mechanical_system['Path'] = self.model.system.mechanical_systems_library_path + mechanical_system['Name'] + '\\'
        mechanical_system['Dimensions'] = int(self.frame.number_dimensions_input.get().rstrip('\n'))
        mechanical_system['Particles'] = int(self.frame.number_particles_input.get().rstrip('\n'))

        parameters_list = self.frame.parameters_input.get('1.0', 'end-1c').rstrip('\n').split('\n')
        parameters = {}
        for index in range(len(parameters_list)):
            parameter_name = parameters_list[index].partition('=')[0].strip(' ')
            parameter = float(parameters_list[index].partition('=')[2])
            parameters[parameter_name] = parameter
        mechanical_system['Parameters'] = parameters

        degrees_of_freedom_list = self.frame.degrees_of_freedom_input.get('1.0', 'end-1c').rstrip('\n').split('\n')
        degrees_of_freedom = {}
        for index in range(len(degrees_of_freedom_list)):
            degree_of_freedom_name = degrees_of_freedom_list[index]
            degree_of_freedom = degrees_of_freedom_list[index]
            degrees_of_freedom[degree_of_freedom_name] = degree_of_freedom
        mechanical_system['Degrees of Freedom'] = degrees_of_freedom

        cartesian_coordinates_list = self.frame.cartesian_coordinates_input.get('1.0', 'end-1c').rstrip('\n').split('\n')
        cartesian_coordinates = {}
        for index in range(len(cartesian_coordinates_list)):
            cartesian_coordinates_name = cartesian_coordinates_list[index].partition('=')[0].strip(' ')
            cartesian_coordinates_value = cartesian_coordinates_list[index].partition('=')[2].strip(' ')
            cartesian_coordinates[cartesian_coordinates_name] = cartesian_coordinates_value
        mechanical_system['Cartesian Coordinates'] = cartesian_coordinates

        potential_energy_list = self.frame.potential_energy_input.get('1.0', 'end-1c').rstrip('\n').split('\n')
        potential_energy = {}
        for index in range(len(potential_energy_list)):
            potential_energy_name = potential_energy_list[index].partition('=')[0].strip(' ')
            potential_energy_value = potential_energy_list[index].partition('=')[2].strip(' ')
            potential_energy[potential_energy_name] = potential_energy_value
        mechanical_system['Potential Energy'] = potential_energy

        friction_coefficients_list = self.frame.friction_coefficients_input.get('1.0', 'end-1c').rstrip('\n').split('\n')
        friction_coefficients = {}
        for index in range(len(friction_coefficients_list)):
            friction_coefficient_name = friction_coefficients_list[index].partition('=')[0].strip(' ')
            friction_coefficient_value = float(friction_coefficients_list[index].partition('=')[2])
            friction_coefficients[friction_coefficient_name] = friction_coefficient_value
        mechanical_system['Friction Coefficients'] = friction_coefficients

        driving_force_coefficients_list = self.frame.driving_force_coefficients_input.get('1.0', 'end-1c').rstrip('\n').split('\n')
        driving_force_coefficients = {}
        for index in range(len(driving_force_coefficients_list)):
            driving_force_coefficient_name = driving_force_coefficients_list[index].partition('=')[0].strip(' ')
            driving_force_coefficient_value = float(driving_force_coefficients_list[index].partition('=')[2])
            driving_force_coefficients[driving_force_coefficient_name] = driving_force_coefficient_value
        mechanical_system['Driving Force Coefficients'] = driving_force_coefficients

        notes = self.frame.notes_input.get('1.0', 'end-1c').rstrip('\n').split('\n')
        notes_string = ''
        for index in range(len(notes)):
            notes_string = notes_string + '\n' + notes[index]  
        mechanical_system['Notes'] = notes_string.lstrip('\n')

        initial_conditions_list = self.frame.initial_conditions_input.get('1.0', 'end-1c').rstrip('\n').split('\n')
        initial_conditions = {}
        for index in range(len(initial_conditions_list)):
            initial_condition_name = initial_conditions_list[index].partition('=')[0].strip(' ')
            initial_condition_value = float(initial_conditions_list[index].partition('=')[2])
            initial_conditions[initial_condition_name] = initial_condition_value

        integration_parameters_list = self.frame.integration_parameters_input.get('1.0', 'end-1c').rstrip('\n').split('\n')
        integration_parameters = {}
        t_initial = integration_parameters_list[0].partition('=')[0].strip(' ')
        t_initial_value = float(integration_parameters_list[0].partition('=')[2])        
        integration_parameters[t_initial] = t_initial_value
        t_final = integration_parameters_list[1].partition('=')[0].strip(' ')
        t_final_value = float(integration_parameters_list[1].partition('=')[2])        
        integration_parameters[t_final] = t_final_value
        iterations = integration_parameters_list[2].partition('=')[0].strip(' ')
        iterations_value = int(integration_parameters_list[2].partition('=')[2])        
        integration_parameters[iterations] = iterations_value

        equations_of_motion = {}
        output = {}

        self.simulation.mechanical_system = mechanical_system
        self.simulation.initial_conditions = initial_conditions
        self.simulation.integration_parameters = integration_parameters
        self.simulation.equations_of_motion = equations_of_motion
        self.simulation.output = output

        self.simulation.save_to_json()
