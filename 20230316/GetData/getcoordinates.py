import requests
import json
import urllib.parse


# adress = input()
adress = '25 kaprijke'
def getcoordinates(adress):
    percentencodedadress = urllib.parse.quote(adress)
    url = "https://loc.geopunt.be/v4/Location?q=url".replace("url",percentencodedadress)
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        json_string = json.dumps(data, ensure_ascii=False, indent=4)
        with open("./Output/location.json", "w") as write_file:
            write_file.write(json_string)
    else:
        response.raise_for_status()

    x = data['LocationResult'][0]['Location']['X_Lambert72']
    y = data['LocationResult'][0]['Location']['Y_Lambert72']

    return [x,y]

getcoordinates(adress)