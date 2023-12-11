import sympy
import numpy
from scipy.integrate import odeint

def integrate_equations_of_motion(simulation):
	t = sympy.symbols('t')
	masses_names = list(simulation.mechanical_system['Masses'])
	m1 = masses_names[0]

	parameters_names = list(simulation.mechanical_system['Parameters'])
	k = parameters_names[0]

	degrees_of_freedom = list(simulation.mechanical_system['Degrees of Freedom'].values())
	x1 = degrees_of_freedom[0]

	friction_coefficients_names = list(simulation.mechanical_system['Friction Coefficients'])
	x_friction = friction_coefficients_names[0]

	driving_force_coefficients_names = list(simulation.mechanical_system['Driving Force Coefficients'])
	A_x_drive = driving_force_coefficients_names[0]
	w_x_drive = driving_force_coefficients_names[1]
	phi_x_drive = driving_force_coefficients_names[2]

	velocities = list(simulation.mechanical_system['Velocities'].values())
	x1_velocity = velocities[0]

	accelerations = list(simulation.mechanical_system['Accelerations'].values())
	x1_acceleration = accelerations[0]

	momenta = list(simulation.momenta.values())
	p_x1_momentum = momenta[0]

# convert system of second order ODEs into a system of first order ODEs
	dz1dt_f = sympy.lambdify((t, m1, k, x_friction, A_x_drive, w_x_drive, phi_x_drive, x1, x1_velocity), simulation.equations_of_motion[x1_acceleration])
	dx1dt_f = sympy.lambdify((x1_velocity), x1_velocity)

	momenta_functions = []
	for momentum_index in range(len(degrees_of_freedom)):
		momentum = sympy.lambdify((t, m1, k, x_friction, A_x_drive, w_x_drive, phi_x_drive, x1, x1_velocity), momenta[momentum_index])
		momenta_functions.append(momentum)

# define solution vector
	def dSdt(S, t, m1, k, x_friction, A_x_drive, w_x_drive, phi_x_drive):
		x1, z1 = S
		return [
			dx1dt_f(z1),
			dz1dt_f(t, m1, k, x_friction, A_x_drive, w_x_drive, phi_x_drive, x1, z1),
		]

# integrate equations of motion
	sampled_times = numpy.linspace(0.0, 6.28, 100)
	m1 = 1.0
	k = 1.0
	x_friction = 1.0
	A_x_drive = 1.0
	w_x_drive = 2.0
	phi_x_drive = 0.0

	time_evolution = odeint(dSdt, y0=[1.0, 0.0], t = sampled_times, args=(m1, k, x_friction, A_x_drive, w_x_drive, phi_x_drive, ))

	momenta_values = []
	for index_step, sampled_time in enumerate(sampled_times):
		momenta_values.append([None] * len(degrees_of_freedom))
		for index_degree, degree_of_freedom in enumerate(degrees_of_freedom):
			momenta_values[index_step][index_degree] = momenta_functions[index_degree](sampled_time, m1, k, x_friction, A_x_drive, w_x_drive, phi_x_drive, time_evolution[index_step][0], time_evolution[index_step][1] )

	output = {}
	output_step = {}
	index_step = 0
	for sampled_time in sampled_times:
		index_degree = 0
		for degree_of_freedom in simulation.mechanical_system['Degrees of Freedom']:
			step_dynamic_variable_name = str(degree_of_freedom)
			output_step[step_dynamic_variable_name] = time_evolution[index_step][index_degree]
			step_dynamic_variable_name = 'v_' + str(degree_of_freedom)
			output_step[step_dynamic_variable_name] = time_evolution[index_step][index_degree + 1]
			step_dynamic_variable_name = 'p_' + str(degree_of_freedom)
			output_step[step_dynamic_variable_name] = momenta_values[index_step][index_degree // 2]
			index_degree = index_degree + 2
		output[str(sampled_time)] = output_step.copy()
		index_step = index_step + 1

	return output