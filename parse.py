# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""



from espnff import League
import pickle
import dataStructures as ds
import sys



def parseWeek(league,wk):
    thisWeek = league.scoreboard(week=wk)
    weekOut = []
    for eachMatch in thisWeek:
        mData = ds.gameInfo()
        mData.homeTeam = eachMatch.home_team.team_id
        mData.awayTeam = eachMatch.away_team.team_id
        mData.homeScore = eachMatch.home_score
        mData.awayScore = eachMatch.away_score
        mData.week = wk
        mData.game = len(weekOut) + 1
        weekOut.append(mData)
    return weekOut

def loadLeague(reload = 0):
    if sys.version_info[0] < 2:
        print("     requires python 2 or above")
    elif sys.version_info[0] == 2:
        picklePath = "lea2.gue"
    else:
        picklePath = "lea.gue"
    
    leagueID = 412124
    year = 2017
    weeksPlayed = 0

    if reload == 1:
        league = League(leagueID, year)
        fSchedule = []
        for i in range(1,14):
            thisWeek = parseWeek(league,i)
            if thisWeek[0].homeScore == 0:
                played = 0
            else:
                played = 1
            weeksPlayed += played
            fSchedule.append([thisWeek,played])
        teamKey = {}
        for i in range(len(league.teams)):
            teamKey[league.teams[i].team_id] = i 
        leagueDB = [league,fSchedule,weeksPlayed, teamKey]
        with open(picklePath,"wb") as lFile:
            pickle.dump(leagueDB,lFile)
    else:    
        with open(picklePath,"rb") as lFile:
            leagueDB = pickle.load(lFile)
    return leagueDB
    
