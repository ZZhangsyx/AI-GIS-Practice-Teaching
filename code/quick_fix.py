# -*- coding: utf-8 -*-
"""
Generate publication-quality figures with Chinese labels and proper N-S orientation
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import matplotlib.font_manager as fm
import rasterio
import geopandas as gpd

# Configure Chinese font
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'WenQuanYi Micro Hei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# Increase default font sizes
plt.rcParams['font.size'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['xtick.labelsize'] = 11
plt.rcParams['ytick.labelsize'] = 11
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.titlesize'] = 16

OUTPUT_DIR = r"../results"
SRTM_DIR = r"../data"

print("Generating publication-quality figures with Chinese labels...")

# Load road data
roads = gpd.read_file(os.path.join(OUTPUT_DIR, "zhaoqing_road_network.gpkg"))

# Load DEM
with rasterio.open(os.path.join(SRTM_DIR, "srtm_59_08.tif")) as src:
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
dem_cropped[dem_cropped < 0] = np.nan

print(f"Elevation: {np.nanmin(dem_cropped):.1f}m - {np.nanmax(dem_cropped):.1f}m")
print(f"Shape: {dem_cropped.shape}")

# Create publication figure with 4 subplots
fig = plt.figure(figsize=(18, 14))

# Color schemes
road_colors = {
    'Expressway': '#E31A1C',   # 高速
    'Primary': '#FB6502',       # 主干路
    'Secondary': '#FFDA01',     # 次干路
    'Tertiary': '#2E8B57',      # 支路
    'Local': '#1F78B4',         # 集散道路
    'Other': '#999999'          # 其他
}

# ============================================================
# Subplot A: Road Network
# ============================================================
ax1 = fig.add_subplot(2, 2, 1)
for cls in roads['road_class'].unique():
    subset = roads[roads['road_class'] == cls]
    lw = 2.5 if cls == 'Expressway' else 1.5
    subset.plot(ax=ax1, color=road_colors.get(cls, '#999999'), linewidth=lw, alpha=0.8, label=cls)

ax1.set_xlim(zhaoqing_bounds['west'], zhaoqing_bounds['east'])
ax1.set_ylim(zhaoqing_bounds['south'], zhaoqing_bounds['north'])
ax1.set_xlabel('经度 (°E)', fontsize=13)
ax1.set_ylabel('纬度 (°N)', fontsize=13)
ax1.set_title('A. 道路网络分类图\n(数据来源: OpenStreetMap)', fontsize=14, fontweight='bold')
ax1.legend(loc='upper right', fontsize=10, title='道路类型')
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.set_aspect('equal')

# Add N arrow
ax1.annotate('N', xy=(0.97, 0.97), xycoords='axes fraction',
             fontsize=14, fontweight='bold', ha='center', va='top')
ax1.annotate('↑', xy=(0.97, 0.93), xycoords='axes fraction',
             fontsize=18, ha='center', va='top')

# ============================================================
# Subplot B: Digital Elevation Model - FIXED: origin='lower' makes N UP
# ============================================================
ax2 = fig.add_subplot(2, 2, 2)

# Use extent to set geographic coordinates, origin='lower' makes North UP
im2 = ax2.imshow(dem_cropped, cmap='terrain', aspect='auto',
                  extent=[zhaoqing_bounds['west'], zhaoqing_bounds['east'],
                          zhaoqing_bounds['south'], zhaoqing_bounds['north']],
                  origin='lower',  # FIXED: North is UP!
                  vmin=0, vmax=1000)

ax2.set_xlabel('经度 (°E)', fontsize=13)
ax2.set_ylabel('纬度 (°N)', fontsize=13)
ax2.set_title('B. 数字高程模型 (SRTM 90m)\n(肇庆市端州区)', fontsize=14, fontweight='bold')
cbar2 = plt.colorbar(im2, ax=ax2, shrink=0.85, pad=0.02)
cbar2.set_label('高程 (m)', fontsize=12)

# Add N arrow
ax2.annotate('N', xy=(0.97, 0.97), xycoords='axes fraction',
             fontsize=14, fontweight='bold', ha='center', va='top')
ax2.annotate('↑', xy=(0.97, 0.93), xycoords='axes fraction',
             fontsize=18, ha='center', va='top')

# ============================================================
# Subplot C: Elevation Profile (West-East Transect)
# ============================================================
ax3 = fig.add_subplot(2, 2, 3)

# Take profile at middle latitude
mid_lat = (zhaoqing_bounds['north'] + zhaoqing_bounds['south']) / 2
mid_row = dem_cropped.shape[0] // 2
elev_profile = dem_cropped[mid_row, :]
lon_profile = np.linspace(zhaoqing_bounds['west'], zhaoqing_bounds['east'], len(elev_profile))

# Remove NaN for plotting
valid = ~np.isnan(elev_profile)
ax3.fill_between(lon_profile[valid], 0, elev_profile[valid], alpha=0.4, color='steelblue')
ax3.plot(lon_profile[valid], elev_profile[valid], 'b-', linewidth=2)

ax3.set_xlim(zhaoqing_bounds['west'], zhaoqing_bounds['east'])
ax3.set_xlabel('经度 (°E)', fontsize=13)
ax3.set_ylabel('高程 (m)', fontsize=13)
ax3.set_title(f'C. 西-东高程剖面图\n(纬度 {mid_lat:.2f}°N)', fontsize=14, fontweight='bold')
ax3.grid(True, alpha=0.3, linestyle='--')
ax3.set_ylim(0, np.nanmax(elev_profile) * 1.1)

# Add annotation for profile line
profile_lon_start = zhaoqing_bounds['west']
profile_lon_end = zhaoqing_bounds['east']
ax3.axhline(y=0, color='k', linewidth=0.5)

# ============================================================
# Subplot D: Combined - Terrain + Roads - FIXED: origin='lower' makes N UP
# ============================================================
ax4 = fig.add_subplot(2, 2, 4)

# Plot terrain background - FIXED: origin='lower' makes North UP
terrain_display = np.nan_to_num(dem_cropped, nan=0)
shaded = (terrain_display - terrain_display.min()) / (terrain_display.max() - terrain_display.min())
ax4.imshow(shaded, cmap='Greys', alpha=0.4, aspect='auto',
            extent=[zhaoqing_bounds['west'], zhaoqing_bounds['east'],
                    zhaoqing_bounds['south'], zhaoqing_bounds['north']],
            origin='lower')  # FIXED: North is UP!

# Overlay roads - use plot with ax parameter
for cls in roads['road_class'].unique():
    subset = roads[roads['road_class'] == cls]
    lw = 2.5 if cls == 'Expressway' else 1.5
    subset.plot(ax=ax4, color=road_colors.get(cls, '#999999'),
                linewidth=lw, alpha=0.9, label=cls)

ax4.set_xlim(zhaoqing_bounds['west'], zhaoqing_bounds['east'])
ax4.set_ylim(zhaoqing_bounds['south'], zhaoqing_bounds['north'])
ax4.set_xlabel('经度 (°E)', fontsize=13)
ax4.set_ylabel('纬度 (°N)', fontsize=13)
ax4.set_title('D. 道路网与地形叠加分析\n(综合分析结果)', fontsize=14, fontweight='bold')
ax4.legend(loc='upper right', fontsize=9, ncol=2, title='道路类型')
ax4.grid(True, alpha=0.2, linestyle='--')
ax4.set_aspect('equal')

# Add N arrow
ax4.annotate('N', xy=(0.97, 0.97), xycoords='axes fraction',
             fontsize=14, fontweight='bold', ha='center', va='top')
ax4.annotate('↑', xy=(0.97, 0.93), xycoords='axes fraction',
             fontsize=18, ha='center', va='top')

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "zhaoqing_publication_figures.png"), dpi=200, bbox_inches='tight')
plt.close()

print("Publication figures (with Chinese labels) saved!")

# ============================================================
# Generate slope classification figure with Chinese labels
# ============================================================
print("Generating slope classification figure...")

fig, axes = plt.subplots(1, 2, figsize=(16, 7))

# Calculate slope from DEM gradient (approximate)
slope_approx = np.abs(np.gradient(dem_cropped, axis=0)) * 100 / 90  # degrees
slope_approx = np.nan_to_num(slope_approx, nan=0)
slope_degrees = np.degrees(np.arctan(slope_approx))

# Classify slope
slope_classified = np.zeros_like(slope_degrees, dtype=np.uint8)
valid_elev_mask = ~np.isnan(dem_cropped)
slope_classified[(slope_degrees >= 0) & (slope_degrees < 3) & valid_elev_mask] = 5
slope_classified[(slope_degrees >= 3) & (slope_degrees < 8) & valid_elev_mask] = 4
slope_classified[(slope_degrees >= 8) & (slope_degrees < 15) & valid_elev_mask] = 3
slope_classified[(slope_degrees >= 15) & (slope_degrees < 25) & valid_elev_mask] = 2
slope_classified[(slope_degrees >= 25) & valid_elev_mask] = 1
slope_classified[~valid_elev_mask] = 0

# Left: Elevation - FIXED: origin='lower' makes North UP
im1 = axes[0].imshow(dem_cropped, cmap='terrain', aspect='auto',
                       extent=[zhaoqing_bounds['west'], zhaoqing_bounds['east'],
                               zhaoqing_bounds['south'], zhaoqing_bounds['north']],
                       origin='lower',  # FIXED: North is UP!
                       vmin=0, vmax=800)
axes[0].set_xlabel('经度 (°E)', fontsize=13)
axes[0].set_ylabel('纬度 (°N)', fontsize=13)
axes[0].set_title('高程分布图\n(SRTM 90m DEM)', fontsize=14, fontweight='bold')
cbar1 = plt.colorbar(im1, ax=axes[0], shrink=0.85)
cbar1.set_label('高程 (m)', fontsize=12)

# Add N arrow
axes[0].annotate('N', xy=(0.97, 0.97), xycoords='axes fraction',
                fontsize=14, fontweight='bold', ha='center', va='top')
axes[0].annotate('↑', xy=(0.97, 0.93), xycoords='axes fraction',
                fontsize=18, ha='center', va='top')

# Right: Slope suitability - FIXED: origin='lower' makes North UP
colors = ['#8B0000', '#FF4500', '#FFA500', '#90EE90', '#228B22']
cmap_slope = matplotlib.colors.ListedColormap(colors)
valid_mask = slope_classified > 0
masked_slope = np.ma.masked_where(~valid_mask, slope_classified)

im2 = axes[1].imshow(masked_slope, cmap=cmap_slope, aspect='auto',
                       extent=[zhaoqing_bounds['west'], zhaoqing_bounds['east'],
                               zhaoqing_bounds['south'], zhaoqing_bounds['north']],
                       origin='lower',  # FIXED: North is UP!
                       vmin=1, vmax=5)

axes[1].set_xlabel('经度 (°E)', fontsize=13)
axes[1].set_ylabel('纬度 (°N)', fontsize=13)
axes[1].set_title('坡度适宜性评价\n(物流园区选址)', fontsize=14, fontweight='bold')
cbar2 = plt.colorbar(im2, ax=axes[1], shrink=0.85, ticks=[1, 2, 3, 4, 5])
cbar2.ax.set_yticklabels(['>25° 不适宜', '15-25° 较不适宜', '8-15° 中等适宜',
                          '3-8° 适宜', '0-3° 最适宜'])
cbar2.set_label('适宜性等级', fontsize=12)

# Add N arrow
axes[1].annotate('N', xy=(0.97, 0.97), xycoords='axes fraction',
                fontsize=14, fontweight='bold', ha='center', va='top')
axes[1].annotate('↑', xy=(0.97, 0.93), xycoords='axes fraction',
                fontsize=18, ha='center', va='top')

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "zhaoqing_slope_classification.png"), dpi=200, bbox_inches='tight')
plt.close()

print("Slope classification figure (with Chinese labels) saved!")

# ============================================================
# Generate combined analysis figure with Chinese labels
# ============================================================
print("Generating combined analysis figure...")

fig, ax = plt.subplots(1, 1, figsize=(14, 12))

# Plot slope as background - FIXED: origin='lower' makes North UP
colors = ['#8B0000', '#FF4500', '#FFA500', '#90EE90', '#228B22']
cmap_slope = matplotlib.colors.ListedColormap(colors)
valid_mask = slope_classified > 0
masked_slope = np.ma.masked_where(~valid_mask, slope_classified)

im = ax.imshow(masked_slope, cmap=cmap_slope, aspect='auto',
               extent=[zhaoqing_bounds['west'], zhaoqing_bounds['east'],
                       zhaoqing_bounds['south'], zhaoqing_bounds['north']],
               origin='lower', alpha=0.6, vmin=1, vmax=5)

# Overlay roads - use plot with ax parameter
for cls in roads['road_class'].unique():
    subset = roads[roads['road_class'] == cls]
    lw = 2.5 if cls == 'Expressway' else 1.5
    subset.plot(ax=ax, color=road_colors.get(cls, '#999999'),
                linewidth=lw, alpha=0.9, label=cls)

ax.set_xlim(zhaoqing_bounds['west'], zhaoqing_bounds['east'])
ax.set_ylim(zhaoqing_bounds['south'], zhaoqing_bounds['north'])
ax.set_xlabel('经度 (°E)', fontsize=13)
ax.set_ylabel('纬度 (°N)', fontsize=13)
ax.set_title('肇庆市端州区综合分析\n道路网 + 坡度适宜性评价', fontsize=15, fontweight='bold')
ax.legend(loc='upper right', fontsize=10, ncol=2, title='道路类型')
ax.grid(True, alpha=0.2, linestyle='--')
ax.set_aspect('equal')

# Add N arrow
ax.annotate('N', xy=(0.97, 0.97), xycoords='axes fraction',
           fontsize=14, fontweight='bold', ha='center', va='top')
ax.annotate('↑', xy=(0.97, 0.93), xycoords='axes fraction',
           fontsize=18, ha='center', va='top')

# Add colorbar
cbar = plt.colorbar(im, ax=ax, shrink=0.7, ticks=[1, 2, 3, 4, 5])
cbar.ax.set_yticklabels(['>25° 不适宜', '15-25°', '8-15°', '3-8°', '0-3° 最适宜'])
cbar.set_label('坡度适宜性等级', fontsize=12)

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "zhaoqing_combined_analysis.png"), dpi=200, bbox_inches='tight')
plt.close()

print("Combined analysis figure (with Chinese labels) saved!")
print("\nAll publication-quality figures generated successfully!")
