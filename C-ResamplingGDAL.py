from osgeo import gdal
import os
import subprocess

gdal.UseExceptions()

InputRaster_1mDefra = "D:\\Dissertation\\Control-DEFRA1m\\Leek-Defra_1m_Resolution.vrt"
ClipFile = "D:\\Dissertation\\ExtentPolygons\\Shapefile\\Leek.shp" # for into a shell prompt instead of Python Path
OutControlFile = "D:\\Dissertation\\Control-DEFRA1m\\4326Control\\4326-Control1m.tif"

LeekL6 = gdal.Open("D:/Dissertation/LCT-LeekTrgArea/N53W002_D001_S001_T001_L06_U7_R0.tif")
LeekL2 = gdal.Open("D:/Dissertation/UKCDB-LeekTrgArea/L2/N53W002_D001_S001_T001_L02_U0_R0.tif")
LeekVRTW = gdal.Open("D:/Dissertation/VRTheWorld-30mSection/LeekTrgArea-Clipped.tif")
LeekTMS12 = gdal.Open("D:/Dissertation/TMS-VRTheWorldExtract/LeekAreaTiles/Leek.vrt")
SampleList = (LeekL6, LeekL2, LeekVRTW, LeekTMS12)

SampleFileNames = ("LeekL6.tif",
               "LeekL2.tif",
               "LeekVRTW.tif",
               "LeekTMS12.tif")

SampleListTwo = (LeekL2, LeekVRTW, LeekTMS12)
SampleTwoFileNames = ("L6_to_LeekL2.tif",
                      "L6_to_LeekVRTW.tif",
                      "L6_to_LeekTMS12.tif")

toWarpArray = []


#gdal.WarpOptions(
#
#)

"""
https://gdal.org/en/stable/tutorials/geotransforms_tut.html
GT(0) x-coordinate of the upper-left corner of the upper-left pixel.
GT(1) w-e pixel resolution / pixel width.
GT(2) row rotation (typically zero).
GT(3) y-coordinate of the upper-left corner of the upper-left pixel.
GT(4) column rotation (typically zero).
GT(5) n-s pixel resolution / pixel height (negative value for a north-up image).
"""
#This gets the GeoTransform attributes
def LoadTransformAttributes(Samples, SampleNames): #Takes in a list of sample files, and associated sample names
    for raster, Name in zip(Samples, SampleNames):
        GeoTransData = raster.GetGeoTransform() #Create object to access GeoTransofrm attributes
        pixWidth = format(GeoTransData[1], '.32f') #Pixel widht as 32 float
        pixHeight = format(GeoTransData[5], '.32f') #Pixel height as 32 float
        print(GeoTransData)
        toWarpArray.append((Name, pixWidth, pixHeight)) #add to array for use in the Transform function

#https://gdal.org/en/stable/programs/gdalwarp.html
#GDALWarp section
def DoTheTransform(InputRaster):
    #Iterates through an global array with a name, pixel width and height
    for item in toWarpArray:
        OutPutPath = str("D:\\Dissertation\\Control-DEFRA1m\\4326Control\\" + item[0]) #remove 4326 control if doing the other bits
        x = item[1]
        y = item[2]
        #Below line calls the gdalwarp command with associated arguments and python variables for the changing items
        subprocess.call(
            f"gdalwarp -tr {x} {y} -t_srs EPSG:4326 -wm 50% -cutline {ClipFile} -crop_to_cutline -r near  {InputRaster} {OutPutPath}",
            shell=True)
        print(item[0] + "Complete")

def Create4326Control(inFile, outFile):
    subprocess.call(f"gdalwarp -t_srs EPSG:4326 -wm 50% -cutline {ClipFile} -crop_to_cutline -r near {inFile} {outFile}", shell=True)
    print(f"Completed making the 4326 conversion - saved at \n\t{outFile}")

#The below creates the reprojected DEFRA 1m for use in further analysis
#Create4326Control(InputRaster_1mDefra, OutControlFile)

#The below takes loads the rasters to be used as the sample basis, and the names to save as in an array, and the next function iterates through conducting the transform - creating the controlled datasets
LoadTransformAttributes(SampleList, SampleFileNames)
DoTheTransform(OutControlFile)

#LoadTransformAttributes(SampleListTwo, SampleTwoFileNames) # The files and names for the resampling of Leek L6 to the other pixel resolutions to see if that has any better statistical similarity.
#DoTheTransform("D:\\Dissertation\\LCT-L6-Leek-VrtRaster.vrt") # Executes the transform based on the properties loaded in the to Warp array