import requests
import json
import urllib.parse

adress = input()
percentencodedadress = urllib.parse.quote(adress)
url = "https://loc.geopunt.be/v4/Location?q=url".replace("url",percentencodedadress)
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    json_string = json.dumps(data, ensure_ascii=False, indent=4)
    print(json_string)
    with open("adress.json", "w") as write_file:
        write_file.write(json_string)
else:
    response.raise_for_status()

