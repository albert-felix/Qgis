import requests
import json
from random import randrange

latSW = 41.91539393
lonSW = 12.43675127
latNE = 41.91963761
lonNE = 12.44382524

buildingCount = 0
clusterSize = 8

def generateBuilding():
    
    global servicePoints, buildingCount, clusterSize, unique_values

    def toPolygonGeoJson(jsonData):

        geoJson = {
            "type": "FeatureCollection",
            "features": []
            }
        for data in jsonData['elements']:
            coordinates = []
            if 'nodes' in data.keys():
                prop = data['id']
                for id in data['nodes']:
                    for dat in jsonData['elements']:
                        if dat['id'] == id:
                            lat = dat['lat']
                            lon = dat['lon']
                            coordinates.append([lon,lat])
                feature = {
                        "type": "Feature",
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [coordinates]
                        },
                        "properties": {
                            "id":prop
                        }
                    }
                geoJson['features'].append(feature)
        return(json.dumps(geoJson))

    def categorizeSymbol(layer):

        # get unique values 
        fni = layer.fields().indexFromName('CLUSTER_ID')
        unique_values = layer.dataProvider().uniqueValues(fni)

        # define categories
        categories = []
        for unique_value in unique_values:
            symbol = QgsMarkerSymbol.defaultSymbol(layer.geometryType())

            category = QgsRendererCategory(unique_value, symbol, str(unique_value))
            categories.append(category)

        renderer = QgsCategorizedSymbolRenderer('CLUSTER_ID', categories)
        layer.setRenderer(renderer)
        layer.triggerRepaint()

    def generateSplitters(servicePoints):

        params = {'INPUT': servicePoints, 'FIELD':'CLUSTER_ID', 'OUTPUT':'memory:dissolveService'}
        dissolveServiceOutput = processing.run("native:dissolve", params)
        dissolveService = dissolveServiceOutput['OUTPUT']

        params = {'INPUT': dissolveService, 'OUTPUT':'memory:centroidService'}
        centroidServiceOutput = processing.run("native:centroids", params)
        centroidService = centroidServiceOutput['OUTPUT']



    # OSM Overpass API Request
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json][timeout:25];
    // gather results
    (
    // query part for: “building=yes”
    way["building"]({latSW}, {lonSW}, {latNE}, {lonNE});
    relation["building"]({latSW}, {lonSW}, {latNE}, {lonNE});
    );
    // print results
    out body;
    >;
    out skel qt;
    """
    buildingResponse = requests.get(overpass_url, 
                            params={'data': overpass_query})

    buildingResult = buildingResponse.json()
    buildingJson = json.dumps(buildingResult)
    buildingGeoJson = toPolygonGeoJson(json.loads(buildingJson))

    buildingLayer = QgsVectorLayer(buildingGeoJson, "building", "ogr")
    # iface.addVectorLayer(geoJson,"building","ogr")

    params = {'INPUT': buildingLayer, 'OUTPUT':'memory:dissolveBuilding'}
    dissolveBuildingOutput = processing.run("native:dissolve", params)
    dissolveBuilding = dissolveBuildingOutput['OUTPUT']

    params = {'INPUT': dissolveBuilding, 'OUTPUT':'memory:singleBuilding'}
    singleBuildingOutput = processing.run("native:multiparttosingleparts", params)
    singleBuilding = singleBuildingOutput['OUTPUT']

    params = {'INPUT': singleBuilding, 'OUTPUT':'memory:buildingPoints'}
    buildingPointsOutput = processing.run("native:centroids", params)
    buildingPoints = buildingPointsOutput['OUTPUT']
    buildingCount = buildingPoints.featureCount()

    clusters = buildingCount//clusterSize
    params = {'INPUT': buildingPoints, 'CLUSTERS':clusters, 'MINPOINTS':clusterSize, 'OUTPUT':'memory:clusters'}
    cluster = processing.run("script:constrained_kmeans", params)
    servicePoints = cluster['OUTPUT']
    categorizeSymbol(servicePoints)

    # QgsProject.instance().addMapLayer(buildingPoints)
    QgsProject.instance().addMapLayer(servicePoints)


def generateRoad():

    global roadPoints

    def toLineGeoJson(jsonData):

        geoJson = {
            "type": "FeatureCollection",
            "features": []
            }
        for data in jsonData['elements']:
            coordinates = []
            if 'nodes' in data.keys():
                prop = data['id']
                for id in data['nodes']:
                    for dat in jsonData['elements']:
                        if dat['id'] == id:
                            lat = dat['lat']
                            lon = dat['lon']
                            coordinates.append([lon,lat])
                feature = {
                        "type": "Feature",
                        "geometry": {
                            "type": "LineString",
                            "coordinates": coordinates
                        },
                        "properties": {
                            "id":prop
                        }
                    }
                geoJson['features'].append(feature)
        return(json.dumps(geoJson))


    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json][timeout:25];
    (
    way["highway"]({latSW}, {lonSW}, {latNE}, {lonNE});
    relation["highway"]({latSW}, {lonSW}, {latNE}, {lonNE});
    );
    out body;
    >;
    out skel qt;
    """
    roadResponse = requests.get(overpass_url, 
                            params={'data': overpass_query})

    roadResult = roadResponse.json()
    roadJson = json.dumps(roadResult)


    roadGeoJson = toLineGeoJson(json.loads(roadJson))
    roadLayer = QgsVectorLayer(roadGeoJson,"road","ogr")

    # iface.addVectorLayer(roadGeoJson,"road","ogr")
    QgsProject.instance().addMapLayer(roadLayer)

    params = {'INPUT': roadLayer, 'DISTANCE':0.00005, 'OUTPUT':'memory:roadPoints'}
    roadPointsOutput = processing.run("native:pointsalonglines", params)
    roadPoints = roadPointsOutput['OUTPUT']


def generateConnectRoad():

    params = {'INPUT': buildingPoints, 'HUBS': roadPoints, 'FIELD':'id', 'UNIT': 0, 'OUTPUT':'memory:connectRoad'}
    connectRoadOutput = processing.run("qgis:distancetonearesthublinetohub", params)
    connectRoad = connectRoadOutput['OUTPUT']

    QgsProject.instance().addMapLayer(connectRoad)


generateBuilding()
generateRoad()
generateConnectRoad()

