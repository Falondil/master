# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 11:49:25 2021

@author: Vviik
"""
 
import matplotlib.pyplot as plt

"""
ALSO CHANGE SO THAT 'HABITABLE ZONE' GRAPH ONLY PLOTS UNTIL TOPI. BECOMES MESSY OTHERWISE
"""

#----------------------------------PART 1--------------------------------------
# values
Lsun = 3.828e26 # W
S0 = 1360 # W m^-2

# file reading and data arrangement
track = []


with open("tracks/suntrack_parcol_Zinit0.01774_etaReimers0.3.dat") as f:
    for line in f:
        rowlist = line.split()
        track.append(rowlist)
        
track[0].pop(0) # removes the # from start of column names
track.pop(-1)   # removes ['#track', 'terminated'] statement
    
n = len(track)

age = [float(track[i][3]) for i in range(1,n)]
logL = [float(track[i][5]) for i in range(1,n)]
logTe = [float(track[i][6]) for i in range(1,n)]


#----------------------------------PART 2--------------------------------------
# general calculations (for any body)
L = [10**x for x in logL] # L_sun
Lwatt = [Lsun*x for x in L] # Watt
Te = [10**x for x in logTe] # K

cind = min(range(n-1), key=lambda i: abs(logL[i]))

# parameters for each body considered

bodies = ['Earth','Double Earth','Half-Earth','Quadruple-Earth'] # name of the bodies
colors = ['g','royalblue','wheat','xkcd:cyan'] # color of each body for plotting
distances = [1, 2, 0.5, 4] # AU
numb = len(bodies)

# calculations for each body
Seff = [[x/d**2 for x in L] for d in distances] # S0
Scut = [Seff[nb][cind:] for nb in range(numb)] # S0, effective instellations after current time

# Arbitrary upper cut-off value for plotting purposes
maxS = 1.5 # S0

topval = [list(filter(lambda i: i>maxS, Scut[nb]))[0] for nb in range(numb)]
topi = [Scut[nb].index(topval[nb])+cind for nb in range(numb)]

# Plotting instellation at each body w.r.t. stellar age
for nb in range(numb):
    plt.plot(age[cind:topi[nb]],Seff[nb][cind:topi[nb]],'-.',color=colors[nb],label=bodies[nb])
plt.title('Change in instellation')
plt.xlabel('Age of the Sun [yr]')
plt.ylabel('Instellation received by solar system body [S/S0]')
plt.legend()

# enter polynomial fits for T and S
c0, c1, c2, c3, c4 = 1.0140, 8.1774e-5, 1.7063e-9, -4.32415e-12, -6.6462e-16 # moist greenhouse
d0, d1, d2, d3, d4 = 0.3438, 5.8942e-5, 1.6558e-9, -3.0045e-12, -5.2983e-16 # maximum greenhouse

tlist = list(range(2600,7201,10)) 
tast = [x-5780 for x in tlist] # T_asterisk from Kopparapu et al. 2013
inSlim = [c0 + c1*t + c2*t**2 + c3*t**3 + c4*t**4 for t in tast] # inner HZ boundary limit
outSlim = [d0 + d1*t + d2*t**2 + d3*t**3 + d4*t**4 for t in tast] # outer HZ boundary limit

# Find the S limit for a given Te from the stellar track
leftlimit = [c0 + c1*t + c2*t**2 + c3*t**3 + c4*t**4 for t in [x-5780 for x in Te[cind:]]]
rightlimit = [d0 + d1*t + d2*t**2 + d3*t**3 + d4*t**4 for t in [x-5780 for x in Te[cind:]]]
# find indices closest to inner and outer HZ boundary for each body 
leftdiff = [[Scut[nb][i]-leftlimit[i] for i in range(len(Scut[nb]))] for nb in range(numb)] # differences between current S and S at the boundary (same Te)
leftindex = [leftdiff[nb].index(list(filter(lambda i: i>0, leftdiff[nb]))[0])+cind for nb in range(numb)] # first element OUTSIDE boundary
rightdiff = [[Scut[nb][i]-rightlimit[i] for i in range(len(Scut[nb]))] for nb in range(numb)]
rightindex = [cind if Scut[nb][0]>rightlimit[0] else rightdiff[nb].index(list(filter(lambda i: i<0, rightdiff[nb]))[-1])+cind for nb in range(numb)] 
# consider case where the body at no point is outside the outer HZ boundary
# in that case, time in HZ starts counting at current time

yearinHZ = [age[leftindex[nb]]-age[rightindex[nb]] for nb in range(numb)] # how long are the bodies in the HZ
strYears = ['0' if x == 0 else "{:.1e}".format(x) for x in yearinHZ] # list of strings, scientific notation 1 decimal

plt.figure()
plt.gca().set_aspect(aspect = 1/5780) # arbitrary
plt.plot(inSlim, tlist, color='r')
plt.plot(outSlim, tlist, color='b')
plt.axis([1.25, 0.2, 2600, 7200])
plt.title('Habitable zone and solar system body tracks')
plt.xlabel('Instellation [S/S0]')
plt.ylabel('Effective temperature [K]')
for nb in range(numb):
    plt.plot(Seff[nb][cind:],Te[cind:],'--',color=colors[nb],label=bodies[nb]+', '+strYears[nb]+' years in HZ') # list comprehension label, add time in HZ
    plt.plot(Seff[nb][cind],Te[cind],'x',color='k')
    plt.legend()


"""
enter T, S tracks markings each 100 Myr. Can't have markings smaller than smallest
age difference between adjacent 'age' list elements. 
agedifferences = [age[i]-age[i-1] for i in range(n-1)]
"""
timestep = 1e8
marknumber = 1+int((age[-1]-age[cind+1])/timestep)
timelist = [age[cind+1]+x*timestep for x in range(marknumber)]
markedind = [min(range(n-1), key=lambda i: abs(age[i]-timelist[x])) for x in range(marknumber)]
for nb in range(numb):
    for ind in markedind:
        plt.plot(Seff[nb][ind], Te[ind], '.', color=colors[nb])
        
