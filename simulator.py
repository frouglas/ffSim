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
                                    'bye','byeEligible','playoffs','playEligible','finish','wins','losses',
                                    'simWins',
                                    'simLosses','totWins','totLosses',
                                    'tPts','ptsA','simPts','simPtsA','totPts',
                                    'totPtsA','winnings'])
    
    teamList = league.teams
    
    for team in teamList:
        entryID = str(simNo) + "." + str(team.team_id)
        thisEntry = pd.Series({'entryID':entryID,'team_id':team.team_id, 
                               'simulation': simNo, 'team_name':team.team_name,
                               'bye':-1, 'byeEligible':0, 'playoffs':-1, 'playEligible':0, 
                               'finish':-1,'wins':team.wins, 
                               'losses':team.losses,'simWins':0,'simLosses':0,
                               'totWins':team.wins,'totLosses':team.losses,
                               'tPts':team.points_for,
                               'ptsA':team.points_against,'simPts':0,
                               'simPtsA':0,'totPts':team.points_for,
                               'totPtsA':team.points_against,'winnings':0})
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
                if currWins[i]>pClinch:
                    if pList[i]==-1:
                        pList[i] = weekNo + 1
                    if ((currWins[i]>bClinch) & (bList[i]==-1)):
                        bList[i] = weekNo + 1
        else:
            currScores = list(simDB['totPts'])
            currSort = [currWins[i] + currScores[i]/10000 for i in range(len(currScores))]
            currSorted = sorted(currSort)
            finishRanks = [12 - currSorted.index(i) for i in currSort]
            for i in range(len(finishRanks)):
                if finishRanks[i] <= 6:
                    if pList[i]==-1:
                        pList[i] = weekNo + 1
                    if ((finishRanks[i] <=2) & (bList[i]==-1)):
                        bList[i] = weekNo + 1                    
        simDB.loc[:,'playoffs'] = pList
        simDB.loc[:,'bye'] = bList
    
    pWinMin = sorted(currWins)[-6]
    bWinMin = sorted(currWins)[-2]
    pEligible = [(pWinMin<=i)*1 for i in currWins]
    bEligible = [(bWinMin<=i)*1 for i in currWins]
    simDB['maxPts'] = pd.Series(0,index=simDB.index)
    ptsWinner = currScores.index(max(currScores))
    
    simDB.iloc[ptsWinner,-1] = 1
    ptsWinID = str(simNo) + "." + str(teamList[ptsWinner].team_id)
    simDB.loc[ptsWinID,'winnings'] = simDB.loc[ptsWinID,'winnings'] + 250
    simDB.loc[:,'finish'] = finishRanks
    simDB.loc[:,'playEligible'] = pEligible
    simDB.loc[:,'byeEligible'] = bEligible
    
    
    p1Win = 'p1_win'
    simDB[p1Win] = pd.Series(0,index=simDB.index)
    
    # simulate playoff game 1 (3 v 6)
    
    
    pGm1Home = teamList[finishRanks.index(3)]
    pGm1Away = teamList[finishRanks.index(6)]
    pGm1HScores = np.array(pGm1Home.scores[:wksPlayed])
    pGm1HSim = np.random.normal(np.mean(pGm1HScores),np.std(pGm1HScores))
    pGm1AScores = np.array(pGm1Away.scores[:wksPlayed])
    pGm1ASim = np.random.normal(np.mean(pGm1AScores),np.std(pGm1HScores))
    
    if pGm1HSim > pGm1ASim:
        pGm3Away = pGm1Home
    else:
        pGm3Away = pGm1Away
    
    p1WTeam = str(simNo) + "." + str(pGm3Away.team_id)
    simDB.loc[p1WTeam,p1Win] = 1    
        
    # simulate playoff game 2 (4 v 5)
    
    pGm2Home = teamList[finishRanks.index(4)]
    pGm2Away = teamList[finishRanks.index(5)]
    pGm2HScores = np.array(pGm2Home.scores[:wksPlayed])
    pGm2HSim = np.random.normal(np.mean(pGm2HScores),np.std(pGm2HScores))
    pGm2AScores = np.array(pGm2Away.scores[:wksPlayed])
    pGm2ASim = np.random.normal(np.mean(pGm2AScores),np.std(pGm2HScores))
    
    if pGm2HSim > pGm2ASim:
        pGm4Away = pGm2Home
    else:
        pGm4Away = pGm2Away
    
    p2WTeam = str(simNo) + "." + str(pGm4Away.team_id)
    simDB.loc[p2WTeam,p1Win] = 1  
    
    p2Win = 'p2_win'
    simDB[p2Win] = pd.Series(0,index=simDB.index)
    
    # simulate playoff game 3 (2 v winner of game 1)
    
    
    pGm3Home = teamList[finishRanks.index(2)]
    pGm3HScores = np.array(pGm3Home.scores[:wksPlayed])
    pGm3HSim = np.random.normal(np.mean(pGm3HScores),np.std(pGm3HScores))
    pGm3AScores = np.array(pGm3Away.scores[:wksPlayed])
    pGm3ASim = np.random.normal(np.mean(pGm3AScores),np.std(pGm3HScores))
    
    if pGm3HSim > pGm3ASim:
        pGm5Away = pGm3Home
    else:
        pGm5Away = pGm3Away
    
    p3WTeam = str(simNo) + "." + str(pGm5Away.team_id)
    simDB.loc[p3WTeam,p2Win] = 1    
        
    # simulate playoff game 4 (1 v winner of game 2)
    
    pGm4Home = teamList[finishRanks.index(1)]
    pGm4HScores = np.array(pGm4Home.scores[:wksPlayed])
    pGm4HSim = np.random.normal(np.mean(pGm4HScores),np.std(pGm4HScores))
    pGm4AScores = np.array(pGm4Away.scores[:wksPlayed])
    pGm4ASim = np.random.normal(np.mean(pGm4AScores),np.std(pGm4HScores))
    
    if pGm4HSim > pGm4ASim:
        pGm5Home = pGm4Home
    else:
        pGm5Home = pGm4Away
    
    p4WTeam = str(simNo) + "." + str(pGm5Home.team_id)
    simDB.loc[p4WTeam,p2Win] = 1  

    p3Win = 'p3_win'
    simDB[p3Win] = pd.Series(0,index=simDB.index)
    
    # simulate playoff game 5 (championship game)
    
    pGm5HScores = np.array(pGm5Home.scores[:wksPlayed])
    pGm5HSim = np.random.normal(np.mean(pGm5HScores),np.std(pGm5HScores))
    pGm5AScores = np.array(pGm5Away.scores[:wksPlayed])
    pGm5ASim = np.random.normal(np.mean(pGm5AScores),np.std(pGm5HScores))
    
    if pGm5HSim > pGm5ASim:
        champion = pGm5Home
        runUp = pGm5Away
    else:
        champion = pGm5Away
        runUp = pGm5Home
    
    champTeam = str(simNo) + "." + str(champion.team_id)
    runTeam = str(simNo) + "." + str(runUp.team_id)
    simDB.loc[champTeam,p3Win] = 1
    simDB.loc[champTeam,'winnings'] = simDB.loc[champTeam,'winnings'] + 700
    simDB.loc[runTeam,'winnings'] = simDB.loc[runTeam,'winnings'] + 250    

    return simDB     
            