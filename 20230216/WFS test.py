from owslib.wfs import WebFeatureService
from shapely.geometry import Point
import geopandas as gpd

wfstest = WebFeatureService(url="https://www.dov.vlaanderen.be/geoserver/wfs", version="2.0.0")
layer = wfstest['gw_bescherming:beschermingszones_2016']
 
url = "http://example.com/geoserver/wfs?service=WFS&version=2.0.0&request=GetFeature&typeNames=myworkspace:mylayer&outputFormat=application/json"

print(type(layer))
print(layer)