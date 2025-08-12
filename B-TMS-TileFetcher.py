import xml.etree.ElementTree as ET
from urllib.request import urlretrieve
import time
import math

#Loads the locally saved TMS response data - this would otherwise by the XML response from the 'TileMapResource' response
tree = ET.parse('TMS_Response_data.xml')
root = tree.getroot()
Tilesets = root.iter('TileSet')
Origin = root.find('Origin')
TileFormat = root.find('TileFormat')

#iterates through printing out the objects, for development visibility
#for child in root:
#    print(child.tag, child.attrib, child.text)

#Prints out each of the tilesets href, order and pixel size
#for i in Tilesets:
#    print(i.attrib['href'], str(f"\tOrder:{i.attrib['order']} \tUnits per pixel:\t{i.attrib['units-per-pixel']}"))

#Print the origina x and y, as well as tile width and height for this TileMapResource
#print(Origin.attrib['x'] + '\t' +  Origin.attrib['y'])
#print(TileFormat.attrib['width'] + '\t' + TileFormat.attrib['height'])

#The below works to download TIFs
#TODO - turn into a function with inputs for further reuse
urlBaseString = 'http://172.24.62.28/vr-theworld/tiles/1.0.0/149/'
for z in range(12,13): #hard coded LOD range in
    for x in range(4050,4055): #Hard coded the X range in for the moment
        for y in range(3256,3259): #Hard coded the Y range in for the moment
            tileRequestString = str(z) + '/' + str(x) + '/' + str(y) + '.tif' #builds the request string
            tileSaveName = 'Z' + str(z) + '_X' + str(x) + '_Y' + str(y) + '.tif' #builds the save file name
            #time.sleep(2) #added a sleep to slow down the requests
            try:
                #actual http request, and saves file as the tile name generated
                urlretrieve(str(urlBaseString + tileRequestString), tileSaveName)
                #Print which file has just been downloaded
                print(tileSaveName)
            except:
                next