from osgeo import gdal
import os

# Directory to save the VRT files
VRT_OUTPUT_DIR = "/path/to/output/vrt"
os.makedirs(VRT_OUTPUT_DIR, exist_ok=True)

# Create a VRT for each LOD level
for lod in lod_files:
    output_vrt = os.path.join(VRT_OUTPUT_DIR, f"{lod}.vrt")
    print(f"Building VRT: {output_vrt}")

    # Use GDAL to build the VRT
    gdal.BuildVRT(output_vrt, lod_files[lod])
