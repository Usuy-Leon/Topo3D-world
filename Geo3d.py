
import numpy as np
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio.crs import CRS
from stl import mesh


if __name__ == "__main__":
    # === CONFIGURATION - MODIFY THESE PATHS AND SETTINGS ===
    # File paths
    raw_geotiff = "/path/yourfiles/input_dem.tif"
    reprojected_geotiff = "/path/your/reprojected_dem.tif"
    output_stl = "/path/yourfiles/terrain_model.stl"
    
def reproject_geotiff_to_utm(input_geotiff_path, output_geotiff_path, target_epsg_code):

    with rasterio.open(input_geotiff_path) as src:
        # Calculate transformation to target UTM zone
        transform, width, height = calculate_default_transform(
            src.crs,
            CRS.from_epsg(target_epsg_code),
            src.width,
            src.height,
            *src.bounds
        )
        # Update metadata for new projection oo not modify !!
        kwargs = src.meta.copy()
        kwargs.update({
            'crs': CRS.from_epsg(target_epsg_code),
            'transform': transform,
            'width': width,
            'height': height
        })

        # Write reprojected file
        with rasterio.open(output_geotiff_path, 'w', **kwargs) as dst:
            reproject(
                source=rasterio.band(src, 1),
                destination=rasterio.band(dst, 1),
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=transform,
                dst_crs=CRS.from_epsg(target_epsg_code),
                resampling=Resampling.nearest
            )
    print(f"GeoTIFF converted and saved to: {output_geotiff_path}")

def raise_elevation_at_points(dem, transform, points, raise_height):

    for lon, lat in points:
        # Convert GPS coordinates to raster pixel coordinates
        col, row = ~transform * (lon, lat)
        row, col = int(round(row)), int(round(col))
        # Check if point is within raster bounds
        if 0 <= row < dem.shape[0] and 0 <= col < dem.shape[1]:
            # Raise 3x3 pixel area around the point for visibility
            r_min = max(row - 1, 0)
            r_max = min(row + 2, dem.shape[0])
            c_min = max(col - 1, 0)
            c_max = min(col + 2, dem.shape[1])
            dem[r_min:r_max, c_min:c_max] += raise_height
    return dem

def geotiff_to_stl(
    geotiff_path,
    stl_path,
    scale_xy=1.0,
    scale_z=1.0,
    base_height=0.1,
    utm_epsg=32618,
    highlight_points=None,
    raise_height=100.0
):

    with rasterio.open(geotiff_path) as src:
        dem = src.read(1)  # Read elevation data
        transform = src.transform
        nodata = src.nodatavals[0]

        # Handle no-data values (areas with no elevation data)
        if nodata is not None and not np.isnan(nodata):
            dem_valid = dem[dem != nodata]
            min_valid_dem = np.min(dem_valid) if dem_valid.size > 0 else 0
            dem = np.where(dem == nodata, min_valid_dem, dem)

        # Add raised markers for points of interest
        if highlight_points:
            dem = raise_elevation_at_points(dem, transform, highlight_points, raise_height)

        n_rows, n_cols = dem.shape
        
        # Create coordinate grids from georeferencing data
        x_coords = np.arange(n_cols) * transform.a + transform.c
        y_coords = np.arange(n_rows) * transform.e + transform.f
        y_coords = y_coords[::-1]  # Flip Y-axis to match DEM orientation

        # Apply horizontal scaling (convert real-world meters to printable millimeters)
        x_coords = x_coords * scale_xy
        y_coords = y_coords * scale_xy

        # Create 3D coordinate matrices
        xx, yy = np.meshgrid(x_coords, y_coords)
        zz = dem * scale_z  # Apply vertical scaling/exaggeration

        # Create triangular mesh from grid points
        vertices = np.column_stack((xx.ravel(), yy.ravel(), zz.ravel()))
        faces = []
        for row in range(n_rows - 1):
            for col in range(n_cols - 1):
                # Create two triangles for each grid square
                v0 = row * n_cols + col
                v1 = v0 + 1
                v2 = v0 + n_cols
                v3 = v2 + 1
                faces.append([v0, v1, v2])  # Triangle 1
                faces.append([v1, v3, v2])  # Triangle 2
        faces = np.array(faces)

    # Create solid base for 3D printing stability
    min_z = np.min(zz)
    base_z = min_z - base_height  # Base thickness in model units

    # Duplicate vertices for base level
    num_vertices = vertices.shape[0]
    base_vertices = vertices.copy()
    base_vertices[:, 2] = base_z  # Set all base vertices to base height
    all_vertices = np.vstack([vertices, base_vertices])

    # Define base face corners
    top_left = 0
    top_right = n_cols - 1
    bottom_left = (n_rows - 1) * n_cols
    bottom_right = n_rows * n_cols - 1

    # Base vertex indices (offset by original vertex count)
    base_top_left = top_left + num_vertices
    base_top_right = top_right + num_vertices
    base_bottom_left = bottom_left + num_vertices
    base_bottom_right = bottom_right + num_vertices

    # Create base faces (two triangles)
    base_faces = [
        [base_top_left, base_bottom_left, base_top_right],
        [base_top_right, base_bottom_left, base_bottom_right],
    ]

    # Create wall faces to connect terrain to base
    wall_faces = []

    # Bottom edge walls
    for col in range(n_cols - 1):
        s0 = (n_rows - 1) * n_cols + col
        s1 = s0 + 1
        b0 = s0 + num_vertices
        b1 = s1 + num_vertices
        wall_faces.append([s0, s1, b1])
        wall_faces.append([s0, b1, b0])

    # Top edge walls
    for col in range(n_cols - 1):
        s0 = col
        s1 = col + 1
        b0 = s0 + num_vertices
        b1 = s1 + num_vertices
        wall_faces.append([s0, b1, s1])
        wall_faces.append([s0, b0, b1])

    # Left edge walls
    for row in range(n_rows - 1):
        s0 = row * n_cols
        s1 = (row + 1) * n_cols
        b0 = s0 + num_vertices
        b1 = s1 + num_vertices
        wall_faces.append([s0, s1, b1])
        wall_faces.append([s0, b1, b0])

    # Right edge walls
    for row in range(n_rows - 1):
        s0 = row * n_cols + (n_cols - 1)
        s1 = (row + 1) * n_cols + (n_cols - 1)
        b0 = s0 + num_vertices
        b1 = s1 + num_vertices
        wall_faces.append([s0, b1, s1])
        wall_faces.append([s0, b0, b1])

    # Combine all faces
    all_faces = np.vstack([faces, base_faces, wall_faces])

    # Build and save STL mesh
    terrain_mesh = mesh.Mesh(np.zeros(all_faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(all_faces):
        for j in range(3):
            terrain_mesh.vectors[i][j] = all_vertices[f[j], :]

    terrain_mesh.save(stl_path)
    print(f"STL file saved at: {stl_path}")

    \
    
    # UTM Zone for your area (find at: https://mangomap.com/robertyoung/maps/69585/what-utm-zone-am-i-in-)
    
    utm_epsg_code = 32618  # Change this to your UTM zone!!!


    
    # Step 1: Reproject GeoTIFF to UTM (ensures accurate meters)
    reproject_geotiff_to_utm(raw_geotiff, reprojected_geotiff, utm_epsg_code)

    # Step 2: Calculate automatic scaling for 3D printing
    desired_max_print_mm = 150  # Maximum dimension of final print (150mm = 15cm)
    with rasterio.open(reprojected_geotiff) as src:
        real_width_m = src.width * abs(src.transform.a)  # Real width in meters
        real_height_m = src.height * abs(src.transform.e)  # Real height in meters
        max_dim_m = max(real_width_m, real_height_m)

    # Calculate scale to fit desired print size
    calculated_scale_xy = desired_max_print_mm / max_dim_m  # mm per meter
    print(f"Horizontal scale: {calculated_scale_xy} mm/m")

    # Vertical exaggeration (2.0 = 2x Helps a lot with visualization)
    vertical_factor = 2.0  
    calculated_scale_z = calculated_scale_xy * vertical_factor
    print(f"Vertical scale: {calculated_scale_z} mm/m")

    # Calculate base thickness (keep it thin for less material)
    desired_base_thickness_mm = 1.0  # 1mm thick base
    calculated_base_height = desired_base_thickness_mm / calculated_scale_z
    print(f"Base height: {calculated_base_height} DEM units")


    # Step 3: Generate STL
    geotiff_to_stl(
        reprojected_geotiff,
        output_stl,
        scale_xy=calculated_scale_xy,
        scale_z=calculated_scale_z,
        base_height=calculated_base_height,
        utm_epsg=utm_epsg_code,
        highlight_points=points_of_interest,
        raise_height=raise_height_dem_units
    )
