#[Potential Issue] Shape point too close to node point

distance = QgsDistanceArea()
distance.setEllipsoid('WGS84')
f_id = []
layer = iface.mapCanvas().layers()[0]
print(layer.name())
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
