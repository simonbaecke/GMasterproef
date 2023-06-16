import requests
from flask import (Blueprint, jsonify, request)
import urllib.parse
import json
from shapely.geometry import Polygon

bp = Blueprint('recommendedsubtractedinfiltrationarea',__name__)
@bp.route('/recommendedsubtractedinfiltrationarea', methods=['GET','POST'])

def recommendedsubtractedinfiltrationarea():
    """
        if request.method == "POST":
            #nog afhankelijk van hoe data wordt aangeleverd
            data=request.data
            xy = eval(data.decode('utf-8'))
            xy = eval(xy)
            x=xy[0]
            y=xy[1]
            print(x)
            print(y)
            percentencodedxy = urllib.parse.quote(str(x)+' '+str(y))
            print(percentencodedxy)
        else:
    """
    hergebruik=request.args.get("hergebruik")
    dakopp=request.args.get("dakopp")
    hemelwaterput=request.args.get("hemelwaterput")

    hergebruik_scaled = (hergebruik/dakopp)*100
    hemelwaterput_scaled = (hemelwaterput/dakopp)*100

    data= {}

    dakopp_inrekening = dakopp_inrekening_scaled*dakopp/100

