from flask import (
    Blueprint, render_template, request, make_response, jsonify
)
import json
import pandas as pd
import numpy as np
import os

bp = Blueprint('subtractabledrainagesurfacearea', __name__, url_prefix='/op')

# Adding a function to the "/op/" URI
@bp.route('/', methods=['GET'])
def description():
    return render_template('home.html')

# Adding a function to the "/op/some-operation" URI
@bp.route('/subtractabledrainagesurfacearea', methods=('GET', 'POST'))
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
        parameters = eval(data.decode('utf-8'))
        roofarea = float(parameters[0])
        reuse = float(parameters[1])
        rainwatertankcapacity = float(parameters[2])/1000

        reuse_scaled = (reuse/roofarea)*100
        rainwatertankcapacity_scaled = (rainwatertankcapacity/roofarea)*100

        absolute_path = os.path.dirname(__file__)[:-11]
        relative_path = "\public\\reftable.json"
        full_path = absolute_path + relative_path

        with open(full_path, 'r') as table:
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

        if str(roofarea_sub_scaled) == "nan":
            roofarea_sub = 0
        else:
            roofarea_sub = roofarea_sub_scaled*roofarea/100
        
        #nog nakijken dit is als het lager is dan 60 en nog checken of het ok is als het omgekeerd is
        if roofarea_sub <60:
            roofarea_sub = 60

        response = make_response(jsonify(roofarea_sub))
        response.status_code = 200
        return response
    
    


