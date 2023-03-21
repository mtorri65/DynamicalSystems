import os
import time
import glob
import json
from json import JSONEncoder
from PIL import ImageTk, Image

from .base_model import ObservableModel

from . import models_constants as vc

class Simulation(ObservableModel):
    def __init__(self, mechanical_system = {}, initial_conditions = {}, integration_parameters = {}, equations_of_motion = {}, output = {}):
        super().__init__()
        self.mechanical_system = mechanical_system
        self.initial_conditions = initial_conditions
        self.integration_parameters = integration_parameters
        self.equations_of_motion = equations_of_motion
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
    def output(self):
        return self._output
    @output.setter
    def output(self, new_output):
        self._output = new_output

    def save_to_json(self):
        simulation_json_files_folder = self.mechanical_system['Path'] + 'simulations\\'
        mechanical_system_json_file = simulation_json_files_folder + 'simulation_' + time.strftime('%Y%m%d-%H%M%S') + '.json'

        file_type = r'\*json'
        simulation_json_files_list = glob.glob(simulation_json_files_folder + file_type)
        if simulation_json_files_list:
            most_recent_file = max(simulation_json_files_list, key=os.path.getctime)
            with open(most_recent_file, 'r') as f:
                most_recent_json_string = json.load(f)
                if (most_recent_json_string['Mechanical System'] == self.mechanical_system) and (most_recent_json_string['Initial Conditions'] == self.initial_conditions) and (most_recent_json_string['Integration Parameters'] == self.integration_parameters):
#                    messagebox.showwarning('Warning', 'The parameter values specified are identical to those of the last saved file - no new file will be saved')
                    print('Warning', 'The parameter values specified are identical to those of the last saved file - no new file will be saved')
                else:
                    with open(mechanical_system_json_file, 'w') as f:
                        json.dump(self, f, cls=Simulation_Encoder, indent=4, separators=(',',': '))
                        selected_simulation = os.path.basename(mechanical_system_json_file)
        else:
            if not os.path.exists(simulation_json_files_folder):
                os.makedirs(simulation_json_files_folder)
            with open(mechanical_system_json_file, 'w') as f:
                json.dump(self, f, cls=Simulation_Encoder, indent=4, separators=(',',': '))
                selected_simulation = os.path.basename(mechanical_system_json_file)

class Simulation_Encoder(JSONEncoder):
    def default(self, obj):        
        if isinstance(obj, Simulation):
            simulation_json = {}

            mechanical_system = {}

            mechanical_system['Name'] = obj.mechanical_system['Name']
            mechanical_system['Path'] = obj.mechanical_system['Path']
            mechanical_system['Dimensions'] = obj.mechanical_system['Dimensions']
            mechanical_system['Particles'] = obj.mechanical_system['Particles']

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

#            
#            velocities_json = {}
#            for velocity_name, velocity_value in obj.mechanical_system['Velocities'].items():
#                velocity_name_json = str(velocity_name)
#                velocity_value_json = str(velocity_value)
#                velocities_json[velocity_name_json] = velocity_value_json
#            mechanical_system['Velocities'] = velocities_json
#
#            accelerations_json = {}
#            for acceleration_name, acceleration_value in obj.mechanical_system['Accelerations'].items():
#                acceleration_name_json = str(acceleration_name)
#                acceleration_value_json = str(acceleration_value)
#                accelerations_json[acceleration_name_json] = acceleration_value_json
#            mechanical_system['Accelerations'] = accelerations_json
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

            return simulation_json

        return super().default(simulation_json)

class System(object):
    def __init__(self) -> None:
        self.mechanical_systems_library_path = vc.mechanical_system_library_path
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
        no_diagram = ImageTk.PhotoImage(Image.open(self.mechanical_systems_library_path + 'no_diagram_provided.png'))
        if self.selected_system != '':
            self.set_mechanical_system_diagram_path()
            if os.path.exists(self.mechanical_systems_diagram_path):
                mechanical_system_diagram = ImageTk.PhotoImage(Image.open(self.mechanical_systems_diagram_path))
                return mechanical_system_diagram
            else:
                return no_diagram
        else:
            return no_diagram
        
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
            a = 1
        
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
