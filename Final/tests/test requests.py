import requests
import json

data="[100688,207134]"
url = "http://localhost:5000/getpropertyarea"


response = requests.post(url,data=json.dumps(data))

if response.status_code == 200:
    data = response.json()
    print(data)
    json_string = json.dumps(data, ensure_ascii=False, indent=4)

else:
    response.raise_for_status()