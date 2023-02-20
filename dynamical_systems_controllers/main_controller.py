from dynamical_systems_models.main_model import Model
#from dynamical_systems_models.auth_model import Auth
from dynamical_systems_views.main_view import View

from .start_controller import StartController
from .existing_simulations_controller import ExistingSimulationsController
from .system_characteristics_controller import SystemCharacteristicsController


class Controller:
    def __init__(self, model: Model, view: View) -> None:
        self.view = view
        self.model = model
        self.start_controller = StartController(model, view)
        self.existing_simulations_controller = ExistingSimulationsController(model, view)
        self.system_characteristics_controller = SystemCharacteristicsController(model, view)

#        self.model.simulation.add_event_listener("simulation_run", self.auth_state_listener)
        self.model.simulation.add_event_listener("system_list_available", self.systems_listener)

        for frame_name, frame in self.view.frames.items():
#                frame.bind('<<ShowFrame>>', lambda event, frame_name=frame_name:self.model.printMessage(event, frame_name))
                frame.bind('<<ShowFrame>>', lambda event, frame_name=frame_name:self.get_data(event, frame_name))

    def get_data(self, event, frame_name):
        if frame_name == 'start':
            self.model.printMessage_Start()
#            print('Hello from the Start!')
        elif frame_name == 'system_characteristics':
#            self.model.printMessage_SystemCharacteristics()
            self.systems_list = self.model.system.get_list_of_systems()
        elif frame_name == 'existing_simulations':
            self.model.printMessage_ExistingSimulations()
#            print('Hello from the Existing Simulations!')
        else:
            print('I need frame_name!')


#    def auth_state_listener(self) -> None:
#        if self.model.simulation:
#            self.view.switch('existing_simulations')
#        else:
#            self.view.switch('start')

    def systems_listener(self) -> None:
# should show the systems when the start page shows up
        self.view.switch("start", '')
        self.view.frames['start'].mechanical_systems_listbox

    def start(self) -> None:
        # Here, you can do operations required before launching the gui, for example,
        # self.model.auth.load_auth_state()
#        if self.model.auth.is_logged_in:
        self.systems_list = self.model.system.get_list_of_systems()
        for system in self.systems_list:
            self.view.frames["start"].mechanical_systems_listbox.insert('end', system)
        
        self.view.switch("start", '')
#        else:
#            self.view.switch("existing_simulations")

        self.view.start_mainloop()