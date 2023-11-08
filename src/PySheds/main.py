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
# import numpy as np
import fiona
import pandas as pd
import geopandas as gpd
import os

#-------------------------------------------------------------------------------
# Delineate Watershed
#-------------------------------------------------------------------------------
def delineate(dem='', output_dir="output", basins=None, id_field="id"):
    """
    Description
    -----------
    delineate(dem, output_dir, basins) delineates watersheds

    Input           Format          Description
    -----           ------          -----------
    dem             str             The path to the dem
    output_dir      str             The path to the output folder
    basins          DataFrame       Pour point DataFrame or GeoDataFrame..
    id_field        str             Station ID field name.

    Output          Format          Description
    ------          ------          -----------
    watersheds      Shapefiles      The watershed shapefiles delineated

    Returns
    -------
    None

    """
    # Read elevation raster
    # ----------------------------
    print("Read elevation raster")
    grid = Grid.from_raster(dem, nodata=-9999)
    dem = grid.read_raster(dem, nodata=grid.nodata)

    # Condition DEM
    # ----------------------
    # Fill pits in DEM
    print("Filling pits")
    dem = grid.fill_pits(dem)

    # Fill depressions in DEM
    print("Filling depressions")
    dem = grid.fill_depressions(dem)

    # Resolve flats in DEM
    print("Resolving flats")
    dem = grid.resolve_flats(dem)

    # Crosschecking
    print("Asserting filled sinks")
    assert not grid.detect_pits(dem).any()
    assert not grid.detect_depressions(dem).any()
    assert not grid.detect_flats(dem).any()

    # Determine D8 flow directions from DEM
    # ----------------------
    # Specify directional mapping

    # print("Specify directional mapping")
    # dirmap = (64, 128, 1, 2, 4, 8, 16, 32)

    # Cardinal and intercardinal directions are represented by numeric values in
    # the output grid. By default, the ESRI scheme is used:
            # North: 64
            # Northeast: 128
            # East: 1
            # Southeast: 2
            # South: 4
            # Southwest: 8
            # West: 16
            # Northwest: 32

    # Compute flow directions
    # -------------------------------------
    print("Compute flow directions")
    fdir = grid.flowdir(dem)

    # Calculate flow accumulation
    # --------------------------
    print("Calculate flow accumulation")
    acc = grid.accumulation(fdir)

    # Delineate a catchment
    # ---------------------
    # Specify pour point
    print("Specify pour point")
    
    if type(basins) is pd.DataFrame:
        lats = basins['lat'].tolist()
        lons = basins['lon'].tolist()
        ids = basins['id'].tolist()
    elif type(basins) is gpd.GeoDataFrame:
        lats = basins.geometry.y.tolist()
        lons = basins.geometry.x.tolist()
        ids = basins[id_field].tolist()
    # x, y = -80.15, 43.09
    
    watersheds = []

    for index in range(0, len(lats)):
        x = lons[index]
        y = lats[index]
        id = ids[index]
        
        print("lon: {} lat: {} id: {}".format(x, y, id))
        basin_dir = "{}/{}".format(output_dir, id)
        if not os.path.isdir(basin_dir):
            os.mkdir(basin_dir)

        # Snap pour point to high accumulation cell
        x_snap, y_snap = grid.snap_to_mask(acc > 9000, (x, y))

        # Delineate the catchment
        print("Delineate the catchment")
        catch = grid.catchment(x=x_snap, y=y_snap, fdir=fdir, xytype='coordinate')

        # Crop and plot the catchment
        # ---------------------------
        # Clip the bounding box to the catchment
        print("Clip bounding box to catchment")
        grid.clip_to(catch)

        print("Polygonizing watershed")
        for shape, value in grid.polygonize(nodata=grid.nodata):
            watersheds.append((shape, value))

    print("Writing to shapefile")
    # Specify schema
    schema = {'geometry': 'Polygon', 'properties': {'LABEL': 'float:16'}}

    # Write shapefile
    with fiona.open(f'{output_dir}\watersheds.shp', 'w',
                    driver='ESRI Shapefile',
                    crs=grid.crs.srs,
                    schema=schema) as c:
        i = 0
        for shape, value in watersheds:
            rec = {}
            rec['geometry'] = shape
            rec['properties'] = {'LABEL' : str(value)}
            rec['id'] = str(i)
            c.write(rec)
            i += 1


#-------------------------------------------------------------------------------
# Run Program
#-------------------------------------------------------------------------------
def main():
    input = "data"
    output = "output"
    if not os.path.isdir(output):
        os.mkdir(output)

    basins = pd.read_csv("{}/basins.csv".format(input))  # path to csv of pour points
    dem = "data/n40w090_dem.tif"
    delineate(dem, output, basins)

if __name__ == "__main__":
    main()