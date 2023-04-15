import tkinter as tk

from dynamical_systems_models.main_model import Model
from dynamical_systems_views.main_view import View

from .start_controller import StartController
from .existing_simulations_controller import ExistingSimulationsController
from .new_simulation_controller import NewSimulationController
from .system_characteristics_controller import SystemCharacteristicsController
from .output_controller import OutputController

class Controller:
    def __init__(self, model: Model, view: View) -> None:
        self.view = view
        self.model = model
        self.start_controller = StartController(model, view)
        self.existing_simulations_controller = ExistingSimulationsController(model, view)
        self.new_simulation_controller = NewSimulationController(model, view)
        self.system_characteristics_controller = SystemCharacteristicsController(model, view)
        self.output_controller = OutputController(model, view)

        for frame_name, frame in self.view.frames.items():
            frame.bind('<<ShowFrame>>', lambda event, frame_name=frame_name:self._update_frame(event, frame_name))

    def _update_frame(self, event, frame_name):
        if frame_name == 'start':
            self.start_controller.clear_systems_list()
            self.start_controller.populate_systems_list()    
        elif frame_name == 'system_characteristics':
            if self.model.system.selected_system:
                if not self.model.system.selected_simulation:
                    # system selected, but simulation not selected: this happens when a system is picked from the Start page that doesn't have any simulations associated
                    self.system_characteristics_controller.clear_system_characteristics()
                    self.system_characteristics_controller.update_system_name()
                else:
                    # system and simulation selected: this happens when a system is picked from the Start page and one of its simulations is selected from the Existing Simulation page
                    self.system_characteristics_controller.update_system_characteristics(self.model.simulation)
            else:
                # system is not selected: this happens when the button Create New System is clicked on the Start page
                self.system_characteristics_controller.clear_system_characteristics()
            self.system_characteristics_controller.show_diagram()
            self.system_characteristics_controller._change_save_and_run_button_state()   # this always happens
        elif frame_name == 'existing_simulations':
            self.existing_simulations_controller.clear_simulations_list()
            self.existing_simulations_controller.populate_simulations_list()
            self.existing_simulations_controller.replace_system_label()
        elif frame_name == 'new_simulation':
            self.new_simulation_controller.replace_system_label()
        elif frame_name == 'output':
            self.output_controller.replace_system_label()
            self.output_controller.replace_simulation_label()
            self.output_controller.show_output()
            self.output_controller.configure_plot_dropdowns()
            self.output_controller.plot()
        else:
            print('I need frame_name!')

    def start(self) -> None:
        # Here, you can do operations required before launching the gui
        for system in self.model.system.get_list_of_systems():
            self.view.frames['start'].mechanical_systems_listbox.insert('end', system)        
        self.view.switch('start', '')
        self.view.start_mainloop()