import json

with open(r"C:\Users\simon_w3\OneDrive - UGent\School\Ugent\2de ma ing.-arch\Masterproef\GMasterproef\Final\tests\parameters.json", 'r') as p:
  data = json.load(p)
with open(r"C:\Users\simon_w3\OneDrive - UGent\School\Ugent\2de ma ing.-arch\Masterproef\GMasterproef\Final\tests\values.json", 'r') as f:
  values = json.load(f)


print(json.dumps(data, indent = 4, sort_keys=True))
print(values.keys())

for id in values.keys():
  for parameters in data:
    if parameters["id"] == id:
       parameters["value"] = values[id]
aaa = json.dumps(data, indent = 4, sort_keys=True)

datajson = json.dumps(data, indent = 4, sort_keys=True)
with open(r"C:\Users\simon_w3\OneDrive - UGent\School\Ugent\2de ma ing.-arch\Masterproef\GMasterproef\Final\tests\parameters2.json", 'w') as json_file:
  json_file.write(aaa)