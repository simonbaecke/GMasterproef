from flask import (Blueprint, jsonify, request)
import json
import pandas as pd
import numpy as np

bp = Blueprint('rec',__name__)
@bp.route('/rec', methods=['GET','POST'])

def rec():

    if request.method == "POST":
        data=request.data
        parameters = eval(data.decode('utf-8'))
        roofarea = float(parameters[0])
        reuse = float(parameters[1])
        rainwatertankcapacity = float(parameters[2])/1000
    else:
        roofarea = float(request.args.get("roofarea"))
        reuse = float(request.args.get("reuse"))
        rainwatertankcapacity = float(request.args.get("rainwatertankcapacity"))


    reuse_scaled = (reuse/roofarea)*100
    rainwatertankcapacity_scaled = (rainwatertankcapacity/roofarea)*100


    with open(r"C:\Users\simon_w3\OneDrive - UGent\School\Ugent\2de ma ing.-arch\Masterproef\GMasterproef\Final\flask_services\flask_recsubsufarea\public\reftable.json", 'r') as table:
        data = json.load(table)
    df = pd.DataFrame(data)

    # Set the index to 'hergebruik'
    df.set_index('hergebruik', inplace=True)

    #input
    hergebruik = reuse_scaled
    if hergebruik not in df.index:
        df.loc[hergebruik] = [np.nan for x in list(df.columns)]

    hemelwaterput = rainwatertankcapacity_scaled
    header = [float(x) for x in df.columns.tolist()]
    if hemelwaterput not in header:
        df[hemelwaterput]=np.nan

    #convert to float and sort
    df.columns = [float(x) for x in list(df.columns)]
    df = df.sort_values("hergebruik")
    df = df.sort_index(axis=1)

    #interpolate
    x = df.interpolate(method="values")
    y = x.interpolate(method="values",axis=1)
    print(y)
    roofarea_sub_scaled = y.loc[hergebruik,hemelwaterput]
    print(roofarea_sub_scaled)

    if roofarea_sub_scaled == "nan":
        roofarea_sub = roofarea
    else:
        roofarea_sub = roofarea_sub_scaled*roofarea/100

    return jsonify(roofarea_sub)