import tkinter as tk

from dynamical_systems_models.main_model import Model
from dynamical_systems_views.main_view import View


class StartController:
    def __init__(self, model: Model, view: View) -> None:
        self.model = model
        self.view = view
        self.frame = self.view.frames["start"]
        self._bind()

#        self._update_list_of_systems()

    def _bind(self) -> None:
#        self.frame.signout_btn.config(command=self.logout)
        self.frame.new_button.config(command=self.switch_system_characteristics)
        self.frame.mechanical_systems_listbox.bind("<<ListboxSelect>>", self._select_system)
#        self.frame.bind("<<ShowFrame>>", self._update_list_of_systems)

    def _select_system(self, event):
#        self.open_button['state'] = tk.ACTIVE
        system = event.widget.curselection()
        if system:
            index = system[0]
            selected_system = event.widget.get(index)    
            self.model.system.selected_system = selected_system
            self.view.frames['existing_simulations'].simulations_listbox.delete(0, tk.END)        
            self.switch_existing_simulations(selected_system)

    def _update_list_of_simulations(self, selected_system):
        selected_system_simulations = self.model.system.get_list_of_simulations(selected_system)
        for simulation in selected_system_simulations:
            self.view.frames['existing_simulations'].simulations_listbox.insert('end', simulation)

    def _update_mechanical_system_label(self, system):
        self.view.frames['existing_simulations'].mechanical_system_label.config(text = system)

    def switch_system_characteristics(self) -> None:
        self.clear_system_characteristics()
        self.view.switch("system_characteristics", 'system description')

    def switch_existing_simulations(self, selected_system) -> None:
        self._update_list_of_simulations(selected_system)
        self._update_mechanical_system_label(selected_system)        
        self.view.switch('existing_simulations', 'existing simulations')

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
