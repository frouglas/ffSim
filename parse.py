# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""



from espnff import League
import pickle
import dataStructures as ds



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
    leagueID = 412124
    year = 2017
    weeksPlayed = 0

    if reload == 1:
        league = League(leagueID, year)
        fSchedule = []
        for i in range(1,14):
            if i>10:
                pauseHere = 1
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
        with open("lea.gue","wb") as lFile:
            pickle.dump(leagueDB,lFile)
    else:    
        with open("lea.gue","rb") as lFile:
            leagueDB = pickle.load(lFile)
    return leagueDB
    
