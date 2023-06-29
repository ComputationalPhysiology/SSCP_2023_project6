"""
This script runs a release test for the Land 2017 model. The Gotran-generated
python code for model has both lambda and dlambda as parameters, and these
must be constants. To avoid this limitation the model is solved in
small steps, with updated parameters for each step. This is a sub-optimal
hack, but it works for this purpose.
"""

import ORdmm_Land as em_model
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
force_ind = em_model.monitor_indices("Ta")
cai_ind = em_model.state_indices("cai")

init = em_model.init_state_values(CaTrpn=0.01)
s = np.zeros((len(t),len(init)))
s[0,:] = init

#solve model in small steps
for i,t0 in enumerate(t[:-1]):
    t1 = t[i+1]
    lmbda_new = lmbda_step(t1)
    lmbda_prev = lmbda_step(t0)
    dlmbda = (lmbda_new-lmbda_prev)/(t1-t0)
    p = em_model.init_parameter_values(lmbda=lmbda_new,dLambda=dlmbda) #,Ca_amplitude=0.6, Ca_diastolic=0.17, tau1=75, tau2=175)
    s[i+1,:] = odeint(em_model.rhs,init,[t0,t1],(p,))[-1]
    init = s[i+1,:]
force = []
cai = s[:,cai_ind]


#loop through the solution and compute outputs of interest:
for tn,sn in zip(t,s):
    m = em_model.monitor(sn,tn,p)
    force.append(m[force_ind])
    #cai.append(m[cai_ind])

plt.plot(t,force,label='Force')

plt.title('Active force')
plt.ylabel('Force (kPa)')
plt.xlabel('Time (ms)')
plt.legend()

plt.figure()
plt.plot(t,cai*1000) #from mM to microM
plt.title('Intracellular calcium')
plt.ylabel('Cai ($\mu$M)')
plt.xlabel('Time (ms)')

plt.show()
