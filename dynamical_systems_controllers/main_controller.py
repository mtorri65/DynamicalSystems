import tkinter as tk

from dynamical_systems_models.main_model import Model
from dynamical_systems_views.main_view import View

from .start_controller import StartController
from .existing_simulations_controller import ExistingSimulationsController
from .new_simulation_controller import NewSimulationController
from .system_characteristics_controller import SystemCharacteristicsController

class Controller:
    def __init__(self, model: Model, view: View) -> None:
        self.view = view
        self.model = model
        self.start_controller = StartController(model, view)
        self.existing_simulations_controller = ExistingSimulationsController(model, view)
        self.new_simulation_controller = NewSimulationController(model, view)
        self.system_characteristics_controller = SystemCharacteristicsController(model, view)

        for frame_name, frame in self.view.frames.items():
            frame.bind('<<ShowFrame>>', lambda event, frame_name=frame_name:self.get_data(event, frame_name))

    def get_data(self, event, frame_name):
        if frame_name == 'start':
            for system in self.model.system.get_list_of_systems():
                self.view.frames[frame_name].mechanical_systems_listbox.insert('end', system)    
        elif frame_name == 'system_characteristics':
            if not self.model.system.selected_simulation:
                self.system_characteristics_controller.clear_system_characteristics()
                self.view.frames[frame_name].name_input.insert(tk.END, self.model.system.selected_system)
            if self.view.frames[frame_name].name_input.get() == '':
                self.view.frames[frame_name].save_button['state'] = 'disabled'
                self.view.frames[frame_name].run_button['state'] = 'disabled'
            else:
                self.view.frames[frame_name].save_button['state'] = 'active'                
        elif frame_name == 'existing_simulations':
            system_simulations = self.model.system.get_list_of_simulations(self.model.system.selected_system)
            for simulation in system_simulations:
                self.view.frames[frame_name].simulations_listbox.insert('end', simulation)
            self.view.frames[frame_name].mechanical_system_label.config(text = self.model.system.selected_system)
        elif frame_name == 'new_simulation':
            self.view.frames[frame_name].mechanical_system_label.config(text = self.model.system.selected_system)
        else:
            print('I need frame_name!')

#    def systems_listener(self) -> None:
# should show the systems when the start page shows up
#        self.view.switch("start", '')
#        self.view.frames['start'].mechanical_systems_listbox

    def start(self) -> None:
        # Here, you can do operations required before launching the gui, for example,
        for system in self.model.system.get_list_of_systems():
            self.view.frames['start'].mechanical_systems_listbox.insert('end', system)        
        self.view.switch("start", '')
        self.view.start_mainloop()