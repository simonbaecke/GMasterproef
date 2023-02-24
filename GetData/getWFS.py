import requests
import json
import urllib.parse
import getcoordinates

# x = float(input())
# y = float(input())
x = 99495
y = 207506

percentencodedxy = urllib.parse.quote(str(getcoordinates.x)+' '+str(getcoordinates.y))
url = "https://www.dov.vlaanderen.be/geoserver/wfs?service=WFS&version=2.0.0&request=GetFeature&typeNames=gw_bescherming:beschermingszones_2016&outputFormat=application/json&CQL_FILTER=CONTAINS(geom,POINT(url))".replace('url',percentencodedxy)
bestandsnaam = 'winwatergebied'

def getWFS(url,bestandsnaam):
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        json_string = json.dumps(data, ensure_ascii=False, indent=4)
        with open("Output/"+bestandsnaam+".json", "w") as write_file:
            write_file.write(json_string)
    else:
        response.raise_for_status()

getWFS(url,bestandsnaam)
