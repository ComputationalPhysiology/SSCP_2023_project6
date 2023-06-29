"""
This script solves a free contraction experiment using the dynamic version
of the Land (2017) model. The force and the cell stretch (lambda) 
are plotted. The force should be lower then in a similar 
isometric experiment. The Ca transient is taken from Rice et al (2008), but 
reparameterized to be visually similar to the one used in Land et al (2017).
"""

import land2017dynamic as land_model
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0,1000,101)

#Get indices representing active force and Cai, for plotting
force_ind = land_model.monitor_indices("Ta")
lmbda_ind = land_model.state_indices("lmbda")

p = land_model.init_parameter_values(Kse=0,Cp=10.0,Ca_amplitude=0.6, Ca_diastolic=0.17, tau1=75, tau2=175)
init = land_model.init_state_values()
s = odeint(land_model.rhs,init,t,(p,))
force = []
lmbda = s[:,lmbda_ind]

#loop through the solution and compute the force:
for tn,sn in zip(t,s):
    m = land_model.monitor(sn,tn,p)
    force.append(m[force_ind])

plt.plot(t,force)
plt.title('Dynamic force')
plt.ylabel('Force (kPa)')
plt.xlabel('Time (ms)')
plt.legend()

plt.figure()
plt.plot(t,lmbda)
plt.title('Cell contraction')
plt.ylabel('Cell stretch ($\lambda$)')
plt.xlabel('Time (ms)')

plt.show()
