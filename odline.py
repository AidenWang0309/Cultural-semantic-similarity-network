import arcpy
import json

arcpy.env.overwriteOutput = True

tb = arcpy.GetParameterAsText(0)
pox = arcpy.GetParameterAsText(1)
poy = arcpy.GetParameterAsText(2)
pdx = arcpy.GetParameterAsText(3)
pdy = arcpy.GetParameterAsText(4)
val = arcpy.GetParameterAsText(5)
out_fc = arcpy.GetParameterAsText(6)

sr_str = arcpy.GetParameterAsText(7)

pid = arcpy.GetParameterAsText(8)

sr = arcpy.SpatialReference()
sr.loadFromString(sr_str)

refID = sr.factoryCode

arcpy.AddMessage(refID)

featureList = []
pidList = []

curveValue = float(val)

fields = [pox, poy, pdx, pdy, pid]

with arcpy.da.SearchCursor(tb, fields) as rows:

    for row in rows:

        arcpy.AddMessage(row[0])

        ox = row[0]
        oy = row[1]
        dx = row[2]
        dy = row[3]
        uid = row[4]

        mx = (ox + dx) / 2 - (oy - dy) * curveValue;
        my = (oy + dy) / 2 - (dx - ox) * curveValue;

        coordO = [ox, oy]
        coordD = [dx, dy]
        coordM = [mx, my]

        a = coordO
        b = [coordD, coordM]

        dic1 = {}
        dic1["c"] = b

        #print(dic1)

        list1 = []
        list1.append(a)
        list1.append(dic1)

        #print(list1)

        list2 = []
        list2.append(list1)

        #print(list2)

        dic2 = {}
        dic2["wkid"] = refID

        #print(dic2)

        dic3 = {}

        dic3["curvePaths"] = list2
        dic3["spatialReference"] = dic2

        #print(dic3)

        json_str = json.dumps(dic3)

        #arcpy.AddMessage(json_str)

        polyline = arcpy.AsShape(json_str, True)

        featureList.append(polyline)
        pidList.append(uid)

arcpy.CopyFeatures_management(featureList, out_fc)

arcpy.management.AddField(out_fc, "pid", "LONG", None, None, None, '', "NULLABLE", "NON_REQUIRED", '')


fields = ["pid"]
i = 0

with arcpy.da.UpdateCursor(out_fc, fields) as cursor:
    
    for row in cursor:
        row[0] = int(pidList[i])
        i = i + 1
        cursor.updateRow(row)

