'''
Routes and views for the flask application.
'''

from typing import Optional
import requests
from flask import render_template
from flask import request
from NZoneScoreboard import app


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def defaultPage(path: str) -> str:
    return render_template('default.html')


@app.route('/nc/scoreboard/<int:uid>')
def scoreboard(uid: int) -> str:
    '''Renders the scoreboard page.'''
    match = getCurrentMatchByUser(uid)

    parameter = request.args
    opacity = float(parameter.get('opacity', 1.0))

    return renderMatchOrLogin(match, opacity)


@app.route('/nc/scoreboard/past/<int:uid>')
def scoreboard_past(uid: int) -> str:
    '''Renders the scoreboard page.'''
    match = getPastMatchByUser(uid)

    parameter = request.args
    opacity = float(parameter.get('opacity', 1.0))

    return renderMatchOrLogin(match, opacity)


def getCurrentMatchByUser(uid: int) -> Optional[dict]:
    return getCommonMatchByUser(uid, 'running')


def getPastMatchByUser(uid: int) -> Optional[dict]:
    return getCommonMatchByUser(uid, 'past')


def getCommonMatchByUser(uid: int, type: str) -> Optional[dict]:
    r = requests.get(
        f'https://new-chapter.eu/app.php/nczone/api/matches/{type}')
    res = r.json()
    if not res:
        return None

    matches = res.get('items', [])
    match = findMatchbyUser(uid, matches or [])
    return getMatchInfo(match) if match else None


def findMatchbyUser(uid: int, matches: list) -> Optional[dict]:
    for match in matches:
        players = match.get('players', [])
        team1 = players.get('team1', [])
        team2 = players.get('team2', [])

        for p in team1 + team2:
            if p.get('id', None) == uid:
                return match
    return None


def getMatchInfo(match: dict) -> dict:
    players = match.get('players', [])
    playersT1 = generatePlayers(players.get('team1', []))
    playersT2 = generatePlayers(players.get('team2', []))
    teamCivs = match.get('civs', [])
    return {
        'team1': playersT1,
        'ratingT1': getTotalTeamRating(playersT1),
        'team2': playersT2,
        'ratingT2': getTotalTeamRating(playersT2),
        'team1Civs': generateCivIcons(teamCivs.get('team1', [])),
        'team2Civs': generateCivIcons(teamCivs.get('team2', [])),
        'teamsize': len(playersT1),
        'map': match.get('map', {}).get('name', ''),
    }


def renderMatchOrLogin(match: Optional[dict], opacity: float = 1.0) -> str:
    if match:
        if len(match.get('team1Civs', [])) > 0:
            return render_template(
                'scoreboardCivPool.html',
                match=match,
                opacity=opacity
            )
        else:
            return render_template(
                'scoreboard.html',
                match=match,
                opacity=opacity
            )
    else:
        loggedIn = getCurrentlyLoggedIn()

        return render_template(
            'login_horizontal.html',
            loggedIn=loggedIn,
            opacity=opacity
        )


def getTotalTeamRating(players: list) -> int:
    return sum([int(p['rating']) for p in players])


def generatePlayers(players: list) -> list[dict]:
    out = []
    for p in players:
        player = {}
        username = p.get('username', '')
        if len(username) > 16:
            username = username[:14] + '..'
        player['name'] = username
        player['rating'] = int(p.get('rating', 0))
        player['civs'] = generateCivIcons(p.get('civs', []))
        out.append(player)
    return out


def generateCivIcons(civs: list) -> list[dict]:
    out = []
    for c in civs:
        civ = {}
        title = c.get('title', '')
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


def getCurrentlyLoggedIn() -> dict:
    r = requests.get(
        'https://new-chapter.eu/app.php/nczone/api/players/logged_in')
    logged_in = r.json()

    out = {'players': [], 'playerslength': 0}
    if logged_in:
        for p in logged_in:
            out['players'].append({
                'name': p.get('username', ''),
                'rating': int(p.get('rating', 0)),
            })
        out['playerslength'] = len(out['players'])
    return out
