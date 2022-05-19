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
track1 = []

filename1 = "tracks/alpha00_M100_RGB.txt"
filenum1 = filename1[-7:-4]

with open(filename1) as f:
    for line in f:
        rowlist = line.split()
        track1.append(rowlist)
        
track1[0].pop(0) # removes the # from start of column names
    
n1 = len(track1)

age1 = [float(track1[i][0]) for i in range(1,n1)]
logL1 = [float(track1[i][3]) for i in range(1,n1)]
logTe1 = [float(track1[i][1]) for i in range(1,n1)]

track2 = []

filename2 = "tracks/alpha00_M100_HB.txt"
filenum2 = filename2[-7:-4]
with open(filename2) as f:
    for line in f:
        rowlist = line.split()
        track2.append(rowlist)
        
track2[0].pop(0) # removes the # from start of column names

n2 = len(track2)

age2 = [float(track2[i][0]) for i in range(1,n2)]
logL2 = [float(track2[i][3]) for i in range(1,n2)]
logTe2 = [float(track2[i][1]) for i in range(1,n2)]

n = n1+n2-1

age = age1+[a+age1[-1] for a in age2]
logL = logL1+logL2
logTe = logTe1+logTe2

#----------------------------------PART 2--------------------------------------
# general calculations (for any body)
L = [10**x for x in logL] # L_sun
Lwatt = [Lsun*x for x in L] # Watt
Te = [10**x for x in logTe] # K

cind = min(range(n-1), key=lambda i: abs(age[i]-4.6e9))

# Plot luminosity w.r.t. stellar age
plt.figure()
plt.semilogy(age[cind:],L[cind:],'-', color = 'y')
plt.gca().yaxis.set_ticks_position('both')
plt.title('Change in luminosity (Dartmouth)')
plt.xlabel('Age of the Sun [yr]')
plt.ylabel('Luminosity [L_sun]')    

plt.figure()
plt.semilogy(age[cind:n1],L[cind:n1],linestyle='-', marker='.', color='y', mfc = 'gray', markeredgecolor='C0', label = 'pre-MS to RGB')
plt.semilogy(age[n1-1:],L[n1-1:],linestyle='-', marker='.', color = 'y', mfc = 'gray', markeredgecolor='C1', label = 'HB to AGB')
plt.gca().yaxis.set_ticks_position('both')
plt.title('Half-zoomed change in luminosity (Dartmouth)')
plt.gca().set_xlim(1.15e10, 1.25e10)
plt.xlabel('Age of the Sun [yr]')
plt.ylabel('Luminosity [L_sun]')
plt.legend()
plt.savefig('Plots/DartmouthConcatenation.pdf')

# plot Te w.r.t. stellar age
plt.figure()
plt.plot(age[cind:], Te[cind:], linestyle='--',marker='.', color = 'orange')
plt.xlabel('Age of the Sun [yr]')
plt.ylabel('Effective temperature [K]')
plt.title('Change in temperature (Dartmouth)')

#----------------------------------PART 3--------------------------------------
# instellation 

# parameters for each body considered
bodies = ['Jupiter','Saturn','Uranus','Neptune', 'Pluto'] # name of the bodies
colors = ['xkcd:light brown','xkcd:peach','xkcd:light blue','xkcd:bright blue', 'xkcd:maroon'] # color of each body for plotting
distances = [5.2, 9.54, 19.2, 30.0, 39.5] # AU, https://www.jpl.nasa.gov/edu/pdfs/ssbeads_answerkey.pdf
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



#----------------------------------PART 4a-------------------------------------
# Habitable Zone and time within

# enter polynomial fits for T and S
c0, c1, c2, c3, c4 = 1.0140, 8.1774e-5, 1.7063e-9, -4.32415e-12, -6.6462e-16 # moist greenhouse
d0, d1, d2, d3, d4 = 0.3438, 5.8942e-5, 1.6558e-9, -3.0045e-12, -5.2983e-16 # maximum greenhouse
e0, e1, e2, e3, e4 = 1.776, 2.136e-4, 2.533e-8, -1.332e-11, -3.097e-15 # recent venus
f0, f1, f2, f3, f4 = 0.32, 5.547e-5, 1.526e-9, -2.874e-12, -5.011e-16 # early mars

Tlist = list(range(2600,7201,10)) 
def IHZKopp(T):
    Tast = T-5780 # T_asterisk from Kopparapu et al. 2013
    return c0 + c1*Tast + c2*Tast**2 + c3*Tast**3 + c4*Tast**4

def OHZKopp(T):
    Tast = T-5780 # T_asterisk from Kopparapu et al. 2013
    return d0 + d1*Tast + d2*Tast**2 + d3*Tast**3 + d4*Tast**4

def RecentVenus(T):
    Tast = T-5780
    return e0 + e1*Tast + e2*Tast**2 + e3*Tast**3 + e4*Tast**4

def EarlyMars(T):
    Tast = T-5780
    return f0 + f1*Tast + f2*Tast**2 + f3*Tast**3 + f4*Tast**4

# choose which HZ boundary definition to use
funclist = [IHZKopp, OHZKopp]
boundaries = 'Kopp'
boundword = 'Conservative'

# funclist = [RecentVenus, EarlyMars]
# boundaries = 'RVEM'
# boundword = 'Optimistic'

# Plotting instellation at each body w.r.t. stellar age
plt.figure()
for nb in range(numb):
    plt.semilogy(age[cind:topi[nb]],Seff[nb][cind:topi[nb]],'-',color=colors[nb],label=bodies[nb])
plt.gca().yaxis.set_ticks_position('both')
plt.title('Change in instellation (Dartmouth)')
plt.xlabel('Age of the Sun [yr]')
plt.ylabel('Instellation received by solar system body [S/S0]')
plt.legend()

plt.figure()
for nb in range(numb):
    plt.semilogy(age[cind:],Seff[nb][cind:],'-',linewidth=2,color=colors[nb],label=bodies[nb])
plt.gca().yaxis.set_ticks_position('both')
plt.gca().set_xlim(left= 1.15e10, right= 1.24e10)
plt.semilogy(age[cind:], [funclist[0](T) for T in Te[cind:]], color='r', linewidth=1.5, linestyle='--')
plt.semilogy(age[cind:], [funclist[1](T) for T in Te[cind:]], color='b', linewidth=1.5, linestyle='--')
plt.title('Change in instellation (Dartmouth)')
plt.xlabel('Age of the Sun [yr]')
plt.ylabel('Instellation received by solar system body [S/S0]')
plt.legend()
plt.savefig('Plots/Dartmouth-instellation-'+boundaries+'.pdf')

inSlim = [IHZKopp(T) for T in Tlist] # inner HZ boundary limit
outSlim = [OHZKopp(T) for T in Tlist] # outer HZ boundary limit
rvSlim = [RecentVenus(T) for T in Tlist] # optimistic inner HZ
emSlim = [EarlyMars(T) for T in Tlist] # optimistic outer HZ

# Find the S limit for a given Te from the stellar track
leftlimit = [funclist[0](T) for T in Te[cind:]]
rightlimit = [funclist[1](T) for T in Te[cind:]]
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
for nb in range(numb):
    booleanHZ[nb][-1]=False # Stupid way to ensure that the habitablity time calculations work even if you have a track too short to plot all the timespans inside HZ
# for nb in range(numb): # plotting is for working purposes
    # plt.figure()
    # plt.plot(range(len(leftlimit)), booleanHZ[nb], color = colors[nb], label=bodies[nb])
    # plt.legend()
    # plt.figure()
    # plt.plot(range(len(leftlimit)), inIHZ[nb], color = 'r')
    # plt.plot(range(len(leftlimit)), inOHZ[nb], color = 'b')
    # plt.figure()
    # plt.plot(age[cind:], booleanHZ[nb], color = colors[nb], label=bodies[nb])
    # plt.axis([1.15e10, 1.25e10, 0, 1])
    # Make this legible
    
trueindices= [[i for i, x in enumerate(booleanHZ[nb]) if x] for nb in range(numb)]
anytrue = [i for i, x in enumerate(booleanHZ[nb]) if any(i in sl for sl in trueindices)] # is the index true for any of the planets
truestarts = [[i for i in trueindices[nb] if i-1 not in trueindices[nb]] for nb in range(numb)] # first true index in sequence
truestops = [[i for i in trueindices[nb] if i+1 not in trueindices[nb]] for nb in range(numb)] # last true index in sequence
trueranges = [[[truestarts[nb][i], truestops[nb][i]] for i in range(len(truestarts[nb]))] for nb in range(numb)]

# plot HR esque diagram
plt.figure()
plt.loglog(Te[cind:], L[cind:], linestyle='--',marker='.', color = 'gray', mfc = 'gray', markeredgecolor='k', label=boundaries)
plt.loglog([Te[cind+i] for i in anytrue], [L[cind+i] for i in anytrue], '.', color = 'g')
plt.xlabel('Effective temperature [K]')
plt.ylabel('Luminosity [L_sun]')
plt.title('HR-esque diagram (Dartmouth)')
plt.gca().invert_xaxis()
plt.legend()

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
startagepolyval = [[np.polyval(startpolys[nb][i], funclist[not inOHZ[nb][truestarts[nb][i]-1]](meanTestarts[nb][i])) if 2600<meanTestarts[nb][i]<7200 else sum(agestarts[nb][i])/2 for i in range(len(truestarts[nb]))] for nb in range(numb)] # interpolated ages of entering HZ
stopagepolyval = [[np.polyval(stoppolys[nb][i], funclist[not inOHZ[nb][truestops[nb][i]+1]](meanTestops[nb][i])) if 2600<meanTestops[nb][i]<7200 else sum(agestops[nb][i])/2 for i in range(len(truestops[nb]))] for nb in range(numb)] # interpolated ages of leaving HZ
# removing if else part of list comprehension utilizes polynomial fits where they are no longer applicable. 0.2 had negative times late when Te >~= 10000. 
middleage = [[(stopagepolyval[nb][i]+startagepolyval[nb][i])/2 for i, x in enumerate(stopagepolyval[nb])] for nb in range(numb)]

allyearsinHZ = [[stopagepolyval[nb][i] - startagepolyval[nb][i] for i in range(len(stopagepolyval[nb]))] for nb in range(numb)]

plt.figure()
for nb in range(numb):
    plt.bar([nb + 0.25*i for i in range(len(allyearsinHZ[nb]))], allyearsinHZ[nb], width=0.25, color=colors[nb], label=bodies[nb])
    plt.legend()
plt.xticks(range(numb), bodies)
plt.ylabel('timespan [years]')
plt.title('Timespans inside the Habitable Zone (Dartmouth)')

for nb in range(numb):
    plt.figure()
    plt.bar([x for x in middleage[nb]], allyearsinHZ[nb], width=allyearsinHZ[nb], color=colors[nb], label=bodies[nb])
    # plt.gca().set_xscale("log")
    plt.gca().set_xlim(right=age[-1])
    plt.xlabel('[years]')
    plt.ylabel('timespan [years]')
    plt.title('Timespans inside the Habitable Zone (Dartmouth)')
    plt.legend()
    plt.savefig('Plots/Dartmouth'+bodies[nb]+'TIHZ'+boundaries+'.pdf')

strYears = [['0' if x == 0 else "{:.1e}".format(x) for x in allyearsinHZ[nb]] for nb in range(numb)] # list of strings, scientific notation 1 decimal

# #----------------------------------PART 4b-------------------------------------
# Habitable Zone plotting

# Base case HZ plot
plt.figure()
plt.gca().set_aspect(aspect = 1.05/5780) # arbitrary
plt.gca().yaxis.set_ticks_position('both')
plt.plot(inSlim, Tlist, color='r')
plt.plot(outSlim, Tlist, color='b')
plt.axis([1.25, 0.2, 2600, 7200])
plt.title('First pass through '+boundword+' HZ (Dartmouth)')
plt.xlabel('Instellation [S/S0]')
plt.ylabel('Effective temperature [K]')
for nb in range(numb):
    plt.plot(Seff[nb][cind:topi[nb]],Te[cind:topi[nb]],linestyle='-',linewidth=1,marker='.',color=colors[nb],label=bodies[nb])
    plt.plot(Seff[nb][cind],Te[cind],'o',color='k')
    plt.legend()

# # Same plot for each planet, but full
# for nb in range(numb):
#     plt.figure()
#     plt.gca().set_aspect(aspect = 1.8/5780) # arbitrary
#     plt.plot(inSlim, Tlist, color='r')
#     plt.plot(outSlim, Tlist, color='b')
#     plt.plot(emSlim, Tlist, color='C0')
#     plt.plot(rvSlim, Tlist, color='C1')
#     plt.axis([2, 0.2, 2600, 7200])
#     plt.title('Habitable zone track of '+bodies[nb]+' (Dartmouth)')
#     plt.xlabel('Instellation [S/S0]')
#     plt.ylabel('Effective temperature [K]')
#     plt.plot(Seff[nb][cind:],Te[cind:],linestyle='-',linewidth=1,marker='.',color=colors[nb],label=bodies[nb]+': '+str(strYears[nb])+' years in HZ')
#     plt.plot(Seff[nb][-1],Te[-1],'x',color='k')
#     plt.legend(loc='upper right')



# #----------------------------------EXTRA---------------------------------------
# # Extra plotting code, must be run manually


# plt.figure()
# for nb in range(numb):
#     plt.bar([nb + 0.25*i for i in range(len(allyearsinHZ[nb]))], allyearsinHZ[nb], width=0.25, color=colors[nb])
#     plt.bar([nb + 0.25*i for i in range(len(allyearsinHZPARSEC[nb]))], allyearsinHZPARSEC[nb], width=0.25, fill = False, hatch='//')
# plt.xticks(range(numb), bodies)
# plt.ylabel('timespan [years]')
# plt.title('Timespans inside the '+boundword+' Habitable Zone')
# plt.bar(0, height=0, width=0, facecolor='grey', label='Dartmouth')
# plt.bar(0, height = 0, width=0, fill = False, hatch='//', label ='PARSEC')
# plt.legend()


# plt.savefig('Plots/'+boundaries+'-dartmouth+parsec-TIHZ.pdf')

