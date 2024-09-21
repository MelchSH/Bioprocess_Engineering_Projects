import matplotlib.pyplot as plot
import numpy as np
from scipy.integrate import solve_ivp


X0 = 0.5
S0 = 20
Sf = 70 #Fed stream
F0 = 0.1 #L/h
V0 = 5
Volmax = 7
mumax = 0.4
Ks = 0.5
Yxs = 0.5
alpha = 0.3
beta = 0.05
P0 = 0
Vmin = 1e-6
Sthreshold= 0.1 #g/L
Kd = 0.01
Pkd = 0.1 #g/h Product desintegration or decay rate 
t = np.arange(0,40,0.5)

def main(t,y,F0,mumax,Ks,Sf,alpha,beta,Volmax,Sthreshold,Kd,Pkd):
    X,S,P,V = y
    
    if S <= Sthreshold:
        F = F0
    else:
        F = 0
    if V >= Volmax:
        F = 0
    D = F/V

    V = max(V,Vmin)
    mu = mumax*S/(Ks+S)
    dVdt = F
    dXdt = mu*X -D*X -X*Kd
    dSdt = -(mu*X)/Yxs + D*(Sf-S)
    if S > 0.01:
        dPdt = alpha*mu*X + beta*X
    else:
        dPdt = -Pkd
    return [dXdt,dSdt,dPdt,dVdt]

y0 = [X0,S0,P0,V0]
sol = solve_ivp(main,[t[0],t[-1]],y0,args=(F0,mumax,Ks,Sf,alpha,beta,Volmax,Sthreshold,Kd,Pkd),t_eval=t,method="LSODA",atol=1e-6,rtol=1e-6)

Xsol = sol.y[0]
Ssol = sol.y[1]
Psol = sol.y[2]
Vsol = sol.y[3]


plot.figure(figsize=(14,6))
plot.subplots_adjust(left=0.05,right=0.95)
plot.subplot(1,2,1)

plot.plot(t, Xsol, label="Biomass (g/L)")
plot.plot(t, Ssol, label="Substrate (g/L)")
plot.plot(t, Psol, label="Product (g/L)")
plot.xlabel("Time (h)")
plot.ylabel("Concentration")
plot.legend()
plot.grid(True)
plot.title("Fed-batch Simulation")

plot.subplot(1,2,2)
plot.plot(t,Vsol,label="Volume (L)")
plot.title("Volume over time")
plot.grid(True)
plot.xlabel("Time (h)")
plot.ylabel("Volume (L)")
plot.legend()
plot.show()