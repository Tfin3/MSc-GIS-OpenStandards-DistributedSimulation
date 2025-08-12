import math
"""
#The lat long below is for Cadair Berwyn, Denbighsire - spot height 830m
reqLong = -3.38191
reqLat = 52.88011
"""

#The lat long below is for Cadair Berwyn, Denbighsire - spot height 830m
reqLong = -3.38191
reqLat = 52.88011

#OrderUnitsPerPixel = 0.17509727626459142824 #Order 2
OrderUnitsPerPixel = 0.00017099343385214007 #Order 12


OriginX = -180.0
OriginY = -90.0

tileWidth = 257
tileHeight = 257

def GetTileCoordinate(desLong,desLat):
    if desLong < 0.0:
        tileX = math.floor(((desLong - OriginX)/OrderUnitsPerPixel)/tileWidth)
    if desLong >= 0.0:
        tileX = math.floor(((desLong + (-OriginX)) / OrderUnitsPerPixel) / tileWidth)
    if desLat < 0.0:
        tileY = math.floor(((desLat - OriginY)/OrderUnitsPerPixel)/tileWidth)
    if desLat >= 0.0:
        tileY = math.floor(((desLat + (-OriginY)) / OrderUnitsPerPixel) / tileHeight)
    else:
        print('Not valid!')
    return (tileX,tileY)

def GetTileCorners(X,Y):
    XLong = -180.0 + (X * (tileWidth * OrderUnitsPerPixel))
    YLat = -90 + (Y * (tileHeight * OrderUnitsPerPixel))
    ULX = XLong
    ULY = YLat + (tileHeight * OrderUnitsPerPixel)
    LRX = XLong + (tileWidth * OrderUnitsPerPixel)
    LRY = YLat
    #print('UL is: ' + str(ULX) + '  ' + str(ULY))
    #print('LR is: ' + str(LRX) + '  ' + str(LRY))
    return (ULX, ULY, LRX, LRY)

def GetTileRange(ALong,ALat,BLong,BLat):
    #A being the UL, and B being the LR of the bounding box
    ATileCoordinates = GetTileCoordinate(ALong,ALat)
    BTileCoordinates = GetTileCoordinate(BLong,BLat)
    AX = ATileCoordinates[0]
    AY = ATileCoordinates[1]
    BX = BTileCoordinates[0]
    BY = BTileCoordinates[1]
    #These two lines print the tile coordinate for the UL and LR tiles respectively
    print('A (UL): ' + str(AX) + ' ' + str(AY))
    print('B (LR): ' + str(BX) + ' ' + str(BY))
    # This is good and prints the range of tiles needed...
    for x in range(AX, (BX + 1)):
        for y in range(BY, (AY + 1)):
            print(str(x) + ' is X, and Y is ' + str(y))

"""
#Creates an object with the Tile X and Y value for the requested Lat Long
Query = GetTileCoordinate(reqLong,reqLat)
#Prints the object, showing the X and Y Tile value
print(Query)

#Prints out the UL and LR lat longs for the tile requested above
print(GetTileCorners(Query[0],Query[1]))
"""

"""
#Notional area to test the GetTileRange function works
GetTileRange(-3.4, 52.9, -3.2, 52.6)
"""
"""
print('Sennybridge area')
GetTileRange(-3.75,52.125, -3.41, 51.99)

#Output of above
#Sennybridge area
#A (UL): 4010 3234
#B (LR): 4018 3231

print('Leek area')
GetTileRange(-2.01,53.188, -1.843, 53.108)

#Output of above
#Leek area
#A (UL): 4050 3258
#B (LR): 4054 3256
#4050 is X, and Y is 3256
#4050 is X, and Y is 3257
#4050 is X, and Y is 3258
#4051 is X, and Y is 3256
#4051 is X, and Y is 3257
#4051 is X, and Y is 3258
#4052 is X, and Y is 3256
#4052 is X, and Y is 3257
#4052 is X, and Y is 3258
#4053 is X, and Y is 3256
#4053 is X, and Y is 3257
#4053 is X, and Y is 3258
#4054 is X, and Y is 3256
#4054 is X, and Y is 3257
#4054 is X, and Y is 3258

Shown for development purposes, the idea being to populat these tile values to a list and then feed into the tile fetcher

"""
