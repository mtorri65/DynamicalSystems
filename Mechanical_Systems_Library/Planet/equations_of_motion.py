import sympy
import os
from sympy.parsing.sympy_parser import parse_expr

def derive_equations_of_motion(simulation):
	t = sympy.symbols('t')
	degrees_of_freedom = list(simulation.mechanical_system['Degrees of Freedom'].values())
	velocities = list(simulation.mechanical_system['Velocities'].values())
	accelerations = list(simulation.mechanical_system['Accelerations'].values())
	second_derivatives_simplified = {}

	if len(simulation.equations_of_motion) != 0:
		for acceleration in simulation.mechanical_system['Accelerations'].values():
			second_derivatives_simplified[acceleration] = simulation.equations_of_motion[str(acceleration)]
	else:
		masses_names = list(simulation.mechanical_system['Masses'])
		m1 = masses_names[0]
		parameters_names = list(simulation.mechanical_system['Parameters'])
		G = parameters_names[0]
		M = parameters_names[1]
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

# calculate cartesian coordinates
		x = r * sympy.cos(theta)
		y = r * sympy.sin(theta)

# calculate kinetic energy
		v1_square = sympy.diff(x, t)**2 + sympy.diff(y, t)**2
		T1 = 1/2 * m1 * v1_square
		T = T1
		T_expand = 2*T.expand() # the factor 1/2 in the kinetic energy is not part of the kinetic energy matrix. To neautralize it, T_expand is multiplied by 2

# calculate kinetic energy matrix
		K ={ (row,column):0 for row in range(len(simulation.mechanical_system['Degrees of Freedom'])) for column in range(len(simulation.mechanical_system['Degrees of Freedom']))}
		n = 0
		for velocity_name_n in simulation.mechanical_system['Velocities']:
			velocity_n = simulation.mechanical_system['Velocities'][velocity_name_n]
			K[n, n] = (T_expand.coeff(velocity_n, 2)).simplify()
			n = n + 1
		n = 0
		for velocity_name_n in simulation.mechanical_system['Velocities']:
			velocity_n = simulation.mechanical_system['Velocities'][velocity_name_n]
			p = 0
			for velocity_name_p in simulation.mechanical_system['Velocities']:
				velocity_p = simulation.mechanical_system['Velocities'][velocity_name_p]
				if n < p:
					K[n,p] = (T_expand.coeff(velocity_n*velocity_p)).simplify()
				p = p + 1
			n = n + 1

		dKdq ={ (degree_of_freedom, row,column):0 for degree_of_freedom in range(len(simulation.mechanical_system['Degrees of Freedom'])) for row in range(len(simulation.mechanical_system['Degrees of Freedom'])) for column in range(len(simulation.mechanical_system['Degrees of Freedom']))}
		degrees_of_freedom = list(simulation.mechanical_system['Degrees of Freedom'].values())
		h = 0
		for degree_of_freedom_h in degrees_of_freedom:
			for n in range(len(simulation.mechanical_system['Degrees of Freedom'])):
				for p in range(len(simulation.mechanical_system['Degrees of Freedom'])):
					dKdq[h,p,n] = sympy.diff(K[p,n], degree_of_freedom_h).simplify()
			h = h + 1

# calculate potential energy
		V_single_particle = { (row):1 for row in range(simulation.mechanical_system['Particles'] + 1)}
		V_single_particle[0] = -G * M * m1 / r

		dVdq ={ (row, column):0 for row in range(simulation.mechanical_system['Particles']) for column in range(len(simulation.mechanical_system['Degrees of Freedom']))}
		for n in range(simulation.mechanical_system['Particles']):
			p = 0
			for degree_of_freedom_p in degrees_of_freedom:
				dVdq[n, p] = sympy.diff(V_single_particle[n], degree_of_freedom_p).simplify()
				p = p + 1

# calculate equations_of_motion
		LE = []
		momenta = {}
		accelerations = list(simulation.mechanical_system['Accelerations'].values())
		velocities = list(simulation.mechanical_system['Velocities'].values())
		for h in range(len(simulation.mechanical_system['Degrees of Freedom'])):
			term1 = 0
			term2 = 0
			term3 = 0
			term4 = 0
			momentum_h = 0
			for p in range(len(simulation.mechanical_system['Velocities'])):
				momentum_h = momentum_h + 1/2 * (K[h,p] + K[p,h])*velocities[p]
			for p in range(len(simulation.mechanical_system['Accelerations'])):
				term1 = term1 + (K[h,p] + K[p,h])*accelerations[p]
			for p in range(len(simulation.mechanical_system['Velocities'])):
				for n in range(len(simulation.mechanical_system['Velocities'])):
					term2 = term2 + (dKdq[n,h,p] + dKdq[n,p,h])*velocities[n]*velocities[p]
			for p in range(len(simulation.mechanical_system['Velocities'])):
				for n in range(len(simulation.mechanical_system['Degrees of Freedom'])):
					term3 = term3 + dKdq[h,n,p]*velocities[n]*velocities[p]
			for r in range(simulation.mechanical_system['Particles']):
				term4 = term4 + dVdq[r,h]
			Lagrange_equation = (.5*(term1 + term2 - term3) + term4).simplify()
			momenta['p_' + str(degrees_of_freedom[h]).partition('(')[0]] = momentum_h
			LE.append(Lagrange_equation)

		LE_expand = []
		for index in range(len(simulation.mechanical_system['Degrees of Freedom'])):
			LE_expand.append(LE[index].expand())
		Mat ={ (row, column):0 for row in range(len(simulation.mechanical_system['Degrees of Freedom'])) for column in range(len(simulation.mechanical_system['Degrees of Freedom']) + 1)}
		Mat[0, 0] = LE_expand[0].coeff(sympy.Derivative(degrees_of_freedom[0], (t, 2)))
		Mat[0, 1] = LE_expand[0].coeff(sympy.Derivative(degrees_of_freedom[1], (t, 2)))
		Mat[1, 0] = LE_expand[1].coeff(sympy.Derivative(degrees_of_freedom[0], (t, 2)))
		Mat[1, 1] = LE_expand[1].coeff(sympy.Derivative(degrees_of_freedom[1], (t, 2)))
		coeffs = { (row):0 for row in range(len(simulation.mechanical_system['Degrees of Freedom'])) }
		coeffs[0] = sympy.collect(LE_expand[0], [sympy.Derivative(degrees_of_freedom[0], (t, 2)), sympy.Derivative(degrees_of_freedom[1], (t, 2))], evaluate=False)
		coeffs[1] = sympy.collect(LE_expand[1], [sympy.Derivative(degrees_of_freedom[0], (t, 2)), sympy.Derivative(degrees_of_freedom[1], (t, 2))], evaluate=False)
		Mat[0,2] = -coeffs[0][1]
		Mat[1,2] = -coeffs[1][1]

		Matx = sympy.Matrix((
							(Mat[0, 0], Mat[0, 1], Mat[0, 2]),
							(Mat[1, 0], Mat[1, 1], Mat[1, 2]),
							))

		second_derivatives = sympy.solve_linear_system_LU(Matx, [sympy.Derivative(degrees_of_freedom[0], (t, 2)), sympy.Derivative(degrees_of_freedom[1], (t, 2))])
		second_derivatives_simplified[sympy.Derivative(degrees_of_freedom[0], (t, 2))] = second_derivatives[sympy.Derivative(degrees_of_freedom[0], (t, 2))].simplify()
		second_derivatives_simplified[sympy.Derivative(degrees_of_freedom[1], (t, 2))] = second_derivatives[sympy.Derivative(degrees_of_freedom[1], (t, 2))].simplify()

	return second_derivatives_simplified, momenta