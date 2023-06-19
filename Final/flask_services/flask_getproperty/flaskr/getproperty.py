import requests
from flask import (Blueprint, jsonify, request)
import urllib.parse
import json
from shapely.geometry import Polygon

bp = Blueprint('getpropertyarea',__name__)
@bp.route('/getpropertyarea', methods=['GET','POST'])

def getpropertyarea():

    if request.method == "POST":
        data=request.data
        xy = eval(data.decode('utf-8'))
        x=xy[0]
        y=xy[1]
        percentencodedxy = urllib.parse.quote(str(x)+' '+str(y))
    else:
        percentencodedxy=request.args.get("xy")

    url = "https://geo.api.vlaanderen.be/GRB/wfs?service=WFS&version=2.0.0&request=GetFeature&typeNames=GRB:ADP&outputFormat=application/json&CQL_FILTER=CONTAINS(SHAPE,POINT(lambert72coordinates))".replace('lambert72coordinates',percentencodedxy)
    
    #omzeilen bescherming tegen script
    user_agent = 'Mozilla/5.0'
    response = requests.get(url, headers={'User-Agent': user_agent})

    if response.status_code == 200:
        data = response.json()
        json_string = json.dumps(data, ensure_ascii=False, indent=4)
        with open("private/property.json", "w") as write_file:
            write_file.write(json_string)

        coords = data["features"][0]['geometry']['coordinates'][0]

        perceel = Polygon(coords)
        area = perceel.area    
        return jsonify(area)
    else:
        response.raise_for_status()
