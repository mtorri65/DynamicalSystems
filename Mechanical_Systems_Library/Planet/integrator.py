import sympy
import numpy
from scipy.integrate import odeint

def integrate_equations_of_motion(simulation):
	t = sympy.symbols('t')
	parameters_names = list(simulation.mechanical_system['Parameters'])
	G = parameters_names[0]
	M = parameters_names[1]
	m1 = parameters_names[2]

	degrees_of_freedom = list(simulation.mechanical_system['Degrees of Freedom'].values())
	r = degrees_of_freedom[0]
	theta = degrees_of_freedom[1]

	friction_coefficients_names = list(simulation.mechanical_system['Friction Coefficients'])
	r_friction = friction_coefficients_names[0]
	theta_friction = friction_coefficients_names[1]

	driving_force_coefficients_names = list(simulation.mechanical_system['Driving Force Coefficients'])
	A_r_drive = driving_force_coefficients_names[0]
	w_r_drive = driving_force_coefficients_names[1]
	phi_r_drive = driving_force_coefficients_names[2]
	A_theta_drive = driving_force_coefficients_names[3]
	w_theta_drive = driving_force_coefficients_names[4]
	phi_theta_drive = driving_force_coefficients_names[5]

	velocities = list(simulation.mechanical_system['Velocities'].values())
	r_velocity = velocities[0]
	theta_velocity = velocities[1]

	accelerations = list(simulation.mechanical_system['Accelerations'].values())
	r_acceleration = accelerations[0]
	theta_acceleration = accelerations[1]

# convert system of second order ODEs into a system of first order ODEs
	dz1dt_f = sympy.lambdify((t, G, M, m1, r_friction, theta_friction, A_r_drive, w_r_drive, phi_r_drive, A_theta_drive, w_theta_drive, phi_theta_drive, r, theta, r_velocity, theta_velocity), simulation.equations_of_motion[r_acceleration])
	drdt_f = sympy.lambdify((r_velocity), r_velocity)
	dz2dt_f = sympy.lambdify((t, G, M, m1, r_friction, theta_friction, A_r_drive, w_r_drive, phi_r_drive, A_theta_drive, w_theta_drive, phi_theta_drive, r, theta, r_velocity, theta_velocity), simulation.equations_of_motion[theta_acceleration])
	dthetadt_f = sympy.lambdify((theta_velocity), theta_velocity)

# define solution vector
	def dSdt(S, t, G, M, m1, r_friction, theta_friction, A_r_drive, w_r_drive, phi_r_drive, A_theta_drive, w_theta_drive, phi_theta_drive):
		r, z1, theta, z2 = S
		return [
			drdt_f(z1),
			dz1dt_f(t, G, M, m1, r_friction, theta_friction, A_r_drive, w_r_drive, phi_r_drive, A_theta_drive, w_theta_drive, phi_theta_drive, r, theta, z1, z2),
			dthetadt_f(z2),
			dz2dt_f(t, G, M, m1, r_friction, theta_friction, A_r_drive, w_r_drive, phi_r_drive, A_theta_drive, w_theta_drive, phi_theta_drive, r, theta, z1, z2),
		]

# integrate equations of motion
	sampled_times = numpy.linspace(0.0, 12.56, 205)
	G = 1.0
	M = 1.0
	m1 = 3e-06
	r_friction = 0.0
	theta_friction = 0.0
	A_r_drive = 0.0
	w_r_drive = 0.0
	phi_r_drive = 0.0
	A_theta_drive = 0.0
	w_theta_drive = 0.0
	phi_theta_drive = 0.0

	time_evolution = odeint(dSdt, y0=[1.7, 0.0, 0.0, 0.353], t = sampled_times, args=(G, M, m1, r_friction, theta_friction, A_r_drive, w_r_drive, phi_r_drive, A_theta_drive, w_theta_drive, phi_theta_drive, ))

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