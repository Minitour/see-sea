import pandas as pd
from geopy import distance
import pathlib

path = pathlib.Path(__file__).parent.resolve()

points = pd.read_csv(f'{path}/data/points.csv')


def _distance_between(point_a: dict, point_b: dict):
    p1 = point_a['latitude'], point_a['longitude']
    p2 = point_b['latitude'], point_b['longitude']

    return distance.distance(p1, p2).meters


def closest(point: dict, what='sea') -> dict:
    entries = points[points['type'] == what].T.to_dict().values()

    def add_distance_to(sea: dict):
        dis = _distance_between(sea, point)
        sea['distance'] = dis

    for entry in entries:
        add_distance_to(entry)

    return min(entries, key=lambda e: e['distance'])
