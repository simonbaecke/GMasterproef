import requests
import json
import urllib.parse
from flask import (Blueprint, jsonify, request)

bp = Blueprint('getcoordinates',__name__)
@bp.route('/getcoordinates', methods=['GET','POST'])

# adress = input()
def getcoordinates():

    if request.method == "POST":
        data=request.data
        adress = eval(data.decode('utf-8'))
        percentencodedadress = urllib.parse.quote(adress)
    else:
        percentencodedadress=request.args.get("adress")


    url = "https://loc.geopunt.be/geolocation/Location?q=adressdata".replace("adressdata",percentencodedadress)
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        json_string = json.dumps(data, ensure_ascii=False, indent=4)
        with open("./public/location.json", "w") as write_file:
            write_file.write(json_string)
        x = data['LocationResult'][0]['Location']['X_Lambert72']
        y = data['LocationResult'][0]['Location']['Y_Lambert72']
    else:
        response.raise_for_status()

    return jsonify([x,y])