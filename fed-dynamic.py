### MUST FINISH
### ADJUST PARAMETERS


import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

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

y0 = [X0,S0,V0,P0]

def integrate(bioreactor):
    def wrapper(self,*args,**kwargs):
        def fun(t,y,*args):
            return bioreactor(self,t,y,*args[0])
        sol = solve_ivp(fun,[t[0],t[-1]],y0,args=(F0,mumax,Ks,Sf,alpha,beta,Volmax,Sthreshold,Kd,Pkd),t_eval=t,method="LSODA",atol=1e-6,rtol=1e-6)
        return sol
    return wrapper

class fedbatch():
    def __init__(self):
        pass

    @integrate
    def monod_main(self,t,y,mumax,Ks,Kd,Yxs,V,F0,alpha,beta,Sthreshold,Pkd):
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

fb1 = fedbatch()
sol = fb1.monod_main(mumax, Ks, Kd, Yxs, V0, F0, alpha, beta, Sthreshold, Pkd)


t = sol.t
Xsol = sol.y[0]
Ssol = sol.y[1]
Vsol = sol.y[2]
Psol = sol.y[3]

plt.figure()
plt.plot(t,Xsol,label="Biomass (g/L)")
plt.plot(t,Ssol,label="Substrate (g/L)")
plt.plot(t,Psol,label="Product (g/L)")
plt.legend()
plt.grid()
plt.title("Fed-Batch Bioreactor Kinetics")

plt.figure()
plt.plot(t,Vsol,label="Volume (L)")
plt.grid()
plt.legend()
plt.title("Volume change")
plt.show()




