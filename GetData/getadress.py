import requests
import json
import urllib.parse

#x = float(input())
#y = float(input())
x=108588.48
y=214985.36
percentencodedxy = urllib.parse.quote(str(x)+','+str(y))
url = "https://loc.geopunt.be/v4/Location?xy=url".replace("url",percentencodedxy)
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    json_string = json.dumps(data, ensure_ascii=False, indent=4)
    with open("./Output/location.json", "w") as write_file:
        write_file.write(json_string)
else:
    response.raise_for_status()

adress = data['LocationResult'][0]['FormattedAddress']

print(adress)