# Watershed_Delineation

## General Setup
The following steps describe the process to setup the environments and packages needed to run this script (using anaconda):
1. Install anaconda (https://docs.anaconda.com/free/anaconda/install/index.html)
2. Create a conda environment with your preferred python version (I used python 3.9) installed and activate it
   ```
   conda create --name <environment name> python=3.9
   ```
   ```
   conda activate <environment name>
   ```

4. Install the geopandas package
   ```
   conda install -c conda-forge geopandas
   ```
   - Note: geopandas supports python 3.8+


Note: The example figure was gotten from running the script with the grand river watershed shapefile that can be found in the data folder
![Figure_1](https://github.com/kokubadejo/Watershed_Delineation/assets/90711306/116ff1bb-61fa-4e23-8de3-628b62f3b1be)

## Getting Started
### Read_plot_shp.py
Read in and plot a shapefile

```
# load conda environment
conda activate map
```

```
# run the read_plot_shp.py script in a terminal with the function arguments
#    first arg = path to the shapefile
#    second arg = name of shapefile
#    third arg = output plot format (one of jpg, pdf, png, webmap)
#    Note: if the path to shapefile or name of shapefile contains spaces, wrap it around double quotes, i.e "my shapefile"

python read_plot_shp.py \data\02GB001 02GB001 png
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

The script is based on the jupyter notebook (https://ravenpy.readthedocs.io/en/latest/notebooks/01_Getting_watershed_boundaries.html) with the added functionality of converting and saving the created geojson boundary file to a shapefile

#### Notes
- Each delineation took < 1 minute
- Grand River -> pourpoint = [-80.15, 43.09]
- Salmon River -> pourpoint = [-122.66, 54.08]
- West Arrowwood Creek -> pourpoint = [-113.22, 50.77]


## Common Errors/Warning When Running
1. FutureWarning: is_categorical_dtype is deprecated and will be removed in a future version. Use isinstance(dtype, CategoricalDtype) instead
  if pd.api.types.is_categorical_dtype(values.dtype):
- https://github.com/geopandas/geopandas/blob/main/geopandas/plotting.py#L258 (line 742)
- add import => from pandas import CategoricalDtype
- change line => if isinstance(values.dtype, CategoricalDtype):
- similar issue with explore.py (same fix)
