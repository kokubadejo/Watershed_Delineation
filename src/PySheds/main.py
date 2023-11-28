# ------------------------------------------------------------------------------
# MIT License
# ------------------------------------------------------------------------------
# Copyright (c) 2023 Kasopefoluwa Okubadejo
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ---

#-------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------
from pysheds.grid import Grid
import numpy as np
import fiona
import pandas as pd
import geopandas as gpd
import os
from area import area

#-------------------------------------------------------------------------------
# Constants
#-------------------------------------------------------------------------------
# dem = "data/n40w090_dem.tif"
FLDIR = os.path.join("data", "Rasters", "hyd_na_dir_15s.tif")
FLACC = os.path.join("data", "Rasters", "hyd_na_acc_15s.tif")

#-------------------------------------------------------------------------------
# Calculate Watershed Area
#-------------------------------------------------------------------------------
def calculate_area(shape=None):
    # print("my shape")
    # print(shape)
    # format of shape => {'type': 'Polygon', 'coordinates': [[[x, y], [x, y] ...]]}
    area_km2 = area(shape) / 1e+6
    return round(area_km2, 2)


#-------------------------------------------------------------------------------
# Delineate Watershed
#-------------------------------------------------------------------------------
def delineate(fldir_file=FLDIR, flacc_file=FLACC, output_dir="output", output_fname='watersheds', basins=None, id_field="id"):
    """
    Description
    -----------
    delineate(dem, output_dir, basins) delineates watersheds

    Input           Format          Description
    -----           ------          -----------
    fldir_file      str             The path to the flow direction raster
    flacc_file      str             The path to the flow accumulation raster
    output_dir      str             The path to the output folder
    output_fname    str             The path to the output file
    basins          DataFrame       Pour point DataFrame or GeoDataFrame..
    id_field        str             Station ID field name.

    Output          Format          Description
    ------          ------          -----------
    watersheds      Shapefiles      The watershed shapefiles delineated

    Returns
    -------
    None

    """
    # # Read elevation raster
    # # ----------------------------
    # print("Read elevation raster")
    # grid = Grid.from_raster(dem, nodata=-9999)
    # dem = grid.read_raster(dem, nodata=grid.nodata)
    #
    # # Condition DEM
    # # ----------------------
    # # Fill pits in DEM
    # print("Filling pits")
    # dem = grid.fill_pits(dem)
    #
    # # Fill depressions in DEM
    # print("Filling depressions")
    # dem = grid.fill_depressions(dem)
    #
    # # Resolve flats in DEM
    # print("Resolving flats")
    # dem = grid.resolve_flats(dem)
    #
    # # Crosschecking
    # print("Asserting filled sinks")
    # # assert not grid.detect_pits(dem).any()
    # # assert not grid.detect_depressions(dem).any()
    # # assert not grid.detect_flats(dem).any()
    #
    # # Determine D8 flow directions from DEM
    # # ----------------------
    # # Specify directional mapping
    #
    # # print("Specify directional mapping")
    # # dirmap = (64, 128, 1, 2, 4, 8, 16, 32)
    #
    # # Cardinal and intercardinal directions are represented by numeric values in
    # # the output grid. By default, the ESRI scheme is used:
    #         # North: 64
    #         # Northeast: 128
    #         # East: 1
    #         # Southeast: 2
    #         # South: 4
    #         # Southwest: 8
    #         # West: 16
    #         # Northwest: 32

    # Compute flow directions
    # -------------------------------------
    print("Compute flow directions")
    # fdir = grid.flowdir(dem)
    grid = Grid.from_raster(fldir_file)
    fdir = grid.read_raster(fldir_file)

    # Calculate flow accumulation
    # --------------------------
    print("Calculate flow accumulation")
    # acc = grid.accumulation(fdir)
    acc = grid.read_raster(flacc_file)
    # Delineate a catchment
    # ---------------------
    # Specify pour point
    print("Specify pour point")
    
    if type(basins) is pd.DataFrame:
        lats = basins['lat'].tolist()
        lons = basins['lng'].tolist()
        st_ids = basins[id_field].tolist()
    elif type(basins) is gpd.GeoDataFrame:
        lats = basins.geometry.y.tolist()
        lons = basins.geometry.x.tolist()
        st_ids = basins[id_field].tolist()
    # x, y = -80.15, 43.09
    
    watersheds = []

    for index in range(0, len(lats)):
        x = lons[index]
        y = lats[index]
        st_id = st_ids[index]

        # Snap pour point to high accumulation cell
        x_snap, y_snap = grid.snap_to_mask(acc > 9000, (x, y))

        # Delineate the catchment
        print("Delineate the catchment")
        catch = grid.catchment(x=x_snap, y=y_snap, fdir=fdir, xytype='coordinate')
        # catch_view = grid.view(catch, dtype=np.uint8)

        watershed = grid.polygonize(data=catch, nodata=grid.nodata)
        
        for shape, value in watershed:
            if value == 0:
                continue
            watersheds.append((shape, value, st_id, x, y))

    print("Writing to shapefile")
    # Specify schema
    schema = {'geometry': 'Polygon', 'properties': {'LABEL': 'float:16', id_field: 'str',
                                                    'lat': 'float', 'lng': 'float',
                                                    'area': 'float'}}

    # Write shapefile
    with fiona.open(output_fname + ".geojson", 'w',
                    driver='GeoJSON',
                    crs=grid.crs.srs,
                    schema=schema) as c:
        i = 0
        for shape, value, st_id, x, y in watersheds:
            calc_area = calculate_area(shape)
            rec = {}
            rec['geometry'] = shape
            rec['properties'] = {'LABEL': str(value), id_field: st_id, 'lat': y, 'lng': x, 'area': calc_area}
            rec['id'] = str(i)
            c.write(rec)
            i += 1


#-------------------------------------------------------------------------------
# Run Program
#-------------------------------------------------------------------------------
def main():
    input_dir = "data"
    output_dir = "output"
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    # basins = pd.read_csv(f"{input_dir}/basins.csv")  # path to csv of pour points
    basins = pd.read_csv(f"{input_dir}/watersheds.csv")

    fname = "watershed_points"       # CHANGE ME!!!
    output_fname = os.path.join(output_dir, fname)
    delineate(fldir_file=FLDIR, flacc_file=FLACC, output_dir=output_dir, output_fname=output_fname,
              basins=basins)

if __name__ == "__main__":
    main()
