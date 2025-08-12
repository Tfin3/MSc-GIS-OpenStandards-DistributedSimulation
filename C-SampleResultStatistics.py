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
pd.set_option('display.max_columns', None) #Helps with reading columns using df.head()


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

NewControlResultsThree = ('D:/Dissertation/Control-DEFRA1m/4326Control/Cubic-Interpolation_results-CDBAndTMS.geojson')

Pair_TMSCDB2 = ('D:/Dissertation/Control-DEFRA1m/4326Control/Cubic_TMSandCDB2.geojson')
Pair_TMSCDB6 = ('D:/Dissertation/Control-DEFRA1m/4326Control/Cubic_TMSandCDB6.geojson')
Pair_CDB6CDB2 = ('D:/Dissertation/Control-DEFRA1m/4326Control/Cubic_CDB6andCDB2.geojson')

blind_G_nearest = ["GDAL_Nearest_VRTWSRC","GDAL_Nearest_VRTWTMS","GDAL_Nearest_UKCDB","GDAL_Nearest_LCT"]
blind_G_bilinear = ["GDAL_Bilinear_VRTWSRC","GDAL_Bilinear_VRTWTMS","GDAL_Bilinear_UKCDB","GDAL_Bilinear_LCT"]
warp_nearest = ["WarpedVRT_Nearest_VRTWSRC","WarpedVRT_Nearest_VRTWTMS","WarpedVRT_Nearest_UKCDB","WarpedVRT_Nearest_LCT"]
warp_bilinear = ["WarpedVRT_Bilinear_VRTWSRC","WarpedVRT_Bilinear_VRTWTMS","WarpedVRT_Bilinear_UKCDB","WarpedVRT_Bilinear_LCT"]

blindColumns = (blind_G_nearest, blind_G_bilinear, warp_nearest, warp_bilinear)

blindCA_G_nearest = ["GDAL_Nearest_VRTW-Src","GDAL_Nearest_VRTW-TMS","GDAL_Nearest_UKCDB","GDAL_Nearest_LCT"]
blindCA_G_bilinear = ["GDAL_Bilinear_VRTW-Src","GDAL_Bilinear_VRTW-TMS","GDAL_Bilinear_UKCDB","GDAL_Bilinear_LCT"]
warpCA_nearest = ["WarpedVRT_Nearest_VRTW-Src","WarpedVRT_Nearest_VRTW-TMS","WarpedVRT_Nearest_UKCDB","WarpedVRT_Nearest_LCT"]
warpCA_bilinear = ["WarpedVRT_Bilinear_VRTW-Src","WarpedVRT_Bilinear_VRTW-TMS","WarpedVRT_Bilinear_UKCDB","WarpedVRT_Bilinear_LCT"]

blindControlAColumns = (blindCA_G_nearest, blindCA_G_bilinear, warpCA_nearest, warpCA_bilinear)

blindCB_G_nearest = ["GDAL_Nearest_Ali_VRTW-Src","GDAL_Nearest_Ali_VRTW-TMS","GDAL_Nearest_Ali_UKCDB","GDAL_Nearest_Ali_LCT"]
blindCB_G_bilinear = ["GDAL_Bilinear_Ali_VRTW-Src","GDAL_Bilinear_Ali_VRTW-TMS","GDAL_Bilinear_Ali_UKCDB","GDAL_Bilinear_Ali_LCT"]
warpCB_nearest = ["WarpedVRT_Nearest_Ali_VRTW-Src","WarpedVRT_Nearest_Ali_VRTW-TMS","WarpedVRT_Nearest_Ali_UKCDB","WarpedVRT_Nearest_Ali_LCT"]
warpCB_bilinear = ["WarpedVRT_Bilinear_Ali_VRTW-Src","WarpedVRT_Bilinear_Ali_VRTW-TMS","WarpedVRT_Bilinear_Ali_UKCDB","WarpedVRT_Bilinear_Ali_LCT"]

blindControlBColumns = (blindCB_G_nearest, blindCB_G_bilinear, warpCB_nearest, warpCB_bilinear)


#Control dataset - without 4326 reprojection - The original source data is EPSG:27700
controlA_G_nearest = ["GDAL_Nearest_DEFRA-1m", "GDAL_Nearest_DEFRA-1m-4326","GDAL_Nearest_VRTW-Src","GDAL_Nearest_VRTW-TMS","GDAL_Nearest_UKCDB","GDAL_Nearest_LCT"]
controlA_G_bilinear = ["GDAL_Bilinear_DEFRA-1m", "GDAL_Bilinear_DEFRA-1m-4326","GDAL_Bilinear_VRTW-Src","GDAL_Bilinear_VRTW-TMS","GDAL_Bilinear_UKCDB","GDAL_Bilinear_LCT"]
controlA_warp_nearest = ["WarpedVRT_Nearest_DEFRA-1m", "WarpedVRT_Nearest_DEFRA-1m-4326","WarpedVRT_Nearest_VRTW-Src","WarpedVRT_Nearest_VRTW-TMS","WarpedVRT_Nearest_UKCDB","WarpedVRT_Nearest_LCT"]
controlA_warp_bilinear = ["WarpedVRT_Bilinear_DEFRA-1m", "WarpedVRT_Bilinear_DEFRA-1m-4326","WarpedVRT_Bilinear_VRTW-Src","WarpedVRT_Bilinear_VRTW-TMS","WarpedVRT_Bilinear_UKCDB","WarpedVRT_Bilinear_LCT"]

#Control dataset - with 4326 reprojection - Src was OSBG EPSG:27700
controlB_G_nearest = ["GDAL_Nearest_DEFRA-1m", "GDAL_Nearest_DEFRA-1m--4326","GDAL_Nearest_Ali_VRTW-Src","GDAL_Nearest_Ali_VRTW-TMS","GDAL_Nearest_Ali_UKCDB","GDAL_Nearest_Ali_LCT"]
controlB_G_bilinear = ["GDAL_Bilinear_DEFRA-1m", "GDAL_Bilinear_DEFRA-1m--4326","GDAL_Bilinear_Ali_VRTW-Src","GDAL_Bilinear_Ali_VRTW-TMS","GDAL_Bilinear_Ali_UKCDB","GDAL_Bilinear_Ali_LCT"]
controlB_warp_nearest = ["WarpedVRT_Nearest_DEFRA-1m", "WarpedVRT_Nearest_DEFRA-1m--4326","WarpedVRT_Nearest_Ali_VRTW-Src","WarpedVRT_Nearest_Ali_VRTW-TMS","WarpedVRT_Nearest_Ali_UKCDB","WarpedVRT_Nearest_Ali_LCT"]
controlB_warp_bilinear = ["WarpedVRT_Bilinear_DEFRA-1m", "WarpedVRT_Bilinear_DEFRA-1m--4326","WarpedVRT_Bilinear_Ali_VRTW-Src","WarpedVRT_Bilinear_Ali_VRTW-TMS","WarpedVRT_Bilinear_Ali_UKCDB","WarpedVRT_Bilinear_Ali_LCT"]

ControlAColumns = (controlA_G_nearest, controlA_G_bilinear, controlA_warp_nearest, controlA_warp_bilinear)
ControlBColumns = (controlB_G_nearest, controlB_G_bilinear, controlB_warp_nearest, controlB_warp_bilinear)

InterpolationLabels = ("GDAL_Nearest", "GDAL_Bilinear", "Warped_Nearest", "Warped_Bilinear")

DatasetLabels = ("DEFRA-1m_Reproj","VRTW-SRC", "VRTW-TMS", "UKCDB", "LCT")
RangeDatasetLabels = ("VRTW-SRC", "VRTW-TMS", "UKCDB", "LCT")

regExFields = (r'^GDAL_Nearest', r'^GDAL_Bilinear', r'^GDAL_Cubic', r'^WarpedVRT_Nearest', r'^WarpedVRT_Bilinear')

#This is used for all the RMSE means to be added to in a dictionary, the value added is the RMSE Mean for that field in the results.
RMSEMeans = {}

figs = []

def GetRange(TheItems):
    range = TheItems.max(axis=1) - TheItems.min(axis=1)

    return range


def GetColumnList(file):
    toAnalyse = gpd.read_file(file)
    ColumnList = toAnalyse.columns.tolist()
    ColumnList.sort()
    return ColumnList

def AnalyseBlindData(file, field, theColumns):
    toAnalyse = gpd.read_file(file)
    print(f"Reading {file} now...")
    for columns in theColumns:
        fig, ax = plt.subplots()
        toAnalyse[str(columns)] = GetRange(toAnalyse[columns])
        print(toAnalyse[str(columns)].mean())
        print(toAnalyse[str(columns)].head())
        for i in columns:
            DescribeMe(toAnalyse[str(i)], str(i))
        toAnalyse[str(columns)].hist(bins=30, edgecolor='black', ax=ax)
        ax.set_title(f'{file.split('-')[0]} - Range of ' + str(columns[0].split('_')[0:2]))
        ax.set_xlabel('Range Value')
        ax.set_ylabel('Count')
        ax.text(0.95, 0.95, f'Mean: {toAnalyse[str(columns)].mean():.4f}',
                transform=ax.transAxes,  # Use Axes coordinates (0 to 1)
                fontsize=12, color='darkred',
                ha='right', va='top')
        fig.savefig(f'Hist_{file.split('-')[0]}_{str(columns[0].split('_')[0:2])}.png')
        plt.show()


#This function takes in an actual dataframe column, and a predicted dataframe column -
# in the case of my research, this is the control value (actual) and the dataset sample (predicted)
def GetRMSE(actual, predicted):
    sampleSize = actual.shape[0] # gets the value for the number of rows in a column.
    difference = actual - predicted
    squared_difference = difference ** 2
    divide_sample_difference = squared_difference / (sampleSize - 1)
    RMSE = np.sqrt(divide_sample_difference)
    return RMSE

def MakeADiagram(dataframeColumn, label ):
    fig, ax = plt.subplots()
    dataframeColumn.hist(bins=30, edgecolor='black', ax=ax)
    ax.set_title(f'Histogram of {label}')
    ax.set_xlabel('RMSE')
    ax.set_ylabel('Count')
    ax.text(0.95, 0.95, f'Mean: {dataframeColumn.mean():.4f}',
            transform=ax.transAxes,  # Use Axes coordinates (0 to 1)
            fontsize=12, color='darkred',
            ha='right', va='top')
    fig.savefig(f'Histogram_{label}.png')  # Save the figure
    figs.append(fig)


def AnalyseControlData(file, field):
    toAnalyse = gpd.read_file(file)
    sampleSize = toAnalyse.shape[0]

    #Control A Loop
    if file == ResultsFiles[2]:
        for index, label in enumerate(DatasetLabels):
            field = str(label) + '-RMSE-GN'
            toAnalyse[field] = GetRMSE(toAnalyse[controlA_G_nearest[0]], toAnalyse[controlA_G_nearest[(index+1)]])
            RMSEMeans[field] = toAnalyse[field].mean()
            MakeADiagram(toAnalyse[field], field)
            print(f"{field}: \t\t{toAnalyse[field].mean()}")
        for index, label in enumerate(DatasetLabels):
            field = str(label) + '-RMSE-GB'
            toAnalyse[field] = GetRMSE(toAnalyse[controlA_G_bilinear[0]], toAnalyse[controlA_G_bilinear[(index+1)]])
            RMSEMeans[field] = toAnalyse[field].mean()
            MakeADiagram(toAnalyse[field], field)
            print(f"{field}: \t\t{toAnalyse[field].mean()}")
        for index, label in enumerate(DatasetLabels):
            field = str(label) + '-RMSE-WN'
            toAnalyse[field] = GetRMSE(toAnalyse[controlA_warp_nearest[0]], toAnalyse[controlA_warp_nearest[(index+1)]])
            RMSEMeans[field] = toAnalyse[field].mean()
            MakeADiagram(toAnalyse[field], field)
            print(f"{field}: \t\t{toAnalyse[field].mean()}")
        for index, label in enumerate(DatasetLabels):
            field = str(label) + '-RMSE-WB'
            toAnalyse[field] = GetRMSE(toAnalyse[controlA_warp_bilinear[0]], toAnalyse[controlA_warp_bilinear[(index+1)]])
            RMSEMeans[field] = toAnalyse[field].mean()
            MakeADiagram(toAnalyse[field], field)
            print(f"{field}: \t\t{toAnalyse[field].mean()}")
        print("\n\nHere is the Range for the 4 dataset sample columns selected...")
        for index, item in enumerate(ControlAColumns):
            field = 'A_' + str(InterpolationLabels[index]) + '_Range'
            toAnalyse[field] = GetRange(toAnalyse[item[2:]])
            print(InterpolationLabels[index] + ":\t " + str(toAnalyse[field].mean()))


    #Control B Loop
    elif file == ResultsFiles[3]:
        for index, label in enumerate(DatasetLabels):
            field = 'Ali_' + str(label) + '-RMSE-GN'
            toAnalyse[field] = GetRMSE(toAnalyse[controlB_G_nearest[0]], toAnalyse[controlB_G_nearest[(index+1)]])
            RMSEMeans[field] = toAnalyse[field].mean()
            MakeADiagram(toAnalyse[field], field)
            print(f"{field}: \t\t{toAnalyse[field].mean()}")
        for index, label in enumerate(DatasetLabels):
            field = 'Ali_' + str(label) + '-RMSE-GB'
            toAnalyse[field] = GetRMSE(toAnalyse[controlB_G_bilinear[0]], toAnalyse[controlB_G_bilinear[(index+1)]])
            RMSEMeans[field] = toAnalyse[field].mean()
            MakeADiagram(toAnalyse[field], field)
            print(f"{field}: \t\t{toAnalyse[field].mean()}")
        for index, label in enumerate(DatasetLabels):
            field = 'Ali_' + str(label) + '-RMSE-WN'
            toAnalyse[field] = GetRMSE(toAnalyse[controlB_warp_nearest[0]], toAnalyse[controlB_warp_nearest[(index+1)]])
            RMSEMeans[field] = toAnalyse[field].mean()
            MakeADiagram(toAnalyse[field], field)
            print(f"{field}: \t\t{toAnalyse[field].mean()}")
        for index, label in enumerate(DatasetLabels):
            field = 'Ali_' + str(label) + '-RMSE-WB'
            toAnalyse[field] = GetRMSE(toAnalyse[controlB_warp_bilinear[0]], toAnalyse[controlB_warp_bilinear[(index+1)]])
            RMSEMeans[field] = toAnalyse[field].mean()
            MakeADiagram(toAnalyse[field], field)
            print(f"{field}: \t\t{toAnalyse[field].mean()}")
        print("\n\nHere is the Range for the 4 dataset sample columns selected...")
        for index, item in enumerate(ControlBColumns):
            field = 'A_' + str(InterpolationLabels[index]) + '_Range'
            toAnalyse[field] = GetRange(toAnalyse[item[2:]])
            print(InterpolationLabels[index] + ":\t " + str(toAnalyse[field].mean()))

    for i in toAnalyse.columns.tolist():
        print(i)

    return


def GetRangesandPlot(file):
    ControlInterpolations = gpd.read_file(file)
    ColumnList = ControlInterpolations.columns.tolist()
    ColumnList.sort()
    for i in ColumnList:
        print(i)
    """
    #Hardcoded way of finding the columns, not the best
    GDALBilinear = ColumnList[0:6]
    GDALNearest = ColumnList[6:12]
    WarpedVRT = ['WarpedVRT_Bilinear_DEFRA-1m','WarpedVRT_Bilinear_DEFRA-1m-4326',  'WarpedVRT_Bilinear_LCT', 'WarpedVRT_Bilinear_UKCDB', 'WarpedVRT_Bilinear_VRTW-Src', 'WarpedVRT_Bilinear_VRTW-TMS']
    Segments = (GDALBilinear, GDALNearest, WarpedVRT)


    for item in Segments:
        Range = GetRange(ControlInterpolations[item].round(1))
        print(item)

        ColumnName = str(str(item) + 'Range')

        ControlInterpolations[ColumnName] = Range
        ControlInterpolations.hist(column=ColumnName, bins=10, label=str(item))
    """
def DescribeMe(array, name):
    print(f"Describing {name}...")
    print(stats.describe(array))


def PrepareFriedmanArgs(
    gdf: str,
    pattern: str,
    rounding: int,
    exclude: List[str] = ["geometry", "id"]) -> Tuple:
    """
    #Use a REGEX pattern to identify columns, and make them usable for analysis
    Makes a list of columns that match a regex pattern ready for use in FriedmanResults.

    Inputs
        gdf GeoPandas dataframe for columns to be regex matched
        pattern The 'regex' pattern - using to filter by interpolation method basically
        rounding how many decimal places to round to when it is returned
        exclude Columns to exclude from filtering, and not return

    Returns
        A tuple of column arrays that can be used in SciPy - they are then unpacked with the * operator.
    """

    gdf = gpd.read_file(gdf)

    matching_fields = [
        col for col in gdf.columns
        if re.match(pattern, col)
        and col not in exclude
        and gdf[col].dtype.kind in 'iufc'  # numeric datatypes only
    ]
    print("\t" + str(matching_fields))
#    if len(matching_fields) < 2:
#        raise ValueError(f"Need at least two matching fields for Friedman test, found: {matching_fields}")

    return tuple(gdf[col].round(rounding).values for col in matching_fields) #Returns a tuple with an array based on the values in each dataframe column that was matched by the regex pattern

"""
https://search.r-project.org/CRAN/refmans/rstatix/html/friedman_effsize.html
Description
Compute the effect size estimate (referred to as w) for Friedman test: W = X2/N(K-1); where W is the Kendall's W value; X2 is the Friedman test statistic value; N is the sample size. k is the number of measurements per subject.

The Kendall’s W coefficient assumes the value from 0 (indicating no relationship) to 1 (indicating a perfect relationship).

Kendall's uses the Cohen’s interpretation guidelines of 0.1 - < 0.3 (small effect), 0.3 - < 0.5 (moderate effect) and >= 0.5 (large effect)
"""

def FriedmanResults(ListofFiles, rounding):
    for i in ListofFiles:
        print(str(i))
        # for count, j in enumerate(GetColumnList(i)):
        #    print(f"\t{count}\t{j}")
        # Example: Friedman test for Bilinear interpolation method
        for j in regExFields:
            args = PrepareFriedmanArgs(i, j, rounding)
            if len(args) >= 3:
                # Run the test
                stat, p = friedmanchisquare(*args) #Need to use the star operator to unpack the arguments from the Tuple - https://stackoverflow.com/questions/31195941/what-is-the-correct-way-of-passing-parameters-to-stats-friedmanchisquare-based-o
                n = len(args[0])
                k = len(args)
                WValue = stat/(n*(k-1))
                print(f"\t{j[1:]} - Friedman test: stat={stat:.4f}, p={p}, W Value:{WValue:.4f}")
            elif len(args) <= 2:
                # print(f"\t{j} - Not enough for the Friedman test!")
                continue

def FriedmanNoListResults(FileForAnalysis, rounding):
    print(f"{FileForAnalysis} is being analysed...")
    for j in regExFields: #iterates through the list of different interpolation labels (regExFields)
        args = PrepareFriedmanArgs(FileForAnalysis, j, rounding)
        if len(args) >= 3:
            # Run the test
            stat, p = friedmanchisquare(*args) #Need to use the star operator to unpack the arguments from the Tuple
            #https://stackoverflow.com/questions/31195941/what-is-the-correct-way-of-passing-parameters-to-stats-friedmanchisquare-based-o
            n = len(args[0]) #numer of rows in the column / array, so sample locations
            k = len(args) #number of columns / arrays
            WValue = stat/(n*(k-1)) #Calculate Kendall's W Value
            print(f"\t\t{j[1:]} - Friedman test: stat={stat:.4f}, p={p}, W Value:{WValue:.4f}")
        elif len(args) <= 2:
            # print(f"\t{j} - Not enough for the Friedman test!")
            continue

""" Leek Layer index
0 EGM96Value
1 LCT-L6
2 SrcVRTW-LCT
3 SrcVRTW-UKCDB
4 SrcVRTW-VRTW
5 UKCDB-L2
6 VRTW-LeekO12
7 VRTW-SRCData
8 geometry
9 id"""

def AbsoluteDifferenceComparison(layerName):
    toAnalyse = gpd.read_file(GeoPkg_Results,layer=layerName)
    SortedList = toAnalyse.columns.tolist()
    SortedList.sort()
    tolerance = 0.01 #How close
    #for count, i in enumerate(SortedList):
    #    print(f"{count} {i}")
    """
    https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.abs.html 
    Use Absolute value, as this ignores the +/- of the value. 
    Allowing for a better indication of the closeness to the EGM96 value, 
    to assess if this accounts for the difference
    """
    #see how close the difference between the two layers are to the EGM96 values
    if 'Leek' in layerName:
        toAnalyse['ErrorA'] = np.abs((toAnalyse[SortedList[5]] - toAnalyse[SortedList[7]]) - toAnalyse[SortedList[0]]) #(UKCDBL2 - VRTW Src) - EGM96 values
        toAnalyse['ErrorB'] = np.abs((toAnalyse[SortedList[1]] - toAnalyse[SortedList[7]]) - toAnalyse[SortedList[0]])  # (LCTL6 - VRTW Src) - EGM96 values
        toAnalyse['A_Closeness'] = toAnalyse['ErrorA'] <= tolerance
        toAnalyse['B_Closeness'] = toAnalyse['ErrorB'] <= tolerance
        print(f"Leek - The count of close values for set A and B respectively are: {toAnalyse['A_Closeness'].sum()}\t{toAnalyse['B_Closeness'].sum()}")

        #print(toAnalyse)
    elif 'Sennybridge' in layerName:
        toAnalyse['ErrorA'] = np.abs((toAnalyse[SortedList[2]] - toAnalyse[SortedList[4]]) - toAnalyse[SortedList[0]]) #(UKCDBL2 - VRTW Src) - EGM96 values
        toAnalyse['ErrorB'] = np.abs((toAnalyse[SortedList[1]] - toAnalyse[SortedList[4]]) - toAnalyse[SortedList[0]])  # (LCTL6 - VRTW Src) - EGM96 values
        toAnalyse['A_Closeness'] = toAnalyse['ErrorA'] <= tolerance
        toAnalyse['B_Closeness'] = toAnalyse['ErrorB'] <= tolerance
        print(f"Sennybridge - The count of close values for set A and B respectively are: {toAnalyse['A_Closeness'].sum()}\t{toAnalyse['B_Closeness'].sum()}")


#AnalyseBlindData(ResultsFiles[0], ResultFields[0], blindColumns) #Leek Results
#AnalyseBlindData(ResultsFiles[1], ResultFields[1],blindColumns) #Sennybridge Results
#AnalyseControlData(ResultsFiles[2], ResultFields[2]) #Control A -1m resolution, resampled to respective datasets
#AnalyseControlData(ResultsFiles[3], ResultFields[3]) # Control B, resampled datasets resampled back to 1m resolution and compared.
#AnalyseBlindData(ResultsFiles[2], ResultFields[2], blindControlAColumns)
#AnalyseBlindData(ResultsFiles[3], ResultFields[3], blindControlBColumns)

#Prints out all the files' Friedman results nicely, just need to pass the file names, it shows the columns used in the calculation
#FriedmanResults(ResultsFiles, rounding=5)
#FriedmanResults(CubicResultsFiles,rounding=5)


#These two functions get the absolute difference, and calculate the closeness. Printing a count of how close they are within the tolerance...
#AbsoluteDifferenceComparison('Leek_SampleValues_EGM') #Leek EGM layer
#AbsoluteDifferenceComparison('Sennybridge_SampleValues_EGM') #Sennybridge EGM layer

#The results file with columns, the expression to match in the columns, label for the graph
def AnalysisControlData(file, expression, label, y_maxValue):
    toAnalyse = gpd.read_file(file)
    binsValue = 30
    print(f"Reading {file} now...")
    exclude = ["geometry", "id"]
    columns = [
        col for col in toAnalyse.columns #iterate through all columns in the dataframe
        if re.match(expression, col) #logical test if a column matches the regex pattern
        and col not in exclude #check that the colum isn't in the exclude list
        and toAnalyse[col].dtype.kind in 'iufc' ] # ensure the column is numeric data types only

    print("\t" + str(columns)) #Prints the list of columns identified for use matching the regex pattern
    #Plotting the range histograms
    fig, ax = plt.subplots()
    #Passes all the columns in this interpolation method, to find min / max and retrun range to plot it
    toAnalyse[str(columns)] = GetRange(toAnalyse[columns])

    print(toAnalyse[str(columns)].mean()) #Print the columns and the mean, to see an output during development
    print(toAnalyse[str(columns)].head()) # See the column names, and sample of data
    print("Max value is..." + str(toAnalyse[str(columns)]))  #
    for i in columns: #This just iterates through the column using 'stats.describe[array]
        DescribeMe(toAnalyse[str(i)], str(i)) #Not essential for the plotting of histograms - used for development confidence in data
    toAnalyse[str(columns)].hist(bins=binsValue, edgecolor='black', ax=ax)
    ax.set_title(f'{label} - Range of ' + str(expression))
    ax.set_xlabel('Range Value')
    ax.set_ylabel('Count')
    ax.set_ylim(0,y_maxValue) #
    ax.text(0.95, 0.95, f'Mean: {toAnalyse[str(columns)].mean():.4f}',
            transform=ax.transAxes,  # Use Axes coordinates (0 to 1)
            fontsize=12, color='darkred',
            ha='right', va='top')
    #Save theplotted figure locally
    fig.savefig(f'D:/Dissertation/Control-DEFRA1m/4326Control/HistC_{label}_{expression}.png')
    plt.show()

def RMSEControl(ResultsFile, expression):
    toAnalyse = gpd.read_file(ResultsFile)
    print(f"Reading {ResultsFile} now...")
    exclude = ["geometry", "id"]
    columns = [
        col for col in toAnalyse.columns
        if re.match(expression, col)
        and col not in exclude
        and toAnalyse[col].dtype.kind in 'iufc'  # numeric only
    ]
    print("\t" + str(columns))
    actual = []
    for element in columns:
        if "Control1m" in element:
            print("Found it...")
            actual.append(str(element))
    print(actual)
    actualIndex = columns.index(actual[0])
    columns.pop(actualIndex)
    for j in columns:
        toAnalyse[str(j+ "-RMSE")] = GetRMSE(toAnalyse[actual[0]], toAnalyse[j])
        #print(toAnalyse[str(j + "-RMSE")].head())
        print(f"{j} - Mean RMSE is ...\t {toAnalyse[str(j + "-RMSE")].mean().round(5)}")
        """
        #######
        TODO - Sort the Get RMSE function, or write a new one...
        #######
        """

"""
#Analysis including the source data
AnalysisControlData(NewControlResults, "GDAL_Nearest", "Control", 40)
AnalysisControlData(NewControlResults, "GDAL_Bilinear", "Control", 40)
AnalysisControlData(NewControlResults, "GDAL_Cubic", "Control", 40)
AnalysisControlData(NewControlResults, "WarpedVRT_Nearest", "Control", 40)
AnalysisControlData(NewControlResults, "WarpedVRT_Bilinear", "Control", 40)

#Analysis excluding the source data
AnalysisControlData(NewControlResultsTwo, "GDAL_Nearest", "Control_less_Src", 40)
AnalysisControlData(NewControlResultsTwo, "GDAL_Bilinear", "Control_less_Src", 40)
AnalysisControlData(NewControlResultsTwo, "GDAL_Cubic", "Control_less_Src", 40)
AnalysisControlData(NewControlResultsTwo, "WarpedVRT_Nearest", "Control_less_Src", 40)
AnalysisControlData(NewControlResultsTwo, "WarpedVRT_Bilinear", "Control_less_Src", 40)

#Analysis with only OGC CDB and TMS
AnalysisControlData(NewControlResultsThree, "GDAL_Nearest", "Control_StdOnly", 46)
AnalysisControlData(NewControlResultsThree, "GDAL_Bilinear", "Control_StdOnly", 46)
AnalysisControlData(NewControlResultsThree, "GDAL_Cubic", "Control_StdOnly", 46)
AnalysisControlData(NewControlResultsThree, "WarpedVRT_Nearest", "Control_StdOnly", 46)
AnalysisControlData(NewControlResultsThree, "WarpedVRT_Bilinear", "Control_StdOnly", 46)
"""
#Pairing analysis
AnalysisControlData(Pair_TMSCDB2, "GDAL_Nearest", "TMS_CDB2", 54)
AnalysisControlData(Pair_TMSCDB2, "GDAL_Bilinear", "TMS_CDB2", 54)
AnalysisControlData(Pair_TMSCDB2, "GDAL_Cubic", "TMS_CDB2", 54)

AnalysisControlData(Pair_TMSCDB6, "GDAL_Nearest", "TMS_CDB6", 54)
AnalysisControlData(Pair_TMSCDB6, "GDAL_Bilinear", "TMS_CDB6", 54)
AnalysisControlData(Pair_TMSCDB6, "GDAL_Cubic", "TMS_CDB6", 54)

AnalysisControlData(Pair_CDB6CDB2, "GDAL_Nearest", "CDB6_CDB2", 56)
AnalysisControlData(Pair_CDB6CDB2, "GDAL_Bilinear", "CDB6_CDB2", 56)
AnalysisControlData(Pair_CDB6CDB2, "GDAL_Cubic", "CDB6_CDB2", 56)

"""
AnalysisControlData(CubicResultsFiles[0], "GDAL_Nearest", "Leek", 16)
AnalysisControlData(CubicResultsFiles[0], "GDAL_Bilinear", "Leek", 16)
AnalysisControlData(CubicResultsFiles[0], "GDAL_Cubic", "Leek", 16)
AnalysisControlData(CubicResultsFiles[0], "WarpedVRT_Nearest", "Leek", 16)
AnalysisControlData(CubicResultsFiles[0], "WarpedVRT_Bilinear", "Leek", 16)

AnalysisControlData(CubicResultsFiles[1], "GDAL_Nearest", "Sennybridge", 12)
AnalysisControlData(CubicResultsFiles[1], "GDAL_Bilinear", "Sennybridge", 12)
AnalysisControlData(CubicResultsFiles[1], "GDAL_Cubic", "Sennybridge", 12)
AnalysisControlData(CubicResultsFiles[1], "WarpedVRT_Nearest", "Sennybridge", 12)
AnalysisControlData(CubicResultsFiles[1], "WarpedVRT_Bilinear", "Sennybridge", 12)
"""


#The below all workd for Friedman results
#FriedmanNoListResults(NewControlResults, 5) #This has 5 dataset samples...
#FriedmanNoListResults(CubicResultsFiles[0], 5) #Leek Sample results
#FriedmanNoListResults(CubicResultsFiles[1], 5) #Sennybridge sample results
#FriedmanNoListResults(NewControlResultsTwo, 5) #This removes the control set, and is equivalent of the case study




#RMSEControl(NewControlResults, "GDAL_Nearest")
#RMSEControl(NewControlResults, "GDAL_Bilinear")
#RMSEControl(NewControlResults, "GDAL_Cubic")
#RMSEControl(NewControlResults, "WarpedVRT_Nearest")
#RMSEControl(NewControlResults, "WarpedVRT_Bilinear")

#AnalysisControlData(ResultsFiles[0], "GDAL_Nearest", "Leek")
#AnalysisControlData(ResultsFiles[0], "GDAL_Bilinear", "Leek")


#print("\n\nHere is RMSE Means info\n")
#print(RMSEMeans)
#print(type(RMSEMeans))
#for key in RMSEMeans.keys():
#    print(str(key) + "  " + str(RMSEMeans[key]))