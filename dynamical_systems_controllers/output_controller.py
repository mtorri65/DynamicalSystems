import tkinter as tk
from tkinter import scrolledtext
import json

from dynamical_systems_models.main_model import Model
from dynamical_systems_views.main_view import View

class OutputController:
    def __init__(self, model: Model, view: View) -> None:
        self.model = model
        self.view = view
        self.frame = self.view.frames['output']
        self._bind()

'''
    def _bind(self) -> None:
        self.frame.create_button.config(command=self._switch_system_characteristics)        
        self.frame.previous_button.config(command=self._switch_start)

    def _switch_start(self) -> None:
        self.view.switch('start', '')

    def _switch_system_characteristics(self) -> None:
        self.model.system.selected_simulation = ''       
        self.view.switch('system_characteristics', 'system description')

    def replace_system_label(self):
        self.frame.mechanical_system_label.config(text = self.model.system.selected_system.replace('_',' '))

    def clear_system_diagram(self):
        p = self.model.system.mechanical_systems_diagram_path.rsplit("\\", 1)[0]
#        self.model.system.test_diagram(p)
        self.model.system.set_mechanical_system_diagram_path(p)
'''