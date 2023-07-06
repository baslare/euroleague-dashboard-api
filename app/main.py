from typing import Union
import pymongo
from fastapi import FastAPI
from bson.json_util import dumps

app = FastAPI()


@app.get("/Players")
def get_player(player_id: str):
    client = pymongo.MongoClient("mongodb://root:password@mongo:27017/")

    db = client["euroleague_dashboard"]
    players_agg = db["players_agg"]

    q = {"PLAYER_ID": player_id}
    response = list(players_agg.find(q))
    return dumps(response)


@app.get("/Team")
def get_team(team: str):
    client = pymongo.MongoClient("mongodb://root:password@mongo:27017/")

    db = client["euroleague_dashboard"]
    teams_agg = db["teams_agg"]

    q = {"CODETEAM": team}
    response = list(teams_agg.find(q))
    return dumps(response)
