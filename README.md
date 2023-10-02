# Watershed_Delineation
Note: DEMs and flow direction rasters can be downloaded from the [HydroSheds products](https://www.hydrosheds.org/hydrosheds-core-downloads)
## General Setup
The following steps describe the process to setup the environments and packages needed to run this script (using anaconda):
1. Install [Anaconda](https://docs.anaconda.com/free/anaconda/install/index.html)
2. Create a conda environment with your preferred python version (I used python 3.9) installed and activate it
   ```
   conda create --name <environment name> python=3.9
   ```
   
   ```
   conda activate <environment name>
   ```

Note: The example figure was gotten from running the script with the grand river watershed shapefiles gotten from manual, ravenpy and the example (Basinmaker?) delineations
![Figure](https://github.com/kokubadejo/Watershed_Delineation/assets/90711306/4a5ebbf9-7019-4281-bf19-4b5d48eee39b)

## Getting Started
### Read_plot_shp.py
Read in and plot a shapefile

```
# load conda environment
conda activate map
```
Install necessary packages
```
# install the geopandas package
conda install -c conda-forge geopandas
# Note: geopandas supports python 3.8+
```

```
# install folium
conda install -c conda-forge folium
```

```
# install matplotlib
conda install -c conda-forge matplotlib
```

```
# install contextily
conda install -c conda-forge contextily
```

```
# run the read_plot_shp.py script in a terminal with the function arguments
#    first arg = path to the directory containing all shapefiles
#    second arg = output plot format (one of jpg, pdf, png, webmap)
#    Note: if the path to shapefile or name of shapefile contains spaces, wrap it around double quotes, i.e "my shapefile"

python read_plot_shp.py \data png
```

### Ravenpy (Full Installation)
create an environment:
```
conda create -c conda-forge --name ravenpy
```
activate the environment:
```
conda activate ravenpy
```
install ravenpy[gis] (full installation) using conda-forge:
```
conda install -c conda-forge ravenpy[gis]
```
install birdy:
```
conda install -c conda-forge birdy
```
install geopandas: 
```
conda install geopandas
```

The script is based on the [jupyter notebook](https://ravenpy.readthedocs.io/en/latest/notebooks/01_Getting_watershed_boundaries.html) with the added functionality of converting and saving the created geojson boundary file to a shapefile

run the script:
```
python ravenpy_delineation.py
```

#### Notes
- Each delineation took < 1 minute
- Grand River -> pourpoint = [-80.15, 43.09]
![Grand_River_ravenpy](https://github.com/kokubadejo/Watershed_Delineation/assets/90711306/2da811b9-cab6-4ae6-8c2f-918a0765a6a7)

- Salmon River -> pourpoint = [-122.66, 54.08]
![Salmon_River_ravenpy](https://github.com/kokubadejo/Watershed_Delineation/assets/90711306/aea72910-511d-46bd-b04d-7301fc9462ad)

- West Arrowwood Creek -> pourpoint = [-113.22, 50.77]
![Arrowwood_ravenpy](https://github.com/kokubadejo/Watershed_Delineation/assets/90711306/6835bc76-6f91-489b-a14f-e21d4b290cb9)

### Whitebox
- download and unzip the toolbox from [Whitebox Geospatial Inc.](https://www.whiteboxgeo.com/download-whiteboxtools/)
- read the [setup documentation](https://www.whiteboxgeo.com/manual/wbt_book/install.html)
- the whitebox_delineation.py script must be run from the parent directory of the unzipped toolbox
- the toolbox folder name must match the import (i.e if the folder is called WBT, then change the import to:
  - ```from WBT.whitebox_tools import WhiteboxTools```
- installs (can be done in a conda environment):
  ```
  # install anaconda package
  conda install -c conda-forge whitebox_tools
  ```
  
- Note:
  - the input files must have the same coordinate reference system
  - must have python3
  - multiple pourpoints would give a Multipolygon result
  - depending on the size of the dem/flow direction raster, time to run = 10 - 20 minutes
  - input fldir must be a d8 flow direction raster using the ESRI scheme

## Common Errors/Warning When Running
1.
   ```
   FutureWarning: is_categorical_dtype is deprecated and will be removed in a future version. Use isinstance(dtype, CategoricalDtype) instead
   if pd.api.types.is_categorical_dtype(values.dtype):
   ```
   - https://github.com/geopandas/geopandas/blob/main/geopandas/plotting.py#L258 (line 742)
   - add import to script:
     ```
     from pandas import CategoricalDtype
     ```
   - change line
     ```
     if isinstance(values.dtype, CategoricalDtype):
     ```
   - similar issue with explore.py (same fix)
