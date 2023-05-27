'''
Routes and views for the flask application.
'''

import requests
from flask import render_template
from flask import request
from NZoneScoreboard import app

@app.route('/nc/scoreboard/<int:id>')
def scoreboard(id):
    '''Renders the scoreboard page.'''
    print('Open Scoreboard')
    match = getCurrentMatchByUser(id)
    parameter = request.args
    opacity = parameter.get('opacity')
    print(opacity)
    if match is not None:
        if len(match['team1Civs']) > 0:
            return render_template(
            'scoreboard2CivPool.html',
             match=match,
             opacity=opacity
        )
        else:
            return render_template(
                'scoreboard3.html',
                 match=match,
                 opacity=opacity
            )
    else:
        loggedIn = getCurrentlyLoggedIn()

        return render_template(
            'login_horizontal.html',
             loggedIn=loggedIn
        )

@app.route('/nc/login_queue_board')
def login_queue():
    '''Renders the scoreboard page.'''
    print('Open Login Queue Board')
    loggedIn = getCurrentlyLoggedIn()
    return render_template(
        'login_vertical.html',
        loggedIn=loggedIn
    )

@app.route('/nc/scoreboard/past/<int:uid>')
def scoreboard_past(uid):
    '''Renders the scoreboard page.'''
    print('Open Scoreboard')
    match = getPastMatchByUser(uid)
    parameter = request.args
    opacity = 1
    if not (parameter.get('opacity') is None):
        opacity = float(parameter.get('opacity'))
    
    print(opacity)
    if not (match is None):
        if len(match['team1Civs']) > 0:
            return render_template(
            'scoreboard2CivPool.html',
             match=match,
             opacity=opacity
        )
        else:
            return render_template(
                'scoreboard3.html',
                 match=match,
                 opacity=opacity
            )
    else:
        loggedIn = getCurrentlyLoggedIn()

        return render_template(
            'login_horizontal.html',
             loggedIn=loggedIn
        )

def getPastMatchByUser(uid):
    r = requests.get('https://new-chapter.eu/app.php/nczone/api/matches/past')
    matches = r.json()
    return getMatchInfo(findMatchbyUser(uid, matches['items']))

def getMatchInfo(match):
    out = {}
    if match is not None:
        playersT1 = generatePlayers(match['players']['team1'])
        out['team1'] = playersT1
        out['ratingT1'] = getTotalTeamRating(playersT1)
        playersT2 = generatePlayers(match['players']['team2'])
        out['team2'] = playersT2
        out['ratingT2'] = getTotalTeamRating(playersT2)
        teamCivs = match['civs']
        out['team1Civs'] = generateCivIcons(teamCivs['team1'])
        out['team2Civs'] = generateCivIcons(teamCivs['team2'])
        out['teamsize'] = len(out['team1'])
        out['map'] = match['map']['name']
        return out
    return None

def getTotalTeamRating(players):
    out = 0
    for p in players:
        out += p['rating']
    return out

def generatePlayers(players):
    out = []
    for p in players:
        player = {}
        username = p['username']
        if(len(username) > 16):
            username = username[:14] + '..'
        player['name'] = username
        player['rating'] = p['rating']
        player['civs'] = generateCivIcons( p['civs'])
        out.append(player)
    return out

def generateCivIcons(civs):
    out = []
    for c in civs:
        civ = {}
        title = c['title']
        titleArr = title.split('_')
        if len(titleArr) > 1:
            civName = titleArr[1]
            civ['name'] = civName
            civ['src'] = f'/static/images/wappen/{civName.lower()}.png'
        elif len(titleArr) == 1:
            civName = titleArr[0]
            civ['name'] = civName
            civ['src'] = f'/static/images/wappen/{civName.lower()}.png'
        else:
            civ['name'] = 'Not Found'
            civ['src'] = '/static/images/wappen/NotFound.png'
        out.append(civ)

    return out



def getCurrentMatchByUser(uid):
    r = requests.get('https://new-chapter.eu/app.php/nczone/api/matches/running')
    matches = r.json()
    return getMatchInfo(findMatchbyUser(uid, matches))

def findMatchbyUser(uid, matches):
    if not (matches is None):
        for m in matches:
            for p in m['players']['team1']:
                if p['id'] == int(uid):
                    return m
            for p in m['players']['team2']:
                if p['id'] == int(uid):
                    return m
    return None



def getCurrentlyLoggedIn():
    r = requests.get('https://new-chapter.eu/app.php/nczone/api/players/logged_in')
    logged_in = r.json()
    out = {}
    players = []
    out['players'] = players
    dummyplayers = ["Test 1", "Test 2","Test 3", "Test 4","Test 5", "Test 6","Test 7", "Test 8","Test 9", "Test 10","Test 11", "Test 12","Test 13", "Test 14","Test 15", "Test 16","Test 17", "Test 18","Test 19", "Test 20"]
    if not (logged_in is None):
        for p in logged_in:
            player = {}
            player['name'] = p['username']
            player['rating'] = p['rating']
            players.append(player)
        for p in dummyplayers:
            player = {}
            player['name'] = p
            player['rating'] = 9999
            players.append(player)
        out['playerslegth'] = len(players)
    return out
