import math
import json

def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

with open(r"C:\Users\simon_w3\OneDrive - UGent\School\Ugent\2de ma ing.-arch\Masterproef\GMasterproef\Final\Input\reftable.json", 'r') as p:
  data = json.load(p)

  print(list((data.keys()))[1:])
  newdata = {'hergebruik' : data['hergebruik']}

  for key in list(data.keys())[1:]:
    x =  data[key]
    lijst = []
    for nummer in x:
        newnummer = round(100 - nummer,2)
        lijst.append(newnummer)
    newdata[key] = lijst


datajson = json.dumps(newdata, indent = 4)

print(datajson)
with open(r"C:\Users\simon_w3\OneDrive - UGent\School\Ugent\2de ma ing.-arch\Masterproef\GMasterproef\Final\Input\reftableinverted.json", 'w') as json_file:
  json_file.write(datajson)