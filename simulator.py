#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 01:17:37 2017

@author: frouglas
"""

import parse as pa
import dataStructures as ds
import pandas as pd
import numpy as np

def runSim(thisLeagueDB,simNo):
    league = thisLeagueDB[0]
    weeks = thisLeagueDB[1]
    wksPlayed = thisLeagueDB[2]
    teamKey = thisLeagueDB[3]
    
    simDB = pd.DataFrame(columns = ['entryID','simulation','team_id','team_name',
                                    'bye','playoffs','finish','wins','losses',
                                    'simWins',
                                    'simLosses','totWins','totLosses',
                                    'tPts','ptsA','simPts','simPtsA','totPts',
                                    'totPtsA'])
    
    for team in league.teams:
        entryID = str(simNo) + "." + str(team.team_id)
        thisEntry = pd.Series({'entryID':entryID,'team_id':team.team_id, 
                               'simulation': simNo, 'team_name':team.team_name,
                               'bye':-1, 'playoffs':-1, 'finish':-1,'wins':team.wins, 
                               'losses':team.losses,'simWins':0,'simLosses':0,
                               'totWins':team.wins,'totLosses':team.losses,
                               'tPts':team.points_for,
                               'ptsA':team.points_against,'simPts':0,
                               'simPtsA':0,'totPts':team.points_for,
                               'totPtsA':team.points_against})
        simDB = simDB.append(thisEntry,ignore_index=True)
        
    simDB = simDB.set_index('entryID')
        
    for weekNo in range(wksPlayed,len(weeks)):
        weekID = 'wk' + str(weekNo)
        thisWeekWin = weekID + '_win'
        thisWeekPts = weekID + '_pts'
        simDB[thisWeekWin] = pd.Series(0,index=simDB.index)
        simDB[thisWeekPts] = pd.Series(0,index=simDB.index)
        thisWeek = weeks[weekNo]
        for game in thisWeek[0]:
            hTeam = league.teams[teamKey[game.homeTeam]]
            hTeamScores = np.array(hTeam.scores[:wksPlayed])
            hTeamSim = np.random.normal(np.mean(hTeamScores),np.std(hTeamScores))
            aTeam = league.teams[teamKey[game.awayTeam]]
            aTeamScores = np.array(aTeam.scores[:wksPlayed])
            aTeamSim = np.random.normal(np.mean(aTeamScores),np.std(aTeamScores))
            aTeamID = str(simNo) + "." + str(aTeam.team_id)
            hTeamID = str(simNo) + "." + str(hTeam.team_id)
            simDB.loc[aTeamID,'simPts'] = simDB.loc[aTeamID,'simPts'] + aTeamSim
            simDB.loc[aTeamID,'totPts'] = simDB.loc[aTeamID,'totPts'] + aTeamSim
            simDB.loc[aTeamID,'simPtsA'] = simDB.loc[aTeamID,'simPtsA'] + hTeamSim
            simDB.loc[aTeamID,'totPtsA'] = simDB.loc[aTeamID,'totPtsA'] + hTeamSim
            simDB.loc[aTeamID,thisWeekPts] = aTeamSim
            simDB.loc[hTeamID,'simPts'] = simDB.loc[hTeamID,'simPts'] + hTeamSim
            simDB.loc[hTeamID,'totPts'] = simDB.loc[hTeamID,'totPts'] + hTeamSim
            simDB.loc[hTeamID,'simPtsA'] = simDB.loc[hTeamID,'simPtsA'] + aTeamSim
            simDB.loc[hTeamID,'totPtsA'] = simDB.loc[hTeamID,'totPtsA'] + aTeamSim
            simDB.loc[hTeamID,thisWeekPts] = hTeamSim
            if aTeamSim < hTeamSim:
                simDB.loc[hTeamID,'simWins'] = simDB.loc[hTeamID,'simWins'] + 1
                simDB.loc[hTeamID,'totWins'] = simDB.loc[hTeamID,'totWins'] + 1
                simDB.loc[hTeamID,thisWeekWin] = 1
                simDB.loc[aTeamID,'simLosses'] = simDB.loc[aTeamID,'simLosses'] + 1
                simDB.loc[aTeamID,'totLosses'] = simDB.loc[aTeamID,'totLosses'] + 1
            else:
                simDB.loc[aTeamID,'simWins'] = simDB.loc[aTeamID,'simWins'] + 1
                simDB.loc[aTeamID,'totWins'] = simDB.loc[aTeamID,'totWins'] + 1
                simDB.loc[aTeamID,thisWeekWin] = 1
                simDB.loc[hTeamID,'simLosses'] = simDB.loc[hTeamID,'simLosses'] + 1
                simDB.loc[hTeamID,'totLosses'] = simDB.loc[hTeamID,'totLosses'] + 1
        currWins = list(simDB['totWins'])
        pList = list(simDB['playoffs'])
        bList = list(simDB['bye'])
        if not weekNo == len(weeks) - 1:
            bClinch = sorted(currWins)[-3]+len(weeks)-weekNo
            pClinch = sorted(currWins)[-7]+len(weeks)-weekNo
            for i in range(len(pList)):
                if ((currWins[i]>pClinch) & (pList[i]==-1)):
                    pList[i] = weekNo + 1
                    if ((currWins[i]>bClinch) & (bList[i]==-1)):
                        bList[i] = weekNo + 1
        else:
            currScores = list(simDB['totPts'])
            currSort = [currWins[i] + currScores[i]/10000 for i in range(len(currScores))]
            currSorted = sorted(currSort)
            finishRanks = [12 - currSorted.index(i) for i in currSort]
            for i in range(len(finishRanks)):
                if ((finishRanks[i] <= 6) & (pList[i]==-1)):
                    pList[i] = weekNo + 1
                    if ((finishRanks[i] <=2) & (bList[i]==-1)):
                        bList[i] = weekNo + 1                    
        simDB.loc[:,'playoffs'] = pList
        simDB.loc[:,'bye'] = bList
    
    
    simDB.loc[:,'finish'] = finishRanks
           
    return simDB     
            