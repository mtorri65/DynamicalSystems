import sympy
import numpy
from scipy.integrate import odeint

def integrate_equations_of_motion(simulation):
	t = sympy.symbols('t')
	parameters_names = list(simulation.mechanical_system['Parameters'])
	g = parameters_names[0]
	m1 = parameters_names[1]
	m2 = parameters_names[2]
	L1 = parameters_names[3]
	L2 = parameters_names[4]

	degrees_of_freedom = list(simulation.mechanical_system['Degrees of Freedom'].values())
	theta1 = degrees_of_freedom[0]
	theta2 = degrees_of_freedom[1]

	friction_coefficients_names = list(simulation.mechanical_system['Friction Coefficients'])
	theta1_friction = friction_coefficients_names[0]
	theta2_friction = friction_coefficients_names[1]

	driving_force_coefficients_names = list(simulation.mechanical_system['Driving Force Coefficients'])
	A_theta1_drive = driving_force_coefficients_names[0]
	w_theta1_drive = driving_force_coefficients_names[1]
	phi_theta1_drive = driving_force_coefficients_names[2]
	A_theta2_drive = driving_force_coefficients_names[3]
	w_theta2_drive = driving_force_coefficients_names[4]
	phi_theta2_drive = driving_force_coefficients_names[5]

	velocities = list(simulation.mechanical_system['Velocities'].values())
	theta1_velocity = velocities[0]
	theta2_velocity = velocities[1]

	accelerations = list(simulation.mechanical_system['Accelerations'].values())
	theta1_acceleration = accelerations[0]
	theta2_acceleration = accelerations[1]

# convert system of second order ODEs into a system of first order ODEs
	dz1dt_f = sympy.lambdify((t, g, m1, m2, L1, L2, theta1_friction, theta2_friction, A_theta1_drive, w_theta1_drive, phi_theta1_drive, A_theta2_drive, w_theta2_drive, phi_theta2_drive, theta1, theta2, theta1_velocity, theta2_velocity), simulation.equations_of_motion[theta1_acceleration])
	dtheta1dt_f = sympy.lambdify((theta1_velocity), theta1_velocity)
	dz2dt_f = sympy.lambdify((t, g, m1, m2, L1, L2, theta1_friction, theta2_friction, A_theta1_drive, w_theta1_drive, phi_theta1_drive, A_theta2_drive, w_theta2_drive, phi_theta2_drive, theta1, theta2, theta1_velocity, theta2_velocity), simulation.equations_of_motion[theta2_acceleration])
	dtheta2dt_f = sympy.lambdify((theta2_velocity), theta2_velocity)

# define solution vector
	def dSdt(S, t, g, m1, m2, L1, L2, theta1_friction, theta2_friction, A_theta1_drive, w_theta1_drive, phi_theta1_drive, A_theta2_drive, w_theta2_drive, phi_theta2_drive):
		theta1, z1, theta2, z2 = S
		return [
			dtheta1dt_f(z1),
			dz1dt_f(t, g, m1, m2, L1, L2, theta1_friction, theta2_friction, A_theta1_drive, w_theta1_drive, phi_theta1_drive, A_theta2_drive, w_theta2_drive, phi_theta2_drive, theta1, theta2, z1, z2),
			dtheta2dt_f(z2),
			dz2dt_f(t, g, m1, m2, L1, L2, theta1_friction, theta2_friction, A_theta1_drive, w_theta1_drive, phi_theta1_drive, A_theta2_drive, w_theta2_drive, phi_theta2_drive, theta1, theta2, z1, z2),
		]

# integrate equations of motion
	sampled_times = numpy.linspace(0.0, 1.0, 102)
	g = 9.81
	m1 = 2.0
	m2 = 1.0
	L1 = 2.0
	L2 = 1.0
	theta1_friction = 0.0
	theta2_friction = 0.0
	A_theta1_drive = 0.0
	w_theta1_drive = 0.0
	phi_theta1_drive = 0.0
	A_theta2_drive = 0.0
	w_theta2_drive = 0.0
	phi_theta2_drive = 0.0

	time_evolution = odeint(dSdt, y0=[1.57, 0.0, 0.0, 1.0], t = sampled_times, args=(g, m1, m2, L1, L2, theta1_friction, theta2_friction, A_theta1_drive, w_theta1_drive, phi_theta1_drive, A_theta2_drive, w_theta2_drive, phi_theta2_drive, ))

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
			index_degree = index_degree + 2
		output[str(sampled_time)] = output_step.copy()
		index_step = index_step + 1

	return output