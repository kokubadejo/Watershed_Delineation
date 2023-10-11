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
import os
import time
import rabpro
import pandas as pd
import geopandas as gpd

# PLEASE NOTE: Downloading HydroBasin & Merit data only needs to be done once

def delineate(coords=None, name='', method='hydrobasins'):
    """
        Definition
        ----------
        def delineate(coords, name, method) delineates watersheds according to the method specified

        Input       Format      Description
        -----       ------      -----------
        coords      pair        Pair of x,y coordinates
        name        string      The name of the watershed
        method      string      Source data for delineating watershed
                                one of:
                                - MERIT
                                - HydroBasins

        Output
        ------
        shapefile and json of the watersheds

        Returns
        ------
        None

        """
    if method == 'hydrobasins':
        # HydroBasins
        # from rabpro import data_utils
        # data_utils.download_hydrobasins()
        rpo = rabpro.profiler(coords, name=name)
    elif method == 'merit':
        rpo = rabpro.profiler(coords, name=name, da=500)        # play around with the da
        # MERIT
        datapaths = rabpro.utils.get_datapaths()
        from rabpro import data_utils
        merit_tile = rabpro.utils.coords_to_merit_tile(coords[1], coords[0])
        print(merit_tile, datapaths)
        username = '*****'      # enter username
        password = '*****'      # enter password

        merit_file = merit_tile
        if coords[1] < 100:
            merit_file = merit_tile[:4] + '0' + merit_tile[4:]
        elevation_file = os.path.join(datapaths['MERIT_root'], 'MERIT_ELEV_HP/{'
                                                               '}_elv.tif'.format(merit_file))
        if not os.path.isfile(elevation_file):
            print("Downloading MERIT data")
            data_utils.download_merit_hydro(merit_tile, username, password) # Can also add proxy argument.

        if os.path.isfile(datapaths['DEM_fdr']) is True:
            print('Flow directions virtual raster was built.')
        if os.path.isfile(datapaths['DEM_uda']) is True:
            print('Drainage area virtual raster was built.')
        if os.path.isfile(datapaths['DEM_elev_hp']) is True:
            print('Elevations virtual raster was built.')
        if os.path.isfile(datapaths['DEM_width']) is True:
            print('Width virtual raster was built.')

    else:
        print("Invalid method. Pick one of 'merit' or 'hydrobasins'")
        exit(1)

    rpo.delineate_basin(force_merit=True)
    rpo.export("watershed")


def main():
    t1_start = time.perf_counter()

    basins = pd.read_csv("data/basins_salmon.csv")  # path to csv of pour points
    # Specify pour point
    print("Specify pour point")
    lats = basins['lat'].tolist()
    lons = basins['lon'].tolist()
    ids = basins['id'].tolist()
    # method = input("Pick a method (merit/hydrobasins): ")
    method = 'merit'        ## Edit this to your method

    # Delineate each pour point
    for index in range(0, len(lats)):
        x = lons[index]
        y = lats[index]
        id = ids[index]
        coords = (y, x)
        print("lon: {} lat: {} id: {}".format(x, y, id))

        # Delineating Watersheds
        delineate(coords=coords, name=id, method=method)

        # Making Shapefile
        gdf = gpd.read_file(os.path.join(os.getcwd(), 'results\\{}\\watershed.json'.format(id)))
        gdf.to_file(os.path.join(os.getcwd(), 'results\\{}\\{}.shp'.format(id, id)))

    t1_stop = time.perf_counter()
    print("Elapsed time:", t1_stop, t1_start)
    print("Elapsed time during the whole program in seconds:", t1_stop - t1_start)

if __name__ == "__main__":
    main()