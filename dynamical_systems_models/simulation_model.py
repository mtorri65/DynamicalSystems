import os
import time
import glob
import json
from json import JSONEncoder
from PIL import ImageTk, Image
import sys
import importlib
import numpy as np

from .base_model import ObservableModel

from . import models_constants as mc

class Simulation(ObservableModel):
    def __init__(self, mechanical_system = {}, initial_conditions = {}, integration_parameters = {}, equations_of_motion = {}, momenta = {}, output = {}):
        super().__init__()
        self.mechanical_system = mechanical_system
        self.initial_conditions = initial_conditions
        self.integration_parameters = integration_parameters
        self.equations_of_motion = equations_of_motion
        self.momenta = momenta
        self.output = output

    @property
    def mechanical_system(self):
        return self._mechanical_system
    @mechanical_system.setter
    def mechanical_system(self, new_mechanical_system):
        self._mechanical_system = new_mechanical_system

    @property
    def initial_conditions(self):
        return self._initial_conditions
    @initial_conditions.setter
    def initial_conditions(self, new_initial_conditions):
        self._initial_conditions = new_initial_conditions

    @property
    def integration_parameters(self):
        return self._integration_parameters
    @integration_parameters.setter
    def integration_parameters(self, new_integration_parameters):
        self._integration_parameters = new_integration_parameters

    @property
    def equations_of_motion(self):
        return self._equations_of_motion
    @equations_of_motion.setter
    def equations_of_motion(self, new_equations_of_motion):
        self._equations_of_motion = new_equations_of_motion

    @property
    def momenta(self):
        return self._momenta
    @momenta.setter
    def momenta(self, new_momenta):
        self._momenta = new_momenta

    @property
    def output(self):
        return self._output
    @output.setter
    def output(self, new_output):
        self._output = new_output

    def save_to_json(self, json_file_folder):
        simulation_json_file = self.get_simulation_file(json_file_folder)

        with open(simulation_json_file, 'w') as f:
            json.dump(self, f, cls=Simulation_Encoder, indent=4, separators=(',',': '))
            self.new_simulation = os.path.basename(simulation_json_file)

    def get_equations_of_motion_from_previous_simulation(self, simulation_file_folder):
        recent_simulation_file = self.get_recent_simulation_file(simulation_file_folder, 'second_most_recent')
        equations_of_motion = {}
        if recent_simulation_file['Equations of Motion']:
            equations_of_motion = recent_simulation_file['Equations of Motion']
        return equations_of_motion
    
    def get_momenta_from_previous_simulation(self, simulation_file_folder):
        recent_simulation_file = self.get_recent_simulation_file(simulation_file_folder, 'second_most_recent')
        momenta = {}
        if recent_simulation_file['Momenta']:
            momenta = recent_simulation_file['Momenta']
        return momenta

    def get_output_from_previous_simulation(self, simulation_file_folder):
        most_recent_simulation_file = self.get_recent_simulation_file(simulation_file_folder, 'second_most_recent')
        if most_recent_simulation_file['Output']:
            output = most_recent_simulation_file['Output']
        return output

    def previous_simulation_is_different(self, simulation_json_files_folder, position_in_sorted_list):
        initial_conditions_are_different_or_integration_parameters_are_different_or_output_previous_simulation_does_not_exist = True
        equations_of_motion_are_different = True
        recent_json_string = self.get_recent_simulation_file(simulation_json_files_folder, position_in_sorted_list)
        if recent_json_string != '':
            if (recent_json_string['Mechanical System'] == self.mechanical_system) and recent_json_string['Equations of Motion']:
                equations_of_motion_are_different = False
            if (recent_json_string['Initial Conditions'] == self.initial_conditions) and (recent_json_string['Integration Parameters'] == self.integration_parameters) and recent_json_string['Output']:
    #                   messagebox.showwarning('Warning', 'The parameter values specified are identical to those of the last saved file - no new file will be saved')
                print('Warning', 'The parameter values specified are identical to those of the last saved simulation - no new file will be saved')
                initial_conditions_are_different_or_integration_parameters_are_different_or_output_previous_simulation_does_not_exist = False
        else:
                initial_conditions_are_different_or_integration_parameters_are_different_or_output_previous_simulation_does_not_exist = True

        return equations_of_motion_are_different, initial_conditions_are_different_or_integration_parameters_are_different_or_output_previous_simulation_does_not_exist            
    
    def get_recent_simulation_file(self, simulation_json_files_folder, position_in_sorted_list):
        file_type = r'\*json'
        simulation_json_files_list = glob.glob(simulation_json_files_folder + file_type)
        index = 0
        if position_in_sorted_list == 'most_recent':
            index = -1
        elif position_in_sorted_list == 'second_most_recent':
            index = -2
        else:
            raise Exception("position_in_sorted list must be either most_recent or second_most_recent")

        recent_json_string = ''
        if simulation_json_files_list:
            sorted_files = sorted(simulation_json_files_list, key=os.path.getmtime)
            with open(sorted_files[index], 'r') as f:
                recent_json_string = json.load(f)
        
        return recent_json_string


    def get_simulation_file(self, json_file_folder):
        simulation_json_file = json_file_folder + 'simulation_' + time.strftime('%Y%m%d-%H%M%S') + '.json'
        return simulation_json_file

    def get_simulation_folder(self):
        simulation_json_files_folder = self.mechanical_system['Path'] + 'simulations\\'
        if not os.path.exists(simulation_json_files_folder):
            os.makedirs(simulation_json_files_folder)
        return simulation_json_files_folder
    
    def get_simulation_data(self, simulation_file_path, x_axis_variable, y_axis_variable):
        simulation_json = ''
        with open(self.mechanical_system['Path'] + 'simulations\\' + simulation_file_path, 'r') as f:
            simulation_json = json.load(f)

        self.x = []
        self.y = []
        for time_iteration_step, time_iteration_dynamical_variables_values in simulation_json['Output'].items():
            if x_axis_variable == 't':
                self.x.append(float(time_iteration_step))
            else:
                self.x.append(float(time_iteration_dynamical_variables_values[x_axis_variable]))
            self.y.append(float(time_iteration_dynamical_variables_values[y_axis_variable]))

    def serialize_equations_of_motion(self):
        new_equations_of_motion = {}
        for second_derivative, equations_of_motion in self.equations_of_motion.items():
            new_equations_of_motion_key = str(second_derivative)
            new_equations_of_motion_value = str(equations_of_motion)
            new_equations_of_motion[new_equations_of_motion_key] = new_equations_of_motion_value
        self._save_simulation_to_json(new_equations_of_motion, 'Equations of Motion')

    def serialize_momenta(self):
        new_momenta = {}
        for momentum_name, momentum_equation in self.momenta.items():
            new_momentum_key = str(momentum_name)
            new_momentum_equation = str(momentum_equation)
            new_momenta[new_momentum_key] = new_momentum_equation
        self._save_simulation_to_json(new_momenta, 'Momenta')

    def serialize_output(self):
        new_output = {}
        for output_key, output_value in self.output.items():
            new_output_key = output_key
            new_output_value = output_value
            new_output[new_output_key] = new_output_value
        self._save_simulation_to_json(new_output, 'Output')

    def _save_simulation_to_json(self, new_property, property_name):
        simulation_json = ''
        with open(self.mechanical_system['Path'] + '\\simulations\\' + self.new_simulation, 'r') as f:
            simulation_json = json.load(f)
        simulation_json[property_name] = new_property
        with open(self.mechanical_system['Path'] + '\\simulations\\' + self.new_simulation, 'w') as f:
            json.dump(simulation_json, f, indent=2, separators=(',',': '))


class Simulation_Encoder(JSONEncoder):
    def default(self, obj):        
        if isinstance(obj, Simulation):
            simulation_json = {}

            mechanical_system = {}

            mechanical_system['Name'] = obj.mechanical_system['Name']
            mechanical_system['Path'] = obj.mechanical_system['Path']
            mechanical_system['Dimensions'] = obj.mechanical_system['Dimensions']
            mechanical_system['Particles'] = obj.mechanical_system['Particles']

            masses_json = {}
            for mass_name, mass_value in obj.mechanical_system['Masses'].items():
                mass_name_json = str(mass_name)
                mass_value_json = mass_value
                masses_json[mass_name_json] = mass_value_json
            mechanical_system['Masses'] = masses_json

            parameters_json = {}
            for parameter_name, parameter_value in obj.mechanical_system['Parameters'].items():
                parameter_name_json = str(parameter_name)
                parameter_value_json = parameter_value
                parameters_json[parameter_name_json] = parameter_value_json
            mechanical_system['Parameters'] = parameters_json

            degrees_of_freedom_json = {}
            for degree_of_freedom_name, degree_of_freedom_value in obj.mechanical_system['Degrees of Freedom'].items():
                degree_of_freedom_name_json = str(degree_of_freedom_name)
                degree_of_freedom_value_json = str(degree_of_freedom_value)
                degrees_of_freedom_json[degree_of_freedom_name_json] = degree_of_freedom_value_json
            mechanical_system['Degrees of Freedom'] = degrees_of_freedom_json

            cartesian_coordinates_json = {}
            for cartesian_coordinate_name, cartesian_coordinate_value in obj.mechanical_system['Cartesian Coordinates'].items():
                cartesian_coordinate_name_json = str(cartesian_coordinate_name)
                cartesian_coordinate_value_json = str(cartesian_coordinate_value)
                cartesian_coordinates_json[cartesian_coordinate_name_json] = cartesian_coordinate_value_json
            mechanical_system['Cartesian Coordinates'] = cartesian_coordinates_json

            single_particle_potential_energies_json = {}
            for single_particle_potential_energy_name, single_particle_potential_energy_value in obj.mechanical_system['Potential Energy'].items():
                single_particle_potential_energy_name_json = str(single_particle_potential_energy_name)
                single_particle_potential_energy_value_json = str(single_particle_potential_energy_value)
                single_particle_potential_energies_json[single_particle_potential_energy_name_json] = single_particle_potential_energy_value_json
            mechanical_system['Potential Energy'] = single_particle_potential_energies_json

            friction_coefficients_json = {}
            for friction_coefficient_name, friction_coefficient_value in obj.mechanical_system['Friction Coefficients'].items():
                friction_coefficient_name_json = str(friction_coefficient_name)
                friction_coefficient_value_json = friction_coefficient_value
                friction_coefficients_json[friction_coefficient_name_json] = friction_coefficient_value_json
            mechanical_system['Friction Coefficients'] = friction_coefficients_json

            driving_force_coefficients_json = {}
            for driving_force_coefficient_name, driving_force_coefficient_value in obj.mechanical_system['Driving Force Coefficients'].items():
                driving_force_coefficient_name_json = str(driving_force_coefficient_name)
                driving_force_coefficient_value_json = driving_force_coefficient_value
                driving_force_coefficients_json[driving_force_coefficient_name_json] = driving_force_coefficient_value_json
            mechanical_system['Driving Force Coefficients'] = driving_force_coefficients_json

            mechanical_system['Notes'] = obj.mechanical_system['Notes']

            simulation_json['Mechanical System'] = mechanical_system

            initial_conditions_json = {}
            for initial_condition_name, initial_condition_value in obj.initial_conditions.items():
                initial_condition_name_json = str(initial_condition_name)
                initial_condition_value_json = initial_condition_value
                initial_conditions_json[initial_condition_name_json] = initial_condition_value_json
            simulation_json['Initial Conditions'] = initial_conditions_json

            integration_parameters_json = {}
            for integration_parameter_name, integration_parameter_value in obj.integration_parameters.items():
                integration_parameter_name_json = str(integration_parameter_name)
                integration_parameter_value_json = integration_parameter_value
                integration_parameters_json[integration_parameter_name_json] = integration_parameter_value_json
            simulation_json['Integration Parameters'] = integration_parameters_json

            equations_of_motion_json = {}
            for equation_of_motion_name, equation_of_motion_value in obj.equations_of_motion.items():
                equation_of_motion_name_json = str(equation_of_motion_name)
                equation_of_motion_value_json = str(equation_of_motion_value)
                equations_of_motion_json[equation_of_motion_name_json] = equation_of_motion_value_json
            simulation_json['Equations of Motion'] = equations_of_motion_json

            output_json = {}
            for output_key, output_value in obj.output.items():
                output_key_json = output_key
                output_value_json = output_value.tolist()
                output_json[output_key_json] = output_value_json
            simulation_json['Output'] = output_json

            momenta_json = {}
            for momentum_key, momentum_value in obj.momenta.items():
                momentum_key_json = momentum_key
                momentum_value_json = momentum_value.tolist()
                momenta_json[momentum_key_json] = momentum_value_json
            simulation_json['Momenta'] = momenta_json

            return simulation_json

        return super().default(simulation_json)

class System(object):
    def __init__(self) -> None:
        self.mechanical_systems_library_path = mc.mechanical_system_library_path
        self.selected_simulation = ''
        self.selected_system = ''
        self.mechanical_systems_diagram_path = ''
        self.diagram = ''

    def get_list_of_systems(self):
        systems = [ f.name for f in os.scandir(self.mechanical_systems_library_path) if f.is_dir() ]
        return systems
    
    def get_list_of_simulations(self, system):
        simulations = []
        if system:
            simulations = [ f.name for f in os.scandir(self.mechanical_systems_library_path + system + '\\simulations') if f.is_file() ]
        return simulations
    
    def get_mechanical_system_diagram(self):
        no_diagram = self._resize_image(self.mechanical_systems_library_path + 'no_diagram_provided.png')
        if self.selected_system != '':
            self.set_mechanical_system_diagram_path()
            if os.path.exists(self.mechanical_systems_diagram_path):
                mechanical_system_diagram = self._resize_image(self.mechanical_systems_diagram_path)
                return mechanical_system_diagram
            else:
                return no_diagram
        else:
            return no_diagram

    def _resize_image(self, diagram_path):
        image = Image.open(diagram_path)
        image.thumbnail((300, 300))        
        resized_image = ImageTk.PhotoImage(image)
        return resized_image

    def set_mechanical_system_path(self):
        if self.selected_system == '':
            self.mechanical_system_path = self.mechanical_systems_library_path
        else:
            self.mechanical_system_path = self.mechanical_systems_library_path + self.selected_system + '\\'

    def set_mechanical_system_simulation_path(self):
        self.set_mechanical_system_path()
        if self.selected_simulation == '':
            self.mechanical_systems_simulation_path = self.mechanical_system_path + 'simulations\\'
        else:
            self.mechanical_systems_simulation_path = self.mechanical_system_path + 'simulations\\' + self.selected_simulation
        
    def set_mechanical_system_diagram_path(self):
        self.set_mechanical_system_path()
        if self.selected_system == '':
            self.mechanical_systems_diagram_path = self.mechanical_system_path
        else:
            self.mechanical_systems_diagram_path = self.mechanical_system_path + self.selected_system + '.png'

    @property
    def mechanical_systems_library_path(self):
        return self._mechanical_systems_library_path
    @mechanical_systems_library_path.setter
    def mechanical_systems_library_path(self, new_mechanical_systems_library_path):
        self._mechanical_systems_library_path = new_mechanical_systems_library_path

    @property
    def selected_system(self):
        return self._selected_system
    @selected_system.setter
    def selected_system(self, new_selected_system):
        self._selected_system = new_selected_system
    
    @property
    def selected_simulation(self):
        return self._selected_simulation
    @selected_simulation.setter
    def selected_simulation(self, new_selected_simulation):
        self._selected_simulation = new_selected_simulation
    
    @property
    def mechanical_system_simulation_path(self):
        return self._mechanical_system_simulation_path
    
class Equations_Of_Motion_Builder():
    def __init__(self, simulation):
        self.simulation = simulation

    def build_equations_of_motion_module(self):
        # build equations_of_motion.py file
        with open(self.simulation.mechanical_system['Path'] + 'equations_of_motion.py', 'w') as file_write:
            file_write.write('import sympy\n')
            file_write.write('import os\n')
            file_write.write('from sympy.parsing.sympy_parser import parse_expr\n')
            file_write.write('\n')
            file_write.write('def derive_equations_of_motion(simulation):\n')
            file_write.write('\tt = sympy.symbols(\'t\')')
            file_write.write('\n')
            file_write.write('\tdegrees_of_freedom = list(simulation.mechanical_system[\'Degrees of Freedom\'].values())\n')
            file_write.write('\tvelocities = list(simulation.mechanical_system[\'Velocities\'].values())\n')
            file_write.write('\taccelerations = list(simulation.mechanical_system[\'Accelerations\'].values())\n')
            file_write.write('\tsecond_derivatives_simplified = {}\n')
            file_write.write('\n')
            file_write.write('\tif len(simulation.equations_of_motion) != 0:\n')
            file_write.write('\t\tfor acceleration in simulation.mechanical_system[\'Accelerations\'].values():\n')
            file_write.write('\t\t\tsecond_derivatives_simplified[acceleration] = simulation.equations_of_motion[str(acceleration)]\n')
            file_write.write('\telse:\n')
            
            file_write.write('\t\tmasses_names = list(simulation.mechanical_system[\'Masses\'])\n')
            masses_names = list(self.simulation.mechanical_system['Masses'])
            for index in range(len(masses_names)):
                file_write.write('\t\t' + str(masses_names[index]) + ' = masses_names[' + str(index) + ']\n')
            file_write.write('\t\tparameters_names = list(simulation.mechanical_system[\'Parameters\'])\n')
            parameters_names = list(self.simulation.mechanical_system['Parameters'])
            for index in range(len(parameters_names)):
                file_write.write('\t\t' + str(parameters_names[index]) + ' = parameters_names[' + str(index) + ']\n')
            file_write.write('\t\tdegrees_of_freedom = list(simulation.mechanical_system[\'Degrees of Freedom\'].values())\n')
            degrees_of_freedom_names = list(self.simulation.mechanical_system['Degrees of Freedom'])
            for index in range(len(degrees_of_freedom_names)):
                file_write.write('\t\t' + str(degrees_of_freedom_names[index]) + ' = degrees_of_freedom[' + str(index) + ']\n')
            file_write.write('\t\tfriction_coefficients_names = list(simulation.mechanical_system[\'Friction Coefficients\'])\n')
            friction_coefficients_names = list(self.simulation.mechanical_system['Friction Coefficients'])
            for index in range(len(friction_coefficients_names)):
                file_write.write('\t\t' + str(friction_coefficients_names[index]) + ' = friction_coefficients_names[' + str(index) + ']\n')
            file_write.write('\t\tdriving_force_coefficients_names = list(simulation.mechanical_system[\'Driving Force Coefficients\'])\n')
            driving_force_coefficients_names = list(self.simulation.mechanical_system['Driving Force Coefficients'])
            for index in range(len(driving_force_coefficients_names)):
                file_write.write('\t\t' + str(driving_force_coefficients_names[index]) + ' = driving_force_coefficients_names[' + str(index) + ']\n')
                index = index + 1
            file_write.write('\n')

            file_write.write('# calculate cartesian coordinates\n')
            for cartesian_coordinate_name in self.simulation.mechanical_system['Cartesian Coordinates']:
                cartesian_coordinate = self.simulation.mechanical_system['Cartesian Coordinates'][cartesian_coordinate_name]
                file_write.write('\t\t' + str(cartesian_coordinate_name) + ' = ' + cartesian_coordinate + '\n')
            file_write.write('\n')

            file_write.write('# calculate kinetic energy\n')
            for index_p in range(self.simulation.mechanical_system['Particles']):
                v_square = '\t\tv' + str(index_p + 1) + '_square = '

                index_c = 0
                for cartesian_coordinate_name in self.simulation.mechanical_system['Cartesian Coordinates']:
                    cartesian_coordinate = self.simulation.mechanical_system['Cartesian Coordinates'][cartesian_coordinate_name]
                    if index_c // self.simulation.mechanical_system['Dimensions'] == index_p:
                        v_square = v_square + 'sympy.diff(' + str(cartesian_coordinate_name) + ', t)**2'
                        if index_c % self.simulation.mechanical_system['Dimensions'] < self.simulation.mechanical_system['Dimensions'] - 1:
                            v_square = v_square + ' + '
                    index_c = index_c + 1        
                file_write.write(v_square + '\n')

            for index in range(self.simulation.mechanical_system['Particles']):
                file_write.write('\t\t' + 'T' + str(index + 1) + ' = 1/2 * m' + str(index + 1) + ' * v' + str(index + 1) + '_square\n')

            T = 'T = '
            for index in range(self.simulation.mechanical_system['Particles']):
                T = T + 'T' + str(index + 1)
                if index < self.simulation.mechanical_system['Particles'] - 1:
                    T = T + ' + '

            file_write.write('\t\t' + T + '\n')
            file_write.write('\t\tT_expand = 2*T.expand() # the factor 1/2 in the kinetic energy is not part of the kinetic energy matrix. To neautralize it, T_expand is multiplied by 2')
            file_write.write('\n')
            file_write.write('\n')

            file_write.write('# calculate kinetic energy matrix\n')
            file_write.write('\t\tK ={ (row,column):0 for row in range(len(simulation.mechanical_system[\'Degrees of Freedom\'])) for column in range(len(simulation.mechanical_system[\'Degrees of Freedom\']))}\n')
            file_write.write('\t\tn = 0\n')
            file_write.write('\t\tfor velocity_name_n in simulation.mechanical_system[\'Velocities\']:\n')
            file_write.write('\t\t\tvelocity_n = simulation.mechanical_system[\'Velocities\'][velocity_name_n]\n')
            file_write.write('\t\t\tK[n, n] = (T_expand.coeff(velocity_n, 2)).simplify()\n')
            file_write.write('\t\t\tn = n + 1\n')

            file_write.write('\t\tn = 0\n')
            file_write.write('\t\tfor velocity_name_n in simulation.mechanical_system[\'Velocities\']:\n')
            file_write.write('\t\t\tvelocity_n = simulation.mechanical_system[\'Velocities\'][velocity_name_n]\n')
            file_write.write('\t\t\tp = 0\n')
            file_write.write('\t\t\tfor velocity_name_p in simulation.mechanical_system[\'Velocities\']:\n')
            file_write.write('\t\t\t\tvelocity_p = simulation.mechanical_system[\'Velocities\'][velocity_name_p]\n')
            file_write.write('\t\t\t\tif n < p:\n')
            file_write.write('\t\t\t\t\tK[n,p] = (T_expand.coeff(velocity_n*velocity_p)).simplify()\n')            
            file_write.write('\t\t\t\tp = p + 1\n')
            file_write.write('\t\t\tn = n + 1\n')
            file_write.write('\n')

            file_write.write('\t\tdKdq ={ (degree_of_freedom, row,column):0 for degree_of_freedom in range(len(simulation.mechanical_system[\'Degrees of Freedom\'])) for row in range(len(simulation.mechanical_system[\'Degrees of Freedom\'])) for column in range(len(simulation.mechanical_system[\'Degrees of Freedom\']))}\n')
            file_write.write('\t\tdegrees_of_freedom = list(simulation.mechanical_system[\'Degrees of Freedom\'].values())\n')
            file_write.write('\t\th = 0\n')
            file_write.write('\t\tfor degree_of_freedom_h in degrees_of_freedom:\n')
            file_write.write('\t\t\tfor n in range(len(simulation.mechanical_system[\'Degrees of Freedom\'])):\n')
            file_write.write('\t\t\t\tfor p in range(len(simulation.mechanical_system[\'Degrees of Freedom\'])):\n')
            file_write.write('\t\t\t\t\tdKdq[h,p,n] = sympy.diff(K[p,n], degree_of_freedom_h).simplify()\n')
            file_write.write('\t\t\th = h + 1\n')
            file_write.write('\n')

            file_write.write('# calculate potential energy\n')
            file_write.write('\t\tV_single_particle = { (row):1 for row in range(simulation.mechanical_system[\'Particles\'] + 1)}\n')
            index = 0
            for single_particle_potential_energy in self.simulation.mechanical_system['Potential Energy'].values():            
                file_write.write('\t\tV_single_particle['+ str(index) + '] = ' + single_particle_potential_energy + '\n')
                index = index + 1
            file_write.write('\n')

            file_write.write('\t\tdVdq ={ (row, column):0 for row in range(simulation.mechanical_system[\'Particles\']) for column in range(len(simulation.mechanical_system[\'Degrees of Freedom\']))}\n')
            file_write.write('\t\tfor n in range(simulation.mechanical_system[\'Particles\']):\n')
            file_write.write('\t\t\tp = 0\n')
            file_write.write('\t\t\tfor degree_of_freedom_p in degrees_of_freedom:\n')
            file_write.write('\t\t\t\tdVdq[n, p] = sympy.diff(V_single_particle[n], degree_of_freedom_p).simplify()\n')
            file_write.write('\t\t\t\tp = p + 1\n')
            file_write.write('\n')

            file_write.write('# calculate equations_of_motion\n')
            file_write.write('\t\tLE = []\n')
            file_write.write('\t\tmomenta = {}\n')            		
            file_write.write('\t\taccelerations = list(simulation.mechanical_system[\'Accelerations\'].values())\n')
            file_write.write('\t\tvelocities = list(simulation.mechanical_system[\'Velocities\'].values())\n')
            file_write.write('\t\tfor h in range(len(simulation.mechanical_system[\'Degrees of Freedom\'])):\n')
            file_write.write('\t\t\tterm1 = 0\n')
            file_write.write('\t\t\tterm2 = 0\n')
            file_write.write('\t\t\tterm3 = 0\n')
            file_write.write('\t\t\tterm4 = 0\n')
            file_write.write('\t\t\tmomentum_h = 0\n')
            file_write.write('\t\t\tfor p in range(len(simulation.mechanical_system[\'Velocities\'])):\n')
            file_write.write('\t\t\t\tmomentum_h = momentum_h + 1/2 * (K[h,p] + K[p,h])*velocities[p]\n')
            file_write.write('\t\t\tfor p in range(len(simulation.mechanical_system[\'Accelerations\'])):\n')
            file_write.write('\t\t\t\tterm1 = term1 + (K[h,p] + K[p,h])*accelerations[p]\n')
            file_write.write('\t\t\tfor p in range(len(simulation.mechanical_system[\'Velocities\'])):\n')
            file_write.write('\t\t\t\tfor n in range(len(simulation.mechanical_system[\'Velocities\'])):\n')
            file_write.write('\t\t\t\t\tterm2 = term2 + (dKdq[n,h,p] + dKdq[n,p,h])*velocities[n]*velocities[p]\n')
            file_write.write('\t\t\tfor p in range(len(simulation.mechanical_system[\'Velocities\'])):\n')
            file_write.write('\t\t\t\tfor n in range(len(simulation.mechanical_system[\'Degrees of Freedom\'])):\n')
            file_write.write('\t\t\t\t\tterm3 = term3 + dKdq[h,n,p]*velocities[n]*velocities[p]\n')
            file_write.write('\t\t\tfor r in range(simulation.mechanical_system[\'Particles\']):\n')
            file_write.write('\t\t\t\tterm4 = term4 + dVdq[r,h]\n')
            file_write.write('\t\t\tLagrange_equation = (.5*(term1 + term2 - term3) + term4).simplify()\n')
            file_write.write('\t\t\tmomenta[\'p_\' + str(degrees_of_freedom[h]).partition(\'(\')[0]] = momentum_h\n')
            file_write.write('\t\t\tLE.append(Lagrange_equation)\n')
            file_write.write('\n')

            file_write.write('\t\tLE_expand = []\n')
            file_write.write('\t\tfor index in range(len(simulation.mechanical_system[\'Degrees of Freedom\'])):\n')
            file_write.write('\t\t\tLE_expand.append(LE[index].expand())\n')
            file_write.write('\t\tMat ={ (row, column):0 for row in range(len(simulation.mechanical_system[\'Degrees of Freedom\'])) for column in range(len(simulation.mechanical_system[\'Degrees of Freedom\']) + 1)}\n')

            for n in range(len(self.simulation.mechanical_system['Degrees of Freedom'])):
                for p in range(len(self.simulation.mechanical_system['Degrees of Freedom'])):
                    file_write.write('\t\tMat[' + str(n) + ', ' + str(p) + '] = LE_expand[' + str(n) + '].coeff(sympy.Derivative(degrees_of_freedom[' + str(p) + ']' + ', (t, 2)))\n')
            file_write.write('\t\tcoeffs = { (row):0 for row in range(len(simulation.mechanical_system[\'Degrees of Freedom\'])) }\n')

            for n in range(len(self.simulation.mechanical_system['Degrees of Freedom'])):
                args = '\t\tcoeffs[' + str(n) + '] = sympy.collect(LE_expand[' + str(n) + '], ['
                for p in range(len(self.simulation.mechanical_system['Degrees of Freedom'])):
                    args = args + 'sympy.Derivative(degrees_of_freedom[' + str(p) + '], (t, 2))'
                    if p < len(self.simulation.mechanical_system['Degrees of Freedom']) - 1:
                        args = args + ', '                
                file_write.write(args + '], evaluate=False)\n')
            for n in range(len(self.simulation.mechanical_system['Degrees of Freedom'])):
                file_write.write('\t\tMat[' + str(n) + ',' + str(len(self.simulation.mechanical_system['Degrees of Freedom'])) + '] = -coeffs[' + str(n) + '][1]\n')
            file_write.write('\n')
            
            file_write.write('\t\tMatx = sympy.Matrix((\n')
            for n in range(len(self.simulation.mechanical_system['Degrees of Freedom'])):
                args = '\t\t\t\t\t\t\t('
                for p in range(len(self.simulation.mechanical_system['Degrees of Freedom']) + 1):
                    args = args + 'Mat[' + str(n) + ', ' + str(p) + ']'
                    if p < len(self.simulation.mechanical_system['Degrees of Freedom']):
                        args = args + ', '
                args = args + ')'
                if n < len(self.simulation.mechanical_system['Degrees of Freedom']):
                    args = args + ','
                file_write.write(args + '\n')
            file_write.write('\t\t\t\t\t\t\t))\n')
            file_write.write('\n')
            file_write.write('\t\tsecond_derivatives = sympy.solve_linear_system_LU(Matx, [')
            args = ''
            for n in range(len(self.simulation.mechanical_system['Degrees of Freedom'])):
                args = args + 'sympy.Derivative(degrees_of_freedom[' + str(n) + '], (t, 2))'
                if n < len(self.simulation.mechanical_system['Degrees of Freedom']) - 1:
                    args = args + ', '
            file_write.write(args + '])\n')            

            for n in range(len(self.simulation.mechanical_system['Degrees of Freedom'])):
                file_write.write('\t\tsecond_derivatives_simplified[sympy.Derivative(degrees_of_freedom[' + str(n) + '], (t, 2))] = second_derivatives[sympy.Derivative(degrees_of_freedom[' + str(n) + '], (t, 2))].simplify()\n')
            file_write.write('\n')    

            file_write.write('\treturn second_derivatives_simplified, momenta')

        sys.path.insert(0, self.simulation.mechanical_system['Path'])
        self.imported_module = importlib.import_module('equations_of_motion')
        self.imported_module = importlib.reload(self.imported_module)
        return self.imported_module

class Integrator_Builder():
    def __init__(self, simulation):
        self.simulation = simulation

    def build_integrator_module(self):
        with open(self.simulation.mechanical_system['Path'] + 'integrator.py', 'w') as file_write:
            file_write.write('import sympy\n')
            file_write.write('import numpy\n')
            file_write.write('from scipy.integrate import odeint\n')
            file_write.write('\n')
            file_write.write('def integrate_equations_of_motion(simulation):\n')
            file_write.write('\tt = sympy.symbols(\'t\')')
            file_write.write('\n')

            file_write.write('\tmasses_names = list(simulation.mechanical_system[\'Masses\'])\n')
            masses_names = list(self.simulation.mechanical_system['Masses'])
            index = 0
            for mass_name in masses_names:
                file_write.write('\t' + str(mass_name) + ' = masses_names[' + str(index) + ']\n')
                index = index + 1
            file_write.write('\n')

            file_write.write('\tparameters_names = list(simulation.mechanical_system[\'Parameters\'])\n')
            parameters_names = list(self.simulation.mechanical_system['Parameters'])
            index = 0
            for parameter_name in parameters_names:
                file_write.write('\t' + str(parameter_name) + ' = parameters_names[' + str(index) + ']\n')
                index = index + 1
            file_write.write('\n')

            file_write.write('\tdegrees_of_freedom = list(simulation.mechanical_system[\'Degrees of Freedom\'].values())\n')
            degrees_of_freedom_names = list(self.simulation.mechanical_system['Degrees of Freedom'])
            index = 0
            for degree_of_freedom_name in degrees_of_freedom_names:
                file_write.write('\t' + str(degree_of_freedom_name) + ' = degrees_of_freedom[' + str(index) + ']\n')
                index = index + 1
            file_write.write('\n')

            file_write.write('\tfriction_coefficients_names = list(simulation.mechanical_system[\'Friction Coefficients\'])\n')
            friction_coefficients_names = list(self.simulation.mechanical_system['Friction Coefficients'])
            index = 0
            for friction_coefficient_name in friction_coefficients_names:
                file_write.write('\t' + str(friction_coefficient_name) + ' = friction_coefficients_names[' + str(index) + ']\n')
                index = index + 1
            file_write.write('\n')

            file_write.write('\tdriving_force_coefficients_names = list(simulation.mechanical_system[\'Driving Force Coefficients\'])\n')
            driving_force_coefficients_names = list(self.simulation.mechanical_system['Driving Force Coefficients'])
            index = 0
            for driving_force_coefficient_name in driving_force_coefficients_names:
                file_write.write('\t' + str(driving_force_coefficient_name) + ' = driving_force_coefficients_names[' + str(index) + ']\n')
                index = index + 1
            file_write.write('\n')                

            file_write.write('\tvelocities = list(simulation.mechanical_system[\'Velocities\'].values())\n')
            velocities_names = list(self.simulation.mechanical_system['Velocities'])
            index = 0
            for velocity_name in velocities_names:
                file_write.write('\t' + str(velocity_name) + '_velocity = velocities[' + str(index) + ']\n')
                index = index + 1
            file_write.write('\n')

            file_write.write('\taccelerations = list(simulation.mechanical_system[\'Accelerations\'].values())\n')
            accelerations_names = list(self.simulation.mechanical_system['Accelerations'])
            index = 0
            for acceleration_name in accelerations_names:
                file_write.write('\t' + str(acceleration_name) + '_acceleration = accelerations[' + str(index) + ']\n')
                index = index + 1
            file_write.write('\n')

            file_write.write('\tmomenta = list(simulation.momenta.values())\n')
            momenta_names = list(self.simulation.momenta)
            for index, momentum_name in enumerate(momenta_names):
                file_write.write('\t' + str(momentum_name) + '_momentum = momenta[' + str(index) + ']\n')
            file_write.write('\n')

# 	momenta = list(simulation.momenta.values())
#	theta1_momentum = momenta[0]
#	theta2_momentum = momenta[1]
            

            degrees_of_freedom_names = list(self.simulation.mechanical_system['Degrees of Freedom'])
            file_write.write('# convert system of second order ODEs into a system of first order ODEs\n')
            for index in range(len(degrees_of_freedom_names)):
                args = 't, '
                for index1 in range(len(masses_names)):
                    args = args +  str(masses_names[index1]) + ', '
                for index1 in range(len(parameters_names)):
                    args = args +  str(parameters_names[index1]) + ', '
                for index1 in range(len(friction_coefficients_names)):
                    args = args +  str(friction_coefficients_names[index1]) + ', '
                for index1 in range(len(driving_force_coefficients_names)):
                    args = args +  str(driving_force_coefficients_names[index1]) + ', '
                for index1 in range(len(degrees_of_freedom_names)):
                    args = args +  str(degrees_of_freedom_names[index1]) + ', '
                for index1 in range(len(velocities_names)):
                    args = args +  str(velocities_names[index1]) + '_velocity'
                    if index1 < len(velocities_names) - 1:
                        args = args + ', '
                file_write.write('\tdz' + str(index + 1) + 'dt_f = sympy.lambdify((' + args + '), simulation.equations_of_motion[' + str(degrees_of_freedom_names[index]) + '_acceleration]' + ')\n')
                file_write.write('\td' + str(degrees_of_freedom_names[index]) + 'dt_f = sympy.lambdify((' + str(degrees_of_freedom_names[index]) + '_velocity), ' + str(degrees_of_freedom_names[index]) + '_velocity)\n')
            file_write.write('\n')

            file_write.write('\tmomenta_functions = []\n')
            file_write.write('\tfor momentum_index in range(len(degrees_of_freedom)):\n')
            for index in range(len(degrees_of_freedom_names)):
                args = 't, '
                for index1 in range(len(masses_names)):
                    args = args +  str(masses_names[index1]) + ', '
                for index1 in range(len(parameters_names)):
                    args = args +  str(parameters_names[index1]) + ', '
                for index1 in range(len(friction_coefficients_names)):
                    args = args +  str(friction_coefficients_names[index1]) + ', '
                for index1 in range(len(driving_force_coefficients_names)):
                    args = args +  str(driving_force_coefficients_names[index1]) + ', '
                for index1 in range(len(degrees_of_freedom_names)):
                    args = args +  str(degrees_of_freedom_names[index1]) + ', '
                for index1 in range(len(velocities_names)):
                    args = args +  str(velocities_names[index1]) + '_velocity'
                    if index1 < len(velocities_names) - 1:
                        args = args + ', '
            file_write.write('\t\tmomentum = sympy.lambdify((' + args + '), momenta[momentum_index])\n')
            file_write.write('\t\tmomenta_functions.append(momentum)\n')
            file_write.write('\n')

# 	momenta_functions = []
#	for momentum_index in len(degrees_of_freedom):
#		momentum = sympy.lambdify((t, m1, m2, g, L1, L2, theta1_friction, theta2_friction, A_theta1_drive, w_theta1_drive, phi_theta1_drive, A_theta2_drive, w_theta2_drive, phi_theta2_drive, theta1, theta2, theta1_velocity, theta2_velocity), simulation.momenta[momentum_index])
#		momenta_functions.append(momentum)
            

            file_write.write('# define solution vector\n')
            args = 'S, t, '
            for index in range(len(masses_names)):
                args = args +  str(masses_names[index]) + ', '
            for index in range(len(parameters_names)):
                args = args +  str(parameters_names[index]) + ', '
            for index in range(len(friction_coefficients_names)):
                args = args + str(friction_coefficients_names[index]) + ', '
            for index in range(len(driving_force_coefficients_names)):
                args = args + str(driving_force_coefficients_names[index])
                if index < len(driving_force_coefficients_names) - 1:
                    args = args + ', '
            file_write.write('\tdef dSdt(' + args + '):\n')

            args = ''
            for index in range(len(degrees_of_freedom_names)):
                args = args + str(degrees_of_freedom_names[index]) + ', z' + str(index + 1)
                if index < len(degrees_of_freedom_names) - 1:
                    args = args + ', '
            file_write.write('\t\t' + args + ' = S\n')
            file_write.write('\t\treturn [\n')
            for index in range(len(degrees_of_freedom_names)):
                file_write.write('\t\t\td' + str(degrees_of_freedom_names[index]) + 'dt_f(z' + str(index + 1) + '),\n')
                args = 't, '
                for index1 in range(len(masses_names)):
                    args = args + str(masses_names[index1]) + ', ' 
                for index1 in range(len(parameters_names)):
                    args = args + str(parameters_names[index1]) + ', ' 
                for index1 in range(len(friction_coefficients_names)):
                    args = args + str(friction_coefficients_names[index1]) + ', ' 
                for index1 in range(len(driving_force_coefficients_names)):
                    args = args + str(driving_force_coefficients_names[index1]) + ', '
                for index1 in range(len(degrees_of_freedom_names)):
                    args = args + str(degrees_of_freedom_names[index1]) + ', ' 
                for index1 in range(len(degrees_of_freedom_names)):
                    args = args + 'z' + str(index1 + 1) 
                    if index1 < len(degrees_of_freedom_names) - 1:
                        args = args + ', '
                file_write.write('\t\t\tdz' + str(index + 1) + 'dt_f(' + args + '),\n')
            file_write.write('\t\t]\n')
            file_write.write('\n')

            file_write.write('# integrate equations of motion\n')
            t_initial_value = self.simulation.integration_parameters['t_initial'] 
            t_final_value = self.simulation.integration_parameters['t_final'] 
            iterations_value = self.simulation.integration_parameters['iterations'] 

            file_write.write('\tsampled_times = numpy.linspace(' + str(t_initial_value) + ', ' + str(t_final_value) + ', ' + str(iterations_value) + ')\n')
            masses = list(self.simulation.mechanical_system['Masses'].values())
            for index in range(len(masses_names)):
                file_write.write('\t' + str(masses_names[index]) + ' = ' + str(masses[index]) + '\n')
            parameters = list(self.simulation.mechanical_system['Parameters'].values())
            for index in range(len(parameters_names)):
                file_write.write('\t' + str(parameters_names[index]) + ' = ' + str(parameters[index]) + '\n')
            friction_coefficients = list(self.simulation.mechanical_system['Friction Coefficients'].values())
            for index in range(len(friction_coefficients_names)):
                file_write.write('\t' + str(friction_coefficients_names[index]) + ' = ' + str(friction_coefficients[index]) + '\n')
            driving_force_coefficients = list(self.simulation.mechanical_system['Driving Force Coefficients'].values())
            for index in range(len(driving_force_coefficients_names)):
                file_write.write('\t' + str(driving_force_coefficients_names[index]) + ' = ' + str(driving_force_coefficients[index]) + '\n')
            file_write.write('\n')
          
            file_write.write('\ttime_evolution = odeint(dSdt, y0=[')
            args = ''
            initial_conditions = list(self.simulation.initial_conditions.values())
            for index in range(len(initial_conditions)):
                args = args +  str(initial_conditions[index])
                if index < len(initial_conditions) - 1:
                    args = args + ', '
            file_write.write(args + '], t = sampled_times, args=(')

            args = ''
            for index in range(len(masses_names)):
                args = args +  str(masses_names[index])
                args = args + ', '
            for index in range(len(parameters_names)):
                args = args +  str(parameters_names[index])
                args = args + ', '
            for index in range(len(friction_coefficients_names)):
                args = args +  str(friction_coefficients_names[index])
                args = args + ', '
            for index in range(len(driving_force_coefficients_names)):
                args = args +  str(driving_force_coefficients_names[index])
                args = args + ', '
            file_write.write(args + '))\n')
            file_write.write('\n')

            file_write.write('\tmomenta_values = []\n')
            file_write.write('\tfor index_step, sampled_time in enumerate(sampled_times):\n')
            file_write.write('\t\tmomenta_values.append([None] * len(degrees_of_freedom))\n')
            file_write.write('\t\tfor index_degree, degree_of_freedom in enumerate(degrees_of_freedom):\n')
            args_parameters = 'sampled_time, '
            for index in range(len(masses_names)):
                args_parameters = args_parameters + str(masses_names[index]) + ', '
            for index in range(len(parameters_names)):
                args_parameters = args_parameters + str(parameters_names[index]) + ', '
            for index in range(len(friction_coefficients_names)):
                args_parameters = args_parameters + str(friction_coefficients_names[index]) + ', '
            for index in range(len(driving_force_coefficients_names)):
                args_parameters = args_parameters + str(driving_force_coefficients_names[index]) + ', '
            args_degree_of_freedom = ''
            for index in range(len(degrees_of_freedom_names)):
                args_degree_of_freedom = args_degree_of_freedom + 'time_evolution[index_step][' + str(2*index) + '], '
            for index in range(len(degrees_of_freedom_names)):
                args_degree_of_freedom = args_degree_of_freedom + 'time_evolution[index_step][' + str(2*index + 1) + '] '
                if index < len(degrees_of_freedom_names) - 1:
                    args_degree_of_freedom = args_degree_of_freedom + ', '

            file_write.write('\t\t\tmomenta_values[index_step][index_degree] = momenta_functions[index_degree](' + args_parameters + args_degree_of_freedom + ')\n')
            file_write.write('\n')

            file_write.write('\toutput = {}\n')
            file_write.write('\toutput_step = {}\n')
            file_write.write('\tindex_step = 0\n')
            file_write.write('\tfor sampled_time in sampled_times:\n')
            file_write.write('\t\tindex_degree = 0\n')
            file_write.write('\t\tfor degree_of_freedom in simulation.mechanical_system[\'Degrees of Freedom\']:\n')
            file_write.write('\t\t\tstep_dynamic_variable_name = str(degree_of_freedom)\n')
            file_write.write('\t\t\toutput_step[step_dynamic_variable_name] = time_evolution[index_step][index_degree]\n')
            file_write.write('\t\t\tstep_dynamic_variable_name = \'v_\' + str(degree_of_freedom)\n')
            file_write.write('\t\t\toutput_step[step_dynamic_variable_name] = time_evolution[index_step][index_degree + 1]\n')

            file_write.write('\t\t\tstep_dynamic_variable_name = \'p_\' + str(degree_of_freedom)\n')
            file_write.write('\t\t\toutput_step[step_dynamic_variable_name] = momenta_values[index_step][index_degree // 2]\n')

            file_write.write('\t\t\tindex_degree = index_degree + 2\n')
            file_write.write('\t\toutput[str(sampled_time)] = output_step.copy()\n')
            file_write.write('\t\tindex_step = index_step + 1\n')
            file_write.write('\n')
            file_write.write('\treturn output')

        sys.path.insert(0, self.simulation.mechanical_system['Path'])
        self.imported_module = importlib.import_module('integrator')
        self.imported_module = importlib.reload(self.imported_module)
        
        return self.imported_module


