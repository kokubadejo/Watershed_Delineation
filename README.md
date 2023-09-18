# Watershed_Delineation

## Setup
The following steps describe the process to setup the environments and packages needed to run this script (using anaconda):
1. Install anaconda and open an Anaconda Command Prompt
2. Create a conda environment with your preferred python version (used python 3.9) installed and activate it
3. Install the geopandas package -> conda install -c conda-forge geopandas
   - Note: geopandas supports python 3.8+

run the read_shp.py script in a terminal

Note: The example figures & files were gotten from running the script with the grand river watershed shapefile

### Common Errors/Warning When Running
1. FutureWarning: is_categorical_dtype is deprecated and will be removed in a future version. Use isinstance(dtype, CategoricalDtype) instead
  if pd.api.types.is_categorical_dtype(values.dtype):
- https://github.com/geopandas/geopandas/blob/main/geopandas/plotting.py#L258 (line 742)
- add import => from pandas import CategoricalDtype
- change line => if isinstance(values.dtype, CategoricalDtype):
- similar issue with explore.py (same fix)