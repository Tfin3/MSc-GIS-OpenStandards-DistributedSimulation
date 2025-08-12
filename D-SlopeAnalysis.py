import geopandas as gpd
import os
import pandas as pd
import matplotlib
from scipy.stats import friedmanchisquare
from scipy import stats
matplotlib.use('TkAgg') #Needs to be before the matplotlib import.
import re
from typing import Tuple, List, Optional

import matplotlib.pyplot as plt
from rasterio.vrt import WarpedVRT
import numpy as np
from array import array

#Get set in the Main Dissertation folder, so any further references are relative from here
print(os.getcwd())
os.chdir('D:/Dissertation/AnalysisResults')
print(os.getcwd())
pd.set_option('display.max_columns', None)


GeoPkg_Results = r"D:/Dissertation/SamplePoints/DB_Samples.gpkg" #This GeoPkg has the layers in it for EGM values, and Sample values. It was prepared using QGIS..

ResultsFiles = ("Leek-Interpolation_results.geojson",
                "Sennybridge-Interpolation_results.geojson",
                "Control-Interpolation_results.geojson",
                "ControlAligned-Interpolation_results.geojson")

ResultFields = ("Leek",
                "Sennybridge",
                "Control",
                "Control-Aligned")

CubicResultsFiles = ("Cubic_Leek-Interpolation_results.geojson",
                "Cubic_Sennybridge-Interpolation_results.geojson",
                "Cubic_Control-Interpolation_results.geojson",
                "Cubic_ControlAligned-Interpolation_results.geojson",
                     "Cubic_L6_to_Others-Interpolation_results.geojson" )

CubicResultFields = ("Leek",
                "Sennybridge",
                "Control",
                "Control-Aligned",
                     "L6_toOthers")

NewControlResults = 'D:/Dissertation/Control-DEFRA1m/4326Control/Cubic-Interpolation_results.geojson'

NewControlResultsTwo = 'D:/Dissertation/Control-DEFRA1m/4326Control/Cubic-Interpolation_results-NoControlSamples.geojson'

LeekSlopeSrc = "D:\\Dissertation\\Control-DEFRA1m\\SlopeAnalysis\\SlopeAnalysis.geojson"

def GetRange(TheItems):
    range = TheItems.max(axis=1) - TheItems.min(axis=1)

    return range

def GetColumnList(file):
    toAnalyse = gpd.read_file(file)
    ColumnList = toAnalyse.columns.tolist()
    ColumnList.sort()
    return ColumnList

def DescribeMe(array, name):
    print(f"Describing {name}...")
    print(stats.describe(array))

print("Leek Slope list...")
for i in GetColumnList(LeekSlopeSrc):
    print(i)
print("Results - Case Study")
for i in GetColumnList(CubicResultsFiles[0]): #Leek analysis
    print(i)
print("Results - Control")
for i in GetColumnList(CubicResultsFiles[2]): #Leek Control analysis
    print(i)

caseAnalysis = gpd.read_file(CubicResultsFiles[0])
controlAnalysis = gpd.read_file(CubicResultsFiles[2])
SlopeResults = gpd.read_file(LeekSlopeSrc)

caseAnalysis['Range'] = GetRange(caseAnalysis[['GDAL_Cubic_LCT','GDAL_Cubic_UKCDB','GDAL_Cubic_VRTWSRC','GDAL_Cubic_VRTWTMS']])
controlAnalysis['Range'] = GetRange(controlAnalysis[['GDAL_Cubic_LCT','GDAL_Cubic_UKCDB','GDAL_Cubic_VRTW-Src','GDAL_Cubic_VRTW-TMS']])

print(caseAnalysis['Range'].head())
print(controlAnalysis['Range'].head())

plt.scatter(SlopeResults['GDAL_Cubic_Source'],caseAnalysis['Range'],  label="Range against slope - CaseStudy")
plt.scatter(SlopeResults['GDAL_Cubic_Source'],controlAnalysis['Range'],  label="Range against slope - Control")
plt.legend()
plt.xlabel("Slope (degrees) \nUsing GDAL Cubic interpolation")
plt.ylabel("Range value (m)")
plt.title("Plot showing slope vs. range for case study and control experiment")
#Got a diagram that shows something just need some labels now and to describe
plt.show()