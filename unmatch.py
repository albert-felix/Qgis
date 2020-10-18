members = 10
layer = iface.activeLayer()
f_len = len(layer.fields())
features = layer.getFeatures()
layer_count = layer.featureCount()
layerProvider = layer.dataProvider()
layerProvider.addAttributes([QgsField("Members",QVariant.String)])
layer.updateFields()
u_counts = layer_count // members
r_counts = layer_count % members
a = 0
allot = 0
layer.startEditing()
for i in range(layer_count):
    if r_counts > 0:
        if allot < u_counts+1:
            new_value = {f_len:chr(65+a)}
            layerProvider.changeAttributeValues({i:new_value})
            allot += 1
            if allot == u_counts+1:
                allot = 0
                r_counts -= 1
                a += 1
    else:
        if allot < u_counts:
            new_value = {f_len:chr(65+a)}
            layerProvider.changeAttributeValues({i:new_value})
            allot += 1
            if allot == u_counts:
                allot = 0
                a += 1
layer.commitChanges()
