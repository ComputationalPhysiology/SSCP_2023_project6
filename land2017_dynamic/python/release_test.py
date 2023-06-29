"""
This script runs a release test for the Land 2017 model. The cell is held
at a fixed length for 300ms while driven by a prescribed calcium 
transient Then the length is reduced in 1ms to 98% of the original length
and then held fixed.

The Gotran-generated python code for model has both lambda and 
dlambda as parameters, and these must be constants. To bypass this 
limitation the model is solved in small steps, with updated parameters 
for each step. This is a sub-optimal hack, but it works for this purpose.

The expected effect of a release is a rapid drop indevloped force, 
and a small effect on the amount of calcium bound to troponin C. 
The intracellular calcium transient is prescribed and therefore not 
affected by the release.
"""

import land2017dynamic as land_model
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt


def lmbda_step(t, release_time = 300,step_length = 1,step_height=0.02):
    loc_t = t-release_time
    if loc_t < 0:
        return 1.0
    elif loc_t < step_length:
        return 1.0-step_height*loc_t/step_length
    else:
        return 1.0-step_height


t = np.linspace(0,1000,1001)

#Get indices representing active force and Cai, for plotting
force_ind = land_model.monitor_indices("Ta")
catrpn_ind = land_model.state_indices("CaTrpn")


init = land_model.init_state_values()

s = np.zeros((len(t),len(init)))
s[0,:] = init

#solve model in small steps
for i,t0 in enumerate(t[:-1]):
    t1 = t[i+1]
    lmbda_new = lmbda_step(t1)
    p = land_model.init_parameter_values(lmbda_set=lmbda_new,Kse=1e5,Ca_amplitude=0.6, Ca_diastolic=0.17, tau1=75, tau2=175)
    s[i+1,:] = odeint(land_model.rhs,init,[t0,t1],(p,))[-1]
    init = s[i+1,:]

catrpn = s[:,catrpn_ind]

force = []
#loop through the solution and compute outputs of interest:
for tn,sn in zip(t,s):
    m = land_model.monitor(sn,tn,p)
    force.append(m[force_ind])

plt.plot(t,force,label='Force')

plt.title('Active force')
plt.ylabel('Force (kPa)')
plt.xlabel('Time (ms)')
plt.legend()

plt.figure()
plt.plot(t, catrpn)
plt.title('Ca bound to troponin C')
plt.ylabel('Bound calcium concentration ()$\mu$M)')
plt.xlabel('Time (ms)')

plt.show()
