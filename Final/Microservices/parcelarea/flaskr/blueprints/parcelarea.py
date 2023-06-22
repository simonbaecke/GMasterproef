from flask import (
    Blueprint, render_template, request, make_response, jsonify
)
import requests
import urllib.parse
import json
from shapely.geometry import Polygon
import os

bp = Blueprint('parcelarea', __name__, url_prefix='/op')

@bp.route('/', methods=['GET'])
def description():
    return render_template('home.html')

@bp.route('/parcelarea', methods=('GET', 'POST'))
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

        url = "https://geo.api.vlaanderen.be/GRB/wfs?service=WFS&version=2.0.0&request=GetFeature&typeNames=GRB:ADP&outputFormat=application/json&CQL_FILTER=CONTAINS(SHAPE,POINT(lambert72coordinates))".replace('lambert72coordinates',percentencodedxy)
        
        #bypass script protection
        user_agent = 'Mozilla/5.0'
        responsewfs = requests.get(url, headers={'User-Agent': user_agent})

        if responsewfs.status_code == 200:
            data = responsewfs.json()
            json_string = json.dumps(data, ensure_ascii=False, indent=4)
            absolute_path = os.path.dirname(__file__)[:-11]
            relative_path = "\private\parcel.json"
            full_path = absolute_path + relative_path
            with open(full_path, "w") as write_file:
                write_file.write(json_string)

            coords = data["features"][0]['geometry']['coordinates'][0]
            parcel = Polygon(coords)
            area = parcel.area    
        
            response = make_response( jsonify(area) )
            response.status_code = 200
            return response
        
        else:
            error_message = "cannot reach parcelarea microservice"
            error_response = {'error': error_message}
            return jsonify(error_response), 400
    
    


