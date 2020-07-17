#-----------[Potential Issue] Shape point too close to node point------------------

distance = QgsDistanceArea()
distance.setEllipsoid('WGS84')
f_id = []
layer = iface.mapCanvas().layers()[0]
features = layer.getFeatures()
for feature in features:
    geoms = feature.geometry()
    geom = geoms.asMultiPolyline()
    for r in range(len(geom[0])):
        if r == 0:
            diff = distance.measureLine(geom[0][r],geom[0][r+1])
            if diff < 1:
                f_id.append(feature.id())
        elif r == len(geom[0]):
            diff = distance.measureLine(geom[0][r],geom[0][r-1])
            if diff < 1:
                f_id.append(feature.id())
layer.selectByIds([p for p in f_id])


#--------------------------------Adjacent Grid Viaduct--------------------------------

layer = iface.mapCanvas().layers()[0]
roadSelected = layer.materialize(QgsFeatureRequest().setSubsetOfAttributes(['plid','roadclass'],layer.fields()))
params = {'INPUT' : roadSelected, u'PREDICATE': [7], 'INTERSECT' : roadSelected, 'METHOD': 0, 'OUTPUT':'memory:overlap'}
overlapLayer = processing.run("native:extractbylocation", params)

params = {'INPUT':overlapLayer['OUTPUT'], 'OUTPUT':'memory:verticesA'}
verticesAll = processing.run("native:extractvertices", params)

params = {'INPUT':overlapLayer['OUTPUT'], 'INTERSECT':overlapLayer['OUTPUT'], 'OUTPUT':'memory:verticesI'}
verticesIntersect = processing.run("native:lineintersections", params)

params = {'INPUT' : verticesAll['OUTPUT'], u'PREDICATE': [3], 'INTERSECT' : verticesIntersect['OUTPUT'], 'METHOD': 0, 'OUTPUT':'memory:final'}
finalLayer = processing.run("native:extractbylocation", params)
QgsProject.instance().addMapLayer(finalLayer['OUTPUT'])


