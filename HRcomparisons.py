# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 13:38:57 2022

@author: Vviik
"""

import matplotlib.pyplot as plt
#------------------------------------------------------------------------------

filename1 = "tracks/Z0.017Y0.279O_IN0.00OUTA1.74_F7_M1.00.TAB"
filename2 = "tracks/Z0.017Y0.279O_IN0.00OUTA1.74_F7_M1.00.TAB.HB"

solarmodel = 'Control'

track1 = []
track2 = []
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

L = [10**x for x in logL]
Te = [10**x for x in logTe]

#------------------------------------------------------------------------------

comparisonfiles = ["tracks/SolarCalibratedRGB.tab",
                   ["tracks/PARSEC_VaryingMass/M0.500.TAB", "tracks/PARSEC_VaryingMass/M0.500.HB"], 
                   ["tracks/PARSEC_VaryingMass/M0.750.TAB", "tracks/PARSEC_VaryingMass/M0.750.HB"],
                   ["tracks/PARSEC_VaryingMass/M1.250.TAB", "tracks/PARSEC_VaryingMass/M1.250.HB"],
                   ["tracks/PARSEC_VaryingMass/M1.500.TAB", "tracks/PARSEC_VaryingMass/M1.500.HB"],
                   ["tracks/PARSEC_VaryingMetal/Z0.014.TAB","tracks/PARSEC_VaryingMetal/Z0.014.HB"],
                   ["tracks/PARSEC_VaryingMetal/Z0.010.TAB","tracks/PARSEC_VaryingMetal/Z0.010.HB"],
                   ["tracks/PARSEC_VaryingMetal/Z0.008.TAB","tracks/PARSEC_VaryingMetal/Z0.008.HB"],
                   ["tracks/PARSEC_VaryingMetal/Z0.006.TAB","tracks/PARSEC_VaryingMetal/Z0.006.HB"],
                   ["tracks/PARSEC_VaryingMetal/Z0.004.TAB","tracks/PARSEC_VaryingMetal/Z0.004.HB"],
                   ]

comparisonwords = ['Solar calibration',
                  'M=0.50',
                  'M=0.75',
                  'M=1.25',
                  'M=1.50',
                  'Z=0.014',
                  'Z=0.010',
                  'Z=0.008',
                  'Z=0.006',
                  'Z=0.004']

# list of index for tracks you want to compare. 
choices = [5, 9]

comparisonfiles = [comparisonfiles[i] for i in sorted(choices)]
comparisonwords = [comparisonwords[i] for i in sorted(choices)]

comparisontracks = [[] for i in range(len(comparisonfiles))]
linestyles = ['-','--', '-.', ':', (0, (1, 10))]
mapcolors = ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c'] 

ns = []
ages = []
Ls = []
Tes = []
PHSs = []

for i in range(len(comparisonfiles)):
    if type(comparisonfiles[i]) == str:
        with open(comparisonfiles[i]) as f:
            for line in f:
                rowlist = line.split()
                comparisontracks[i].append(rowlist)
                
        comparisontracks[i].pop(-1)
        ages.append([float(x[2]) for x in comparisontracks[i][5:]])
        Ls.append([10**float(x[4]) for x in comparisontracks[i][5:]])
        Tes.append([10**float(x[5]) for x in comparisontracks[i][5:]])
        PHSs.append([float(x[95]) for x in comparisontracks[i][5:]])
        ns.append(len(ages[-1]))
            
    if type(comparisonfiles[i])==list:
        comparisontracks[i] = [[] for k in range(len(comparisonfiles[i]))]
        tempages = []
        tempLs = []
        tempTes = []
        tempPHSs = []
        
        for k in range(len(comparisonfiles[i])):
            with open(comparisonfiles[i][k]) as f:
                for line in f:
                    rowlist = line.split()
                    comparisontracks[i][k].append(rowlist)
                    
            comparisontracks[i][k].pop(-1)
            
            tempages.append([float(x[2]) for x in comparisontracks[i][k][5:]])
            tempLs.append([10**float(x[4]) for x in comparisontracks[i][k][5:]])
            tempTes.append([10**float(x[5]) for x in comparisontracks[i][k][5:]])
            tempPHSs.append([float(x[95]) for x in comparisontracks[i][k][5:]])
            
        ages.append(tempages[0]+[tempages[0][-1]+tempages1 for tempages1 in tempages[1]])
        Ls.append(tempLs[0]+tempLs[1])
        Tes.append(tempTes[0]+tempTes[1])
        PHSs.append(tempPHSs[0]+tempPHSs[1])
        ns.append(len(ages[-1]))
        
#------------------------------------------------------------------------------
        
plt.figure()
plt.semilogy(age, L, linewidth = 0, marker='.', markersize=1, color='k', label = solarmodel)
for i in range(len(comparisonfiles)):
    plt.semilogy(ages[i], Ls[i], linestyle=linestyles[0], label=comparisonwords[i])
plt.xlabel('Age of the star [yr]')
plt.ylabel('Luminosity '+r'$[L/L_\bigodot]$')
plt.title('Change in luminosity')
plt.legend(bbox_to_anchor=(1.005, 0), loc='lower left')

plt.figure()
plt.plot(age, PHS, linestyle=linestyles[0], color='k', label = solarmodel)
for i in range(len(comparisonfiles)):
    plt.plot(ages[i], PHSs[i], linestyle=linestyles[0], label=comparisonwords[i])
plt.xlabel('Age of the star [yr]')
plt.ylabel('Phase')
plt.title('Evolutionary phases')
plt.legend(bbox_to_anchor=(1.005, 0), loc='lower left')

MStime = []
RGBtime = []
for i in range(len(comparisonfiles)):
    MSstopindex = PHSs[i].index(3+min([abs(x-3) for x in PHSs[i]]))
    MStime.append(ages[i][MSstopindex])
    RGBstopindex = PHSs[i].index(5+min([abs(x-5) for x in PHSs[i]]))
    RGBtime.append(ages[i][RGBstopindex])
RGBduration = [RGBtime[i]-MStime[i] for i in range(len(comparisonfiles))]
                
# HR diagram
plt.figure()
plt.loglog(Te, L, linewidth = 0, marker='.', markersize=1, color='k', label = solarmodel)
for i in range(len(comparisonfiles)):
    plt.loglog(Tes[i], Ls[i], linestyle=linestyles[0], label = comparisonwords[i])
    plt.loglog(Tes[i][0], Ls[i][0], marker='o', color='k', markerfacecolor='None') # start of track
    plt.loglog(Tes[i][-1], Ls[i][-1], marker='x', color='k') # end of track
plt.xlabel('Effective temperature [K]')
plt.ylabel('Luminosity [L_sun]')
plt.title('HR diagram comparison')
plt.vlines(x=7200, ymin=1, ymax=1e3, color='k', linewidth=1)
plt.vlines(2600, ymin=1, ymax=1e3, color='k', linewidth=1)
plt.hlines(1, xmin=2600, xmax=7200, color='k', linewidth=1)
plt.hlines(1e3, xmin=2600, xmax=7200, color='k', linewidth=1)
plt.gca().invert_xaxis()
plt.legend(bbox_to_anchor=(1.005, 0), loc='lower left')


            
                            
        




