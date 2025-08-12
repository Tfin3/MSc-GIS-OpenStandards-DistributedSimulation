from haversine import haversine, Unit

UK_Lats = [49.0,50.0,51.0,52.0,53.0,54.0,55.0,56.0,57.0,58.0,59.0,60.0,61.0]
UK_Longs = [-9.0,-8.0,-7.0,-6.0,-5.0,-4.0,-3.0,-2.0,-1.0,0.0,1.0,2.0]

TMS_Lods = [0.70038910505836571296, #0
            0.35019455252918285648, #1
            0.17509727626459142824, #2
            0.08754863813229571412, #3
            0.04377431906614785706, #4
            0.02188715953307392853, #5
            0.01094357976653696427, #6
            0.00547178988326848213, #7
            0.00273589494163424107, #8
            0.00136794747081712053, #9
            0.00068397373540856027, #10
            0.00034198686770428013, #11
            0.00017099343385214007, #12
            0.00008549671692607003, #13
            0.00004274835846303502, #14
            0.00002137417923151751, #15
            0.00001068708961575875, #16
            0.00000534354480787938, #17
            0.00000267177240393969, #18
            0.00000133588620196984] #19


print(haversine((UK_Lats[0],UK_Longs[0]),(UK_Lats[1],UK_Longs[0]), unit=Unit.METERS))
print(haversine((UK_Lats[0],UK_Longs[0]),(UK_Lats[1],UK_Longs[0]), unit=Unit.DEGREES))
""" #The below, prints things out and is an example of the code working to get a pixel value depending on changing lat / long
for lat in UK_Lats:
    print("This is the UK Lat table at: " + str(lat) + " degrees")
    
    for lod in TMS_Lods:
        print("\t" + str(round(haversine(
        (lat,UK_Longs[0]),
        (lat + lod,UK_Longs[0]),
        unit=Unit.METERS
    ), 6))
    )
    for long in UK_Longs:
        print("This is the UK Long table at: " + str(long) + " degrees")

        for lod in TMS_Lods:
            print(round(haversine(
            (UK_Lats[0],long),
            (UK_Lats[0],lod + long),
            unit=Unit.METERS
        ), 6))
"""
Table = ["LOD Order,"
         "Latitude,"
         "Pixel Height," +
         "-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2"]


#This appears not quite right, but when rounding changed to 12, you can see that after around 8dp things start to fluctuate... so minor changes at this long.
LOD_Counter = 0
for lod in TMS_Lods:
    for lat in UK_Lats:
        Row = str(LOD_Counter) + ','
        Row = Row + str(lat) + ','
        Row = Row + str((round(haversine((lat,UK_Longs[0]),(lat + lod, UK_Longs[0]), unit=Unit.METERS), 6))) + ','
        for long in UK_Longs:
            Row = Row + str(round(haversine((lat,long),(lat,long + lod), unit=Unit.METERS), 6)) + ','
        Table.append(Row)
    LOD_Counter += 1

with open('LODsizes.csv','w') as f:
    for row in Table:
        print(row)
        f.write(row + '\n')

