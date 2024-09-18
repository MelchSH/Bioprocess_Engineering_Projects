from scipy.integrate import odeint
import matplotlib.pyplot as plot
import numpy as np

#init vals.
mumax = 0.5
Ks = 0.1
Ysx = 0.5
S0 = 10.0
X0 = 0.1
Kd = 0.01
t = np.arange(0,25,0.2)

def monod(y,t,mumax,Ks,Ysx,Kd):
        X, S = y
        if S > 0.01:
            mu = mumax*(S/(Ks+S))
        else:
            mu = 0
        dXdt = (mu*X)-(X*Kd)
        if S > 0.01:
            dSdt = -dXdt/Ysx
        else: 
            dSdt = 0
        S = max(S + dSdt, 0)

        return [dXdt, dSdt]
    
y0 = [X0,S0]
sol = odeint(monod,y0,t,args=(mumax,Ks,Ysx,Kd))
Xsol = sol[:,0]
Ssol = sol[:,1]

fig, ax = plot.subplots()
plot.plot(t,Xsol,"g",label="[Biomass]")
plot.plot(t,Ssol,"b",label="[Substrate]")
plot.xlabel("Time (hours)")
plot.ylabel("Concentration (g/L)")
plot.title("Batch bioreactor kinetics")
plot.legend()
plot.grid()
plot.show()


