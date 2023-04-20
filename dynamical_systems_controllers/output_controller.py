import json
import numpy as np
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from dynamical_systems_models.main_model import Model
from dynamical_systems_views.main_view import View

class OutputController:
    def __init__(self, model: Model, view: View) -> None:
        self.model = model
        self.view = view
        self.frame = self.view.frames['output']
        self.x_axis_degree_of_freedom = ''
        self.y_axis_degree_of_freedom = ''
        self._bind()

    def _bind(self) -> None:
        self.frame.x_axis_combo.bind("<<ComboboxSelected>>", self._select_x_degree_of_freedom)
        self.frame.y_axis_combo.bind("<<ComboboxSelected>>", self._select_y_degree_of_freedom)
#        self.frame.start_button.config(command=self._switch_start)        
#        self.frame.simulations_button.config(command=self._switch_existing_simulations)
#        self.frame.close_button.config(command=self._close_window)

    def _select_x_degree_of_freedom(self, event):
        self.x_axis_degree_of_freedom = event.widget.get()
        self.plot()

    def _select_y_degree_of_freedom(self, event):
        self.y_axis_degree_of_freedom = event.widget.get()
        self.plot()

#    def _switch_start(self) -> None:
#        self.view.switch('start', '')

#    def _switch_existing_simulations(self) -> None:
#        self.model.system.selected_simulation = ''       
#        self.view.switch('existing_simulations', 'existing_simulations')

#    def _close_window(self):
#        self.view.output_window.destroy()

    def show_output_window(self):
        self.view.output_window.deiconify()

    def replace_system_label(self):
        self.frame.mechanical_system_label.config(text = self.model.system.selected_system.replace('_',' '))

    def replace_simulation_label(self):
        self.x_axis_degree_of_freedom = ''
        self.y_axis_degree_of_freedom = ''
        self.frame.simulation_label.config(text = self.model.system.selected_simulation)

    def configure_plot_dropdowns(self):
        self.frame.graph_type_combo.config(values=['2D', '3D'])
        self.frame.graph_type_combo.current(0)

        self.x_axis_variables = list(self.model.simulation.mechanical_system['Degrees of Freedom'].values())
        self.degrees_of_freedom = []
        for degree_of_freedom in self.x_axis_variables:
            self.degrees_of_freedom.append(str(degree_of_freedom).split('(')[0])
        self.x_axis_variables_t = self.degrees_of_freedom.copy()
        self.x_axis_variables_t.insert(0, 't')

        self.y_axis_variables = []
        for x_axis_variable in self.degrees_of_freedom:
#            self.y_axis_variables.append('p_' + str(x_axis_variable))
            self.y_axis_variables.append('v_' + str(x_axis_variable))

        self.frame.x_axis_combo.config(values=self.x_axis_variables_t)
        self.frame.x_axis_combo.current(0)
        self.frame.y_axis_combo.config(values=self.y_axis_variables)
        self.frame.y_axis_combo.current(0)
        self.frame.z_axis_combo.config(values=['t', 'z1', 'z2'])


    def plot(self):
#        self.frame.ax.set_xlabel(r'$t$')
#        self.frame.ax.set_ylabel(r'$V$')
        if self.x_axis_degree_of_freedom not in self.x_axis_variables_t:
            self.x_axis_degree_of_freedom = 't'
        if self.y_axis_degree_of_freedom not in self.y_axis_variables:
#            self.y_axis_degree_of_freedom = 'p_' + self.degrees_of_freedom[0]
            self.y_axis_degree_of_freedom = 'v_' + self.degrees_of_freedom[0]
        
        self.model.simulation.get_simulation_data(self.model.system.selected_simulation, self.x_axis_degree_of_freedom, self.y_axis_degree_of_freedom)
        
        if self.frame.canvas: self.frame.canvas.get_tk_widget().pack_forget()

        plt.style.use(['science', 'notebook', 'grid'])
        height = self.frame.winfo_screenheight()
        width = self.frame.winfo_screenmmwidth()
        self.frame.fig = Figure(figsize=(height/96, width/96), dpi=100)
        self.frame.ax = self.frame.fig.add_subplot()

        if self.frame.canvas: self.frame.canvas.get_tk_widget().pack_forget()    

        self.frame.ax.plot(self.model.simulation.x , self.model.simulation.y, '-', color='green', lw = 0.7, label = 'test')
        self.frame.ax.set_xlabel(self.x_axis_degree_of_freedom)
        self.frame.ax.set_ylabel(self.y_axis_degree_of_freedom)

        self.frame.canvas = FigureCanvasTkAgg(self.frame.fig, master=self.frame.plot_frame)  
        self.frame.canvas.draw()
        self.frame.canvas.get_tk_widget().pack()        
