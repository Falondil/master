# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 11:49:25 2021

@author: Vviik
"""
 
import matplotlib.pyplot as plt
import numpy as np

#----------------------------------PART 1--------------------------------------
# values
Lsun = 3.828e26 # W
S0 = 1360 # W m^-2
maxS = 1.5 # S0. Arbitrary upper cut-off value for plotting purposes

# file reading and data arrangement
track = []

filename = "tracks/suntrack_parcol_Zinit0.01774_etaReimers0.3.dat"

with open(filename) as f:
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

# Plot luminosity w.r.t. stellar age
plt.figure()
plt.semilogy(age[cind:],L[cind:],'-', color = 'y')
plt.gca().yaxis.set_ticks_position('both')
plt.title('Change in luminosity')
plt.xlabel('Age of the Sun [yr]')
plt.ylabel('Luminosity [L_sun]')

plt.figure()
plt.plot(age[cind:],L[cind:],'-', color = 'y')
plt.gca().yaxis.set_ticks_position('both')
plt.title('Change in luminosity')
plt.xlabel('Age of the Sun [yr]')
plt.ylabel('Luminosity [L_sun]')

plt.figure()
plt.plot(age[cind:],L[cind:],linestyle='-', marker='.', color = 'y')
plt.gca().yaxis.set_ticks_position('both')
plt.title('Half-zoomed change in luminosity')
plt.axis([1.15e10, 1.25e10, 0, 2600])
plt.xlabel('Age of the Sun [yr]')
plt.ylabel('Luminosity [L_sun]')

plt.figure()
plt.semilogy(age[cind:],L[cind:],linestyle='-', marker='.', color = 'y', label=filename)
plt.gca().yaxis.set_ticks_position('both')
plt.title('Half-zoomed change in luminosity')
plt.gca().set_xlim(1.15e10, 1.25e10)
plt.xlabel('Age of the Sun [yr]')
plt.ylabel('Luminosity [L_sun]')
plt.legend()

plt.figure()
plt.semilogy(age[cind:],L[cind:],linestyle='-', marker='.', color = 'y', label=filename)
plt.gca().yaxis.set_ticks_position('both')
plt.title('Zoomed change in luminosity')
plt.gca().set_xlim(1.19e10, 1.202e10)
plt.xlabel('Age of the Sun [yr]')
plt.ylabel('Luminosity [L_sun]')
plt.legend()

# [Seff[nb][102+cind] for nb in range(numb)] # for the instellation right after the jump down. Paste this after Seff has been calculated

#----------------------------------PART 3--------------------------------------
# instellation 

# parameters for each body considered
bodies = ['Jupiter','Saturn','Uranus','Neptune', 'Pluto'] # name of the bodies
colors = ['xkcd:light brown','xkcd:peach','xkcd:light blue','xkcd:bright blue', 'xkcd:maroon'] # color of each body for plotting
distances = [5.2, 9.6, 19.2, 30.0, 39.5] # AU, https://www.jpl.nasa.gov/edu/pdfs/ssbeads_answerkey.pdf
numb = len(bodies)

# calculations for each body
Seff = [[x/d**2 for x in L] for d in distances] # S0
Scut = [Seff[nb][cind:] for nb in range(numb)] # S0, effective instellations after current time
roughLlimits = [[0.25*d**2, 0.9*d**2] for d in distances] # useful for graph reading

topval = []
topi = []
for nb in range(numb):
    try:
        topval += [list(filter(lambda i: i>maxS, Scut[nb]))[0]] # first value exceeding maxS
        topi += [Scut[nb].index(topval[nb])+cind] # index of that value
    except IndexError:
        topval += [max(Scut[nb])] # max value instead if it never exceeds maxS
        topi += [len(Seff[nb])] # entire length should be plotted

# Plotting instellation at each body w.r.t. stellar age
plt.figure()
for nb in range(numb):
    plt.semilogy(age[cind:topi[nb]],Seff[nb][cind:topi[nb]],'-.',color=colors[nb],label=bodies[nb])
plt.gca().yaxis.set_ticks_position('both')
plt.title('Change in instellation')
plt.xlabel('Age of the Sun [yr]')
plt.ylabel('Instellation received by solar system body [S/S0]')
plt.legend()

#----------------------------------PART 4a-------------------------------------
# Habitable Zone and time within

# enter polynomial fits for T and S
c0, c1, c2, c3, c4 = 1.0140, 8.1774e-5, 1.7063e-9, -4.32415e-12, -6.6462e-16 # moist greenhouse
d0, d1, d2, d3, d4 = 0.3438, 5.8942e-5, 1.6558e-9, -3.0045e-12, -5.2983e-16 # maximum greenhouse

Tlist = list(range(2600,7201,10)) 
def IHZKopp(T):
    Tast = T-5780 # T_asterisk from Kopparapu et al. 2013
    return c0 + c1*Tast + c2*Tast**2 + c3*Tast**3 + c4*Tast**4

def OHZKopp(T):
    Tast = T-5780 # T_asterisk from Kopparapu et al. 2013
    return d0 + d1*Tast + d2*Tast**2 + d3*Tast**3 + d4*Tast**4

funclist = [IHZKopp, OHZKopp]

inSlim = [IHZKopp(T) for T in Tlist] # inner HZ boundary limit
outSlim = [OHZKopp(T) for T in Tlist] # outer HZ boundary limit

# Find the S limit for a given Te from the stellar track
leftlimit = [IHZKopp(T) for T in Te[cind:]]
rightlimit = [OHZKopp(T) for T in Te[cind:]]
# find indices closest to inner and outer HZ boundary for each body 
leftdiff = [[Scut[nb][i]-leftlimit[i] for i in range(len(Scut[nb]))] for nb in range(numb)] # differences between current S and S at the boundary (same Te)
leftindex = [leftdiff[nb].index(list(filter(lambda i: i>0, leftdiff[nb]))[0])+cind for nb in range(numb)] # first element OUTSIDE IHZ
rightdiff = [[Scut[nb][i]-rightlimit[i] for i in range(len(Scut[nb]))] for nb in range(numb)]
rightindex = [cind if Scut[nb][0]>rightlimit[0] else rightdiff[nb].index(list(filter(lambda i: i>0, rightdiff[nb]))[0])+cind-1 for nb in range(numb)] # last point outside OHZ
# consider case where the body at no point is outside the outer HZ boundary
# in that case, time in HZ starts counting at current time

inIHZ = [[leftlimit[i]>Scut[nb][i] for i in range(len(Scut[nb]))] for nb in range(numb)]
inOHZ = [[Scut[nb][i]>rightlimit[i] for i in range(len(Scut[nb]))] for nb in range(numb)]
# Boolean HZ. perhaps alternate way of getting indices. Does not distinguish IHZ and OHZ. 
booleanHZ = [[inIHZ[nb][i] and inOHZ[nb][i] for i in range(len(Scut[nb]))] for nb in range(numb)]
for nb in range(numb): # plotting is for working purposes
    plt.figure()
    plt.plot(range(len(leftlimit)), booleanHZ[nb], color = colors[nb], label=bodies[nb])
    plt.legend()
    # plt.figure()
    # plt.plot(range(len(leftlimit)), inIHZ[nb], color = 'r')
    # plt.plot(range(len(leftlimit)), inOHZ[nb], color = 'b')
    # plt.figure()
    # plt.plot(age[cind:], booleanHZ[nb], color = colors[nb], label=bodies[nb])
    # plt.axis([1.15e10, 1.25e10, 0, 1])
    
trueindices= [[i for i, x in enumerate(booleanHZ[nb]) if x] for nb in range(numb)]
truestarts = [[i for i in trueindices[nb] if i-1 not in trueindices[nb]] for nb in range(numb)] # first true index in sequence
truestops = [[i for i in trueindices[nb] if i+1 not in trueindices[nb]] for nb in range(numb)] # last true index in sequence
trueranges = [[[truestarts[nb][i], truestops[nb][i]] for i in range(len(truestarts[nb]))] for nb in range(numb)]

# preliminary timespan calculation
approxyearsinHZ = [[age[cind+x[1]]-age[cind+x[0]] for x in trueranges[nb]] for nb in range(numb)]
approxstrYears = [['0' if x == 0 else "{:.1e}".format(x) for x in y] for y in approxyearsinHZ]

# list comprehension magic, ADD a polynomial fit between first index outside HZ boundary and first index inside HZ boundary for each of the two boundaries.
Sstarts = [[Scut[nb][x-1:x+1] for x in truestarts[nb]] for nb in range(numb)] # [last S outside, first S inside]
Sstops = [[Scut[nb][x:x+2] for x in truestops[nb]] for nb in range(numb)] # [last S inside, first S outside]
agestarts = [[age[cind+x-1:cind+x+1] for x in truestarts[nb]] for nb in range(numb)] # same as above
agestops = [[age[cind+x:cind+x+2] for x in truestops[nb]] for nb in range(numb)]
meanTestarts = [[(Te[x+cind-1]+Te[x+cind])/2 for x in truestarts[nb]] for nb in range(numb)]
meanTestops = [[(Te[x+cind]+Te[x+cind+1])/2 for x in truestops[nb]] for nb in range(numb)]

startpolys = [[list(np.polyfit(Sstarts[nb][i], agestarts[nb][i], 1)) for i in range(len(Sstarts[nb]))] for nb in range(numb)] # list of polynomial coefficients for age(S) for each time entering HZ
stoppolys = [[list(np.polyfit(Sstops[nb][i], agestops[nb][i], 1)) for i in range(len(Sstops[nb]))] for nb in range(numb)] # list of polynomial coefficients for age(S) for each time leaving HZ
startagepolyval = [[np.polyval(startpolys[nb][i], funclist[not inOHZ[nb][truestarts[nb][i]-1]](meanTestarts[nb][i])) for i in range(len(truestarts[nb]))] for nb in range(numb)] # interpolated ages of entering HZ
stopagepolyval = [[np.polyval(stoppolys[nb][i], funclist[not inOHZ[nb][truestops[nb][i]+1]](meanTestops[nb][i])) for i in range(len(truestops[nb]))] for nb in range(numb)] # interpolated ages of leaving HZ

allyearsinHZ = [[stopagepolyval[nb][i] - startagepolyval[nb][i] for i in range(len(stopagepolyval[nb]))] for nb in range(numb)]

plt.figure()
for nb in range(numb):
    plt.bar([nb + 0.25*i for i in range(len(allyearsinHZ[nb]))], allyearsinHZ[nb], width=0.25, color=colors[nb], label=bodies[nb])
    plt.legend()
plt.xticks(range(numb), bodies)
plt.ylabel('timespan [years]')
plt.title('Timespans inside the Habitable Zone')

# keep these outdated fits maybe so that the double ranges with a quick outdip for Jupiter and Saturn are added. 
leftS = [Seff[nb][leftindex[nb]-1:leftindex[nb]+1] for nb in range(numb)] # [last S inside IHZ, first S outside IHZ]
leftAge = [age[leftindex[nb]-1:leftindex[nb]+1] for nb in range(numb)]
leftpolys = [list(np.polyfit(leftS[nb], leftAge[nb], 1)) for nb in range(numb)]
leftTeMean = [(Te[leftindex[nb]-1]+Te[leftindex[nb]])/2 for nb in range(numb)] # find average Te between last point inside IHZ and first outside IHZ
ageleftintersect = [np.polyval(leftpolys[nb], IHZKopp(leftTeMean[nb])) for nb in range(numb)] # calculate age from polyval of the Kopparapu S at the IHZ

rightS = [Seff[nb][rightindex[nb]:rightindex[nb]+2] for nb in range(numb)] # [last S outside OHZ, first S inside OHZ]
rightAge = [age[rightindex[nb]:rightindex[nb]+2] for nb in range(numb)]
rightpolys = [list(np.polyfit(rightS[nb], rightAge[nb], 1)) for nb in range(numb)]
rightTeMean =  [(Te[rightindex[nb]]+Te[rightindex[nb]+1])/2 for nb in range(numb)] # find average Te between last point outside OHZ and first inside OHZ
agerightintersect = [np.polyval(rightpolys[nb], OHZKopp(rightTeMean[nb])) for nb in range(numb)] # calculate age from polyval of the Kopparapu S at the OHZ

yearinHZ = [ageleftintersect[nb]-agerightintersect[nb] for nb in range(numb)] # how long are the bodies in the HZ
strYears = ['0' if x == 0 else "{:.1e}".format(x) for x in yearinHZ] # list of strings, scientific notation 1 decimal

#----------------------------------PART 4b-------------------------------------
# Habitable Zone plotting

# Base case HZ plot
plt.figure()
plt.gca().set_aspect(aspect = 1/5780) # arbitrary
plt.gca().yaxis.set_ticks_position('both')
plt.plot(inSlim, Tlist, color='r')
plt.plot(outSlim, Tlist, color='b')
plt.axis([1.25, 0.2, 2600, 7200])
plt.title('Habitable zone and solar system body tracks')
plt.xlabel('Instellation [S/S0]')
plt.ylabel('Effective temperature [K]')
for nb in range(numb):
    plt.plot(Seff[nb][cind:topi[nb]],Te[cind:topi[nb]],linestyle='--',marker='.',color=colors[nb],label=bodies[nb]+', '+strYears[nb]+' years in HZ') # list comprehension label, add time in HZ
    plt.plot(Seff[nb][cind],Te[cind],'x',color='k')
    plt.legend()

#  SATURN BRIEFLY BOUNCES OUTSIDE OHZ
# plt.figure()
# plt.plot(inSlim, Tlist, color='r')
# plt.plot(outSlim, Tlist, color='b')
# plt.plot(Seff[1][cind:topi[1]],Te[cind:topi[1]],linestyle='--',marker='.',color=colors[1],label=bodies[1]+', '+strYears[1]+' years in HZ') # list comprehension label, add time in HZ
# plt.axis([0.4, 0.2, 4300, 4600])

# Same plot but only including tracks beyond first spike in instellation
# plt.figure()
# plt.gca().set_aspect(aspect = 1/5780) # arbitrary
# plt.plot(inSlim, Tlist, color='r')
# plt.plot(outSlim, Tlist, color='b')
# plt.axis([1.25, 0.2, 2600, 7200])
# plt.title('Habitable zone and solar system body tracks')
# plt.xlabel('Instellation [S/S0]')
# plt.ylabel('Effective temperature [K]')
# for nb in range(numb):
#     plt.plot(Seff[nb][topi[nb]:],Te[topi[nb]:],linestyle='--',marker='.',color=colors[nb],label=bodies[nb]+', '+strYears[nb]+' years in HZ') # list comprehension label, add time in HZ
#     plt.legend()