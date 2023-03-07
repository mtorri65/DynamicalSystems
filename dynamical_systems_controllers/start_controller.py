import tkinter as tk

from dynamical_systems_models.main_model import Model
from dynamical_systems_views.main_view import View

class StartController:
    def __init__(self, model: Model, view: View) -> None:
        self.model = model
        self.view = view
        self.frame = self.view.frames["start"]
        self.selected_system = ''
        self._bind()

    def _bind(self) -> None:
        self.frame.create_new_system_button.config(command=self.switch_system_characteristics)
        self.frame.mechanical_systems_listbox.bind("<<ListboxSelect>>", self._select_system)

    def _select_system(self, event):
        system = self.frame.mechanical_systems_listbox.curselection()
        if system:
            index = system[0]
            self.selected_system = event.widget.get(index)    
            self.model.system.selected_system = self.selected_system
            self.switch_next_frame(self.selected_system)
    '''
    def _check_if_simulations_exist(self, selected_system):
        frame = self.view.frames['existing_simulations']
        are_there_any_simulations = False

        selected_system_simulations = self.model.system.get_list_of_simulations(selected_system)
        if selected_system_simulations:
            are_there_any_simulations = True

        if are_there_any_simulations:
            # make the label and the listbox visible
            frame.select_label.grid(row=1, column=0, padx=10, pady=10, sticky='wn')
            frame.simulations_listbox.grid(row=1, column=1, padx=10, pady=10)
            for simulation in selected_system_simulations:
                frame.simulations_listbox.insert('end', simulation)
            # hide the create new simulation button
            frame.create_button.grid_forget()
        else:
            # hide the label and the listbox visible
            frame.simulations_listbox.grid_forget()
            frame.select_label.grid_forget()
            # make the create new simulation button visible
            frame.create_button.grid(row=1, column=0, padx=10, pady=10, sticky='wn')

        return are_there_any_simulations
    '''
    def update_mechanical_system_label(self, system, frame_name):
        self.view.frames[frame_name].mechanical_system_label.config(text = system)

    def switch_system_characteristics(self) -> None:
        self.model.system.selected_system = ''
        self.clear_system_characteristics()
        self.view.switch('system_characteristics', 'system description')

    def switch_next_frame(self, selected_system) -> None:
        system_simulations = self.model.system.get_list_of_simulations(selected_system)
        if system_simulations:
            self.view.frames['existing_simulations'].simulations_listbox.delete(0, tk.END)
            self.view.frames['existing_simulations'].mechanical_system_label.config(text = '')
            self.view.switch('existing_simulations', 'existing simulations')
        else:
            self.view.frames['start'].mechanical_systems_listbox.delete(0, tk.END)        
            self.view.frames['new_simulation'].mechanical_system_label.config(text = '')
            self.view.switch('new_simulation', 'new simulation')

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
