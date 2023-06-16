import json

with open('./Output/winwatergebied.json') as f:
    data = json.load(f)

if data["totalFeatures"]==0:
    print('lege lijst')
    Grondwaterwingebied = 0
else:
    Grondwaterwingebied = data["features"][0]["properties"]["zone_"]

print(Grondwaterwingebied)