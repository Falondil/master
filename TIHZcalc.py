# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 11:49:25 2021

@author: Vviik
"""
 
import matplotlib.pyplot as plt
import numpy as np

#----------------------------------PART 1--------------------------------------
# file reading and data arrangement

fileselect = input('Enter 1, 2, 3 for PARSEC, Dartmouth or MIST solar evolution tracks: ')
if fileselect == '1':
    filename1 = "tracks/Z0.017Y0.279O_IN0.00OUTA1.74_F7_M1.00.TAB"
    filename2 = "tracks/Z0.017Y0.279O_IN0.00OUTA1.74_F7_M1.00.TAB.HB"
    solarmodel = 'PARSEC'
elif fileselect == '2':
    filename1 = "tracks/alpha00_M100_RGB.txt"
    filename2 = "tracks/alpha00_M100_HB.txt"
    solarmodel = 'Dartmouth'
elif fileselect == '3':
    filename = "tracks/MIST1M.track.eep"
    solarmodel = 'MIST'
elif fileselect == '4':
    filename = "tracks/SolarCalibratedRGB.tab"
    solarmodel = 'Solar PARSEC RGB'
else:
    print('Invalid track choice')
    quit()

# PARSEC has split RGB and HB-AGB tracks to concatenate
if fileselect == '1':
    track1 = []

    with open(filename1) as f:
        for line in f:
            rowlist = line.split()
            track1.append(rowlist)
            
    track1.pop(-1) # removes end row 

    age1 = [float(x[2]) for x in track1[5:]]
    logL1 = [float(x[4]) for x in track1[5:]]
    logTe1 = [float(x[5]) for x in track1[5:]]
    PHS1 = [float(x[95]) for x in track1[5:]]
    n1 = len(age1)

    track2 = []

    with open(filename2) as f:
        for line in f:
            rowlist = line.split()
            track2.append(rowlist)
            
    track2.pop(-1) # removes end row 
            
    age2 = [float(x[2]) for x in track2[5:]]
    logL2 = [float(x[4]) for x in track2[5:]]
    logTe2 = [float(x[5]) for x in track2[5:]]
    PHS2 = [float(x[95]) for x in track2[5:]]
    n2 = len(age2)

    n = n1+n2+1

    age = age1+[a+age1[-1] for a in age2]
    logL = logL1+logL2
    logTe = logTe1+logTe2
    PHS = PHS1+PHS2
    
# Dartmouth has split RGB and HB-AGB tracks to concatenate
elif fileselect == '2':
    track1 = []

    with open(filename1) as f:
        for line in f:
            rowlist = line.split()
            track1.append(rowlist)
            
    track1[0].pop(0)
    
    age1 = [float(x[0]) for x in track1[1:]]
    logL1 = [float(x[3]) for x in track1[1:]]
    logTe1 = [float(x[1]) for x in track1[1:]]
    n1 = len(age1)
    
    track2 = []
    
    with open(filename2) as f:
        for line in f:
            rowlist = line.split()
            track2.append(rowlist)
    
    age2 = [float(x[0]) for x in track2[1:]]
    logL2 = [float(x[3]) for x in track2[1:]]
    logTe2 = [float(x[1]) for x in track2[1:]]
    n2 = len(age2)
    
    n = n1+n2+1
    
    age = age1+[a+age1[-1] for a in age2]
    logL = logL1+logL2
    logTe = logTe1+logTe2
    
# MIST does not require concatenation
elif fileselect=='3':
    track = []
    with open(filename) as f:
        for line in f:
            rowlist = line.split()
            track.append(rowlist)
    
    age = [float(track[i][0]) for i in range(12,1420)] # end-point chosen such that it ends before post-AGB. Visual choice from HR diagram
    logL = [float(track[i][6]) for i in range(12,1420)]
    logTe = [float(track[i][11]) for i in range(12,1420)]

    n = len(age)+1
    n1 = 605 # determined visually from plt.semilogy(age[580:6XX], L[580:6XX], '.') by changing XX down until the last point is the tip

# Solarcalibrated    
else:
    track = []
    with open(filename) as f:
        for line in f:
            rowlist = line.split()
            track.append(rowlist) 
    track.pop(-1) # removes end row 
    
    n = len(track)
    age = [float(track[i][2]) for i in range(5,n)]
    logL = [float(track[i][4]) for i in range(5,n)]
    logTe = [float(track[i][5]) for i in range(5,n)]
    n = len(age)
    n1 = n
    
#----------------------------------PART 2--------------------------------------
# general calculations (for any body)
L = [10**x for x in logL] # L_sun
Te = [10**x for x in logTe] # K

cind = min(range(n-1), key=lambda i: abs(age[i]-4.6e9))

# Plot luminosity w.r.t. stellar age
plt.figure()
plt.semilogy(age[cind:],L[cind:],'-', color = 'y')
plt.gca().yaxis.set_ticks_position('both')
plt.title('Change in luminosity ('+solarmodel+')')
plt.xlabel('Age of the Sun [yr]')
plt.ylabel('Luminosity '+r'$[L/L_\bigodot]$')    

# plot Te w.r.t. stellar age
plt.figure()
plt.plot(age[cind:], Te[cind:], linestyle='--',marker='.', color = 'orange')
plt.xlabel('Age of the Sun [yr]')
plt.ylabel('Effective temperature [K]')
plt.title('Change in temperature ('+solarmodel+')')

#----------------------------------PART 3--------------------------------------
# instellation 
maxS = 1.5 # S0. Arbitrary upper cut-off value for plotting purposes

# parameters for each body considered
bodies = ['Jupiter','Saturn','Uranus','Neptune', 'Pluto'] # name of the bodies
colors = ['xkcd:light brown','xkcd:peach','xkcd:light blue','xkcd:bright blue', 'xkcd:maroon'] # color of each body for plotting
distances = [5.2, 9.57, 19.17, 30.18, 39.48] # AU, https://nssdc.gsfc.nasa.gov/planetary/factsheet/planet_table_ratio.html
numb = len(bodies)

barwidth = 0.3

# Uncomment these lines to get sum of TIHZ graph
startdistance = 5
distances = [startdistance+barwidth*r for r in range(int((39.5+barwidth-startdistance)/barwidth))] # list from startdistance to roughly 39.5 AU 
bodies = [str(d) for d in distances]
numb = len(distances)
colors = ['C'+str(i) for i in range(numb)]

# calculations for each body
Seff = [[x/d**2 for x in L] for d in distances] # S0
Scut = [Seff[nb][cind:] for nb in range(numb)] # S0, effective instellations after current time

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

# enter polynomial fits for T and S from Kopp2013
c0, c1, c2, c3, c4 = 1.0140, 8.1774e-5, 1.7063e-9, -4.32415e-12, -6.6462e-16 # moist greenhouse
d0, d1, d2, d3, d4 = 0.3438, 5.8942e-5, 1.6558e-9, -3.0045e-12, -5.2983e-16 # maximum greenhouse
e0, e1, e2, e3, e4 = 1.7753, 1.4316e-4, 2.9875e-9, -7.5702e-12, -1.1635e-15 # recent venus, Kopp2014: 1.776, 2.136e-4, 2.533e-8, -1.332e-11, -3.097e-15
f0, f1, f2, f3, f4 = 0.3179, 5.4513e-5, 1.5313e-9, -2.7786e-12, -4.8997e-16 # early mars, Kopp2014: 0.32, 5.547e-5, 1.526e-9, -2.874e-12, -5.011e-16
g0, g1, g2, g3, g4 = 1.0512, 1.3242e-4, 1.5418e-8, -7.9895e-12, -1.8328e-15 # runaway greenhouse

# Ramirez2018
h0, h1, h2, h3, h4 = 0.3050, 2.216e-5, 4.1913e-9, -1.3177e-12, 1.1796e-16 # Methane: 0.1 CH4/CO2. 

Tlist = list(range(2600,7201,10)) 
def IHZKopp(T): # moist greenhouse
    Tast = T-5780 # T_asterisk from Kopparapu et al. 2013
    return c0 + c1*Tast + c2*Tast**2 + c3*Tast**3 + c4*Tast**4

def OHZKopp(T): # maximum greenhouse
    Tast = T-5780
    return d0 + d1*Tast + d2*Tast**2 + d3*Tast**3 + d4*Tast**4

def RecentVenus(T): # Recent Venus empiric limit
    Tast = T-5780
    return e0 + e1*Tast + e2*Tast**2 + e3*Tast**3 + e4*Tast**4

def EarlyMars(T): # Early Mars empiric limit
    Tast = T-5780
    return f0 + f1*Tast + f2*Tast**2 + f3*Tast**3 + f4*Tast**4

def RunawayKopp(T): # runaway greenhouse
    Tast = T-5780 
    return g0 + g1*Tast + g2*Tast**2 + g3*Tast**3 + g4*Tast**4

def Methane(T): # 0.1 CH4/CO2 from Ramirez&Kaltenegger 2018
    Tast = T-5780 
    return h0 + h1*Tast + h2*Tast**2 + h3*Tast**3 + h4*Tast**4

# choose which HZ boundary definition to use
# funclist = [RunawayKopp, OHZKopp]
# boundaries = 'Kopp'
# boundword = 'Conservative'

funclist = [RecentVenus, EarlyMars]
boundaries = 'RVEM'
boundword = 'Optimistic'

# Plotting instellation at each body w.r.t. stellar age
plt.figure()
for nb in range(numb):
    plt.semilogy(age[cind:topi[nb]],Seff[nb][cind:topi[nb]],'-',color=colors[nb],label=bodies[nb])
plt.gca().yaxis.set_ticks_position('both')
plt.title('Change in instellation ('+solarmodel+')')
plt.xlabel('Age of the Sun [yr]')
plt.ylabel('Instellation received by solar system body '+r'$[S/S_\bigoplus]$')
plt.legend()

plt.figure()
for nb in range(numb):
    plt.semilogy(age[cind:],Seff[nb][cind:],'-',linewidth=2,color=colors[nb],label=bodies[nb])
plt.gca().yaxis.set_ticks_position('both')
plt.gca().set_xlim(left= age[-1]*0.95, right= age[-1]*1.005)
plt.semilogy(age[cind:], [funclist[0](T) for T in Te[cind:]], color='r', linewidth=1.5, linestyle='--')
plt.semilogy(age[cind:], [funclist[1](T) for T in Te[cind:]], color='b', linewidth=1.5, linestyle='--')
plt.title('Change in instellation ('+solarmodel+')')
plt.xlabel('Age of the Sun [yr]')
plt.ylabel('Instellation received by solar system body '+r'$[S/S_\bigoplus]$')
plt.legend()

# HZ boundaries for plotting
inSlim = [funclist[0](T) for T in Tlist] # inner HZ boundary limit
outSlim = [funclist[1](T) for T in Tlist] # outer HZ boundary limit

emSlim = [EarlyMars(T) for T in Tlist] # Early Mars instellation limit
rvSlim = [RecentVenus(T) for T in Tlist] # Recent Venus instellation limit
moistSlim = [IHZKopp(T) for T in Tlist] # Moist greenhouse instellation limit
runawaySlim = [RunawayKopp(T) for T in Tlist] # Runaway greenhouse instellation limit
maxGHSlim = [OHZKopp(T) for T in Tlist] # Maximum greenhouse instellation limit

# Plotting HZ limits devoid of anything else
plt.figure()
plt.gca().set_aspect(aspect=(2-0.2)/5780) # arbitrary
plt.gca().yaxis.set_ticks_position('both')
plt.plot(rvSlim, Tlist, color='r', linestyle=':', label='Recent Venus')
plt.plot(runawaySlim, Tlist, color='r', linestyle='--', label='Runaway')
plt.plot(moistSlim, Tlist, color='r', label='Moist')
plt.plot(maxGHSlim, Tlist, color='b', label='Maximum')
plt.plot(emSlim, Tlist, color='b', linestyle=':', label='Early Mars')
plt.axis([2, 0.2, 2600, 7200])
plt.title('Conservative and optimistic HZ comparison')
plt.xlabel('Instellation '+r'$[S/S_\bigoplus]$')
plt.ylabel('Effective temperature [K]')
plt.legend(loc='lower left')

# Find the S limit for a given Te from the stellar track
leftlimit = [funclist[0](T) for T in Te[cind:]]
rightlimit = [funclist[1](T) for T in Te[cind:]]
# find indices closest to inner and outer HZ boundary for each body 
leftdiff = [[Scut[nb][i]-leftlimit[i] for i in range(len(Scut[nb]))] for nb in range(numb)] # differences between current S and S at the boundary (same Te)
leftindex = [leftdiff[nb].index(list(filter(lambda i: i>0, leftdiff[nb]))[0])+cind for nb in range(numb)] # first element OUTSIDE IHZ (i.e. first point with too much instellation)
rightdiff = [[Scut[nb][i]-rightlimit[i] for i in range(len(Scut[nb]))] for nb in range(numb)]
rightindex = [cind if Scut[nb][0]>rightlimit[0] else rightdiff[nb].index(list(filter(lambda i: i>0, rightdiff[nb]))[0])+cind-1 for nb in range(numb)] # last point outside OHZ
# consider case where the body at no point is outside the outer HZ boundary
# in that case, time in HZ starts counting at current time

inIHZ = [[leftlimit[i]>Scut[nb][i] for i in range(len(Scut[nb]))] for nb in range(numb)]
inOHZ = [[Scut[nb][i]>rightlimit[i] for i in range(len(Scut[nb]))] for nb in range(numb)]
booleanHZ = [[inIHZ[nb][i] and inOHZ[nb][i] for i in range(len(Scut[nb]))] for nb in range(numb)]
for nb in range(numb):
    booleanHZ[nb][-1]=False # Stupid way to ensure that the habitablity time calculations work even if you have a track too short to plot all the timespans inside HZ
    booleanHZ[nb][0]=False # same as above, but for start
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

# calculate water-loss timespan
runawaylimit = [RunawayKopp(T) for T in Te[cind:]] # limit for runaway greenhouse
runawaybool = [[runawaylimit[i]<Scut[nb][i] for i in range(len(Scut[nb]))] for nb in range(numb)] # boolean where S>instellation limit of runaway
runawayind = [[i for i, x in enumerate(runawaybool[nb]) if x] for nb in range(numb)] # find indices where runawaybool == True
runawaystarts = [[i for i in runawayind[nb] if i-1 not in runawayind[nb]] for nb in range(numb)]
runawaystops = [[i for i in runawayind[nb] if i+1 not in runawayind[nb]] for nb in range(numb)]
waterlosstimes = [[age[cind+runawaystops[nb][i]]-age[cind+runawaystarts[nb][i]] for i in range(len(runawaystops[nb]))] for nb in range(numb)]

# plot HR diagram
plt.figure()
plt.loglog(Te[cind:], L[cind:], linestyle='--',marker='.', color = 'gray', mfc = 'gray', markeredgecolor='k')
plt.loglog([Te[cind+i] for i in anytrue], [L[cind+i] for i in anytrue], '.', color = 'g', label=boundword+' HZ')
plt.xlabel('Effective temperature [K]')
plt.ylabel('Luminosity '+r'$[L/L_\bigodot]$')
plt.title('HR diagram ('+solarmodel+')')
plt.gca().invert_xaxis()
plt.xlim([7200, 2600])
plt.ylim([0.9*10**0, 10**4])
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
    plt.bar([nb + 0.1666*i for i in range(len(allyearsinHZ[nb]))], allyearsinHZ[nb], width=0.1666, color=colors[nb])
plt.xticks(range(numb), bodies)
plt.ylabel('timespan [years]')
plt.title('Timespans inside the Habitable Zone ('+solarmodel+')')

for nb in range(numb):
    plt.figure()
    plt.bar([x for x in middleage[nb]], allyearsinHZ[nb], width=allyearsinHZ[nb], color=colors[nb], label=bodies[nb])
    # plt.gca().set_xscale("log")
    plt.gca().set_xlim(right=age[-1])
    plt.xlabel('[years]')
    plt.ylabel('timespan [years]')
    plt.title('Timespans inside the Habitable Zone ('+solarmodel+')')
    plt.legend()

strYears = [['0' if x == 0 else "{:.1e}".format(x) for x in allyearsinHZ[nb]] for nb in range(numb)] # list of strings, scientific notation 1 decimal

# Water-loss time plot
EarthOceanLossTime = 5e14/(86400*365.241) # from Kasting et al 1993 using mixing ratio f(H20) = 1 (completely water dominated).
wfig=plt.figure()
wax=wfig.add_subplot(111)
for nb in range(numb):
    plt.bar([nb + 0.1666*i for i in range(len(waterlosstimes[nb]))], waterlosstimes[nb], width=0.1666, color=colors[nb])
plt.xticks(range(numb), bodies)
wax2 = wax.secondary_yaxis('right', functions=(lambda x: x/EarthOceanLossTime, lambda x: x*EarthOceanLossTime))
wax2.set_ylabel('Earth Ocean(s) lost')

plt.ylabel('timespan [years]')
plt.title('Waterloss timespans ('+solarmodel+')')

# #----------------------------------PART 4b-------------------------------------
# Habitable Zone plotting

# Base case HZ plot
plt.figure()
Smax = 2 if boundword == 'Optimistic' else 1.25
plt.gca().set_aspect(aspect = (Smax-0.2)/5780) # arbitrary
plt.gca().yaxis.set_ticks_position('both')
plt.plot(inSlim, Tlist, color='r')
plt.plot(outSlim, Tlist, color='b')
plt.axis([Smax, 0.2, 2600, 7200])
plt.title('First pass through '+boundword+' HZ ('+solarmodel+')')
plt.xlabel('Instellation '+r'$[S/S_\bigoplus]$')
plt.ylabel('Effective temperature [K]')
for nb in range(numb):
    plt.plot(Seff[nb][cind:n1],Te[cind:n1],linestyle='-',linewidth=1,marker='.',color=colors[nb],label=bodies[nb]) # n1 is index for last point before helium flash
    plt.plot(Seff[nb][cind],Te[cind],'o',color='k')
    plt.legend()

# #----------------------------------EXTRA---------------------------------------
# # Extra plotting code, must be run manually


# SUM OF TIHZ GRAPH. Might want to split it in two where the colors are not present in the first. 
if len(distances)>10:
    mapcolors = ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c'] 
    
    plt.figure()
    for nb in range(numb):
        plt.bar(distances[nb], allyearsinHZ[nb][0], width = barwidth, color=mapcolors[0], edgecolor='k', linewidth=0)
        prevTIHZ = allyearsinHZ[nb][0]
        for i in range(1, len(allyearsinHZ[nb])):
            plt.bar(distances[nb], allyearsinHZ[nb][i], width = barwidth, bottom=prevTIHZ, color=mapcolors[1:][(i-1)%(len(mapcolors)-1)], edgecolor = 'k', linewidth=0)
            prevTIHZ = prevTIHZ+allyearsinHZ[nb][i]
    plt.xlabel('Orbiting radius [AU]')
    plt.ylabel('Timespan inside HZ [yr]')
    plt.plot([], label="Pass #1", color=mapcolors[0])
    for i in range(max([len(allyearsinHZ[nb]) for nb in range(numb)])):
        plt.plot([], label="Pass #"+str(2+i), color=mapcolors[1:][(i-1)%(len(mapcolors)-1)])
    plt.xlim([distances[0]*0.75, distances[-1]*1.1])
    plt.ylim([0, 4e8])
    # legend1 = plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0.)
    plt.title('Sum of '+boundword+' TIHZ ('+solarmodel+')')
    
    # add vlines at orbital distances of the planets
    planets = ['Jupiter','Saturn','Uranus','Neptune', 'Pluto'] # name of the bodies
    planetstyle = ['-','--', '-.', ':', (0, (1, 10))]
    planetcolors = ['xkcd:light brown','xkcd:peach','xkcd:light blue','xkcd:bright blue', 'xkcd:maroon'] # color of each body for plotting
    planetdistances = [5.2, 9.57, 19.17, 30.18, 39.48] # AU
    nump = len(planets)
    
    linelist = []
    for nm in range(nump):
        line = plt.axvline(planetdistances[nm], linestyle=planetstyle[nm], color='k',linewidth=1, label=planets[nm])
        linelist += [line]
    # plt.legend(handles=linelist, bbox_to_anchor=(1.005, 0), loc='lower left')
    # plt.gca().add_artist(legend1)    
    
    for nm in range(nump):
        plt.text(planetdistances[nm]+0.2, 3.5e8, planets[nm])
    

# plt.figure()
# for nb in range(numb):
#     plt.bar([nb + 0.25*i for i in range(len(allyearsinHZ[nb]))], allyearsinHZ[nb], width=0.25, color=colors[nb])
#     plt.bar([nb + 0.25*i for i in range(len(allyearsinHZPARSEC[nb]))], allyearsinHZPARSEC[nb], width=0.25, fill = False, hatch='//')
# plt.xticks(range(numb), bodies)
# plt.ylabel('timespan [years]')
# plt.title('Timespans inside the '+boundword+' Habitable Zone')
# plt.bar(0, height=0, width=0, facecolor='grey', label=solarmodel)
# plt.bar(0, height = 0, width=0, fill = False, hatch='//', label ='PARSEC')
# plt.legend()



# How to save figures
# plt.savefig('Plots/NAMEHERE.png', bbox_inches = 'tight')