
<div align="center">
<div style="background-color: #1a1b1e; padding: 20px; border-radius: 8px; margin-bottom: 20px;">

# Topo3D-world

</div>
<div align="left">
 
Get topography data from any part of the world and trasforms it in a 3D STL file ready to be printed. Improve resolution beyond the ooriginal Geotiff file.

The National Geospatial-Intelligence Agency (NGA) and NASA. Created the most complete, high-resolution topographic map of Earth, which is very useful for many scientific and practical purposes. The Shuttle Radar Topography Mission (SRTM) collected detailed elevation data for almost the entire Earth. It used a special radar system flying on the Space Shuttle Endeavour. This project data is open source and free. 

     
</div>
<div align="center">
 
<img width="2549" height="1499" alt="Screenshot From 2025-07-25 15-05-38" src="https://github.com/user-attachments/assets/33391e51-d3ba-4ac2-a8c7-47787a2e39a9" />

Convert Digital Elevation Model (DEM) files into 3D printable mountain models with proper scaling and automatic sizing. 

![output](https://github.com/user-attachments/assets/1f0f4a4a-ba7b-4223-95a6-be187c9740d0)

</div>
<div align="left">
<hr>
 
# How to Download a GeoTIFF from OpenTopography 
 
  1. Go to the website: Visit the specific OpenTopography link for the Shuttle Radar Topography Mission data.

     
</div>
<div align="center">

 https://portal.opentopography.org/raster?opentopoID=OTSRTM.082016.4326.1   


<img width="1600" height="800" alt="image" src="https://github.com/user-attachments/assets/b91c2ebe-1121-4f75-aa67-418287d594e6" />

</div>
<div align="left">
 
  2. Choose your area: Use the map or tools on the site to select the exact area you want the elevation data from.
  3. Select data format: Make sure to pick the GeoTIFF format if there’s an option, as this is a standard file type for elevation and raster data. (do not add any vizualization extra features)
     

# Use the Script
The script does four main modifications 
(1) Change all units to meters. 
(2) Scale height for vizualization 
(3) Improves resolution (only for vizualization not real data) 
(4) Trasforms GeoTiff to STL 
(5) Adds a base and walls to make it 3D compatible.

## Install required Python packages

```python

  pip install numpy rasterio numpy-stl

```
  
## 2.Path to file

### Modify these paths in the script
```python
 raw_geotiff = "path/yourfiles/terrain.tif"
  output_stl = "path/yourfiles/model.stl"
```
## 3. Run the script
```python
  python geotiff_to_stl.py
```

please colaborate to make it easier to new users

Enjoy!

# Feel free to add or chage this repo
</div>
