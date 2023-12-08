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
import os
os.environ['USE_PYGEOS'] = '0'
import pandas as pd
from shapely.geometry import Polygon
from shapely.ops import unary_union
from area import area

#-------------------------------------------------------------------------------
# Constants
#-------------------------------------------------------------------------------
# dem = "data/n40w090_dem.tif"
FLDIR = os.path.join(os.path.dirname(__file__), "data", "Rasters", "hyd_na_dir_15s.tif")
FLACC = os.path.join(os.path.dirname(__file__), "data", "Rasters", "hyd_na_acc_15s.tif")

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
# Calculate Bounding Box
#-------------------------------------------------------------------------------
def calculate_bbox(lat, lng, radius):
    lat_dist = 0.00902
    lng_dist = 0.00898
    minx = lng - (radius * lng_dist)
    miny = lat - (radius * lat_dist)
    maxx = lng + (radius * lng_dist)
    maxy = lat + (radius * lat_dist)
    
    return (minx, miny, maxx, maxy)


#-------------------------------------------------------------------------------
# Delineate Watershed
#-------------------------------------------------------------------------------
def delineate(fldir_file=FLDIR, flacc_file=FLACC, output_dir="output", output_fname='', basins=None, id_field="id"):
    """
    Description
    -----------
    delineate(dem, output_dir, basins) delineates watersheds

    Input           Format          Description
    -----           ------          -----------
    fldir_file      str             The path to the flow direction raster
    flacc_file      str             The path to the flow accumulation raster
    output_dir      str             The path to the output folder
    output_fname    str             The name of the output file
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

    
    # Delineate a catchment
    # ---------------------
    # Specify pour point
    print("Specify pour point")    
    lats = basins['lat'].tolist()
    lons = basins['lng'].tolist()
    st_ids = basins[id_field].tolist()
    # watersheds = []

    for index in range(0, len(lats)):
        x = lons[index]
        y = lats[index]
        st_id = st_ids[index]
        
        # Calculate flow accumulation
        # --------------------------
        print("Calculate flow accumulation")
        # acc = grid.accumulation(fdir)
        bbox = calculate_bbox(y, x, 5)
        acc = grid.read_raster(flacc_file, window=bbox, window_crs=grid.crs)

        # Snap pour point to high accumulation cell
        print("Snapping pour point")
        x_snap, y_snap = grid.snap_to_mask(acc > 1000, (x, y))

        # Delineate the catchment
        print("Delineate the catchment")
        catch = grid.catchment(x=x_snap, y=y_snap, fdir=fdir, xytype='coordinate')
        # catch_view = grid.view(catch, dtype=np.uint8)

        watershed = grid.polygonize(data=catch, nodata=grid.nodata)
        watershed_dict = {st_id: []}
        
        # Merging Multi-Part Watersheds
        print("Merging Multi-Part Watersheds")
        for shape, val in watershed:
            if val != 0:
                shp = Polygon(shape['coordinates'][0]).buffer(0.0001)
                watershed_dict[st_id].append(shp)
        
        merged = Polygon(unary_union(watershed_dict[st_id]).buffer(-0.0001))
        new_shape = {'type': 'Polygon', 'coordinates': [tuple(merged.exterior.coords)]}

        print("Writing to shapefile")
        file = f"{output_dir}/{output_fname}{st_id}.geojson"
        # Specify schema
        schema = {'geometry': 'Polygon', 'properties': {'LABEL': 'float:16', id_field: 'str',
                                                        'lat': 'float', 'lng': 'float',
                                                        'area': 'float'}}
        if not (os.path.exists(file) and os.path.isfile(file)):
            # Write shapefile
            with fiona.open(file, 'w',
                            driver='GeoJSON',
                            crs=grid.crs.srs,
                            schema=schema) as c:
                i = 0
                calc_area = calculate_area(new_shape)
                rec = {}
                rec['geometry'] = new_shape
                rec['properties'] = {'LABEL': str(val), id_field: st_id, 'lat': y, 'lng': x, 'area': calc_area}
                rec['id'] = str(i)
                c.write(rec)
                i += 1
                    
                # for shape, value in watershed:
                #     print("value")
                #     print(value)
                #     if value == 0:
                #         continue
                #     shape['coordinates'][0] = shp
                #     calc_area = calculate_area(shape)
                #     rec = {}
                #     rec['geometry'] = shape
                #     rec['properties'] = {'LABEL': str(value), id_field: st_id, 'lat': y, 'lng': x, 'area': calc_area}
                #     rec['id'] = str(i)
                #     c.write(rec)
                #     i += 1
                #     print("check it")
                #     print(st_id, shape)


#-------------------------------------------------------------------------------
# Run Program
#-------------------------------------------------------------------------------
def main():
    input_dir = "data"
    output_dir = "output"
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    # basins = pd.read_csv(f"{input_dir}/basins.csv")  # path to csv of pour points
    basins = pd.read_csv(f"{input_dir}/basins_random.csv")
    delineate(output_dir=output_dir, basins=basins)

if __name__ == "__main__":
    main()