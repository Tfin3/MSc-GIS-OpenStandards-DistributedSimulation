import os
from collections import defaultdict

# Replace with the path to your CDB Elevation root directory
CDB_ROOT = "E:\\UK_CDB_OUTPUT\\UK_ELEVATION_13FEB17"
ELEVATION_DIR = os.path.join(CDB_ROOT, "Tiles")

# Valid raster file extensions
VALID_EXTENSIONS = {'.tif', '.tiff'}

# Dictionary to hold files by LOD level,
# defaultdict allows any key to be added with a list created if not present
lod_files = defaultdict(list)

#Check it is a valid raster file extension
def is_valid_raster(filename):
    name, ext = os.path.splitext(filename)
    return ext.lower() in VALID_EXTENSIONS

def walk_cdb_elevation(elevation_root):
    for root, dirs, files in os.walk(elevation_root):
        parts = root.split(os.sep)
        # Try to detect LOD level from folder path (e.g., LOD1, LOD2...)
        for part in parts:
            if part.startswith("L") and part[1:].isdigit():
                lod_level = part
                break
        else:
            continue  # Skip if no LOD directory found in path

        for file in files:
            if is_valid_raster(file):
                full_path = os.path.join(root, file)
                lod_files[lod_level].append(full_path)

# Run the walk
walk_cdb_elevation(ELEVATION_DIR)


# Optional: print results
# Sort LOD Keys numerically, slicing the first character 'L' from the key when sorting
for lod in sorted(lod_files.keys(), key=lambda x: int(x[1:])):
    print(f"{lod}: {len(lod_files[lod])} files")
    # Uncomment to print file paths
    #for path in lod_files[lod]:
    #     print(f"  {path}")

#This seems to work on the UK CDB FOlder... Now to build a VRT with it.
#The Below builds a text file which can be used in gdalbuildvrt -
# 'gdalbuildvrt -overwrite -resolution average -input_file_list "D:\Dissertation\PythonWork\A400M_CDB-L04.txt" A400_LOD4_noResample.vrt'
#And it makes a VRT to be used in QGIS for example.

#TODO make the below a function so it can just be called when needed
for lod in sorted(lod_files.keys(), key=lambda x: int(x[1:])):
    for path in lod_files[lod]:
        with open("UK_CDB-" + str(lod) + ".txt", "a") as f:
            f.write(path + "\n")