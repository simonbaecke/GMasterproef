import pandas as pd
import numpy as np
import json

# Create the dataframe from the JSON
data = {"hergebruik":[20,40],"1":[1,2],"2":[3,4],"3":[5,6],"4":[7,8]}
with open(r"C:\Users\simon_w3\OneDrive - UGent\School\Ugent\2de ma ing.-arch\Masterproef\GMasterproef\Final\flask_services\flask_recsubsufarea\flaskr\public\reftable.json", 'r') as table:
    data = json.load(table)
df = pd.DataFrame(data)

# Set the index to 'hergebruik'
df.set_index('hergebruik', inplace=True)

#input
hergebruik = float(input())
if hergebruik not in df.index:
    df.loc[hergebruik] = [np.nan for x in list(df.columns)]

hemelwaterput = float(input())
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
print(y.loc[hergebruik,hemelwaterput])

