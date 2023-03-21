from tkinter import Frame, Label, LabelFrame, Entry, scrolledtext, Checkbutton, Button, BooleanVar

from . import views_constants as vc


class SystemCharacteristicsView(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ''' system characteristics frame layout'''
        fontsize = str(11)    
        font_parameters = vc.font + fontsize
        # frame
        self.system_characteristics_frame = LabelFrame(self, text='System Characteristics', font= (font_parameters))
        self.system_characteristics_frame.grid(row = 0, column = 0, padx=10, pady=10)
        
        # labels
        self.name_label = Label(self.system_characteristics_frame, text= 'Name', font= (font_parameters))
        self.number_dimensions_label = Label(self.system_characteristics_frame, text= '# Dimensions', font= (font_parameters))
        self.number_particles_label = Label(self.system_characteristics_frame, text= '# Particles', font= (font_parameters))
        self.degrees_of_freedom_label = Label(self.system_characteristics_frame, text= 'Degrees of Freedom', font= (font_parameters))
        self.parameters_label = Label(self.system_characteristics_frame, text= 'Parameters', font= (font_parameters))
        self.cartesian_coordinates_label = Label(self.system_characteristics_frame, text= 'Cartesian Coordinates', font= (font_parameters))
        self.potential_energy_label = Label(self.system_characteristics_frame, text= 'Potential Energy', font= (font_parameters))
        self.friction_coefficients_label = Label(self.system_characteristics_frame, text= 'Friction Coefficients', font= (font_parameters))
        self.driving_force_coefficients_label = Label(self.system_characteristics_frame, text= 'Driving Force Coefficients', font= (font_parameters))
        self.notes_label = Label(self.system_characteristics_frame, text= 'Notes', font= (font_parameters))
#        self.diagram_label = Label(self.system_characteristics_frame, text= 'Diagram image', font= (font_parameters))

        fontsize = str(12)
        font_parameters = vc.font + fontsize
        # text boxes
        self.name_input = Entry(self.system_characteristics_frame, width=40, font=(font_parameters), bd=2)
        self.number_dimensions_input = Entry(self.system_characteristics_frame, width=40, font=(font_parameters), bd=2)
        self.number_particles_input = Entry(self.system_characteristics_frame, width=40, font=(font_parameters), bd=2)
        self.degrees_of_freedom_input = scrolledtext.ScrolledText(self.system_characteristics_frame, width=40, height=4, font=(font_parameters), bd=2)
        self.parameters_input = scrolledtext.ScrolledText(self.system_characteristics_frame, width=40, height=4, font=(font_parameters), bd=2)
        self.cartesian_coordinates_input = scrolledtext.ScrolledText(self.system_characteristics_frame, width=40, height=4, font=(font_parameters), bd=2)
        self.potential_energy_input = scrolledtext.ScrolledText(self.system_characteristics_frame, width=40, height=4, font=(font_parameters), bd=2)
        self.friction_coefficients_input = scrolledtext.ScrolledText(self.system_characteristics_frame, width=40, height=4, font=(font_parameters), bd=2)
        self.driving_force_coefficients_input = scrolledtext.ScrolledText(self.system_characteristics_frame, width=40, height=4, font=(font_parameters), bd=2)
        self.notes_input = scrolledtext.ScrolledText(self.system_characteristics_frame, width=100, height=6, font=(font_parameters), bd=2)
#        self.diagram_input = Entry(self.system_characteristics_frame, width=40, font=(font_parameters), bd=2)

        self.name_label.grid(row=0, column=0, padx=10, pady=10, sticky='wn')
        self.name_input.grid(row=0, column=1, padx=10, pady=10, sticky='wn')
        self.number_dimensions_label.grid(row=1, column=0, padx=10, pady=10, sticky='wn')
        self.number_dimensions_input.grid(row=1, column=1, padx=10, pady=10, sticky='wn')
        self.number_particles_label.grid(row=1, column=2, padx=10, pady=10, sticky='wn')
        self.number_particles_input.grid(row=1, column=3, padx=10, pady=10, sticky='wn')
        self.degrees_of_freedom_label.grid(row=3, column=0, padx=10, pady=10, sticky='wn')
        self.degrees_of_freedom_input.grid(row=3, column=1, pady=10, padx=10, sticky='wn')
        self.parameters_label.grid(row=3, column=2, padx=10, pady=10, sticky='wn')
        self.parameters_input.grid(row=3, column=3, pady=10, padx=10, sticky='wn')
        self.cartesian_coordinates_label.grid(row=5, column=0, padx=10, pady=10, sticky='wn')
        self.cartesian_coordinates_input.grid(row=5, column=1, pady=10, padx=10, sticky='wn')
        self.potential_energy_label.grid(row=5, column=2, padx=10, pady=10, sticky='wn')
        self.potential_energy_input.grid(row=5, column=3, pady=10, padx=10, sticky='wn')
        self.friction_coefficients_label.grid(row=6, column=0, padx=10, pady=10, sticky='wn')
        self.friction_coefficients_input.grid(row=6, column=1, pady=10, padx=10, sticky='wn')
        self.driving_force_coefficients_label.grid(row=6, column=2, padx=10, pady=10, sticky='wn')
        self.driving_force_coefficients_input.grid(row=6, column=3, pady=10, padx=10, sticky='wn')
        self.notes_label.grid(row=8, column=0, padx=10, pady=10, sticky='wn')
        self.notes_input.grid(row=8, column=1, pady=10, padx=10, columnspan = 3, sticky='ewn')
#        self.diagram_label.grid(row=9, column=0, pady=10, padx=10, columnspan = 3, sticky='wn')
#        self.diagram_input.grid(row=9, column=1, pady=10, padx=10, columnspan = 3, sticky='wn')

        ''' simulation parameters frame layout'''
        fontsize = str(11)    
        font_parameters = vc.font + fontsize
        # frame
        self.simulation_parameters_frame = LabelFrame(self, text='Simulation Parameters', font= (font_parameters))
        self.simulation_parameters_frame.grid(row = 1, column = 0, padx=10, pady=10, sticky='we', columnspan=1)

        # labels
        self.initial_conditions_label = Label(self.simulation_parameters_frame, text= 'Initial Conditions', font= (font_parameters))
        self.initial_conditions_input = scrolledtext.ScrolledText(self.simulation_parameters_frame, width=40, height=4, font=(font_parameters), bd=2)
        self.integration_parameters_label = Label(self.simulation_parameters_frame, text= 'Integration Parameters', font= (font_parameters))
        self.integration_parameters_input = scrolledtext.ScrolledText(self.simulation_parameters_frame, width=40, height=4, font=(font_parameters), bd=2)

        self.initial_conditions_label.grid(row=0, column=0, padx=10, pady=10, sticky='wn')
        self.initial_conditions_input.grid(row=0, column=1, pady=10, padx=10, sticky='wn')
        self.integration_parameters_label.grid(row=0, column=2, padx=10, pady=10, sticky='wn')
        self.integration_parameters_input.grid(row=0, column=3, pady=10, padx=10, sticky='wn')

        ''' diagram frame layout'''
        # frame
        self.diagram_frame = LabelFrame(self, text='Diagram', font= (font_parameters))
        self.diagram_frame.grid(row = 0, column = 1, padx=10, pady=10)
        
        # labels
        self.label_diagram = Label(self.diagram_frame)
        self.label_diagram.pack()

        ''' buttons frame layout'''
        # frame
        self.buttons_frame = Frame(self)
        self.buttons_frame.grid(row = 2, column = 0, padx=10, pady=10, columnspan=2)

        # buttons
        self.previous_button = Button(self.buttons_frame,text='Previous', font=(font_parameters))
        self.save_button = Button(self.buttons_frame,text='Save', font=(font_parameters))
        self.run_button = Button(self.buttons_frame,text='Run', font=(font_parameters))

        self.previous_button.grid(row=0, column=0, padx = 10, pady=10)        
        self.save_button.grid(row=0, column=1, padx = 10, pady=10)
        self.run_button.grid(row=0, column=2, padx = 10, pady=10)

        self.fields = {'name': self.name_input,
                        'dimensions' : self.number_dimensions_input,
                        'particles' : self.number_particles_input,
                        'degrees_of_freedom' : self.degrees_of_freedom_input,
                        'parameters' : self.parameters_input,
                        'cartesian_coordinates' : self.cartesian_coordinates_input,
                        'potential_energy' : self.potential_energy_input,
                        'friction_coefficients' : self.friction_coefficients_input,
                        'driving_force_coefficients' : self.driving_force_coefficients_input,
                        'notes' : self.notes_input,
                        'initial_conditions' : self.initial_conditions_input,
                        'integration_parameters' : self.integration_parameters_input}
