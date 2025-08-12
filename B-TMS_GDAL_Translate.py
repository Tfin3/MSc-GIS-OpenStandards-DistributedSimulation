import os
import B_TMS_TileCalculator
from B_TMS_TileCalculator import GetTileCorners

#This needs to be run from OSGeo4W Shell in my environment, so the GDAL binaries are accessible
#This should not be hardcoded... It should be loaded from a module that imports the data from the TMS GEtCapabilities XML file, then for use across the application

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



def PrepareListTiles(ListFiles):
    tileListXYZ = []
    for tile in ListFiles:
        if ".tif" not in tile:
            continue
        z = tile.split('_')[0][1:]
        x = tile.split('_')[1][1:]
        y = tile.split('_')[2].split('.tif')[0][1:]
        ULLR = GetTileCorners(int(x),int(y))
        ULX = ULLR[0]
        ULY = ULLR[1]
        LRX = ULLR[2]
        LRY = ULLR[3]
        #print(str(z) + ',' + str(X) + ',' + str(y))
        tileListXYZ.append((tile, z, int(x), int(y), ULX, ULY, LRX, LRY))
    return tileListXYZ

print(os.getcwd())
#Change directory to Sennybridge area tiles folder
os.chdir('D:/Dissertation/TMS-VRTheWorldExtract/SennybridgeAreaTiles') #TODO not use hardcoded folders
print(os.getcwd())
ListFiles = os.listdir() # Create a list of all files, should be the downloaded tiles from TMS server
if not os.path.exists('Translated'): #If this hasn't been run before, then there will be no Translated folder
    MyTileList = PrepareListTiles(ListFiles) #Pass the list of files, for create a list of filenames and geotransform data
    os.makedirs('Translated') #Make a Translated (output) folder
    for i in MyTileList: #Iterate through the Tilelist
        #Below is the Shell command for the GDAL_translate call
        os.system("gdal_translate -ot float32 -a_srs EPSG:4326 -a_ullr " #TODO Data type and EPSG should come from XML of the TMS service
                  + str(i[4]) + " " #ULX
                  + str(i[5]) + " " #ULY
                  + str(i[6]) + " " #LRX
                  + str(i[7]) + " " #LRY
                  + str(os.getcwd() + str("\\") + i[0] + " ") #Tile source
                  + str(os.getcwd() + str("\\") +"Translated\\" + i[0])) #Tile destination in Translated

#Build Virtual Raster of all tiles in translated
os.system("gdalbuildvrt SENNYBRIDGE.vrt Translated/*.tif") # this is hardcoded, just to get it to work... and it did.