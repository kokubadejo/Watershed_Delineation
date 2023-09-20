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
# ------------------------------------------------------------------------------

# Imports
# ------------------------------------------------------------------------------
import os
import sys

import matplotlib.pyplot as plt
import geopandas
import webbrowser
# ------------------------------------------------------------------------------

def read_in_shapefile(shp_path=None, shp_name=None):
    """
    Definition
    ----------
    def read_in_shapefile(file_path=None)

    Input       Format      Description
    -----       ------      -----------
    shp_path    string      The path to the shapefile
    shp_name    string      The name of the shapefile

    Output      Format      Description
    ------      ------      -----------
    shp_gdf     gdf         GeoDataFrame of the shapefile

    """
    # get shapefile path
    # shp_path = input("Enter path to shapefile: ")

    # while (not os.path.isdir(shp_path)):
    #     print("No such path exists")
    #     shp_path = input("Enter path to shapefile: ")

    if not os.path.isdir(shp_path):
        print("Invalid file path. Shapefile not read")
        return

    # read in shapefile
    shp_gdf = geopandas.read_file(shp_path)
    shp_gdf["area"] = shp_gdf.area
    return shp_gdf

def plot_shp(shapefile=None, plot=None, filename=None):
    """
    Definition
    ----------
    def plot_shp(shapefile=None) plots the

    Input       Format      Description
    -----       ------      -----------
    shp_gdf     gdf         GeoDataFrame of the shapefile
    plot        string      string specifying the output format of the
                            plotted shapefile.
                            Allowed strings: 'png', 'webmap', 'pdf', 'jpg'
    filename    string      The name of the shapefile

    """

    # Note for future update:
        # to plot multiple layers:
        # fig = gdf1.plot()
        # gdf2.plot(ax=fig)

    # plot map
    if plot in ['png', 'pdf', 'jpg']:
        fig = shapefile.plot("area", legend=True)  # plain background
        # plt.show()
        if plot == 'jpg':
            plt.savefig(filename + '.jpg')
        elif plot == 'png':
            plt.savefig(filename + '.png')
        else:
            plt.savefig(filename + '.pdf')

    # plot web map
    elif plot == 'webmap':
        webmap = shapefile.explore("area", legend=True)  # interactive map
        # webmap_file = os.getcwd() + r"\{filename}.html".format(shapefile_name=filename)
        webmap.save(filename + '.html')
        # webbrowser.open(webmap_file)

    else:
        print("Invalid output format. Please select from:")
        print("jpg, pdf, png, webmap")
        return

    print("Map Plotted!")

def main():


    print("Map Plotted!")

if __name__ == "__main__":
    # Gather arguments
    shp_path = sys.argv[1]
    shp_name = sys.argv[2]
    plot = sys.argv[3]

    # Run functions
    shpfile = read_in_shapefile(shp_path=shp_path, shp_name=shp_name)
    plot_shp(shapefile=shpfile, plot=plot, filename=shp_name)
