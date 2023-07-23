import pymongo
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from simplejson import dumps
import json
import inspect

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


@app.get("/GameLite")
def get_single_game_data_lite(game_code: int):
    teams = db["teams"]

    q = {"game_code": game_code}
    cols = ["CODETEAM", "OPP", "home", "AS", "TO",
            "2FGM", "2FGA", "2FGR",
            "3FGM", "3FGA", "3FGR",
            "FTM", "FTA", "FTR",
            "D", "DRBEBR", "O", "ORBEBR",
            "FV", "ST", "pos", "PPP"]

    cols_dict = {x: 1 for x in cols}
    cols_dict["_id"] = 0
    cursor = teams.find(q, cols_dict)
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


@app.get("/PointsSingleGame")
def get_single_game_points_data(game_code: int):
    points = db["points_agg"]

    q = {"game_code": game_code}
    cursor = points.find(q, {"_id": 0})
    response = list(cursor)
    return JSONResponse(json.loads(dumps(response, ignore_nan=True)))


@app.get("/PointsTeam")
def get_agg_team_points_data(team: str):
    points = db["points_agg"]

    q = {"TEAM": team}
    cursor = points.find(q, {"_id": 0})
    response = list(cursor)
    return JSONResponse(json.loads(dumps(response, ignore_nan=True)))


@app.get("/PointsPlayer")
def get_agg_player_points_data(player_id: str
                               ):
    points = db["points_agg"]

    q = {"ID_PLAYER": player_id}
    cursor = points.find(q, {"_id": 0})
    response = list(cursor)
    return JSONResponse(json.loads(dumps(response, ignore_nan=True)))


@app.get("/AssistsSingleGame")
def get_game_assists(game_code: int):
    assists = db["assists"]

    q = {"game_code": game_code}
    cursor = assists.find(q, {"_id": 0})
    response = list(cursor)
    return JSONResponse(json.loads(dumps(response, ignore_nan=True)))


@app.get("/AssistsPlayer")
def get_game_assists(player_id: str | None = None,
                     assisting_player: str | None = None):
    frame = inspect.currentframe()
    args, _, _, values = inspect.getargvalues(frame)

    assists = db["assists"]
    query_params = ["PLAYER_ID", "assisting_player"]

    q = {key: values.get(arg) for key, arg in zip(query_params, args) if values.get(arg)}

    cursor = assists.find(q, {"_id": 0})
    response = list(cursor)
    return JSONResponse(json.loads(dumps(response, ignore_nan=True)))


@app.get("/Quantile")
def get_quantile(type: str):
    quantiles = db["quantiles"]

    q = {"type": type}
    cursor = quantiles.find(q, {"_id": 0})
    response = list(cursor)
    return JSONResponse(json.loads(dumps(response, ignore_nan=True)))
