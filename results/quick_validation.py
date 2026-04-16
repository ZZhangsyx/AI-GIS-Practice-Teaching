# Quick visualization using vectorized operations
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import rasterio
import geopandas as gpd

OUTPUT_DIR = r"F:\科研\CCS-1\paper\results"

print("Generating publication-quality figures...")

# Load data
roads = gpd.read_file(os.path.join(OUTPUT_DIR, "zhaoqing_road_network.gpkg"))

# Load and process DEM for simple visualization
srtm_dir = r"F:\Data\SRTM_90m"
with rasterio.open(os.path.join(srtm_dir, "srtm_59_08.tif")) as src:
    dem_data = src.read(1)

# Crop to study area
zhaoqing_bounds = {'north': 23.25, 'south': 22.95, 'east': 112.70, 'west': 112.35}
bounds = src.bounds
pixel_size_lon = (bounds.right - bounds.left) / dem_data.shape[1]
pixel_size_lat = (bounds.top - bounds.bottom) / dem_data.shape[0]

col_start = int((zhaoqing_bounds['west'] - bounds.left) / pixel_size_lon)
col_end = int((zhaoqing_bounds['east'] - bounds.left) / pixel_size_lon)
row_start = int((bounds.top - zhaoqing_bounds['north']) / pixel_size_lat)
row_end = int((bounds.top - zhaoqing_bounds['south']) / pixel_size_lat)

dem_cropped = dem_data[row_start:row_end, col_start:col_end].astype(np.float32)
nodata_mask = (dem_cropped < 0) | (dem_cropped == -32768)
dem_cropped[nodata_mask] = np.nan

print(f"Elevation range: {np.nanmin(dem_cropped):.1f}m - {np.nanmax(dem_cropped):.1f}m")

# Create figure with subplots
fig = plt.figure(figsize=(16, 12))

# Road network only
ax1 = fig.add_subplot(2, 2, 1)
for cls in roads['road_class'].unique():
    subset = roads[roads['road_class'] == cls]
    colors = {'Expressway': '#E31A1C', 'Primary': '#FB6502', 'Secondary': '#FFDA01',
              'Tertiary': '#2E8B57', 'Local': '#1F78B4', 'Other': '#999999'}
    lw = 2 if cls == 'Expressway' else 1
    subset.plot(ax=ax1, color=colors.get(cls, '#999999'), linewidth=lw, alpha=0.8, label=cls)
ax1.set_title('A. Road Network (OpenStreetMap)', fontsize=12, fontweight='bold')
ax1.set_xlabel('Longitude')
ax1.set_ylabel('Latitude')
ax1.legend(loc='upper right', fontsize=8)
ax1.grid(True, alpha=0.3)

# Elevation map
ax2 = fig.add_subplot(2, 2, 2)
im2 = ax2.imshow(np.flipud(dem_cropped), cmap='terrain', aspect='auto',
                  extent=[zhaoqing_bounds['west'], zhaoqing_bounds['east'],
                          zhaoqing_bounds['south'], zhaoqing_bounds['north']])
ax2.set_title('B. Digital Elevation Model (SRTM 90m)', fontsize=12, fontweight='bold')
ax2.set_xlabel('Longitude')
ax2.set_ylabel('Latitude')
plt.colorbar(im2, ax=ax2, label='Elevation (m)', shrink=0.8)

# Transect showing elevation profile
ax3 = fig.add_subplot(2, 2, 3)
# Take a west-east transect at mid-latitude
mid_row = dem_cropped.shape[0] // 2
elev_profile = dem_cropped[mid_row, :]
lon_profile = np.linspace(zhaoqing_bounds['west'], zhaoqing_bounds['east'], len(elev_profile))
valid = ~np.isnan(elev_profile)
ax3.plot(lon_profile[valid], elev_profile[valid], 'b-', linewidth=1)
ax3.fill_between(lon_profile[valid], 0, elev_profile[valid], alpha=0.3)
ax3.set_title('C. West-East Elevation Profile (at 23.1N)', fontsize=12, fontweight='bold')
ax3.set_xlabel('Longitude')
ax3.set_ylabel('Elevation (m)')
ax3.set_xlim(zhaoqing_bounds['west'], zhaoqing_bounds['east'])
ax3.grid(True, alpha=0.3)

# Combined visualization
ax4 = fig.add_subplot(2, 2, 4)
# Simple terrain shading from elevation
terrain = np.nan_to_num(dem_cropped, nan=0)
shaded = (terrain - terrain.min()) / (terrain.max() - terrain.min())
shaded = np.flipud(shaded)
ax4.imshow(shaded, cmap='Greys', alpha=0.5, aspect='auto',
            extent=[zhaoqing_bounds['west'], zhaoqing_bounds['east'],
                    zhaoqing_bounds['south'], zhaoqing_bounds['north']])
# Overlay roads
for cls in roads['road_class'].unique():
    subset = roads[roads['road_class'] == cls]
    colors = {'Expressway': '#E31A1C', 'Primary': '#FB6502', 'Secondary': '#FFDA01',
              'Tertiary': '#2E8B57', 'Local': '#1F78B4', 'Other': '#999999'}
    lw = 2 if cls == 'Expressway' else 1
    subset.plot(ax=ax4, color=colors.get(cls, '#999999'), linewidth=lw, alpha=0.9, label=cls)
ax4.set_title('D. Combined: Terrain + Road Network', fontsize=12, fontweight='bold')
ax4.set_xlabel('Longitude')
ax4.set_ylabel('Latitude')
ax4.legend(loc='upper right', fontsize=7, ncol=2)
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "zhaoqing_publication_figures.png"), dpi=200, bbox_inches='tight')
plt.close()

print("Publication figures saved!")

# Generate statistics report
print("\nFinal Statistics:")
print(f"Elevation: {np.nanmin(dem_cropped):.1f}m - {np.nanmax(dem_cropped):.1f}m (mean: {np.nanmean(dem_cropped):.1f}m)")
print(f"Road segments: {len(roads)}")
print(f"Road classes: {roads['road_class'].value_counts().to_dict()}")
