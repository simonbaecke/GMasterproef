from flask import (
    Blueprint, render_template, request, make_response, jsonify
)
import requests
import json
import urllib.parse
import os

bp = Blueprint('coordinateconversion', __name__, url_prefix='/conv')

@bp.route('/', methods=['GET'])
def description():
    return render_template('home.html')

@bp.route('/coordinateconversion', methods=('GET', 'POST'))
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
        adress = eval(data.decode('utf-8'))
        percentencodedadress = urllib.parse.quote(adress)

        url = "https://loc.geopunt.be/geolocation/Location?q=adressdata".replace("adressdata",percentencodedadress)
        apiresponse = requests.get(url)

        if apiresponse.status_code == 200:
            data = apiresponse.json()
            json_string = json.dumps(data, ensure_ascii=False, indent=4)
            absolute_path = os.path.dirname(__file__)[:-11]
            relative_path = "\private\location.json"
            full_path = absolute_path + relative_path

            with open(full_path, "w") as write_file:
                write_file.write(json_string)
            x = data['LocationResult'][0]['Location']['X_Lambert72']
            y = data['LocationResult'][0]['Location']['Y_Lambert72']

            response = make_response( jsonify([x,y]) )
            response.status_code = 200
            return response
        
        else:
            error_message = "cannot reach coordinateconversion microservice"
            error_response = {'error': error_message}
            return jsonify(error_response), 400
    
    


