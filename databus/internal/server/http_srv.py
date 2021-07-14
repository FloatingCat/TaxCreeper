import http
from typing import Optional, List
from fastapi import FastAPI, Path, Query
from pydantic import BaseModel
from databus.internal.service.poster.mission_create import create_mission
from databus.internal.service.mission_seq.mission_checker import mission_check
app = FastAPI()


class CreateReq(BaseModel):
    topic: str
    url: str


class CheckMissionReq(BaseModel):
    topic: str
    url: str
    latest_receive: float


@app.post("/post_mission/")
async def post_mission(mission: CreateReq):
    res = create_mission(mission.topic, mission.url)  # 'tax_crawler', url=""
    return {"result": res}


@app.post("/check_mission/")
async def check_mission(mission: CheckMissionReq):
    res = mission_check(mission.topic, mission.url, mission.latest_receive)  # 'tax_crawler', url=""
    return {"result": res}
