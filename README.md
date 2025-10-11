# Topo3D-world-
Get topography data from any part of the world and trasforms it in a 3D STL file ready to be printed. Convert Digital Elevation Model (DEM) files into 3D printable mountain models with proper scaling and automatic sizing. 

# Simple Steps
## 1. Python Packages

### Install required Python packages
  pip install numpy rasterio numpy-stl
  
## 2.Path to file

# Modify these paths in the script
  raw_geotiff = "path/to/your/terrain.tif"
  output_stl = "path/to/your/model.stl"

## 3. Run the script
  python geotiff_to_stl.py
