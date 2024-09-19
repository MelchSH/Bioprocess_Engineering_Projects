### Chroma - Nickelback  Affinity (HisTagProt) #lol
"""
based on Langmui isotherm or Langmui absorption model, - means: absorbant acts as ideal gas at isothermal conditions, and convection-diffusion model with absorption kinetics.

TODO:
- add thermodinamic derivations to model
- add optional competitive absorption model
- add elution complexity models and args
- add non-linear behavior -> bi-Langmuir / multisite models
- add pore diffusion (for large prots.)
"""

# init vars

# qmax = 10
# C0 = 1
# Kd = 0.1
# D = 0.01
# v = 1

#model stuff
"""
mid stuff - to integrate
def langmuir_prot(qmax,C,Kd) -> float:
    return(qmax*C)/(Kd*C)
    
def mass_bal(q,t,C,D,v,qmax,Kd):
    q = langmuir_prot(qmax,C,Kd)
    dCdt = -v*()
"""
import numpy as np
import matplotlib.pyplot as plt

# Parameters
L = 10.0          # Length of the column (cm)
N = 100           # Number of spatial steps
dz = L / N        # Spatial step size
v = 1.0           # Flow velocity (cm/min)
D = 0.1           # Diffusion coefficient (cm^2/min)
q_max = 10.0      # Maximum binding capacity (mg/cm^3)
k_on = 1.0        # Association rate constant (cm^3/mg/min)
k_off = 0.1       # Dissociation rate constant (1/min)
C0_inj = 5.0      # Initial concentration of protein in the mobile phase (mg/cm^3)

# Time parameters
t_total = 20.0    # Total simulation time (min)
dt = 0.01         # Time step (min)
nt = int(t_total / dt)

# Spatial grid
z = np.linspace(0, L, N)
C = np.zeros(N)    # Concentration in mobile phase
q = np.zeros(N)    # Concentration bound on stationary phase

# Injection: Apply a pulse at the inlet
def inject(C, t):
    # Simple pulse injection at t=1 min
    if abs(t - 1.0) < dt/2:
        C[0] += C0_inj / dz  # Concentration per spatial step
    return C

# Storage for results
C_profile = []
time_points = []

# Simulation loop
for step in range(nt):
    t = step * dt
    C = inject(C, t)
    
    # Create copies to hold updated values
    C_new = C.copy()
    q_new = q.copy()
    
    for i in range(N):
        # Current concentration
        Ci = C[i]
        qi = q[i]
        
        # Compute reaction term
        reaction = k_on * Ci * (q_max - qi) - k_off * qi
        
        # Update bound concentration
        q_new[i] += reaction * dt
        # Ensure q does not exceed q_max or drop below 0
        q_new[i] = min(max(q_new[i], 0), q_max)
        
        # Compute fluxes using finite differences
        if i == 0:
            dCdz_forward = (C[i+1] - C[i]) / dz
            d2Cdz2 = (C[i+2] - 2*C[i+1] + C[i]) / dz**2
        elif i == N-1:
            dCdz_backward = (C[i] - C[i-1]) / dz
            d2Cdz2 = (C[i] - 2*C[i-1] + C[i-2]) / dz**2
        else:
            dCdz_forward = (C[i+1] - C[i]) / dz
            dCdz_backward = (C[i] - C[i-1]) / dz
            d2Cdz2 = (C[i+1] - 2*C[i] + C[i-1]) / dz**2
        
        # Convection term (central difference)
        if i == 0:
            convection = v * (C[i+1] - C[i]) / dz
        elif i == N-1:
            convection = v * (C[i] - C[i-1]) / dz
        else:
            convection = v * (C[i+1] - C[i-1]) / (2 * dz)
        #dif
        diffusion = D * d2Cdz2
        
        # Update concentration in mobile :O
        C_new[i] += (-convection + diffusion - reaction) * dt
        C_new[i] = max(C_new[i], 0)
    
        C = C_new
        q = q_new
    
    #profiles
    if step % 100 == 0:
        C_profile.append(C.copy())
        time_points.append(t)

# Plot everything!!!
plt.figure(figsize=(12, 6))
for i, C_snapshot in enumerate(C_profile):
    plt.plot(z, C_snapshot, label=f't={time_points[i]:.1f} min')
plt.xlabel('Column Length (cm)')
plt.ylabel('Protein Concentration (mg/cm³)')
plt.title('Protein Concentration Profile in Nickel Affinity Chromatography')
plt.legend()
plt.grid(True)
plt.show()

# Plot the elution profile at the outlet
plt.figure(figsize=(8, 4))
outlet_conc = [profile[-1] for profile in C_profile]
plt.plot(time_points, outlet_conc, marker='o')
plt.xlabel('Time (min)')
plt.ylabel('Outlet Protein Concentration (mg/cm³)')
plt.title('Elution Profile at Column Outlet')
plt.grid(True)
plt.show()



#plot (optional) lol