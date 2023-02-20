from tkinter import Frame, Label, LabelFrame, Entry, scrolledtext, Checkbutton, Button, BooleanVar

from . import views_constants as vc


class SystemCharacteristicsView(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        '''
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.header = Label(self, text="Create a new account")
        self.header.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.fullname_label = Label(self, text="Full Name")
        self.fullname_input = Entry(self)
        self.fullname_label.grid(row=1, column=0, padx=10, sticky="w")
        self.fullname_input.grid(row=1, column=1, padx=(0, 20), sticky="ew")

        self.username_label = Label(self, text="Username")
        self.username_input = Entry(self)
        self.username_label.grid(row=2, column=0, padx=10, sticky="w")
        self.username_input.grid(row=2, column=1, padx=(0, 20), sticky="ew")

        self.password_label = Label(self, text="Password")
        self.password_input = Entry(self, show="*")
        self.password_label.grid(row=3, column=0, padx=10, sticky="w")
        self.password_input.grid(row=3, column=1, padx=(0, 20), sticky="ew")

        self.has_agreed = BooleanVar()
        self.agreement = Checkbutton(
            self,
            text="I've agreed to the Terms & Conditions",
            variable=self.has_agreed,
            onvalue=True,
            offvalue=False,
        )
        self.agreement.grid(row=4, column=1, padx=0, sticky="w")

        self.signup_btn = Button(self, text="Sign Up")
        self.signup_btn.grid(row=5, column=1, padx=0, pady=10, sticky="w")

        self.signin_option_label = Label(self, text="Already have an account?")
        self.signin_btn = Button(self, text="Sign In")
        self.signin_option_label.grid(row=6, column=1, sticky="w")
        self.signin_btn.grid(row=7, column=1, sticky="w")
        '''
#        global selected_system
#        global selected_simulation
#        global simulation
#        global mechanical_system_path
#        global mechanical_system_simulation_path

#        self.title(vc.title + ' - system description')

        '''
        if selected_system != '':
            mechanical_system_path = mechanical_system_library_path + selected_system
            mechanical_system_simulation_path = mechanical_system_path + '\\simulations\\' + selected_simulation
            if selected_simulation != '':
                with open(mechanical_system_simulation_path, 'r') as f:
                    simulation_json = json.load(f)

                    simulation.mechanical_system = simulation_json['Mechanical System']
                    simulation.initial_conditions = simulation_json['Initial Conditions']
                    simulation.integration_parameters = simulation_json['Integration Parameters']
                    simulation.equations_of_motion = simulation_json['Equations of Motion']
                    simulation.output = simulation_json['Output']
        '''
        fontsize = str(11)    
        font_parameters = vc.font + fontsize
        system_characteristics_frame = LabelFrame(self, text='System Characteristics', font= (font_parameters))
        system_characteristics_frame.grid(row = 0, column = 0, padx=10, pady=10)
        
        name_label = Label(system_characteristics_frame, text= "Name", font= (font_parameters)).grid(row=0, column=0, padx=10, pady=10, sticky='wn')
        number_dimensions_label = Label(system_characteristics_frame, text= "# Dimensions", font= (font_parameters)).grid(row=1, column=0, padx=10, pady=10, sticky='wn')
        number_particles_label = Label(system_characteristics_frame, text= "# Particles", font= (font_parameters)).grid(row=1, column=2, padx=10, pady=10, sticky='wn')
        degrees_of_freedom_label = Label(system_characteristics_frame, text= "Degrees of Freedom", font= (font_parameters)).grid(row=3, column=0, padx=10, pady=10, sticky='wn')
        parameters_label = Label(system_characteristics_frame, text= "Parameters", font= (font_parameters)).grid(row=3, column=2, padx=10, pady=10, sticky='wn')
        cartesian_coordinates_label = Label(system_characteristics_frame, text= "Cartesian Coordinates", font= (font_parameters)).grid(row=5, column=0, padx=10, pady=10, sticky='wn')
        potential_energy_label = Label(system_characteristics_frame, text= "Potential Energy", font= (font_parameters)).grid(row=5, column=2, padx=10, pady=10, sticky='wn')
        friction_coefficients_label = Label(system_characteristics_frame, text= "Friction Coefficients", font= (font_parameters)).grid(row=6, column=0, padx=10, pady=10, sticky='wn')
        driving_force_coefficients_label = Label(system_characteristics_frame, text= "Driving Force Coefficients", font= (font_parameters)).grid(row=6, column=2, padx=10, pady=10, sticky='wn')
        notes_label = Label(system_characteristics_frame, text= "Notes", font= (font_parameters)).grid(row=8, column=0, padx=10, pady=10, sticky='wn')

        fontsize = str(12)
        font_parameters = vc.font + fontsize

        self.name_input = Entry(system_characteristics_frame, width=40, font=(font_parameters), bd=2)
        self.name_input.grid(row=0, column=1, padx=10, pady=10, sticky='wn')
        self.number_dimensions_input = Entry(system_characteristics_frame, width=40, font=(font_parameters), bd=2)
        self.number_dimensions_input.grid(row=1, column=1, padx=10, pady=10, sticky='wn')
        self.number_particles_input = Entry(system_characteristics_frame, width=40, font=(font_parameters), bd=2)
        self.number_particles_input.grid(row=1, column=3, padx=10, pady=10, sticky='wn')
        self.degrees_of_freedom_input = scrolledtext.ScrolledText(system_characteristics_frame, width=40, height=4, font=(font_parameters), bd=2)
        self.degrees_of_freedom_input.grid(row=3, column=1, pady=10, padx=10, sticky='wn')
        self.parameters_input = scrolledtext.ScrolledText(system_characteristics_frame, width=40, height=4, font=(font_parameters), bd=2)
        self.parameters_input.grid(row=3, column=3, pady=10, padx=10, sticky='wn')
        self.cartesian_coordinates_input = scrolledtext.ScrolledText(system_characteristics_frame, width=40, height=4, font=(font_parameters), bd=2)
        self.cartesian_coordinates_input.grid(row=5, column=1, pady=10, padx=10, sticky='wn')
        self.potential_energy_input = scrolledtext.ScrolledText(system_characteristics_frame, width=40, height=4, font=(font_parameters), bd=2)
        self.potential_energy_input.grid(row=5, column=3, pady=10, padx=10, sticky='wn')
        self.friction_coefficients_input = scrolledtext.ScrolledText(system_characteristics_frame, width=40, height=4, font=(font_parameters), bd=2)
        self.friction_coefficients_input.grid(row=6, column=1, pady=10, padx=10, sticky='wn')
        self.driving_force_coefficients_input = scrolledtext.ScrolledText(system_characteristics_frame, width=40, height=4, font=(font_parameters), bd=2)
        self.driving_force_coefficients_input.grid(row=6, column=3, pady=10, padx=10, sticky='wn')
        self.notes_input = scrolledtext.ScrolledText(system_characteristics_frame, width=100, height=6, font=(font_parameters), bd=2)
        self.notes_input.grid(row=8, column=1, pady=10, padx=10, columnspan = 3, sticky='ewn')

#        self.show_diagram(font_parameters)

        fontsize = str(11)    
        font_parameters = vc.font + fontsize
        simulation_parameters_frame = LabelFrame(self, text='Simulation Parameters', font= (font_parameters))
        simulation_parameters_frame.grid(row = 1, column = 0, padx=10, pady=10, sticky='we', columnspan=1)

        initial_conditions_label = Label(simulation_parameters_frame, text= "Initial Conditions", font= (font_parameters)).grid(row=0, column=0, padx=10, pady=10, sticky='wn')
        self.initial_conditions_input = scrolledtext.ScrolledText(simulation_parameters_frame, width=40, height=4, font=(font_parameters), bd=2)
        self.initial_conditions_input.grid(row=0, column=1, pady=10, padx=10, sticky='wn')

        integration_parameters_label = Label(simulation_parameters_frame, text= "Integration Parameters", font= (font_parameters)).grid(row=1, column=0, padx=10, pady=10, sticky='wn')
        self.integration_parameters_input = scrolledtext.ScrolledText(simulation_parameters_frame, width=40, height=4, font=(font_parameters), bd=2)
        self.integration_parameters_input.grid(row=1, column=1, pady=10, padx=10, sticky='wn')

        '''
        if selected_simulation != '':
            self.name_input.insert(tk.END, simulation.mechanical_system['Name'])
            self.number_dimensions_input.insert(tk.END, simulation.mechanical_system['Dimensions'])
            self.number_particles_input.insert(tk.END, simulation.mechanical_system['Particles'])
            for degree_of_freedom in simulation.mechanical_system['Degrees of Freedom'].values():
                self.degrees_of_freedom_input.insert(tk.END, degree_of_freedom + '\n')
            for parameter_name, parameter_value in simulation.mechanical_system['Parameters'].items():
                self.parameters_input.insert(tk.END, parameter_name + '= ' + str(parameter_value) + '\n')
            for cartesian_coordinate_name, cartesian_coordinate_value in simulation.mechanical_system['Cartesian Coordinates'].items():
                self.cartesian_coordinates_input.insert(tk.END, cartesian_coordinate_name + '= ' + cartesian_coordinate_value + '\n')
            for potential_energy_name, potential_energy_value in simulation.mechanical_system['Potential Energy'].items():
                self.potential_energy_input.insert(tk.END, potential_energy_name + '= ' + potential_energy_value + '\n')
            for friction_coefficient_name, friction_coefficient_value in simulation.mechanical_system['Friction Coefficients'].items():
                self.friction_coefficients_input.insert(tk.END, friction_coefficient_name + '= ' + str(friction_coefficient_value) + '\n')
            for driving_force_coefficient_name, driving_force_coefficient_value in simulation.mechanical_system['Driving Force Coefficients'].items():
                self.driving_force_coefficients_input.insert(tk.END, driving_force_coefficient_name + '= ' + str(driving_force_coefficient_value) + '\n')
            self.notes_input.insert(tk.END, simulation.mechanical_system['Notes'])
            for initial_condition_name, initial_condition_value in simulation.initial_conditions.items():
                self.initial_conditions_input.insert(tk.END, initial_condition_name + '= ' + str(initial_condition_value) + '\n')
            for integration_parameters_name, integration_parameters_value in simulation.integration_parameters.items():
                self.integration_parameters_input.insert(tk.END, integration_parameters_name + '= ' + str(integration_parameters_value) + '\n')
        '''
        self.buttons_frame = Frame(self)
        self.buttons_frame.grid(row = 2, column = 0, padx=10, pady=10, columnspan=2)
#        home_button = Button(buttons_frame,text='Previous', font=(font_parameters), command=lambda: self.go_home(selected_system))
        self.previous_button = Button(self.buttons_frame,text='Previous', font=(font_parameters))
        self.previous_button.grid(row=0, column=0, padx = 10, pady=10)        
#        save_button = Button(buttons_frame,text='Save', font=(font_parameters), command=self.save)
        self.save_button = Button(self.buttons_frame,text='Save', font=(font_parameters))
        self.save_button.grid(row=0, column=1, padx = 10, pady=10)
#        run_button = Button(buttons_frame,text='Run', font=(font_parameters), command=self.run)
        self.run_button = Button(self.buttons_frame,text='Run', font=(font_parameters))
        self.run_button.grid(row=0, column=2, padx = 10, pady=10)
