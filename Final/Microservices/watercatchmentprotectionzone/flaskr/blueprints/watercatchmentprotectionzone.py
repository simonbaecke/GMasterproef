from flask import (
    Blueprint, render_template, request, make_response,jsonify
)
import requests
import urllib.parse
import json
import os

bp = Blueprint('watercatchmentprotectionzone', __name__, url_prefix='/op')

@bp.route('/', methods=['GET'])
def description():
    return render_template('home.html')

@bp.route('/watercatchmentprotectionzone', methods=('GET', 'POST'))
def operation():
    if request.method == 'GET':
        response = make_response({
            "supported_methods": ["GET", "POST"],
            "POST_request_data": "application/json",
            "POST_response_data": "application/json",
        })

        return response

    elif request.method == 'POST':
        data=request.data
        xy = eval(data.decode('utf-8'))
        x=xy[0]
        y=xy[1]
        percentencodedxy = urllib.parse.quote(str(x)+' '+str(y))
        url = "https://www.dov.vlaanderen.be/geoserver/wfs?service=WFS&version=2.0.0&request=GetFeature&typeNames=gw_bescherming:beschermingszones_2016&outputFormat=application/json&CQL_FILTER=CONTAINS(geom,POINT(lambert72coordinates))".replace('lambert72coordinates',percentencodedxy)

        #bypas script protection
        user_agent = 'Mozilla/5.0'
        wfsresponse = requests.get(url, headers={'User-Agent': user_agent})

        if wfsresponse.status_code == 200:
            data = wfsresponse.json()
            json_string = json.dumps(data, ensure_ascii=False, indent=4)

            absolute_path = os.path.dirname(__file__)[:-11]
            relative_path = "\private\watercatchmentzone.json"
            full_path = absolute_path + relative_path
            with open(full_path, "w") as write_file:
                write_file.write(json_string)

            if data["totalFeatures"]==0:
                Grondwaterwingebied = 4
            else:
                Grondwaterwingebied = data["features"][0]["properties"]["zone_"]
            

            response = make_response(jsonify(Grondwaterwingebied))
            response.status_code = 200
            return response
        else:
            error_message = "cannot reach watercatchmentprotectionzone microservice"
            error_response = {'error': error_message}
            return jsonify(error_response), 400
    
    


