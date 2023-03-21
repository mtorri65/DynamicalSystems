from typing import TypedDict

from .root_view import Root
from .start_view import StartView
from .existing_simulations_view import ExistingSimulationsView
from .new_simulation_view import NewSimulationView
from .system_characteristics_view import SystemCharacteristicsView

from . import views_constants as vc

class Frames(TypedDict):
    system_characteristics: SystemCharacteristicsView
    existing_simulations: ExistingSimulationsView
    new_simulations: NewSimulationView
    start: StartView


class View:
    def __init__(self):
        self.root = Root()
        self.frames: Frames = {}  # type: ignore

        self._add_frame(StartView, "start")
        self._add_frame(ExistingSimulationsView, "existing_simulations")
        self._add_frame(NewSimulationView, "new_simulation")
        self._add_frame(SystemCharacteristicsView, "system_characteristics")

    def _add_frame(self, Frame, name: str) -> None:
        self.frames[name] = Frame(self.root)
        self.frames[name].grid(row=0, column=0, sticky='nsew')

    def switch(self, name: str, title: str) -> None:
        frame = self.frames[name]
        self.title = vc.title + ' - ' + title
        frame.tkraise()
        frame.event_generate('<<ShowFrame>>')
       
    def start_mainloop(self) -> None:
        self.root.mainloop()