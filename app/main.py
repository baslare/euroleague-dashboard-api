import pymongo
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from simplejson import dumps
import json

app = FastAPI()
client = pymongo.MongoClient("mongodb://root:password@mongo:27017/")
db = client["euroleague_dashboard"]


@app.get("/Player")
def get_single_player(player_id: str):
    players_agg = db["players_agg"]

    q = {"PLAYER_ID": player_id}
    response = players_agg.find_one(q, {"_id": 0})
    return JSONResponse(json.loads(dumps(response, ignore_nan=True)))


@app.get("/Team")
def get_single_team(team: str):
    teams_agg = db["teams_agg"]

    q = {"CODETEAM": team}
    cursor = teams_agg.find_one(q, {"_id": 0})
    response = cursor
    return JSONResponse(json.loads(dumps(response, ignore_nan=True)))


@app.get("/Game")
def get_single_game_data(game_code: int):
    teams = db["teams"]

    q = {"game_code": game_code}
    cursor = teams.find(q, {"_id": 0})
    response = list(cursor)
    return JSONResponse(json.loads(dumps(response, ignore_nan=True)))


@app.get("/GamePlayers")
def get_single_game_players_data(game_code: int):
    players = db["players"]

    q = {"game_code": game_code}
    cursor = players.find(q, {"_id": 0})
    response = list(cursor)
    return JSONResponse(json.loads(dumps(response, ignore_nan=True)))


@app.get("/LineupStats")
def get_lineup_stats(p1: str, p2: str, p3: str, p4: str, p5: str):
    lineups_agg = db["lineups_agg"]
    lineup_list = sorted([p1, p2, p3, p4, p5])
    lineup_text = "; ".join(lineup_list)

    q = {"lineups_string": lineup_text}
    cursor = lineups_agg.find(q, {"_id": 0})
    response = list(cursor)
    return JSONResponse(json.loads(dumps(response, ignore_nan=True)))


@app.get("/LineupSingleGameStats")
def get_single_game_lineup_data(game_code: int):
    lineups = db["lineups"]

    q = {"game_code": game_code}
    cursor = lineups.find(q, {"_id": 0})
    response = list(cursor)
    return JSONResponse(json.loads(dumps(response, ignore_nan=True)))
