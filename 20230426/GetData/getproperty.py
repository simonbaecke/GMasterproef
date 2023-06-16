import json
from shapely.geometry import Polygon

with open('./Output/perceel.json') as f:
    data = json.load(f)

coords = data["features"][0]['geometry']['coordinates'][0]

perceel = Polygon(coords)
area = perceel.area
print(area)