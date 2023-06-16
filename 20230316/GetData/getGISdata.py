import requests
import urllib.parse
import json

# x = float(input())
# y = float(input())
x=100152
y=206666

percentencodedxy = urllib.parse.quote(str(x)+' '+str(y))
urlperceel = "https://geo.api.vlaanderen.be/GRB/wfs?service=WFS&version=2.0.0&request=GetFeature&typeNames=GRB:ADP&outputFormat=application/json&CQL_FILTER=CONTAINS(SHAPE,POINT(url))".replace('url',percentencodedxy)
bestandsnaamperceel = 'perceel'
urlwater = "https://www.dov.vlaanderen.be/geoserver/wfs?service=WFS&version=2.0.0&request=GetFeature&typeNames=gw_bescherming:beschermingszones_2016&outputFormat=application/json&CQL_FILTER=CONTAINS(geom,POINT(url))".replace('url',percentencodedxy)
bestandsnaamwater = 'winwatergebied'

def getWFS(url,bestandsnaam):
    #omzeilen bescherming tegen script
    user_agent = 'Mozilla/5.0'
    response = requests.get(url, headers={'User-Agent': user_agent})

    if response.status_code == 200:
        data = response.json()
        json_string = json.dumps(data, ensure_ascii=False, indent=4)
        with open("C:/Users/simon_w3/OneDrive - UGent/School/Ugent/2de ma ing.-arch\Masterproef/GMasterproef/20230316/Output/"+bestandsnaam+".json", "w") as write_file:
            write_file.write(json_string)
        return data
    else:
        response.raise_for_status()

getWFS(urlperceel,bestandsnaamperceel)
getWFS(urlwater,bestandsnaamwater)

print('2 JSON files generated')