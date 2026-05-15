import importlib
import pandas as pd
import numpy as np
import sys

clustername = sys.argv[1]   # first argument
clusternames = [sys.argv[1]] 
age_manual = sys.argv[2] # second argument # in Gyr. 
age_manual = int(age_manual)

pathstartswith = '/Users/lakshgupta/Downloads/Personal/P-NGC2808WD/'
clustername = 'ngc' + clusternames[0]

params = pd.read_csv('cluster_param.csv')

met = round(params.loc[params['ID'] == clustername, "[Fe/H]"].values[0], 3)
reddening = round(params.loc[params['ID'] == clustername, "E(B-V)"].values[0], 3)
DM = params.loc[params['ID'] == clustername, "(m-M)V"].values[0]
aDM = round(DM - 3.1*reddening, 2)
d = round(10 * (10 ** ((aDM) / 5)) - (3.1 * (reddening)), 2)
age = round(params.loc[params['ID'] == clustername, "Age"].values[0], 2)
age_err = round(params.loc[params['ID'] == clustername, "Age_err"].values[0], 2)

print("Parameters of " + clustername + " from Harris Catalogue:")
print("RA and DEC: " + str(round(params.loc[params['ID'] == clustername, "RA"].values[0], 4)) + " " + str(round(params.loc[params['ID'] == clustername, "DEC"].values[0], 4)))
print("Metallicity: " + str(met)) # use this metallicity value to dowload models
print("Reddening: " + str(reddening))
print("Absolute Distance Modulus: " + str(DM))
print("Apparent Distance Modulus: " + str(aDM))
print("Distance in pc: " + str(d))
print("Age from Literature: " + str(age) + " Gyr")
print("Age error from Literature: " + str(age_err) + " Gyr")

ageiso = 1000*((age_manual))
print("IMPORTANT: Age to be used for isochrones: " + str(ageiso) + " Myr.")

print("IMPORTANT: Age to be used for isochrones: " + str(ageiso) + " Myr.")

metavail = [-1.84, -0.60, -2.14, -1.01, -1.31, -1.62]
whichmetuse = abs((met - metavail)).min()

idx = np.argmin(np.abs(met - metavail))
whichmetuse = metavail[idx]

print("Should use models of metallicity", whichmetuse)

import tex # comment this if Python on your system is not "linked" with TeX.
import func_analysis
import func_input

import theoreticalmodels
importlib.reload(theoreticalmodels)
import namingroutine
importlib.reload(namingroutine)
import inputdata
importlib.reload(inputdata)

# following must be loaded as they are used ahead. 
# I have commented the how to use, for example, 'colors' list from namingroutine.py.

models = theoreticalmodels.Initialize(func_input.ReadingModels, pathstartswith)
names = namingroutine.Initialize()
dfclusters_input = inputdata.Initialize(func_input.LoadClusters, pathstartswith, clusternames)

dfclusters = dict(sorted(dfclusters_input['dfclusters'].items()))

c_masset = 80
a_masset1 = 70
a_masset2 = 60
wdmass = '054'

wantabund=False 

isomodel = sys.argv[3] # third argument. can be 'iso131',  etc. depending on which isochrone you want to plot.
et_c_model = sys.argv[4] 
wdmodel = sys.argv[5] 

c_isohold = models[isomodel][str(ageiso)]
canonicaliso_dict = func_analysis.corrections(aDM+0.01, reddening-0.005, {'main': c_isohold[0:600]})
canonicaliso = canonicaliso_dict['main']  
canonicaliso['F336W'] -= 0.1
# print(canonicaliso)

c_ethold = models[et_c_model][str(c_masset)]
canonicalet_dict = func_analysis.corrections(aDM+0.01, reddening-0.030, {'main': c_ethold[0:300]})
canonicalet = canonicalet_dict['main']
canonicalet['F336W'] -= 0.1

wd_hold = models[wdmodel][wdmass]
wdcooling_dict = func_analysis.corrections(aDM-0.01, reddening, {'main': wd_hold})
wdcooling = wdcooling_dict['main'] 
wdcooling['F336W'] -= 0.0  

a_et1hold = models['et131_a1'][str(a_masset1)]
abundantet1_dict = func_analysis.corrections(aDM-0.15, reddening-0.025, {'main': a_et1hold[100:350]})
abundantet1 = abundantet1_dict['main']
abundantet1['F336W'] -= 0.1

a_et2hold = models['et131_a2'][str(a_masset2)]
abundantet2_dict = func_analysis.corrections(aDM-0.11, reddening, {'main': a_et2hold[100:350]})
abundantet2 = abundantet2_dict['main']
abundantet2['F336W'] -= 0.17

import matplotlib.pyplot as plt
plt.switch_backend('TkAgg')

dictholdmodels_ms = {'He-canonical Iso': canonicaliso, 
                     'He-canonical ET': canonicalet, 
                     'He-abundant ET 1': abundantet1, 
                     'He-abundant ET 2': abundantet2, 
                     'WD Cooling Track':wdcooling}

plt.tight_layout()
plt.rcParams['figure.dpi']=100
fig=plt.figure(figsize=(10,10))

plt.scatter(dfclusters[clustername]['F275W'] - dfclusters[clustername]['F336W'], dfclusters[clustername]['F275W'], 
            marker = 'o', s=2, alpha=1, color='black', edgecolors='none')

for i, (label, modelhere) in enumerate(dictholdmodels_ms.items()):
    if not wantabund and i in (2, 3):
        continue  
    plt.plot(modelhere['F275W'] - modelhere['F336W'],
             modelhere['F275W'],
             color=names['colors'][i], lw=1, linestyle='-', markersize=0.1,
             marker='o', label=label)

plt.ylim(14, 26)
plt.xlim(-2, 3)
plt.gca().invert_yaxis()
plt.legend()
plt.show()

import msto
importlib.reload(msto)

Completeness=False

# to select stars with pm > 80.
# df = func_analysis.cleandata(dfclusters[clustername], 80) 

#  to remove stars with dF275W < 1 and dF336W < 1
df = dfclusters[clustername][~((dfclusters[clustername]['dF275W'] > 1) & (dfclusters[clustername]['dF336W'] > 1))]

bluelimit = sys.argv[6]
redlimit = sys.argv[7]

msto_ret = msto.initialize(df,
                ageiso, c_masset, str(a_masset1), str(a_masset2),
                canonicaliso, canonicalet, abundantet1, abundantet2,
                clustername, wantabund, Completeness,
                delalpholder = [0.0040], # this can be loaded with more values.
                g=0, dpi=70,
                bluelimit = float(bluelimit), redlimit = float(redlimit), sigmacut = 1.5, 
                wantcsv=False, wantlegend=False, # printing legend won't be required since everything is being printed as output in text.
                )

# for spatial plot
SPUpperMS = msto_ret['concatnewupper'] 
SPLowerMS = msto_ret['concatnewlower'] 

# SC for ratio calculation (either Completeness or not)
MSSC_c = len(msto_ret['MSSC_c']) 
if Completeness:
    MSSC_c_comp = len(msto_ret['MSSC_c_comp']) 

# CT for ratio calculation (can be more than 1 since He-enhanced models can also be used)
MSCT_c = abs(msto_ret['MSCT_c']) 
if wantabund:
    MSCT_a1 = msto_ret['MSCT_a1'] 
    MSCT_a2 = msto_ret['MSCT_a2'] 

import wd
importlib.reload(wd)

max_allowed_mag = sys.argv[8]
min_allowed_mag = sys.argv[9]
division = sys.argv[10]
wdcolmin = sys.argv[11]
wdcolmax = sys.argv[12]
wdcolminbri = sys.argv[13]
wdcolmaxbri = sys.argv[14]
briwdstart = sys.argv[15]


wd_ret = wd.initialize(dfclusters[clustername],
                wdcooling, clustername,
                max_allowed_mag=float(max_allowed_mag), min_allowed_mag=float(min_allowed_mag), # these numbers come from AST
                dpi=100,
                binsize=0.3, # can be increased or decreased as per choice.
                division=float(division), # can be increased or decreased as per cluster.
                min_mag=17, max_mag=26, min_col=-2.5, max2=1,
                wdcolmin = float(wdcolmin), wdcolmax=float(wdcolmax),
                wdcolminbri = float(wdcolminbri), wdcolmaxbri=float(wdcolmaxbri),
                briwdstart = float(briwdstart),
                wantlegend=False, Completeness=False
              )

SPUpperWD = wd_ret['bin1']
SPLowerWD = wd_ret['bin2'] 
SPBrightWD = wd_ret['dfwdcalbright']

WDCTup = wd_ret['WDCTup']
WDSCup = wd_ret['sum_values_upper_ncorr']
WDSCup_corr = wd_ret['sum_values_upper_corr']

WDCTlo = wd_ret['WDCTlo']
WDSClo = wd_ret['sum_values_lower_ncorr'] + WDSCup
WDSClo_corr = wd_ret['sum_values_lower_corr'] + WDSCup_corr

import ratios
importlib.reload(ratios)

rationumholder = {0: [WDSCup, MSSC_c, WDCTup, MSCT_c],
                  1: [WDSClo, MSSC_c, WDCTlo, MSCT_c]
                  }

ratios.initialize(rationumholder)