# Revisited chroma his

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt


v = 1.0  # velocity (convection term)
D = 0.01  # diffusion coefficient
q_max = 1.0  # max binding capacity
K_d = 0.1  # dissociation constant
n_grid = 100  # number of spatial grid points
L = 1.0  # length of the column
dx = L / (n_grid - 1)  # spatial step
x = np.linspace(0, L, n_grid)  # spatial grid
t = np.linspace(0,10,200)

def init_cond(x):
    C0 = np.zeros_like(x)
    C0[0] = 1.0
    return C0

def chroma_ode(t,C,n_grid,v,dx,D):
    dCdt = np.zeros_like(C)
    dCdt[0] = 0
    for i in range(1, n_grid -1): #i == z/dt thus dx is step size in space or L/space == dx/dzdt
        convection = -v*(C[i]-C[i-1])/dx
        diffusion = D*((C[i+1]-2*C[i]+C[i-1])/(dx**2))
        dCdt[i] = convection + diffusion
    dCdt[-1] = 0
    return dCdt

C0 = init_cond(x)

sol = solve_ivp(fun=chroma_ode,t_span=(t[0],t[-1]),y0=C0,method="LSODA",t_eval=t,args=(n_grid,v,dx,D))
C_sol = sol.y

plt.figure(figsize=(15,8))
for i in range(0,len(t),10):
    plt.plot(np.linspace(0,L,n_grid),C_sol[:,i],label=f"t = {t[i]:.3f}")
plt.legend()
plt.show()