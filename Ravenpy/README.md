# Ravenpy Workflow (Full Installation)
- Using Anaconda (recommended)
	- create an environment => conda create -c conda-forge --name ravenpy
	- activate the environment => conda activate ravenpy
	- install ravenpy[gis] (full installation) using conda-forge => conda install -c conda-forge ravenpy[gis]
- install birdy -> conda install -c conda-forge birdy
- install geopandas -> conda install geopandas

The script is based on the jupyter notebook:
https://ravenpy.readthedocs.io/en/latest/notebooks/01_Getting_watershed_boundaries.html
with the added functionality of converting and saving the created geojson boundary file to a shapefile
