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
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib
import geopandas
import random
import folium
import contextily as cx
import webbrowser
# ------------------------------------------------------------------------------

def read_in_shapefile(data_dict=None):
    """
    Definition
    ----------
    def read_in_shapefile(data_dict=None)

    Input       Format      Description
    -----       ------      -----------
    data_dict   dict        Dictionary with key:value pairs of shapefile name
                            and path to shapefile
    Output
    ------
    None

    Returns      Format      Description
    ------      ------      -----------
    shp_gdfs    dict        Dictionary with key:value pairs of path to
                            shapefile name and GeoDataFrame of the shapefile

    """
    shp_gdfs = dict()

    for shp in data_dict:
        gdf = geopandas.read_file(data_dict[shp])
        # gdf.to_crs(crs=4326)
        gdf["area"] = gdf.area
        shp_gdfs[shp] = gdf

    return shp_gdfs

def get_colours(n):
    """
    Description
    -----------
    get_colours(n) generates a list of n hex colours.

    Input       Format      Description
    -----       ------      -----------
    n           int         Number of colours to generate

    Output
    ------
    None

    Returns     Format      Description
    -------     ------      -----------
    colours     list        List of hex colours

    """
    colours = []
    for i in range(n):
        colours.append('#%06X' % random.randint(0, 0xFFFFFF))
    return colours

def plot_shp(shapefiles=None, plot=None):
    """
    Definition
    ----------
    def plot_shp(shapefile=None) plots the

    Input       Format      Description
    -----       ------      -----------
    shapefiles  dict        Dictionary with key:value pairs of path to
                            shapefile name and GeoDataFrame of the shapefile

    plot        string      String specifying the output format of the
                            plotted shapefile.
                            Allowed strings: 'png', 'webmap', 'pdf', 'jpg'

    Output
    ------
    file of the plot (.html/.jpg/.pdf/.png/ file)

    Returns
    ------
    None

    """
    n = len(shapefiles)
    # Generate list of colours
    colours = get_colours(n)

    # Plot map
    if plot in ['png', 'pdf', 'jpg']:
        # Create side-by-side plot
        # fig, axs = plt.subplots(1, n, figsize=(25, 25))
        # n -= 1
        # axs = axs.flatten()

        # Create single plot
        fig, ax = plt.subplots()
        layers = []

        # Add each shapefile as layer
        for gdf in shapefiles:
            # Pick layer colour
            colour = random.choice(colours)
            colours.remove(colour)
            shapefiles[gdf].boundary.plot(ax=ax, color=colour)

            # shapefiles[gdf].plot(ax=axs[n], color=colour)
            # cx.add_basemap(axs[n], crs=crs)

            layer = matplotlib.patches.Patch(color=colour, label=gdf)
            layers.append(layer)
            # n -= 1

        print("add basemap")
        crs = list(shapefiles.values())[0].crs
        cx.add_basemap(ax, crs=crs)
        print("basemap added")

        # Add legend
        ax.legend(title="Legend", handles=layers, fancybox=False,
                  framealpha=0.45, loc="upper right", fontsize='10')

        # Save plots
        if plot == 'jpg':
            plt.savefig('Figure.jpg')

        elif plot == 'png':
            plt.savefig('Figure.png')

        else:
            plt.savefig('Figure.pdf')
        # plt.show()

    # Plot web map
    elif plot == 'webmap':
        # Create webmap
        m = None

        for gdf in shapefiles:
            # Pick layer colour
            colour = random.choice(colours)
            colours.remove(colour)

            m = shapefiles[gdf].explore(column="area", m=m, name=gdf,
                                        style_kwds={'color': colour,
                                                    'fillColor': colour},
                                        legend=False)

        # Add layer control
        folium.LayerControl().add_to(m)

        # Save map
        m.save('base_map.html')
        # webbrowser.open(webmap_file)

    else:
        print("Invalid output format. Please select from:")
        print("jpg, pdf, png, webmap")
        return



def main():
    # Gather arguments
    shpfolder_path = sys.argv[1]  # path to directory holding all shapefiles
    plot = sys.argv[2]  # type of plot to make

    # Verify paths exist
    if not os.path.isdir(shpfolder_path):
        print("Invalid directory")
        exit(1)

    # Gather all shapefiles in directory - ENSURE THEY ALL HAVE THE SAME CRS
    shape_paths = dict()
    for path in Path(shpfolder_path).rglob('*.shp'):
        shape_paths[path.name[:-4]] = path.parent

    if shape_paths == {}:
        print("No shapefiles found")
        return

    # Run functions
    shape_gdfs = read_in_shapefile(data_dict=shape_paths)
    plot_shp(shapefiles=shape_gdfs, plot=plot)

    print("Map Plotted!")

if __name__ == "__main__":
    main()