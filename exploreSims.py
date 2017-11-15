# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 11:57:04 2017

@author: doug
"""

import pickle
import sys
import numpy as np

if sys.version_info[0] < 2:
    print("     requires python 2 or above")
elif sys.version_info[0] == 2:
    simPath = 'sim2.res'
else:
    simPath = 'sim.res'

with open(simPath,"rb") as lFile:
    simDB = pickle.load(lFile)
    simResults = simDB[0]
    teamKey = simDB[1]

for i in list(simResults.team_name.unique()):
    print(i)
    teamSlice = simResults[simResults['team_name']==i]
    dbSize = float(len(teamSlice))
    aveWins = round(np.mean(list(teamSlice['totWins'])),2)
    print('     average wins:   ' + str(aveWins))
    aveFin = round(np.mean(list(teamSlice['finish'])),1)
    print('     average finish: ' + str(aveFin))
    avePts = round(np.mean(list(teamSlice['totPts'])),2)
    print('     average points: ' + str(avePts))
    propPlayoffs = round((float(len(teamSlice[teamSlice['playoffs']!=-1])) / dbSize)*100,2)
    print('     playoff odds:   ' + str(propPlayoffs) + '%')
    propBye = round((float(len(teamSlice[teamSlice['bye']!=-1])) / dbSize)*100,2)
    print('     bye odds:       ' + str(propBye) + '%')
    propMaxPts = round((float(len(teamSlice[teamSlice['maxPts']==1]))/ dbSize)*100,2)
    print('     max point odds: ' + str(propMaxPts) + '%')
    tPlayoffs = teamSlice[teamSlice['playoffs']!=-1]
    playoffScens = list(tPlayoffs.simulation.unique())
    scenDB = simResults.loc[simResults['simulation'].isin(playoffScens)]
    if len(scenDB) == 0:
        print('-----------------------')
        continue
    else:
        print('     playoff requirements:')
        noReqs = 1
    for j in list(simResults.team_name.unique()):
        if i==j:
            continue
        subDB = scenDB[scenDB['team_name']==j]
        if len(subDB.wk10_win.unique()) == 1:
            winLoss = subDB.wk10_win.unique()[0]
            if winLoss == 1:
                thisStr = 'win'
            else:
                thisStr = 'lose'
            print('          needs ' + j + ' to ' + thisStr + ' in week 10')
            noReqs = 0
        if len(subDB.wk11_win.unique()) == 1:
            winLoss = subDB.wk11_win.unique()[0]
            if winLoss == 1:
                thisStr = 'win'
            else:
                thisStr = 'lose'
            print('          needs ' + j + ' to ' + thisStr + ' in week 11')
            noReqs = 0
        if len(subDB.wk12_win.unique()) == 1:
            winLoss = subDB.wk12_win.unique()[0]
            if winLoss == 1:
                thisStr = 'win'
            else:
                thisStr = 'lose'
            print('          needs ' + j + ' to ' + thisStr + ' in week 12')
            noReqs = 0
    if noReqs == 1:
        print('          NONE')
    print('-----------------------')
    

    