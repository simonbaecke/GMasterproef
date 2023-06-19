import requests
from flask import (Blueprint, jsonify, request)
import urllib.parse
import json

bp = Blueprint('getwatercatchment',__name__)
@bp.route('/getwatercatchment', methods=['GET','POST'])

def getwatercatchment():

    if request.method == "POST":
        data=request.data
        xy = eval(data.decode('utf-8'))
        x=xy[0]
        y=xy[1]
        percentencodedxy = urllib.parse.quote(str(x)+' '+str(y))
    else:
        percentencodedxy=request.args.get("xy")


    url = "https://www.dov.vlaanderen.be/geoserver/wfs?service=WFS&version=2.0.0&request=GetFeature&typeNames=gw_bescherming:beschermingszones_2016&outputFormat=application/json&CQL_FILTER=CONTAINS(geom,POINT(lambert72coordinates))".replace('lambert72coordinates',percentencodedxy)

    #omzeilen bescherming tegen script
    user_agent = 'Mozilla/5.0'
    response = requests.get(url, headers={'User-Agent': user_agent})

    if response.status_code == 200:
        data = response.json()
        json_string = json.dumps(data, ensure_ascii=False, indent=4)
        with open("public/watercatchment.json", "w") as write_file:
            write_file.write(json_string)

        if data["totalFeatures"]==0:
            print('lege lijst')
            Grondwaterwingebied = 4
        else:
            Grondwaterwingebied = data["features"][0]["properties"]["zone_"]
        return jsonify(Grondwaterwingebied)
    else:
        response.raise_for_status()



