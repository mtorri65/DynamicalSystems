import tkinter as tk
from typing import TypedDict

from .root_view import Root
from .start_view import StartView
from .existing_simulations_view import ExistingSimulationsView
from .new_simulation_view import NewSimulationView
from .system_characteristics_view import SystemCharacteristicsView
from .output_view import OutputView

from . import views_constants as vc

class Frames(TypedDict):
    system_characteristics: SystemCharacteristicsView
    existing_simulations: ExistingSimulationsView
    new_simulations: NewSimulationView
    start: StartView
    output: OutputView

class View:
    def __init__(self):
        self.root = Root()
        self.frames: Frames = {}  # type: ignore

        self._add_frame(StartView, self.root, 'start')
        self._add_frame(ExistingSimulationsView, self.root, 'existing_simulations')
        self._add_frame(NewSimulationView, self.root, 'new_simulation')
        self._add_frame(SystemCharacteristicsView, self.root, 'system_characteristics')
        self.output_window = tk.Toplevel()
        self._hide_window()
        self._add_frame(OutputView, self.output_window, 'output')
        self.output_window.protocol('WM_DELETE_WINDOW', self._hide_window)        

    def _add_frame(self, Frame, window, name: str) -> None:
        self.frames[name] = Frame(window)
        self.frames[name].grid(row=0, column=0, sticky='nsew')

    def _hide_window(self):
        self.output_window.withdraw()

    def switch(self, name: str, title: str) -> None:
        if name != 'output':
            window = self.root
        else:
            window = self.output_window
        if title == '':
            window.title(vc.title)
        else:
            window.title(vc.title + ' - ' + title)

        frame = self.frames[name]
        if name != 'output':
            frame.tkraise()
        frame.event_generate('<<ShowFrame>>')
       
    def start_mainloop(self) -> None:
        self.root.mainloop()