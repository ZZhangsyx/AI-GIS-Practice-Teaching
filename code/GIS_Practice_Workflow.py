# -*- coding: utf-8 -*-
"""
肇庆市端州区GIS实践分析工作流
Zhaoqing Duanzhou District GIS Practice Workflow

This script demonstrates AI-assisted GIS practice teaching workflow.
It includes:
1. Road network data acquisition from OpenStreetMap (via osmnx)
2. DEM slope analysis (using SRTM 90m data)
3. Visualization and combined analysis

Dependencies:
    pip install osmnx geopandas rasterio numpy scipy matplotlib

Data Sources:
    - Road Network: OpenStreetMap (https://www.openstreetmap.org/)
    - DEM: SRTM 90m (https://srtm.csi.cgiar.org/)

Author: Claude Code
Date: 2026-04-15
"""

import os
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# Output directory
OUTPUT_DIR = r"../results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Study area bounds: Zhaoqing Duanzhou District
NORTH, SOUTH = 23.25, 22.95
EAST, WEST = 112.70, 112.35

print("=" * 60)
print("Zhaoqing Duanzhou District GIS Analysis Workflow")
print("=" * 60)


# =============================================================================
# Part 1: Road Network Data Acquisition from OSM
# =============================================================================
def download_road_network():
    """Download road network from OpenStreetMap using osmnx."""
    import osmnx as ox

    ox.settings.timeout = 180
    ox.settings.use_cache = True

    from shapely.geometry import Polygon

    print("\n[Step 2] Downloading road network from OSM...")
    print(f"  Study area: N={NORTH}, S={SOUTH}, E={EAST}, W={WEST}")

    bbox_coords = [(WEST, NORTH), (EAST, NORTH), (EAST, SOUTH), (WEST, SOUTH), (WEST, NORTH)]
    study_area = Polygon(bbox_coords)

    print("  Downloading OSM road data...")
    G = ox.graph_from_polygon(study_area, network_type='drive', simplify=True, retain_all=False)
    nodes, edges = ox.graph_to_gdfs(G, nodes=True, edges=True, fill_edge_geometry=True)

    print(f"  [SUCCESS] Road network downloaded!")
    print(f"    Nodes: {len(nodes)}")
    print(f"    Edges: {len(edges)}")

    # Road classification function
    def classify_road(hw):
        if hw is None:
            return 'Unknown'
        if isinstance(hw, (list, tuple)):
            hw_str = str(hw[0]) if len(hw) > 0 else 'unknown'
        else:
            hw_str = str(hw)
        hw_lower = hw_str.lower()
        if any(x in hw_lower for x in ['motorway', 'trunk']):
            return 'Expressway'
        elif 'primary' in hw_lower:
            return 'Primary'
        elif 'secondary' in hw_lower:
            return 'Secondary'
        elif 'tertiary' in hw_lower:
            return 'Tertiary'
        elif any(x in hw_lower for x in ['residential', 'service', 'living']):
            return 'Local'
        else:
            return 'Other'

    edges['road_class'] = edges['highway'].apply(classify_road)
    road_stats = edges['road_class'].value_counts()

    print("\n  Road class statistics:")
    for cls, count in road_stats.items():
        print(f"    - {cls}: {count}")

    # Save road network
    road_file = os.path.join(OUTPUT_DIR, "zhaoqing_road_network.gpkg")
    edges.to_file(road_file, driver="GPKG", encoding="utf-8")
    print(f"\n  [SAVED] Road network: {road_file}")

    return nodes, edges, road_stats


def plot_road_network(edges):
    """Generate road network visualization."""
    fig, ax = plt.subplots(1, 1, figsize=(12, 10))

    color_map = {
        'Expressway': '#FF4444',
        'Primary': '#FF8800',
        'Secondary': '#FFCC00',
        'Tertiary': '#88CC00',
        'Local': '#00AAFF',
        'Other': '#AAAAAA'
    }

    for cls in edges['road_class'].unique():
        subset = edges[edges['road_class'] == cls]
        color = color_map.get(cls, '#AAAAAA')
        subset.plot(ax=ax, color=color, linewidth=1.5, alpha=0.7, label=cls)

    ax.set_title("Zhaoqing Duanzhou District Road Network\n(Data: OpenStreetMap)", fontsize=14)
    ax.set_xlabel("Longitude (E)")
    ax.set_ylabel("Latitude (N)")
    ax.legend(loc='upper right', fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.annotate('N', xy=(0.95, 0.95), xycoords='axes fraction', fontsize=14, fontweight='bold', ha='center')
    ax.annotate('^', xy=(0.95, 0.90), xycoords='axes fraction', fontsize=16, ha='center')

    road_map_file = os.path.join(OUTPUT_DIR, "zhaoqing_road_network.png")
    plt.tight_layout()
    plt.savefig(road_map_file, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  [SAVED] Road map: {road_map_file}")


# =============================================================================
# Part 2: DEM Slope Analysis
# =============================================================================
def analyze_slope():
    """Perform slope analysis using SRTM DEM data."""
    import rasterio

    zhaoqing_bounds = {'north': NORTH, 'south': SOUTH, 'east': EAST, 'west': WEST}
    srtm_dir = r"../data"
    srtm_tile = "srtm_59_08.tif"

    print("\n[Step 3] SRTM DEM Slope Analysis...")
    print(f"  SRTM tile: {srtm_tile}")

    tile_path = os.path.join(srtm_dir, srtm_tile)
    if not os.path.exists(tile_path):
        print(f"  [ERROR] SRTM tile not found: {tile_path}")
        return None, None, None

    with rasterio.open(tile_path) as src:
        dem_data = src.read(1)
        dem_meta = src.meta.copy()
        bounds = src.bounds
        nodata_val = src.nodata

        print(f"  DEM shape: {dem_data.shape}")
        print(f"  Bounds: {bounds}")
        print(f"  NoData value: {nodata_val}")

        pixel_size_lon = (bounds.right - bounds.left) / dem_data.shape[1]
        pixel_size_lat = (bounds.top - bounds.bottom) / dem_data.shape[0]

        col_start = int((zhaoqing_bounds['west'] - bounds.left) / pixel_size_lon)
        col_end = int((zhaoqing_bounds['east'] - bounds.left) / pixel_size_lon)
        row_start = int((bounds.top - zhaoqing_bounds['north']) / pixel_size_lat)
        row_end = int((bounds.top - zhaoqing_bounds['south']) / pixel_size_lat)

        col_start = max(0, col_start)
        col_end = min(dem_data.shape[1], col_end)
        row_start = max(0, row_start)
        row_end = min(dem_data.shape[0], row_end)

        print(f"  Crop: rows {row_start}-{row_end}, cols {col_start}-{col_end}")

        dem_raw = dem_data[row_start:row_end, col_start:col_end].astype(np.float64)

        valid_mask = (dem_raw > 0) & (dem_raw != nodata_val)
        total_valid_cells = np.sum(valid_mask)
        print(f"  Valid pixels: {total_valid_cells} ({total_valid_cells/dem_raw.size*100:.1f}%)")

        valid_elev = dem_raw[valid_mask]
        print(f"  Elevation: {valid_elev.min():.1f}m - {valid_elev.max():.1f}m (mean: {valid_elev.mean():.1f}m)")

        # Calculate slope using finite difference
        slope_deg = np.zeros_like(dem_raw)
        dem_padded = np.pad(dem_raw, 1, mode='edge')
        valid_pad = np.pad(valid_mask, 1, mode='constant', constant_values=False)

        for i in range(1, dem_raw.shape[0] + 1):
            for j in range(1, dem_raw.shape[1] + 1):
                if not valid_mask[i-1, j-1]:
                    slope_deg[i-1, j-1] = -999
                    continue

                neighbors_valid = (
                    valid_pad[i-1, j-1] and valid_pad[i-1, j] and valid_pad[i-1, j+1] and
                    valid_pad[i, j-1] and valid_pad[i, j+1] and
                    valid_pad[i+1, j-1] and valid_pad[i+1, j] and valid_pad[i+1, j+1]
                )

                if neighbors_valid:
                    dz_dy = (dem_padded[i+1, j] - dem_padded[i-1, j]) / (2 * pixel_size_lat)
                    dz_dx = (dem_padded[i, j+1] - dem_padded[i, j-1]) / (2 * pixel_size_lon)
                    slope_rad = np.sqrt(dz_dx**2 + dz_dy**2)
                    slope_deg[i-1, j-1] = np.degrees(np.arctan(slope_rad))
                else:
                    slope_deg[i-1, j-1] = -999

        slope_deg = np.clip(slope_deg, 0, 60)
        slope_deg[~valid_mask] = -999

        valid_slope = slope_deg[valid_mask]
        print(f"  Slope: {valid_slope.min():.2f}deg - {valid_slope.max():.2f}deg (mean: {valid_slope.mean():.2f}deg)")

        # Slope classification (5=best, 1=worst)
        slope_classified = np.zeros_like(slope_deg, dtype=np.uint8)
        slope_classified[(slope_deg >= 0) & (slope_deg < 3) & valid_mask] = 5
        slope_classified[(slope_deg >= 3) & (slope_deg < 8) & valid_mask] = 4
        slope_classified[(slope_deg >= 8) & (slope_deg < 15) & valid_mask] = 3
        slope_classified[(slope_deg >= 15) & (slope_deg < 25) & valid_mask] = 2
        slope_classified[(slope_deg >= 25) & valid_mask] = 1

        print("\n  Slope Classification:")
        level_names = [(5, "Level 5 - Best (0-3 deg)"), (4, "Level 4 (3-8)"),
                       (3, "Level 3 (8-15)"), (2, "Level 2 (15-25)"), (1, "Level 1 (>25)")]
        for level_id, label in level_names:
            count = np.sum(slope_classified == level_id)
            pct = count / total_valid_cells * 100 if total_valid_cells > 0 else 0
            print(f"    {label}: {count} pixels ({pct:.1f}%)")

        # Save slope data
        slope_file = os.path.join(OUTPUT_DIR, "zhaoqing_slope_analysis.tif")
        new_transform = rasterio.transform.from_bounds(
            zhaoqing_bounds['west'], zhaoqing_bounds['south'],
            zhaoqing_bounds['east'], zhaoqing_bounds['north'],
            slope_classified.shape[1], slope_classified.shape[0]
        )
        new_meta = dem_meta.copy()
        new_meta.update({
            'transform': new_transform,
            'width': slope_classified.shape[1],
            'height': slope_classified.shape[0],
            'nodata': 0
        })
        with rasterio.open(slope_file, 'w', **new_meta) as dst:
            dst.write(slope_classified, 1)
        print(f"\n  [SAVED] Slope data: {slope_file}")

        return dem_raw, slope_deg, slope_classified, total_valid_cells


def plot_slope_analysis(dem_raw, slope_deg, slope_classified):
    """Generate slope analysis visualization."""
    valid_mask = slope_deg > 0

    fig, axes = plt.subplots(1, 2, figsize=(16, 7))

    masked_elev = np.ma.masked_where(~valid_mask, dem_raw)
    # origin='lower' 使得北(North)在上方，南(South)在下方
    im1 = axes[0].imshow(masked_elev, cmap='terrain', aspect='auto', origin='lower')
    axes[0].set_title("Zhaoqing Duanzhou District - Elevation\n(SRTM 90m DEM)", fontsize=12)
    axes[0].set_xlabel("Column")
    axes[0].set_ylabel("Row")
    plt.colorbar(im1, ax=axes[0], shrink=0.8, label="Elevation (m)")

    colors = ['#8B0000', '#FF4500', '#FFA500', '#90EE90', '#228B22']
    cmap_slope = matplotlib.colors.ListedColormap(colors)
    masked_slope = np.ma.masked_where(slope_classified == 0, slope_classified)
    im2 = axes[1].imshow(masked_slope, cmap=cmap_slope, aspect='auto', vmin=1, vmax=5, origin='lower')
    axes[1].set_title("Zhaoqing Duanzhou District - Slope Suitability\n(Logistics Park Site Selection)", fontsize=12)
    axes[1].set_xlabel("Column")
    axes[1].set_ylabel("Row")
    cbar2 = plt.colorbar(im2, ax=axes[1], shrink=0.8, ticks=[1, 2, 3, 4, 5])
    cbar2.ax.set_yticklabels(['>25 Unsuitable', '15-25', '8-15', '3-8', '0-3 Best'])
    cbar2.set_label("Slope Suitability Level")

    plt.tight_layout()
    slope_fig_file = os.path.join(OUTPUT_DIR, "zhaoqing_slope_classification.png")
    plt.savefig(slope_fig_file, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  [SAVED] Slope figure: {slope_fig_file}")


def plot_combined_analysis(roads, slope_classified):
    """Generate combined visualization."""
    fig, ax = plt.subplots(1, 1, figsize=(14, 12))

    colors = ['#8B0000', '#FF4500', '#FFA500', '#90EE90', '#228B22']
    cmap_slope = matplotlib.colors.ListedColormap(colors)
    masked_slope = np.ma.masked_where(slope_classified == 0, slope_classified)
    im = ax.imshow(masked_slope, cmap=cmap_slope, aspect='auto', alpha=0.7, vmin=1, vmax=5, origin='lower')

    road_colors = {
        'Expressway': '#FFFFFF', 'Primary': '#FFFF00',
        'Secondary': '#00FFFF', 'Tertiary': '#00FF00',
        'Local': '#0066FF', 'Other': '#888888'
    }
    for cls in roads['road_class'].unique():
        subset = roads[roads['road_class'] == cls]
        color = road_colors.get(cls, '#888888')
        linewidth = 2.5 if cls == 'Expressway' else 1.5
        subset.plot(ax=ax, color=color, linewidth=linewidth, alpha=0.9, label=cls)

    ax.set_title("Zhaoqing Duanzhou District - Combined Analysis\nSlope Suitability + Road Network", fontsize=14)
    ax.set_xlabel("Column")
    ax.set_ylabel("Row")
    ax.legend(loc='upper right', fontsize=8, ncol=2)
    cbar = plt.colorbar(im, ax=ax, shrink=0.8, ticks=[1, 2, 3, 4, 5])
    cbar.ax.set_yticklabels(['>25', '15-25', '8-15', '3-8', '0-3'])
    cbar.set_label("Slope Suitability")

    plt.tight_layout()
    combined_file = os.path.join(OUTPUT_DIR, "zhaoqing_combined_analysis.png")
    plt.savefig(combined_file, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  [SAVED] Combined figure: {combined_file}")


def generate_report(nodes, edges, road_stats, dem_raw, slope_deg, slope_classified, total_valid_cells):
    """Generate analysis report."""
    report = f"""
================================================================================
Zhaoqing Duanzhou District GIS Analysis Report
================================================================================

Date: 2026-04-15
Study Area: Zhaoqing Duanzhou District, Guangdong Province
Location: {SOUTH}-{NORTH}N, {WEST}-{EAST}E

[Data Sources]
- Road Network: OpenStreetMap (OSM) via osmnx Python library
- Elevation: SRTM 90m DEM (tile srtm_59_08.tif)

[Road Network Statistics]
- Total Nodes: {len(nodes)}
- Total Edges: {len(edges)}
"""

    if road_stats is not None:
        report += "\nRoad Classification:\n"
        for cls, count in road_stats.items():
            report += f"  - {cls}: {count} segments\n"

    if dem_raw is not None and slope_deg is not None and total_valid_cells is not None:
        valid_mask = slope_classified > 0
        valid_elev = dem_raw[valid_mask]
        valid_slope = slope_deg[valid_mask]

        report += f"""
[Elevation Statistics (Valid Pixels: {total_valid_cells})]
- Minimum: {valid_elev.min():.1f} m
- Maximum: {valid_elev.max():.1f} m
- Mean: {valid_elev.mean():.1f} m

[Slope Analysis]
- Minimum: {valid_slope.min():.2f} deg
- Maximum: {valid_slope.max():.2f} deg
- Mean: {valid_slope.mean():.2f} deg

Slope Classification (Suitability for Logistics Park):
"""
        for level_id, label in [(5, "Level 5 - Most Suitable (0-3 deg)"),
                                   (4, "Level 4 - Suitable (3-8 deg)"),
                                   (3, "Level 3 - Moderate (8-15 deg)"),
                                   (2, "Level 2 - Poor (15-25 deg)"),
                                   (1, "Level 1 - Unsuitable (>25 deg)")]:
            count = np.sum(slope_classified == level_id)
            pct = count / total_valid_cells * 100 if total_valid_cells > 0 else 0
            report += f"  {label}: {count} pixels ({pct:.1f}%)\n"

    report += """
================================================================================
"""
    report_file = os.path.join(OUTPUT_DIR, "analysis_report.txt")
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(report)
    print(f"\n[COMPLETE] Report saved to: {report_file}")


# =============================================================================
# Main Execution
# =============================================================================
if __name__ == "__main__":
    # Part 1: Road Network
    nodes, edges, road_stats = download_road_network()
    plot_road_network(edges)

    # Part 2: Slope Analysis
    dem_raw, slope_deg, slope_classified, total_valid_cells = analyze_slope()

    # Part 3: Visualizations
    if slope_classified is not None:
        plot_slope_analysis(dem_raw, slope_deg, slope_classified)
        plot_combined_analysis(edges, slope_classified)

    # Part 4: Report
    if dem_raw is not None:
        generate_report(nodes, edges, road_stats, dem_raw, slope_deg, slope_classified, total_valid_cells)

    print("\n" + "=" * 60)
    print("Analysis Complete!")
    print(f"Results saved to: {OUTPUT_DIR}")
    print("=" * 60)
