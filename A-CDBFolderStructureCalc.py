
class CDBFileName:
    def __init__(self, lat,long):
        self.lat = float(lat)
        self.long = float(long)
        self.SliceID = int(self.lat+90)
        self.NbSliceID = 2 * int(90 / 1)
        self.GetDLonZoneLat()
        self.DLonCellBasic = 1.0
        self.DLonCell = self.DLonCellBasic * self.GetDLonZone
        self.SliceIDIndex = int(int((self.long + 180.0) / self.DLonCell) * self.GetDLonZone)
        self.NBSliceIDIndex = 2 * int(180.0 / self.DLonCell)
        self.NBSliceIDIndexEq = 2 * int(180 / self.DLonCellBasic)

    def GetFileName(self):
        filename = "_".join([self.foldOne(), self.foldTwo(), self.GetLOD(), self.GetURef(), self.GetRRef()])
        return filename

    def foldOne(self):
        if self.lat < 0.0:
            folderName = "S"
            folderName = folderName + str(int((self.NbSliceID / 2) - self.SliceID)).zfill(2)
        else:
            folderName = "N"
            folderName = folderName + str(int(self.SliceID - (self.NbSliceID / 2))).zfill(2)

        return folderName

    # todo - further work on this to build it using the sliceIDindex, once the lookup is sorted
    def foldTwo(self):
        if self.long < 0.0:
            folderName = "W"
            folderName = folderName + str(int((self.NBSliceIDIndexEq / 2) - self.SliceIDIndex)).zfill(3)
        else:
            folderName = "E"
            folderName = folderName + str(int(self.SliceIDIndex - (self.NBSliceIDIndexEq / 2))).zfill(3)

        return folderName

    def SetLod(self, lod):
        self.Lod = int(lod)
        self.URef = int((pow(2, self.Lod) * ((self.lat + 90) % 1)))
        self.RRef = int( (((self.long + 180.0)%self.GetDLonZone) * pow(2, self.Lod)) / self.GetDLonZone)

    def GetDLonZoneLat(self):
        if self.lat >= 89.0 and self.lat < 90.0:
            self.GetDLonZone = 12.0
        if self.lat >= 80.0 and self.lat < 89.0:
            self.GetDLonZone = 6.0
        if self.lat >= 75.0 and self.lat < 80.0:
            self.GetDLonZone = 4.0
        if self.lat >= 70.0 and self.lat < 75.0:
            self.GetDLonZone = 3.0
        if self.lat >= 50.0 and self.lat < 70.0:
            self.GetDLonZone = 2.0
        if self.lat >= -50.0 and self.lat < 50.0:
            self.GetDLonZone = 1.0
        if self.lat >= -70.0 and self.lat < -50.0:
            self.GetDLonZone = 2.0
        if self.lat >= -75.0 and self.lat < -70.0:
            self.GetDLonZone = 3.0
        if self.lat >= -80.0 and self.lat < -75.0:
            self.GetDLonZone = 4.0
        if self.lat >= -89.0 and self.lat < -80.0:
            self.GetDLonZone = 6.0
        if self.lat >= -90.0 and self.lat < -89.0:
            self.GetDLonZone = 12.0


    def GetLOD(self):
        return "L" + str(self.Lod).zfill(2)

    def GetURef(self):
        return str("U" + str(self.URef))

    def GetRRef(self):
        return str("R" + str(self.RRef))

def TestGetLonLatZoneFunc(): #This functions, and produces matching output to Table 3-29 of the OGC CDB Std.
    for i in range(-90,90):
        test = CDBFileName(float(i), 32.0)
        print(str(i) + "     " + str(test.GetDLonZone))

#53.14880,-1.92542 - should be N53W002_D001_S001_T001_l06_U9_R2
testObject = CDBFileName(53.14880,-1.92542)
print(testObject.foldOne())
print(testObject.foldTwo())
testObject.SetLod(6)
print(testObject.GetLOD())
print(testObject.GetURef())
print(testObject.GetRRef())
print(testObject.GetFileName())

#Sennybridge Extent - -3.7500000000000000,52.0000000000000000 : -3.4062500000000000,52.1250000000000000
#-3.7501492181602654,52.0001232403299412 : -3.4063994821914525,52.1252551121226446

#Leek extent - -2.0000000000000000,53.1093750000000000 : -1.8437500000000000,53.1875000000000000
#-2.0000449880758033,53.1094709946684915 : -1.8438478952115962,53.1875695411005935

#This section below could be swept up to have an input of a JSON object with area name, and the lat long for each point / file
extentOne = CDBFileName(52.0001232403299412,-3.7501492181602654) #Sennybridge
extentTwo = CDBFileName(52.1252551121226446,-3.4063994821914525) #Sennybridge
extentThree = CDBFileName(53.1094709946684915,-1.99449880758033) #Leek
extentFour = CDBFileName(53.1875695411005935,-1.8438478952115962) #Leek

RequestLod = [0,1,2,3,4,5,6,7,8,9]

#TODO Make this calculate all the files required for a bounding box,
# not just a filename which I then had to read between the lines to get them all.

for i in RequestLod:
    extentOne.SetLod(i)
    extentTwo.SetLod(i)
    extentThree.SetLod(i)
    extentFour.SetLod(i)
    print("Lod " + str(i) + " - Areas of interest:")
    print("\tSennybridge - " + extentOne.GetFileName())
    print("\tSennybridge - " + extentTwo.GetFileName() + "\n")
    print("\tLeek - " + extentThree.GetFileName())
    print("\tLeek - " + extentFour.GetFileName())
