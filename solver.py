# Program 03a: Linear systems in the plane. See Figure 3.8(a).
# Phase portrait with vector field. Check two systems are the same.
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
import pylab as pl

# The 2-dimensional linear system.
a, b, c, d = 3, -6, 0, -7

def dx_dt(x, t):
#    return [a*x[0] + b*x[1], c*x[0] + d*x[1] + (x[0]*x[1] - x[1]**2)]
    return [-4*x[0] - 8*x[1], -2*x[1]]

# Trajectories in forward time.
ts = np.linspace(0, 4, 100)
ic = np.linspace(0.1, 20)
for r in ic:
    for s in ic:
        x0 = [r, s]

x0 = [2, 2]

xs = odeint(dx_dt, x0, ts)

plt.plot(xs[:,0], xs[:,1], "r-")

# Trajectories in backward time.
#ts = np.linspace(0, -4, 100)
#ic = np.linspace(-1, 1, 5)
#for r in ic:
#    for s in ic:
#        x0 = [r, s]

#xs = odeint(dx_dt, x0, ts)

#plt.plot(xs[:,0], xs[:,1], "r-")

# Label the axes and set fontsizes.
plt.xlabel('x', fontsize=15)
plt.ylabel('y', fontsize=15)
plt.tick_params(labelsize=15)
plt.xlim(-2, 2)
plt.ylim(-2, 2)

# Plot the vectorfield.
X,Y = np.mgrid[-2:2:16j, -2:2:16j]
#u = a*X + b*Y
#v = c*X + d*Y + (X*Y - Y**2)
u = -4*X - 8*Y
v = -2*Y 
pl.quiver(X, Y, u, v, color = 'b')

plt.show()

import sympy as sm
x, y = sm.symbols('x, y')
P = x * (1 - x/2 - y)
Q = y * (x - 1 - y/2)
# Set P(x,y)=0 and Q(x,y)=0.
Peqn = sm.Eq(P, 0)
Qeqn = sm.Eq(Q, 0)
criticalpoints = sm.solve((Peqn, Qeqn), x, y)
print(criticalpoints)