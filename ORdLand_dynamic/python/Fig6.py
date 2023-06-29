"""
This script approximately reproduces Figure 6 in Land et al (2017),
using the dynamic version of the coupled ORd-Land model. The action potential and force development
is triggered by a stimulus current of magnitude lasting from 0 to 0.5 ms. These
are the default parameter settings in the coupled model. Isometric conditions
are obtained by setting a high stiffness of the series elastic spring (Kse = 1e6)

The following quantities are plotted:
- Intracellular calcium (left panel of fig 6, but lower amplitude than in Land paper)
- Force for different values of stretch (right panel of Land paper fig 6, but lower magnitude)
- The transmembrane potential
"""

import ORdmm_dynamic as em_model
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0,1000,10001)

#Get indices representing active force and Cai, for plotting
force_ind = em_model.monitor_indices("Ta")
cai_ind = em_model.state_indices("cai")
v_ind = em_model.state_indices("v")

#solve and plot for different values of lambda
for lmbda in np.linspace(0.9,1.1,5):
    #Ca parameters chosen to mimic left panel of Fig 6:
    p = em_model.init_parameter_values(lmbda_set=lmbda,Kse = 1e6) 
    #initialize and solve the model
    init = em_model.init_state_values(CaTrpn=0.01) 

    s = odeint(em_model.rhs,init,t,(p,))
    force = []
    cai = s[:,cai_ind]
    v = s[:,v_ind]

    #loop through the solution and compute outputs of interest:
    for tn,sn in zip(t,s):
        m = em_model.monitor(sn,tn,p)
        force.append(m[force_ind])
        #cai.append(m[cai_ind])

    plt.plot(t,force,label=f'$\lambda$ = {lmbda:.2f}')

plt.title('Fig 6 right, isometric force')
plt.ylabel('Force (kPa)')
plt.xlabel('Time (ms)')
plt.legend()

plt.figure()
plt.plot(t,cai*1000) #convert from mM to microM
plt.title('Fig 6 left, Ca transient')
plt.ylabel('Intracellular calcium concentration ($\mu$M)')
plt.xlabel('Time (ms)')

plt.figure()
plt.plot(t,v)
plt.title('Action potential')
plt.ylabel('Transmembrane potential (mV)')
plt.xlabel('Time (ms)')

plt.show()
