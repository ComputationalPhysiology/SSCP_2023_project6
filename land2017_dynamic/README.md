### Static version of Land 2017 model
This folder contains a dynamic version of the Land 2017 model, where lambda is a state
variable. The formulation of the passive force has been modified from the original publication,
and includes the following forces:
- A viscous component similar to Rice et al (2008)
- A series elastic element similar to Rice et al (2008)
- A passive elastic force similar to Fung type models for tissue stress. 

The model can be used for isometric contraction experiments, by setting the stiffness of the
series elastic element (Kse) very high. The formulation of the calcium transient is 
taken from Rice et al (2008), which can be parameterized to look similar to the 
Ca transient shown in Fig. 6 of Land et al (2017).
The land2017.ode file contains the model specification in Gotran ode format. The 
folder python contains the python model code generated from the .ode-file, as
well as a couple of demo scripts to test the model. 
