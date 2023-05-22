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

@app.route('/nc/scoreboard/<id>')
def scoreboard(id):
    """Renders the scoreboard page."""
    print("Open Scoreboard")
    match = getCurrentMatch(id)
    print(match)
    #getCurrentlyLoggedIn()
    return render_template(
        'scoreboard.html',
        match=match
    )


def getCurrentMatch(id):
    r = requests.get("https://new-chapter.eu/app.php/nczone/api/matches/running")
    matches = r.json()
    out = {}
    match = findMatch(id, matches)
    out['team1'] = []
    out['team2'] = []
    for p in match["players"]["team1"]:
        out['team1'].append(p)
    for p in match["players"]["team2"]:
        out['team2'].append(p)
    out['teamsize'] = len(out['team1'])
    return out

def findMatch(id, matches):
    for m in matches:
        team1 = m["players"]["team1"]
        team2 = m["players"]["team2"]
        for p in  team1:
            if p['id'] == int(id):
                return m
        for p in team2:
            if p['id'] == int(id):
                return m



#def getCurrentlyLoggedIn():
 #   r = requests.get("https://new-chapter.eu/app.php/nczone/api/players/logged_in")
 #   logged_in = r.json();
 #   for p in logged_in:
 #       print("Player: " + str(p))
 #       print("Player Id: " + str(p['id']))
        