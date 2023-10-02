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
from WhiteboxTools.whitebox_tools import WhiteboxTools

#-------------------------------------------------------------------------------
# Check if all required files are present
#-------------------------------------------------------------------------------
def check_inputs(dem, fldir, pourpoint):
    """
    Description
    -----------
    check_inputs(dem, fldir, pourpoint) determines if the provided inputs are valid

    Input           Format          Description
    -----           ------          -----------
    dem             str             The path to the dem
                                    (can be empty)
    fldir           str             The path to the flow direction raster
                                    (can be empty)
    pourpoint       str             The path to the pourpoint shapefile

    Output
    ------

    Returns         Format          Description
    -------         ------          -----------
    check           bool            True/False result of the verification

    """
    check = False
    if (dem != "" or fldir != "") and (pourpoint != ""):
        check = True

    return check

#-------------------------------------------------------------------------------
# Mosaic Rasters
#-------------------------------------------------------------------------------
def mosaic_rasters(wbt, output_dir):
    """
    Description
    -----------
    mosaic_rasters(wbt, output_dir) mosaicks rasters into one raster

    Input       Format          Description
    -----       ------          -----------
    wbt         WhiteboxTool    A whitebox tool instance
    output_dir   str             The path to the output folder

    Output
    ------
    A new raster file

    Returns     Format          Description
    -------     ------          -----------
    outfile     file (.tif)     A tif file of the mosaicked raster

    """
    outfile = os.path.join(output_dir, "mosaic_rast.tif")
    if wbt.mosaic(
            output=outfile,
            method="nn"
    ) != 0:
        # Non-zero returns indicate an error.
        print('ERROR running mosaic')

    print("Complete!")
    return outfile

#-------------------------------------------------------------------------------
# Delineate Watershed
#-------------------------------------------------------------------------------
def whitebox_delineate(wbt, dem, fldir, pourpoint, output_dir):
    """
    Description
    -----------
    whitebox_delineate(wbt, dem, fldir, pourpoint) delineates a watershed
                                                    specified by the pourpoint

    Input       Format          Description
    -----       ------          -----------
    wbt         WhiteboxTool    A whitebox tool instance
    dem         str             The path to the dem
                                (can be empty)
    fldir       str             The path to the flow direction raster
                                (can be empty)
    pourpoint   str             The path to the pourpoint shapefile
    output_dir   str             The path to the output folder

    Output
    ------
    Creates several files:
    - a filled dem raster
    - a flow direction raster (if one isn't already provided)
    - a flow accumulation raster
    - a snapped pourpoint shapefile
    - a delineated watershed raster and shapefile

    Returns
    -------
    None

    """
    print("Validating input files")
    if not check_inputs(dem, fldir, pourpoint):
        print("Must have a pourpoint point shapefile and one of dem or flow "
              "direction raster!")
        exit(1)

    # Only dem was provided
    if (fldir == "") and (dem != ""):
        # Fill sinks
        print("Filling sinks")
        filled_dem = os.path.join(output_dir, 'filled_dem.tif')

        if not os.path.isfile(filled_dem):
            wbt.breach_depressions_least_cost(dem=dem, output=filled_dem,
                                              dist=1000, fill=True)

        # Create flow direction raster
        print("Creating flow direction raster")
        fldir = os.path.join(output_dir, 'flow_direction.tif')

        if not os.path.isfile(fldir):
            wbt.d8_pointer(dem=filled_dem, output=fldir, esri_pntr=True)

    # Create flow accumulation raster
    print("Creating flow accumulation raster")
    flow_acc = os.path.join(output_dir, 'flow_accumulation.tif')

    if not os.path.isfile(flow_acc):
        wbt.d8_flow_accumulation(i=fldir, output=flow_acc, out_type='cells',
                                 pntr=True, esri_pntr=True)

    # Extract stream cells
    print("Extracting stream cells")
    streams = os.path.join(output_dir, 'streams.tif')

    if not os.path.isfile(streams):
        wbt.extract_streams(flow_accum=flow_acc, output=streams, threshold=9000,
                            zero_background=True)

    # Snap pour points
    print("Snapping pourpoints")
    if not os.path.isdir(os.path.join(output_dir, 'snapped_pourpoint')):
        os.mkdir(os.path.join(output_dir, 'snapped_pourpoint'))     # create folder

    snapped_pourpoint = os.path.join(output_dir,
                                     'snapped_pourpoint/snapped_pourpoint.shp')

    if not os.path.isfile(snapped_pourpoint):
        wbt.jenson_snap_pour_points(pour_pts=pourpoint, streams=streams,
                                    output=snapped_pourpoint, snap_dist=150)

    # Delineate
    print("Delineating watershed")
    watershed_r = os.path.join(output_dir, 'watershed.tif')
    wbt.watershed(d8_pntr=fldir, pour_pts=snapped_pourpoint, output=watershed_r,
                  esri_pntr=True)

    # Polygonize
    print("Polygonizing watershed raster")
    if not os.path.isdir(os.path.join(output_dir, 'watershed')):
        os.mkdir(os.path.join(output_dir, 'watershed'))     # create folder

    watershed_p = os.path.join(output_dir, 'watershed/watershed.shp')
    wbt.raster_to_vector_polygons(i=watershed_r, output=watershed_p)

#-------------------------------------------------------------------------------
# Run Program
#-------------------------------------------------------------------------------
def main():
    # Create WhiteboxTools instance
    wbt = WhiteboxTools()

    # Setup directories
    indir = os.path.join(os.getcwd(), 'data')
    outdir = os.path.join(os.getcwd(), 'output')
    dem = ''
    fldir = ''

    if not os.path.isdir(outdir):
        os.mkdir(outdir)     # create folder

    # Set working directory
    wbt.set_working_dir(indir)

    wbt.set_compress_rasters(True)

    # Suppress messages
    wbt.set_verbose_mode(True)

    ## Mosaicking Rasters
    ##  If you have multiple dem rasters and wish to join them to use,
    ## uncomment one line from this section and comment out the dem & fldir
    ## variables in the Data parameters section.
    ## Note: if using the mosaic, only one type of these rasters must be in
    ## the working directory (exclusively either dem rasters or flow direction
    ## rasters)
    # dem = mosaic_rasters(wbt, outdir)
    # fldir = mosaic_rasters(wbt, outdir)

    # Data parameters
    # PLEASE ADD YOUR DATA
    dem = 'n50w120_dem.tif'        # relative path to dem (if any)
    fldir = ''          # relative path to flow direction raster
    # (if any)
    pourpoint_csv = "basins.csv" # relative path to pourpoint csv file

    # Run function
    print("Converting pour point csv to vector data")

    if not os.path.isdir(os.path.join(indir, 'pourpoint')):
        os.mkdir(os.path.join(indir, 'pourpoint'))     # create folder

    pourpoint = os.path.join(indir, 'pourpoint/pourpoint.shp')
    # 0 = first field, 1 = second field, and so on
    if not os.path.isfile(pourpoint):
        wbt.csv_points_to_vector(i=pourpoint_csv, output=pourpoint, xfield=2,
                                 yfield=1, epsg=4326)

    print("Running delineation function")

    whitebox_delineate(wbt, dem, fldir, pourpoint, outdir)

    print("Your watershed has been delineated")


if __name__ == "__main__":
    main()