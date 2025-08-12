import geopandas as gpd
import rasterio
from rasterio.vrt import WarpedVRT
from rasterio.enums import Resampling
import os



#Get set in the Main Dissertation folder, so any further references are relative from here
print(os.getcwd())
os.chdir('D:/Dissertation')
print(os.getcwd())

#The below are all the main inputs for interpolation sampling to be done
Leek_rasters = ("VRTheWorld-30mSection/LeekTrgArea-Clipped.tif",
                "TMS-VRTheWorldExtract/LeekAreaTiles/LEEK.vrt",
                "UKCDB-LeekTrgArea/L2/N53W002_D001_S001_T001_L02_U0_R0.tif",
                "LCT-L6-Leek-VrtRaster.vrt")
Leek_Field_Names = ("VRTWSRC",
                    "VRTWTMS",
                    "UKCDB",
                    "LCT")

Leek_points = "SamplePoints/Leek_SamplePoints - Copy.geojson"
Sennybridge_points = "SamplePoints/Sennybridge_SamplePoints - Copy.geojson"

Sennybridge_rasters = ("VRTheWorld-30mSection/SennyBridgeTrgArea-Clipped.tif",
                "TMS-VRTheWorldExtract/SennybridgeAreaTiles/SENNYBRIDGE.vrt",
                "UKCDB-Sennybridge/UKCDB-Sennybridge-L2.vrt", #Need to find this virtual raster... think it is in the QGIS project.
                "LCT-L6-VrtRasterSennyBridge.vrt")
Sennybridge_Field_Names = ("VRTWSRC",
                    "VRTWTMS",
                    "UKCDB",
                    "LCT")

ControlSampleRasters =("Control-DEFRA1m/Leek-4326-Control1m.vrt",
                       "Control-DEFRA1m/Leek-Defra_1m_Resolution.vrt",#Leek Control sample
                       "Control-DEFRA1m/LeekVRTW.tif",
                       "Control-DEFRA1m/LeekTMS12.tif",
                       "Control-DEFRA1m/LeekL2.tif",
                       "Control-DEFRA1m/LeekL6.tif")
ControlSampleFieldNames = ("DEFRA-1m-4326",
                           "DEFRA-1m",
                           "VRTW-Src",
                           "VRTW-TMS",
                           "UKCDB",
                           "LCT")

NewControlSampleRasters =("Control-DEFRA1m/4326Control/4326-Control1m.tif", #Control Defra reprojected to 4326
                       "Control-DEFRA1m/4326Control/LeekVRTW.tif",
                       "Control-DEFRA1m/4326Control/LeekTMS12.tif",
                       "Control-DEFRA1m/4326Control/LeekL2.tif",
                       "Control-DEFRA1m/4326Control/LeekL6.tif")

NewControlSampleFieldNames = ("Control1m",
                           "VRTW-Src",
                           "VRTW-TMS",
                           "UKCDB",
                           "LCT")


ControlSampleAlignedRasters =("Control-DEFRA1m/Leek-4326-Control1m.vrt",
                       "Control-DEFRA1m/Leek-Defra_1m_Resolution.vrt",#Leek Control sample
                       "Control-DEFRA1m/LeekVRTW-AlignedToCtrl.tif",
                       "Control-DEFRA1m/LeekTMS12-AlignedToCtrl.tif",
                       "Control-DEFRA1m/LeekL2-AlignedToCtrl.tif",
                       "Control-DEFRA1m/LeekL6-AlignedToCtrl.tif")
ControlSampleAlignedFieldNames = ("DEFRA-1m--4326",
                                  "DEFRA-1m",
                                  "Ali_VRTW-Src",
                                  "Ali_VRTW-TMS",
                                  "Ali_UKCDB",
                                  "Ali_LCT")

L6_to_OtherRasters= ("LCT-L6-Leek-VrtRaster.vrt",
                     "Control-DEFRA1m/L6_to_LeekL2.tif",
                      "Control-DEFRA1m/L6_to_LeekVRTW.tif",
                      "Control-DEFRA1m/L6_to_LeekTMS12.tif")
L6_to_Other_FieldNames = ("LeekL6_Orig",
                          "LeekL2_Resample",
                          "LeekVRTW_Resample",
                          "LeekTMS_Resample")

LeekSlope = ("Control-DEFRA1m/Leek-1m-Slope.tif",
             "Control-DEFRA1m/Leek-4326-Slope.tif")
SlopeLabels = ("Source", "4326ReProj")

#Below, are the test inputs, before making a function that can take in a list.
#input_raster = "D:/Dissertation/VRTheWorld-30mSection/LeekTrgArea-Clipped.tif"
#input_points = "SamplePoints/Leek_SamplePoints - Copy.geojson"

def Interpolate(samplePoints, rasterList, rasterFieldNames, saveFileName):
    #Load the feature layer samplepoints
    print("About to read the file... " + str(samplePoints))
    points = gpd.read_file(samplePoints)
    print("\nWorking through the following:") #Identify the raster and field being worked on
    for name in rasterFieldNames:
        print(str("\t" + name))

    for raster, fieldName in zip(rasterList, rasterFieldNames):
        print("\n" + fieldName)
        print("\t1\tGDAL Nearest...")
        GdalNearestValues = [] #Array for the sampled values to go in
        # https://gdal.org/en/stable/programs/gdallocationinfo.html
        for x,y in zip(points.geometry.x, points.geometry.y): #iterate through eachx and y point
            #print(x,y)
            valueA = os.popen(
                f"gdallocationinfo -wgs84 -valonly -r nearest {raster} {x} {y}"
            ).read() #Shell command that uses GDAL Location info and the associated arguments
            GdalNearestValues.append(float(valueA.rstrip())) #Append to array
        points['GDAL_Nearest_' + fieldName] = GdalNearestValues #Add array to the GeoPandas dataframe

        print("\t2\tGDAL Bilinear...")
        GdalInterpolatedValues = []
        # https://gdal.org/en/stable/programs/gdallocationinfo.html
        for x,y in zip(points.geometry.x, points.geometry.y):
            #print(x,y)
            valueB = os.popen(
                f"gdallocationinfo -wgs84 -valonly -r bilinear {raster} {x} {y}"
            ).read()
            GdalInterpolatedValues.append(float(valueB.rstrip()))
        points['GDAL_Bilinear_' + fieldName] = GdalInterpolatedValues

        print("\t2\tGDAL Cubic...")
        GdalCubicValues = []
        # https://gdal.org/en/stable/programs/gdallocationinfo.html
        for x,y in zip(points.geometry.x, points.geometry.y):
            #print(x,y)
            valueC = os.popen(
                f"gdallocationinfo -wgs84 -valonly -r cubic {raster} {x} {y}"
            ).read()
            GdalCubicValues.append(float(valueC.rstrip()))
        points['GDAL_Cubic_' + fieldName] = GdalCubicValues

        print("\t3\tWarpedNearest...")
        with rasterio.open(raster) as src:
            if "EPSG:4326" in str(src.crs):
                print("\t\t\tWarped NOT doing the 4326 reprojection...")
                with WarpedVRT(src, resampling=Resampling.nearest) as dish:
                    WarpedNearest_interpolated_values = [val[0] for val in dish.sample([(x, y) for x, y in zip(points.geometry.x, points.geometry.y)])]
            else:
                print("\t\t\tWarped doing the 4326 reprojection...")
                with WarpedVRT(src, crs='EPSG:4326', resampling=Resampling.nearest) as dish:
                    WarpedNearest_interpolated_values = [val[0] for val in dish.sample([(x, y) for x, y in zip(points.geometry.x, points.geometry.y)])]

            # Take the interpolated values variable from above, and add as a field on the file opened
        # Take the interpolated values variable from above, and add as a field on the file opened
        points['WarpedVRT_Nearest_' + fieldName] = WarpedNearest_interpolated_values
        #Had to modify the WarpedVRT to load the crs of EPSG 4326 - as the sample points were in WGS 84, and the raster were in OSBNG

        print("\t4\tWarpedBilinear...")
        with rasterio.open(raster) as src:
            if "EPSG:4326" in str(src.crs):
                print("\t\t\tWarped NOT doing the 4326 reprojection...")
                with WarpedVRT(src, resampling=Resampling.bilinear) as dish:
                    interpolated_values = [val[0] for val in dish.sample([(x,y) for x, y in zip(points.geometry.x, points.geometry.y) ])]
            else:
                print("\t\t\tWarped doing the 4326 reprojection...")
                with WarpedVRT(src, crs='EPSG:4326', resampling=Resampling.bilinear) as dish:
                    interpolated_values = [val[0] for val in dish.sample([(x,y) for x, y in zip(points.geometry.x, points.geometry.y) ])]
        #Take the interpolated values variable from above, and add as a field on the file opened
        points['WarpedVRT_Bilinear_' + fieldName] = interpolated_values



        #Save the output
        points.to_file(saveFileName)


"""
#The below functions have all been used and succesful, just readjusting my control experiment...
Interpolate(Leek_points, Leek_rasters, Leek_Field_Names, "AnalysisResults/Cubic_Leek-Interpolation_results.geojson")
Interpolate(Sennybridge_points, Sennybridge_rasters, Sennybridge_Field_Names, "AnalysisResults/Cubic_Sennybridge-Interpolation_results.geojson")
Interpolate(Leek_points, ControlSampleRasters, ControlSampleFieldNames, "AnalysisResults/Cubic_Control-Interpolation_results.geojson")
Interpolate(Leek_points, ControlSampleAlignedRasters, ControlSampleAlignedFieldNames, "AnalysisResults/Cubic_ControlAligned-Interpolation_results.geojson")
Interpolate(Leek_points, L6_to_OtherRasters, L6_to_Other_FieldNames , "AnalysisResults/Cubic_L6_to_Others-Interpolation_results.geojson")
"""

#This is the function to interpolate / sample the 4326 control raster, and the associated datasets created from it
#Interpolate(Leek_points, Leek_rasters, Leek_Field_Names, "Control-DEFRA1m/4326Control/Cubic_Leek-Interpolation_results.geojson")
#Interpolate(Sennybridge_points, Sennybridge_rasters, Sennybridge_Field_Names, "Control-DEFRA1m/4326Control/Cubic_Sennybridge-Interpolation_results.geojson")


#Interpolate(Leek_points, NewControlSampleRasters, NewControlSampleFieldNames, "Control-DEFRA1m/4326Control/Cubic-Interpolation_results.geojson")

#This is the Slope Rasters getting sampled for a final bit of analysis
Interpolate(Leek_points, LeekSlope, SlopeLabels, "Control-DEFRA1m/SlopeAnalysis/SlopeAnalysis.geojson")