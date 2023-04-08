import requests
import json

data = "valkstraat%2029%20assenede"
url = "http://localhost:3000/getcoordinates"


response = requests.post(url,data=json.dumps(data))

print(response.text)
"""
if response.status_code == 200:
    data = response.json()
    print(data)
    json_string = json.dumps(data, ensure_ascii=False, indent=4)

else:
    response.raise_for_status()
"""