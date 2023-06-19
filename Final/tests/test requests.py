import requests
import json


data="Hulstlo 9, 8730 Beernem"
url = "http://localhost:5000/getcoordinates"


response = requests.post(url,data=json.dumps(data))

if response.status_code == 200:
    data1 = response.json()
    print(data1)

else:
    response.raise_for_status()
"""
data2 = data1
url2 = "http://localhost:6000/getpropertyarea"


response = requests.post(url2,data=json.dumps(data2))

if response.status_code == 200:
    data2 = response.json()
    print(data2)

else:
    response.raise_for_status()


url3 = "http://localhost:5000/getwatercatchment"
data2 = data1

response = requests.post(url3,data=json.dumps(data2))

if response.status_code == 200:
    data3 = response.json()
    print(data3)

else:
    response.raise_for_status()

"""

url4 = "http://127.0.0.1:3000/rec"
data3 = [500,565,30]

response = requests.post(url4,data=json.dumps(data3))

if response.status_code == 200:
    data3 = response.json()
    print(data3)

else:
    response.raise_for_status()

