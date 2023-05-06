import tkinter as tk

from . import views_constants as vc


class SystemCharacteristicsView(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ''' system characteristics frame layout'''
        fontsize = str(11)    
        font_parameters = vc.font + fontsize
        # frame
        self.system_characteristics_frame = tk.LabelFrame(self, text='System Characteristics', font= (font_parameters))
        self.system_characteristics_frame.grid(row = 0, column = 0, padx=10, pady=10)
        
        # labels
        width_label = 15
        anchor = tk.W
        self.name_label = tk.Label(self.system_characteristics_frame, text= 'Name', anchor=anchor, width=width_label, font= (font_parameters))
        self.number_dimensions_label = tk.Label(self.system_characteristics_frame, text= '# Dimensions', anchor=anchor, width=width_label, font= (font_parameters))
        self.number_particles_label = tk.Label(self.system_characteristics_frame, text= '# Particles', anchor=anchor, width=width_label + 5, font= (font_parameters))
        self.degrees_of_freedom_label = tk.Label(self.system_characteristics_frame, text= 'Degrees of Freedom', anchor=anchor, width=width_label, font= (font_parameters))
        self.masses_label = tk.Label(self.system_characteristics_frame, text='Masses', anchor=anchor, width=width_label, font= (font_parameters))
        self.parameters_label = tk.Label(self.system_characteristics_frame, text= 'Parameters', anchor=anchor, width=width_label + 5, font= (font_parameters))
        self.cartesian_coordinates_label = tk.Label(self.system_characteristics_frame, text= 'Cartesian Coordinates', anchor=anchor, width=width_label, font= (font_parameters))
        self.potential_energy_label = tk.Label(self.system_characteristics_frame, text= 'Potential Energy', anchor=anchor, width=width_label + 5, font= (font_parameters))
        self.friction_coefficients_label = tk.Label(self.system_characteristics_frame, text= 'Friction Coefficients', anchor=anchor, width=width_label, font= (font_parameters))
        self.driving_force_coefficients_label = tk.Label(self.system_characteristics_frame, text= 'Driving Force Coefficients', anchor=anchor, width=width_label + 5, font= (font_parameters))
        self.notes_label = tk.Label(self.system_characteristics_frame, text= 'Notes', anchor=anchor, width=width_label, font= (font_parameters))


        fontsize = str(12)
        font_parameters = vc.font + fontsize
        # text boxes
        width_input = 30
        self.name_input = tk.Entry(self.system_characteristics_frame, width=width_input, font=(font_parameters), bd=2)
        self.number_dimensions_input = tk.Entry(self.system_characteristics_frame, width=width_input, font=(font_parameters), bd=2)
        self.number_particles_input = tk.Entry(self.system_characteristics_frame, width=width_input, font=(font_parameters), bd=2)
        self.degrees_of_freedom_input = tk.scrolledtext.ScrolledText(self.system_characteristics_frame, width=width_input, height=4, font=(font_parameters), bd=2)
        self.masses_input = tk.scrolledtext.ScrolledText(self.system_characteristics_frame, width=width_input, height=4, font= (font_parameters), bd=2)
        self.parameters_input = tk.scrolledtext.ScrolledText(self.system_characteristics_frame, width=width_input, height=4, font=(font_parameters), bd=2)
        self.cartesian_coordinates_input = tk.scrolledtext.ScrolledText(self.system_characteristics_frame, width=width_input, height=4, font=(font_parameters), bd=2)
        self.potential_energy_input = tk.scrolledtext.ScrolledText(self.system_characteristics_frame, width=width_input, height=4, font=(font_parameters), bd=2)
        self.friction_coefficients_input = tk.scrolledtext.ScrolledText(self.system_characteristics_frame, width=width_input, height=4, font=(font_parameters), bd=2)
        self.driving_force_coefficients_input = tk.scrolledtext.ScrolledText(self.system_characteristics_frame, width=width_input, height=4, font=(font_parameters), bd=2)
        self.notes_input = tk.scrolledtext.ScrolledText(self.system_characteristics_frame, width=width_input + 50, height=6, font=(font_parameters), bd=2)


        self.name_label.grid(row=0, column=0, padx=10, pady=10)
        self.name_input.grid(row=0, column=1, padx=10, pady=10, sticky='wn')
        self.number_dimensions_label.grid(row=1, column=0, padx=10, pady=10, sticky='en')
        self.number_dimensions_input.grid(row=1, column=1, padx=10, pady=10, sticky='wn')
        self.number_particles_label.grid(row=1, column=2, padx=10, pady=10, sticky='en')
        self.number_particles_input.grid(row=1, column=3, padx=10, pady=10, sticky='wn')
        self.degrees_of_freedom_label.grid(row=3, column=0, padx=10, pady=10, sticky='en')
        self.degrees_of_freedom_input.grid(row=3, column=1, pady=10, padx=10, sticky='wn')
        self.masses_label.grid(row=4, column=0, padx=10, pady=10, sticky='en')
        self.masses_input.grid(row=4, column=1, padx=10, pady=10, sticky='wn')
        self.parameters_label.grid(row=4, column=2, padx=10, pady=10, sticky='en')
        self.parameters_input.grid(row=4, column=3, pady=10, padx=10, sticky='wn')
        self.cartesian_coordinates_label.grid(row=5, column=0, padx=10, pady=10, sticky='en')
        self.cartesian_coordinates_input.grid(row=5, column=1, pady=10, padx=10, sticky='wn')
        self.potential_energy_label.grid(row=5, column=2, padx=10, pady=10, sticky='en')
        self.potential_energy_input.grid(row=5, column=3, pady=10, padx=10, sticky='wn')
        self.friction_coefficients_label.grid(row=6, column=0, padx=10, pady=10, sticky='en')
        self.friction_coefficients_input.grid(row=6, column=1, pady=10, padx=10, sticky='wn')
        self.driving_force_coefficients_label.grid(row=6, column=2, padx=10, pady=10, sticky='en')
        self.driving_force_coefficients_input.grid(row=6, column=3, pady=10, padx=10, sticky='wn')
        self.notes_label.grid(row=7, column=0, padx=10, pady=10, sticky='en')
        self.notes_input.grid(row=7, column=1, pady=10, padx=10, columnspan = 3, sticky='ewn')


        ''' simulation parameters frame layout'''
        fontsize = str(11)    
        font_parameters = vc.font + fontsize
        # frame
        self.simulation_parameters_frame = tk.LabelFrame(self, text='Simulation Parameters', font= (font_parameters))
        self.simulation_parameters_frame.grid(row = 1, column = 0, padx=10, pady=10, columnspan=1, sticky='ew')

        # labels
        self.initial_conditions_label = tk.Label(self.simulation_parameters_frame, text= 'Initial Conditions', anchor=anchor, width=width_label, font= (font_parameters))
        self.initial_conditions_input = tk.scrolledtext.ScrolledText(self.simulation_parameters_frame, width=width_input + 4, height=4, font=(font_parameters), bd=2)
        self.integration_parameters_label = tk.Label(self.simulation_parameters_frame, text= 'Integration Parameters', anchor=anchor, width=width_label + 5, font= (font_parameters))
        self.integration_parameters_input = tk.scrolledtext.ScrolledText(self.simulation_parameters_frame, width=width_input + 4, height=4, font=(font_parameters), bd=2)

        self.initial_conditions_label.grid(row=0, column=0, padx=10, pady=10, sticky='en')
        self.initial_conditions_input.grid(row=0, column=1, pady=10, padx=10, sticky='wn')
        self.integration_parameters_label.grid(row=0, column=2, padx=10, pady=10, sticky='en')
        self.integration_parameters_input.grid(row=0, column=3, pady=10, padx=10, sticky='wn')

        ''' diagram frame layout'''
        # frame
        self.diagram_frame = tk.LabelFrame(self, text='Diagram', font= (font_parameters))
        self.diagram_frame.grid(row = 0, column = 1, padx=10, pady=10, sticky='n')
        
        # labels
        self.label_diagram = tk.Label(self.diagram_frame)
        self.label_diagram.pack()

        ''' buttons frame layout'''
        # frame
        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.grid(row = 2, column = 0, padx=10, pady=10, columnspan=2)

        # buttons
        self.previous_button = tk.Button(self.buttons_frame,text='Previous', font=(font_parameters))
        self.save_button = tk.Button(self.buttons_frame,text='Save', font=(font_parameters))
        self.run_button = tk.Button(self.buttons_frame,text='Run', font=(font_parameters))

        self.previous_button.grid(row=0, column=0, padx = 10, pady=10)        
        self.save_button.grid(row=0, column=1, padx = 10, pady=10)
        self.run_button.grid(row=0, column=2, padx = 10, pady=10)

        self.fields = {'name': self.name_input,
                        'dimensions' : self.number_dimensions_input,
                        'particles' : self.number_particles_input,
                        'degrees_of_freedom' : self.degrees_of_freedom_input,
                        'masses' : self.masses_input,
                        'parameters' : self.parameters_input,
                        'cartesian_coordinates' : self.cartesian_coordinates_input,
                        'potential_energy' : self.potential_energy_input,
                        'friction_coefficients' : self.friction_coefficients_input,
                        'driving_force_coefficients' : self.driving_force_coefficients_input,
                        'notes' : self.notes_input,
                        'initial_conditions' : self.initial_conditions_input,
                        'integration_parameters' : self.integration_parameters_input}
