"""
Routes and views for the flask application.
"""

from asyncio.windows_events import NULL
import requests
import json
from datetime import datetime
from flask import render_template
from flask import request
from NZoneScoreboard import app

@app.route('/')
def redirect():
    return scoreboard(12313)

@app.route('/nc/scoreboard/<id>')
def scoreboard(id):
    """Renders the scoreboard page."""
    print("Open Scoreboard")
    match = getCurrentMatchByUser(id)
    print(match)
    if not (match is None):
        return render_template(
            'scoreboard2.html',
             match=match
        )
    else: 
        loggedIn = getCurrentlyLoggedIn()

        return render_template(
            'login_horizontal.html',
             loggedIn=loggedIn
        )

@app.route('/nc/login_queue_board')
def login_queue():
    """Renders the scoreboard page."""
    print("Open Login Queue Board")
    loggedIn = getCurrentlyLoggedIn()
    return render_template(
        'login_vertical.html',
        loggedIn=loggedIn
    )
        
@app.route('/nc/scoreboard/past/<uid>')
def scoreboard_past(uid):
    """Renders the scoreboard page."""
    print("Open Scoreboard")
    match = getPastMatchByUser(uid)
    print(match)
    if not (match is None):
        return render_template(
            'scoreboard2.html',
             match=match
        )
    else: 
        loggedIn = getCurrentlyLoggedIn()

        return render_template(
            'login_horizontal.html',
             loggedIn=loggedIn
        )

def getPastMatchByUser(uid):
    r = requests.get("https://new-chapter.eu/app.php/nczone/api/matches/past")
    matches = r.json()
    out = {}
    match = findMatchbyUser(uid, matches['items'])
    if not (match is None):
        out['team1'] = []
        out['team2'] = []
        for p in match['players']['team1']:
            player = {}
            player['name'] = p['username']
            player['rating'] = p['rating']
            out['team1'].append(player)
        for p in match['players']['team2']:
            player = {}
            player['name'] = p['username']
            player['rating'] = p['rating']
            out['team2'].append(player)
        out['teamsize'] = len(out['team1'])
        return out
    return None

def getCurrentMatchByUser(uid):
    r = requests.get("https://new-chapter.eu/app.php/nczone/api/matches/running")
    matches = r.json()
    out = {}
    match = findMatchbyUser(uid, matches)
    if not (match is None):
        out['team1'] = []
        out['team2'] = []
        for p in match['players']['team1']:
            player = {}
            player['name'] = p['username']
            player['rating'] = p['rating']
            out['team1'].append(player)
        for p in match['players']['team2']:
            player = {}
            player['name'] = p['username']
            player['rating'] = p['rating']
            out['team2'].append(player)
        out['teamsize'] = len(out['team1'])
        return out
    return None

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
    r = requests.get("https://new-chapter.eu/app.php/nczone/api/players/logged_in")
    logged_in = r.json();
    out = {}
    players = []
    out['players'] = players
    if not (logged_in is None):
        for p in logged_in:
            player = {}
            player['name'] = p['username']
            player['rating'] = p['rating']
            i = 0
            while i < 30:
                players.append(player)
                i += 1
        out['playerslegth'] = len(players)
    return out
        