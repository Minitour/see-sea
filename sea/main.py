from fastapi import FastAPI

from sea.logic import closest

app = FastAPI()


@app.get("/which/sea")
def read_item(latitude: float, longitude: float):
    return closest({'latitude': latitude, 'longitude': longitude}, 'sea')


@app.get("/which/ocean")
def read_item(latitude: float, longitude: float):
    return closest({'latitude': latitude, 'longitude': longitude}, 'ocean')
