#!/usr/bin/env python
# coding: utf-8

# Import the necessary libraries to format, send, and parse our returned results

import os
import birdy
import geopandas

# Create WPS instances# Set environment variable WPS_URL to "http://localhost:9099" to run on the default local server
pavics_url = "https://pavics.ouranos.ca"
raven_url = os.environ.get("WPS_URL", f"{pavics_url}/twitcher/ows/proxy/raven/wps")
raven = birdy.WPSClient(raven_url)

# Display the lat/lon coordinates of the marker location.
x = float(input('Enter longitude: '))
y = float(input('Enter latitude: '))

user_lonlat = [x, y]
# user_lonlat = [-80.15, 43.09]
print(user_lonlat)

# Get the shape of the watershed contributing to flow at the selected location.
resp = raven.hydrobasins_select(location=str(user_lonlat),
                                aggregate_upstream=True)

# Extract the URL of the resulting GeoJSON feature
feat = resp.get(asobj=False).feature
print(
    "This is the geoJSON file that can be used as the watershed contour in other toolboxes:"
)
print("")
print(feat)
print("")

# Print the properties from the extracted watershed
gdf = geopandas.read_file(feat)

# Converting geojson to shapefile
filename = input("Enter file name: ")
os.mkdir(filename)
gdf.to_file(r'{filename}\{filename}.shp'.format(filename=filename))