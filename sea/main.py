from typing import Optional

from fastapi import FastAPI

from sea.logic import closest

app = FastAPI()

@app.get("/which/{type}")
def read_item(type: str, latitude: float, longitude: float):
    if type not in ['sea', 'ocean']:
        return {
            'error': 'Invalid parameter. Only "sea" and "ocean" are allowed look ups.'
        }
    if not longitude or not latitude:
        return {
            'error': 'Either latitude or longitude where not provided.'
        }

    return closest({'latitude': latitude, 'longitude': longitude}, type)
