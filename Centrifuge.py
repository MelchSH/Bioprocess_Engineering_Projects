import numpy as np
import matplotlib.pyplot as plot

omega = 10000  # angular velocity in rad/s
rf = 1000  # kg/m³ (water) - fluid density
rp = 2500  # kg/m³ (example: silica) - particle density 
dp = 1e-6  # meters - particle diameter
eta = 0.001  # Pa.s (water) - fluid viscosity
init_rad = 0.5
rad = 1  # meters
g = 9.81  # gravitational acceleration m/s²
mass = 0.02

def sedimentation_velocity(rp,rf,dp,eta,omega,r):
    cen_acc = (omega**2) *r
    print(cen_acc,rp-rf,dp**2)
    return (2/9)*(cen_acc*(rp-rf)*dp**2)/eta

tstep = 1
tmax = 24
t = np.arange(0,tmax,tstep)
r = np.full_like(t,init_rad,dtype=float)
print(r[0])
v_s = sedimentation_velocity(rp,rf,dp,eta,omega,r[0])
print("r passed")

for i in range(1, len(t)):
    v_s = sedimentation_velocity(rp,rf,dp,eta,omega,r[i-1])
    r[i] = r[i-1] + v_s*tstep
    print(v_s)
    
    if r[i] >= rad:
        r[i] = rad
        break


plot.plot(t[:i+1],r[:i+1])
plot.xlabel("Time (s)")
plot.ylabel("Sedimentation")
plot.show()



