import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plot

#init vals.
mumax = 0.6
Ks = 0.1
Ysx = 0.5
S0 = 2
X0 = 0.1
Kd = 0.01
t = np.arange(0,25,0.2)
F = 0.3
V = 1
Sin = 10

def monod(y,t, F, V, Ks,Kd,mumax,Ysx,Sin):
    X, S = y
    mu = mumax *(S/(Ks+S))
    D = F/V
    dXdt = (mu-D)*X -(X*Kd)
    dSdt = D*(Sin-S)-(mu/Ysx)*X
    return np.array([dXdt,dSdt])

y0 = [X0,S0]
sol = odeint(monod,y0,t,args=(F, V, Ks,Kd,mumax,Ysx,Sin))
Xsol = sol[:,0]
Ssol = sol[:,1]

fig, ax = plot.subplots()
plot.plot(t,Xsol,label="Biomass")
plot.plot(t,Ssol,label="Substrate")
plot.grid()
plot.legend()
plot.title("Continuous cell culture sim.")
plot.xlabel("Time (hrs)")
plot.ylabel("Concentration (g/L)")
plot.show()




