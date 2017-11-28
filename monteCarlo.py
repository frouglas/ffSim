#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 04:00:59 2017

@author: frouglas
"""

import simulator as sm
import parse as pr
import pandas as pd
import pickle
import numpy as np
import sys

overwriteResults = 1

if sys.version_info[0] < 2:
    print("     requires python 2 or above")
elif sys.version_info[0] == 2:
    picklePath = "lea2.gue"
    simPath = 'sim2_test.res'
else:
    picklePath = "lea.gue"
    simPath = 'sim_test.res'

totSims = 2000
leagueDB = pr.loadLeague(1)

simResults = pd.DataFrame()
np.random.seed(0)

for i in range(totSims):
    if (i + 1) % 500 == 0:
        print('     processed ' + str(i + 1) + "...")
    thisSim = sm.runSim(leagueDB,i)
    if len(simResults)==0:
        simResults = thisSim
    else:
        simResults = simResults.append(thisSim)

if overwriteResults == 1:    
    resultsFile = [simResults,leagueDB[3]]
    with open(simPath,"wb") as lFile:
        pickle.dump(resultsFile,lFile)
