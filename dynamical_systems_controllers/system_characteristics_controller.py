import tkinter as tk
from tkinter import messagebox, scrolledtext
import sympy
from sympy.parsing.sympy_parser import parse_expr

from dynamical_systems_models.main_model import Model
from dynamical_systems_models.simulation_model import Simulation
from dynamical_systems_models.simulation_model import Equations_Of_Motion_Builder
from dynamical_systems_models.simulation_model import Integrator_Builder
from dynamical_systems_views.main_view import View

from . import controllers_constants as cc

class SystemCharacteristicsController:
    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view
        self.frame = self.view.frames['system_characteristics']
        self._bind()

    def _bind(self) -> None:
        self.frame.previous_button.config(command=self._switch_previous)
        self.frame.save_button.config(command=self._save)
        self.frame.run_button.config(command=self._run)

        for field in self.frame.fields.values():
            field.bind('<KeyRelease>',lambda e: self._change_save_and_run_button_state())

    def _change_save_and_run_button_state(self):
        if self.frame.name_input.get():
            self.frame.save_button.configure(state=tk.NORMAL)
        else:
            self.frame.save_button.configure(state=tk.DISABLED)       

        have_fields_content = [False for i in range(len(self.frame.fields))]
        for index, field in enumerate(self.frame.fields.values()):
            field_content = ''
            if type(field) == tk.Entry:
                field_content = field.get()
            elif type(field) == scrolledtext.ScrolledText:
                field_content = field.get('1.0', 'end-1c')
            if field_content:
                have_fields_content[index] = True
        
        if all(have_fields_content):
            self.frame.run_button.configure(state=tk.NORMAL)
        else:        
            self.frame.run_button.configure(state=tk.DISABLED)

    def _switch_previous(self) -> None:
        self.model.system.selected_simulation = ''
        if self.model.system.get_list_of_simulations(self.model.system.selected_system):
            self.view.switch('existing_simulations', 'existing simulations')
        else:
            self.view.switch('start', '')

    def clear_system_characteristics(self):
        for field in self.frame.fields.values():
            if type(field) == tk.Entry:
                start = 0
            elif type(field) == scrolledtext.ScrolledText:
                start = '1.0'
            else:
                print("Unknown type")
            field.delete(start, tk.END)

    def update_system_name(self):
        self.frame.name_input.insert(tk.END, self.model.system.selected_system)

    def update_system_characteristics(self, simulation):
        self.clear_system_characteristics()

        self.fields = {'name': simulation.mechanical_system['Name'],
                        'dimensions' : simulation.mechanical_system['Dimensions'],
                        'particles' : simulation.mechanical_system['Particles'],
                        'degrees_of_freedom' : simulation.mechanical_system['Degrees of Freedom'],
                        'masses' : simulation.mechanical_system['Masses'],
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
                self.frame.fields[field_name].insert(tk.END, field)
            else:
                if field_name == 'degrees_of_freedom':
                    for field_item_value in field.values():
                        self.frame.fields[field_name].insert(tk.END, field_item_value + '\n')
                else:
                    for field_item_name, field_item_value in field.items():
                        self.frame.fields[field_name].insert(tk.END, field_item_name + '= ' + str(field_item_value) + '\n')
        
    def show_diagram(self):
        # see: https://web.archive.org/web/20201111190625/http://effbot.org/pyfaq/why-do-my-tkinter-images-not-appear.htm
        # as to why a reference to the image (diagram, in this case) must be kept
        diagram = self.model.system.get_mechanical_system_diagram()
        self.frame.label_diagram.config(image = diagram)
        self.frame.label_diagram.image = diagram

    def _save(self) -> None:
        self.model.simulation = Simulation()
        mechanical_system = {}
        
        mechanical_system['Name'] = self.frame.name_input.get().rstrip('\n')
        mechanical_system['Path'] = self.model.system.mechanical_systems_library_path + mechanical_system['Name'] + '\\'
        mechanical_system['Dimensions'] = int(self.frame.number_dimensions_input.get().rstrip('\n'))
        mechanical_system['Particles'] = int(self.frame.number_particles_input.get().rstrip('\n'))

        masses_list = self.frame.masses_input.get('1.0', 'end-1c').rstrip('\n').split('\n')
        masses = {}
        for index in range(len(masses_list)):
            mass_name = masses_list[index].partition('=')[0].strip(' ')
            mass = float(masses_list[index].partition('=')[2])
            masses[mass_name] = mass
        mechanical_system['Masses'] = masses

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

        self.model.simulation.mechanical_system = mechanical_system
        self.model.simulation.initial_conditions = initial_conditions
        self.model.simulation.integration_parameters = integration_parameters
        self.model.simulation.equations_of_motion = equations_of_motion
        self.model.simulation.output = output

        self.model.system.selected_system = mechanical_system['Name']

    def _run(self):
        self._save()
        simulation_json_files_folder = self.model.simulation.get_simulation_folder()
        equations_of_motion_are_different, initial_conditions_are_different_or_integration_parameters_are_different_or_output_previous_simulation_does_not_exist = self.model.simulation.previous_simulation_is_different(simulation_json_files_folder, 'most_recent')
        if equations_of_motion_are_different or initial_conditions_are_different_or_integration_parameters_are_different_or_output_previous_simulation_does_not_exist:        
            self.model.simulation.save_to_json(simulation_json_files_folder)
            self.model.system.selected_simulation = self.model.simulation.new_simulation
            self._sympyfy_mechanical_system()

            if equations_of_motion_are_different:
                equations_of_motion_builder = Equations_Of_Motion_Builder(self.model.simulation)
                equations_of_motion_module = equations_of_motion_builder.build_equations_of_motion_module()
                self.model.simulation.equations_of_motion, self.model.simulation.momenta = equations_of_motion_module.derive_equations_of_motion(self.model.simulation)
            else:
                self.model.simulation.equations_of_motion = self.model.simulation.get_equations_of_motion_from_previous_simulation(simulation_json_files_folder)
                self._sympyfy_equations_of_motion()
                self.model.simulation.momenta = self.model.simulation.get_momenta_from_previous_simulation(simulation_json_files_folder)
                self._sympyfy_momenta()
            self.model.simulation.serialize_equations_of_motion()
            self.model.simulation.serialize_momenta()

            if initial_conditions_are_different_or_integration_parameters_are_different_or_output_previous_simulation_does_not_exist:
                integrator_builder = Integrator_Builder(self.model.simulation)
                integrator_module = integrator_builder.build_integrator_module()
                self.model.simulation.output = integrator_module.integrate_equations_of_motion(self.model.simulation)
            else:
                self.model.simulation.get_output_from_previous_simulation(simulation_json_files_folder)
            self.model.simulation.serialize_output()

        self.view.switch('output', 'output')

    def _sympyfy_mechanical_system(self):
        masses = self.model.simulation.mechanical_system['Masses']
        new_masses = {}
        for mass_name, mass_value in masses.items():
            new_mass_name = sympy.symbols(mass_name)
            new_masses[new_mass_name] = mass_value
        self.model.simulation.mechanical_system['Masses'] = new_masses

        parameters = self.model.simulation.mechanical_system['Parameters']
        new_parameters = {}
        for parameter_name, parameter_value in parameters.items():
            new_parameter_name = sympy.symbols(parameter_name)
            new_parameters[new_parameter_name] = parameter_value
        self.model.simulation.mechanical_system['Parameters'] = new_parameters

        t = sympy.symbols('t')
        degrees_of_freedom = self.model.simulation.mechanical_system['Degrees of Freedom']
        new_degrees_of_freedom = {}        
        for degree_of_freedom_name, degree_of_freedom in degrees_of_freedom.items():
            new_degree_of_freedom_name = sympy.symbols(degree_of_freedom_name)
            new_degree_of_freedom = sympy.symbols(degree_of_freedom_name, cls=sympy.Function)
            new_degree_of_freedom = new_degree_of_freedom(t)
            new_degrees_of_freedom[new_degree_of_freedom_name] = new_degree_of_freedom
        self.model.simulation.mechanical_system['Degrees of Freedom'] = new_degrees_of_freedom

        velocities = {}
        for degree_of_freedom_name, degree_of_freedom in self.model.simulation.mechanical_system['Degrees of Freedom'].items():
            velocities[degree_of_freedom_name] = sympy.diff(self.model.simulation.mechanical_system['Degrees of Freedom'][degree_of_freedom_name], t)
        self.model.simulation.mechanical_system['Velocities'] = velocities
        
        accelerations = {}
        for velocity_name, velocity in self.model.simulation.mechanical_system['Velocities'].items():
            accelerations[velocity_name] = sympy.diff(self.model.simulation.mechanical_system['Velocities'][velocity_name], t)
        self.model.simulation.mechanical_system['Accelerations'] = accelerations

        cartesian_coordinates = self.model.simulation.mechanical_system['Cartesian Coordinates']
        new_cartesian_coordinates = {}
        for cartesian_coordinate_name, cartesian_coordinate_value in cartesian_coordinates.items():
            cartesian_coordinate_no_sympy = cartesian_coordinates[cartesian_coordinate_name]
            for mathematical_function in cc.mathematical_functions:
                if mathematical_function in cartesian_coordinate_no_sympy:
                    cartesian_coordinate = cartesian_coordinate_no_sympy.replace(mathematical_function, 'sympy.' + mathematical_function)
                    cartesian_coordinates[cartesian_coordinate_name] = cartesian_coordinate
                    break
                else:
                    cartesian_coordinate = cartesian_coordinate_no_sympy
            new_cartesian_coordinate_name = sympy.symbols(cartesian_coordinate_name)
            new_cartesian_coordinates[new_cartesian_coordinate_name] = cartesian_coordinate
        self.model.simulation.mechanical_system['Cartesian Coordinates'] = new_cartesian_coordinates

        single_particle_potential_energies = self.model.simulation.mechanical_system['Potential Energy']
        new_single_particle_potential_energies = {}
        for single_particle_potential_energy_name, single_particle_potential_energy_value in single_particle_potential_energies.items():
            single_particle_potential_energy_no_sympy = single_particle_potential_energies[single_particle_potential_energy_name]
            for mathematical_function in cc.mathematical_functions:
                if mathematical_function in single_particle_potential_energy_no_sympy:
                    single_particle_potential_energy = single_particle_potential_energy_no_sympy.replace(mathematical_function, 'sympy.' + mathematical_function)
                    single_particle_potential_energies[single_particle_potential_energy_name] = single_particle_potential_energy
                else:
                    single_particle_potential_energy = single_particle_potential_energy_no_sympy
            new_single_particle_potential_energy_name = sympy.symbols(single_particle_potential_energy_name)
            new_single_particle_potential_energies[new_single_particle_potential_energy_name] = single_particle_potential_energy
        self.model.simulation.mechanical_system['Potential Energy'] = new_single_particle_potential_energies

        friction_coefficients = self.model.simulation.mechanical_system['Friction Coefficients']
        new_friction_coefficients = {}
        for friction_coefficient_name, friction_coefficient_value in friction_coefficients.items():
            new_friction_coefficient_name = sympy.symbols(friction_coefficient_name)
            new_friction_coefficients[new_friction_coefficient_name] = friction_coefficient_value
        self.model.simulation.mechanical_system['Friction Coefficients'] = new_friction_coefficients

        driving_force_coefficients = self.model.simulation.mechanical_system['Driving Force Coefficients']
        new_driving_force_coefficients = {}
        for driving_force_coefficient_name, driving_force_coefficient_value in driving_force_coefficients.items():
            new_driving_force_coefficient_name = sympy.symbols(driving_force_coefficient_name)
            new_driving_force_coefficients[new_driving_force_coefficient_name] = driving_force_coefficient_value
        self.model.simulation.mechanical_system['Driving Force Coefficients'] = new_driving_force_coefficients

    def _sympyfy_equations_of_motion(self):
        equations_of_motion = self.model.simulation.equations_of_motion
        new_equations_of_motion = {}
        for equation_of_motion_name, equation_of_motion_value in equations_of_motion.items():
            new_equation_of_motion_name = sympy.sympify(equation_of_motion_name)
            new_equations_of_motion[new_equation_of_motion_name] = parse_expr(equation_of_motion_value)
        self.model.simulation.equations_of_motion = new_equations_of_motion

    def _sympyfy_momenta(self):
        momenta = self.model.simulation.momenta
        new_momenta = {}
        for momentum_name, momentum_value in momenta.items():
            new_momentum_name = sympy.sympify(momentum_name)
            new_momenta[new_momentum_name] = parse_expr(momentum_value)
        self.model.simulation.momenta = new_momenta

