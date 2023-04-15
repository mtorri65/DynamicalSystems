import tkinter as tk
from tkinter import scrolledtext
import json
import numpy as np

from dynamical_systems_models.main_model import Model
from dynamical_systems_views.main_view import View

class OutputController:
    def __init__(self, model: Model, view: View) -> None:
        self.model = model
        self.view = view
        self.frame = self.view.frames['output']
        self._bind()

    def _bind(self) -> None:
        self.frame.start_button.config(command=self._switch_start)        
        self.frame.simulations_button.config(command=self._switch_existing_simulations)
        self.frame.close_button.config(command=self._close_window)

    def _switch_start(self) -> None:
        self.view.switch('start', '')

    def _switch_existing_simulations(self) -> None:
        self.model.system.selected_simulation = ''       
        self.view.switch('existing_simulations', 'existing_simulations')

    def _close_window(self):
        self.view.output_window.destroy()

    def show_output(self):
        self.view.output_window.deiconify()

    def replace_system_label(self):
        self.frame.mechanical_system_label.config(text = self.model.system.selected_system.replace('_',' '))

    def replace_simulation_label(self):
        self.frame.simulation_label.config(text = self.model.system.selected_simulation)

    def configure_plot_dropdowns(self):
        self.frame.graph_type_combo.config(values=['2D', '3D'])
        self.frame.graph_type_combo.current(0)

        x_axis_variables = list(self.model.simulation.mechanical_system['Degrees of Freedom'].values())
        x_axis_variables_t = x_axis_variables.copy()
        x_axis_variables_t.insert(0, 't')

        y_axis_variables = []
        for x_axis_variable in x_axis_variables:
            y_axis_variables.append('p_' + x_axis_variable)

        self.frame.x_axis_combo.config(values=x_axis_variables_t)
        self.frame.x_axis_combo.current(0)
        self.frame.y_axis_combo.config(values=y_axis_variables)
        self.frame.y_axis_combo.current(0)
        self.frame.z_axis_combo.config(values=['t', 'z1', 'z2'])


    def plot(self):
        self.frame.ax.set_xlabel(r'$t$')
        self.frame.ax.set_ylabel(r'$V$')
        x = np.linspace(0, 15, 100)
        y = np.sin(x)
        self.frame.ax.plot(x, y, '-', color='green', lw = 0.7, label = 'test')
        self.frame.canvas.draw()
        self.frame.canvas.get_tk_widget().pack()        


'''
    def replace_system_label(self):
        self.frame.mechanical_system_label.config(text = self.model.system.selected_system.replace('_',' '))

    def clear_system_diagram(self):
        p = self.model.system.mechanical_systems_diagram_path.rsplit("\\", 1)[0]
#        self.model.system.test_diagram(p)
        self.model.system.set_mechanical_system_diagram_path(p)
'''