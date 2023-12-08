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

3. Add conda-forge channel if not added already:
   ```
   conda config --add channels conda-forge
   ```

Note: The example figure was gotten from running the script with the grand river watershed shapefiles gotten from manual, ravenpy and the example (Basinmaker?) delineations
![Figure](https://github.com/kokubadejo/Watershed_Delineation/assets/90711306/4a5ebbf9-7019-4281-bf19-4b5d48eee39b)

# Getting Started
### Read_plot_shp.py
Read in and plot a shapefile

```
# load conda environment
conda activate map
```
Install necessary packages
```
# install the geopandas package
conda install -n <environment name> -c conda-forge geopandas
# Note: geopandas supports python 3.8+
```

```
# install folium
conda install -n <environment name> -c conda-forge folium
```

```
# install matplotlib
conda install -n <environment name> -c conda-forge matplotlib
```

```
# install contextily
conda install -n <environment name> -c conda-forge contextily
```

```
# navigate to the directory of the script
cd "src/Read Shapefiles"
```

```
# run the read_plot_shp.py script in a terminal with the function arguments
#    first arg = path to the directory containing all shapefiles
#    second arg = output plot format (one of jpg, pdf, png, webmap)
#    Note: if the path to shapefile or name of shapefile contains spaces, wrap it around double quotes, i.e "my shapefile"

python read_plot_shp.py \data png
```

## Standalone Scripts
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
conda install -n ravenpy -c conda-forge ravenpy[gis]
```
install birdy:
```
conda install -n ravenpy -c conda-forge birdy
```
install geopandas: 
```
conda install -n ravenpy geopandas
```

The script is based on the [jupyter notebook](https://ravenpy.readthedocs.io/en/latest/notebooks/01_Getting_watershed_boundaries.html) with the added functionality of converting and saving the created geojson boundary file to a shapefile

navigate to the directory of the script:
```
cd src/Ravenpy
```

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
    ![Figure](https://github.com/kokubadejo/Watershed_Delineation/assets/90711306/d2c14f47-0aac-44d3-9078-60ece5d8a817)

  - depending on the size of the dem/flow direction raster, time to run = 10 - 20 minutes
  - input fldir must be a d8 flow direction raster using the ESRI scheme

### MgHydro's Delineator
- this tool was created by [Matthew Heberger](https://mghydro.com/)
- download the [repository](https://github.com/mheberger/delineator) and follow these [instructions](https://github.com/mheberger/delineator#readme) to download the necessary data
  - [Download MERIT-Basins vector data](https://www.reachhydro.org/home/params/merit-basins):
    - [MERIT-Basins hydrography (based on MERIT-Hydro v0.7/v1.0)](https://drive.google.com/drive/folders/1uCQFmdxFbjwoT9OYJxw-pXaP8q_GYH1a?usp=share_link) - pfaf_level_02
  - [Download simplified MERIT-Basins data](https://mghydro.com/watersheds/share/catchments_simplified.zip)
- edit the config.py file according to where your data is located
  - **Note:** If you're using this with the super computer script, it's a good idea to have the paths in config.py as absolute paths
    
  #### Package Installations
- create a python virtual / anaconda environment and activate it:
  ```
  # Python Virtual Environment
  pyenv virtualenv <python_version> <environment_name>
  pyenv activate <environment_name>
  ```
  ```
  # Anaconda Environment
  conda create --name <environment name> python=3.9
  conda activate <environment_name>
  ```
- install all the requirements
  ```
  $ pip install -r requirements.txt
  ```
  - if this doesn't work, try installing the packages individually:
     ```
     pip install geopandas~=0.13.2
     pip install shapely~=2.0.2
     pip install pandas~=2.1.3
     pip install Jinja2~=3.1.2
     pip install matplotlib~=3.8.1
     pip install numpy~=1.26.2
     pip install pysheds~=0.3.5
     pip install sigfig~=1.3.3
     pip install pyproj~=3.6.1
     ```
  - the following package versions also work:
     ```
     pip install pandas~=2.0.3
     pip install pandas~=1.5.3
     pip install matplotlib~=3.7.4
     pip install numpy~=1.24.4
     pip install pyproj~=3.5.0
     ```
- install pygeos
  ```
  pip install pygeos
  ```
  or
  ```
  conda install pygeos
  ```
- navigate to the directory of python script:
  ```
  cd path\to\script
  ```
- run the tool
  ```
  python delineate.py
  ```
  
- **Note:** any pandas version >= 2.0 may have compatibility errors with pickle.
- All these instructions can be found in [mheberger's delineator repository on github](https://github.com/mheberger/delineator)
- Note: To keep things consistent, the [Hydrosheds](https://www.hydrosheds.org/hydrosheds-core-downloads) dem and accumulation rasters were used instead of the [MERIT products](https://mghydro.com/watersheds/rasters/)

### Pysheds
- install the pyshed package
  ```
  pip install pysheds
  ```

- install fiona
  ```
  pip install fiona
  ```
- install area
  ```
  pip install area
  ```

- **Note**
  - replace the flow direction and accumulation files with your path and filenames
  - The files used in the script were downloaded from [HydroSheds Core Products](https://www.hydrosheds.org/hydrosheds-core-downloads). The 15s North and Central America data was used.
 
- navigate to the directory of python script:
  ```
  cd path\to\script
  ```
- run the script:
  ```
  python main.py
  ```
  

### Rabpro
- install the rabpro package in a virtual environment
  ```
  conda install rabpro -c conda-forge
  ```
- navigate to the working directory (folder with script)
  ```
  cd path\to\script
  ```
- run the script:
  ```
  python ravenpy_delineation.py
  ```
- to download MERIT data, fill out this [google form](https://docs.google.com/forms/d/e/1FAIpQLSeguQvFq0L4Afm2nrjjBnNaw6jKyUHA97Li6HGqL84JKLFV8A/viewform) to obtain a username and password
- more information on installation and functionality can be found on the [Rabpro github](https://veinsoftheearth.github.io/rabpro/index.html)

## Super Computer Scripts
- install the packages for the Pysheds and Mghydro tools into one environment
- navigate to the script directory
  ```
  cd path\to\script
  ```
- run the script, eg:
  ```
  python spc5_delineate_basins.py --input_file "Total_Phosphorus_mixed_forms_obs.json" --output_folder "test" --start 10 --end 15 -m "mghydro"
  ```

**Note:**
The format of the json file should be:
```
{
 "value": [station_dicts]
}
```

A station_dict is structured as follows:
```
{
   "Id": 1,                              # mandatory
   "ID": "...",
   "Name": "...",
   "LatitudeNormalized": 46.214947,      # mandatory
   "LongitudeNormalized": -64.674869,    # mandatory
   "observations": [{...}, ...]
}
```

## Delineation Results
![Grand_River (2)](https://github.com/kokubadejo/Watershed_Delineation/assets/90711306/f619b3d3-5466-4fe4-b447-3b20d05f5aa8)
![Salmon_River (2)](https://github.com/kokubadejo/Watershed_Delineation/assets/90711306/0dd4eef5-8042-4af4-a503-b21aa46d461a)
![Arrowwood_Creek (2)](https://github.com/kokubadejo/Watershed_Delineation/assets/90711306/d4a7025c-ebb2-412d-8320-5a9e9f432914)

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

2. 
   ```
   AttributeError: 'NoneType' object has no attribute 'to_file'
   Could not find a suitable flowline to map given coordinate and DA. No basin can be delineated. You can set da=None to      force an attempt with HydroBASINS.
   ```
   - This means there was an issue delineating the watershed, most likely due to the da size.
   - Play around with this arfument in the profiler function call (line 66)
     ```
     rpo = rabpro.profiler(coords, name=name, da=500)        # play around with the da
     ```

3. ```
   from rasterio._version import gdal_version, get_geos_version, get_proj_version
   ImportError: DLL load failed while importing _version: The specified procedure could not be found.
   ```
   - Try removing and reinstalling rasterio & pyshed
     ```
     pip uninstall pysheds
     ```
     ```
     pip uninstall rasterio
     ```
     ```
     pip install pysheds
     ```
     Note: pysheds installation installs rasterio with it
     
4. DLL error from shapely
   - reorder the import statement

5. ```
   from fiona._env import (
   ImportError: DLL load failed while importing _env: The specified procedure could not be found.
   ```
   - Usually caused from incompatibility with gdal
   - quick fix => uninstall gdal and fiona, reinstall fiona:
     
