# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 09:56:18 2022

@author: Vviik
"""
import numpy as np

pi = np.pi

Earea = 510100000 # km^2 

# four largest of Jupiter
diamJupitersmoons = [5268.2, 4820.6, 3643.2, 3121.6] # km
areaJupitersmoons = sum([pi*d**2 for d in diamJupitersmoons]) # km^2, make it a sum of area of Jupiter's moons instead.

# seven largest of Saturn
diamSaturnsmoons = [5149.46, 1527.6, 1468.6, 1122.8, 1062.2, 504.2, 396.4]
areaSaturnsmoons = sum([pi*d**2 for d in diamSaturnsmoons])

# triton of Neptune
diamNeptunesmoons = [2705.2] 
areaNeptunesmoons = sum([pi*d**2 for d in diamNeptunesmoons])

# five largest of Uranus
diamUranusmoons = [1576.8, 1522.8, 1169.4, 1157.8, 471.6] 
areaUranusmoons = sum([pi*d**2 for d in diamNeptunesmoons])

# six largest TNOs: Pluto, Eris, Haumea, Makemake, 225088 Gonggong, Charon. All are approximated (overestimated) to have same TIHZ as Pluto. 
diamTNOs = [2376.6, 2326, 1609.7, 1430, 1230, 1212]
areaTNOs = sum([pi*d**2 for d in diamTNOs])

arealist = [areaJupitersmoons, areaSaturnsmoons, areaNeptunesmoons, areaUranusmoons, areaTNOs]

# TIHZ from PARSEC w/ optmisitic HZ. 
RGBTIHZ = [265761502.50967598, 82975073.10663033, 27421153.146274567, 13882409.799789429, 9819829.844875336]
postRGBTIHZ = [0, 119546545.33863449, 11327017.277606964, 5546138.707178116, 3117540.3279476166]
                   
RGBtimeareas = [RGBTIHZ[i]*arealist[i] for i in range(len(arealist))]
postRGBtimeareas = [postRGBTIHZ[i]*arealist[i] for i in range(len(arealist))]

# 1 Gyr life occurance calc. Assumes life occurs on average every 1 Gyr on an Earth sized habitable body
r1 = 1e-9 # yr^-1
r2 = 2e-9 # yr^-1, if life forms on average every 0.5 Myr
r05 = 0.5e-9 # yr^-1, if life forms on average every 2 Gyr

# probability that life occurs at least once on any of the outer moons. Equation (8).
PRGB1 = 1-np.exp(-r1/Earea*sum(RGBtimeareas))
PpostRGB1 = 1-np.exp(-r1/Earea*sum(postRGBtimeareas))
Ptot1 = 1-np.exp(-r1/Earea*sum(RGBtimeareas+postRGBtimeareas))

PRGB2 = 1-np.exp(-r2/Earea*sum(RGBtimeareas))
PpostRGB2 = 1-np.exp(-r2/Earea*sum(postRGBtimeareas))
Ptot2 = 1-np.exp(-r2/Earea*sum(RGBtimeareas+postRGBtimeareas))


