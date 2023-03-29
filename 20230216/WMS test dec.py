"""
from owslib.wms import WebMapService
from shapely.geometry import Point
import geopandas as gdp
import numpy as np

wms = WebMapService('https://www.dov.vlaanderen.be/geoserver/wms?', version='1.3.0')
layer = wms['gw_bescherming:beschermingszones_2016']


print(wms.identification.type)
print(layer.styles)
bbox= layer.boundingBox
print(bbox)
bound = [Point(bbox[0],bbox[2]),Point(bbox[1],bbox[3])]
d = { 'geometry': [Point(bbox[0],bbox[2]),Point(bbox[1],bbox[3])]}
gdf = gdp.GeoDataFrame(d,crs=4326)
converted = gdf.to_crs(31370)
print(converted)

def get_coordinates(point):
    return (point.x,point.y)

coords = converted['geometry'].apply(get_coordinates)
print(coords[0])
#bboxnew = (coords[0][0],coords[0][1],coords[1][0],coords[1][1])
bboxnew = (14697,20939,297193,246456)


img = wms.getmap(layers=['gw_bescherming:beschermingszones_2016'],styles=['gw_bescherming:beschermingszones'],srs='EPSG:31370',bbox=bboxnew,size=(2000,2000),format='image/jpeg',transparant=True)

out = open('jpl.jpg','wb')
out.write(img.read())
out.close()


"""
from shapely.geometry import Point,Polygon
import geopandas as gpd

def get_coordinates(point):
    return (point.x,point.y)


punt = Point(3.65822, 51.18063)
punt2 = Point(5.65822, 40.18063)
d = { 'geometry': [punt,punt2]}
gdf = gpd.GeoDataFrame(d, crs=4326)
print(gdf.head())
x = gdf['geometry'].x
for getal in x:
    print(getal)
print(gdf['geometry'])
coords = gdf['geometry'].apply(get_coordinates)
for coord in coords:
    print(coord)
print(gdf.crs)
gdft=gdf.to_crs(31370)
print(gdft.crs)
