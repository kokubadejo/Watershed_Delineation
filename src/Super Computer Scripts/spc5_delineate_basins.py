#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Copyright 2016-2023 Juliane Mai - juliane.mai(at)uwaterloo.ca
#
# License
# This file is part of Juliane Mai's personal code library.
#
# Juliane Mai's personal code library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Juliane Mai's personal code library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with Juliane Mai's personal code library.  If not, see <http://www.gnu.org/licenses/>.
#
# pyenv activate env-385-new
# python 5_delineate_basins.py -i "Total_Phosphorus_mixed_forms_obs.json" -o "test" -s 10 -e 15


import os
import sys

# -----------------------
# add subolder scripts/lib to search path
# -----------------------
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path+'/lib')

import argparse
import json



input_file    = None
output_folder = None
start         = None
end           = None
method        = None

parser  = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                  description='''Delineate all basins specified in file.''')
parser.add_argument('-i', '--input_file', action='store', default=input_file, dest='input_file',
                    help="Input JSON file. Default: None.")
parser.add_argument('-o', '--output_folder', action='store', default=output_folder, dest='output_folder',
                    help="Name of folder to dump shapefiles into. Folder will be created if it doesnt exist. Default: None.")
parser.add_argument('-s', '--start', action='store', default=start, dest='start',
                    help="Station number to start with. This is an index. If start=1, first station will be delineated. If start=10, 10th station will be delineated first and first 9 will be skipped. If None, start=1. Default: None.")
parser.add_argument('-e', '--end', action='store', default=end, dest='end',
                    help="Station number to end with. This is an index. If end=2, second station is last station to delineate. If end=5, 5th station is the last one that will be delineated. If None, end=len(stations). Default: None.")
parser.add_argument('-m', '--method', action='store', default=method, dest='method',
                    help="Delineation tool to use. One of mghydro, pysheds. Default: Mghydro.")

args          = parser.parse_args()
input_file    = args.input_file
output_folder = args.output_folder
start         = int(args.start)
end           = int(args.end)
method        = args.method

if (input_file is None):
    raise ValueError("Input file needs to be specified.")

if (output_folder is None):
    raise ValueError("Output folder needs to be specified.")

if not os.path.exists(input_file):
    raise ValueError("Input file {} does not exist.".format(input_file))

if not os.path.exists(output_folder):
    os.makedirs(output_folder)


del parser, args




print("")
print("----------------------------------------------")
print("Working on stations in file: {}".format(input_file))
print("----------------------------------------------")

# -------------------------------
# load data
# -------------------------------
if os.path.exists(input_file):
    print("Read data from: {}".format(input_file))
    with open(input_file, 'r', encoding='utf-8') as ff:
        data = json.load(ff)
        print("no of stations")
        print(len(data['value']))
else:
    raise ValueError("File {} not found".format(input_file))

# -------------------------------
# properly set start and end index
# -------------------------------
if start is None:
    start = 0
else:
    start -= 1  # indexes start with 0 in Python

if end is None:
    end = len(data['value'])


# -------------------------------
# filter only data needed for delineation
# -------------------------------

stations = []
for dd in data['value'][start:end]:

    tmp = { 'id': dd['Id'],
            'lat': dd['LatitudeNormalized'],
            'lng': dd['LongitudeNormalized'],
          }
    stations.append(tmp)

# -------------------------------
# perform delineation
# -------------------------------
print("stations")
print(stations)
print(len(stations))

for iistation,istation in enumerate(stations):

    print("")
    print("----------------------------------------------")
    print("Working on delineating watershed draining towards station {} of {}: id={} (lat={},lng={})".format(
        iistation+1,
        len(stations),
        istation['id'],
        istation['lat'],
        istation['lng']))
    print(istation)
    print("----------------------------------------------")


    # Kasope add code to delineate basin ...
    # os.environ['USE_PYGEOS'] = '0'
    import numpy as np
    import pandas as pd
    
    json_name = input_file[:-5]
    basin = pd.DataFrame.from_records([istation])
    print("basin")
    print(basin, json_name)
        
    if method in [None, 'mghydro']:  # Mghydro as default method
        import Mghydro.delineate as mg
        
        mg.delineate(basin, output_folder, json_name)
    
    elif method == "pysheds":
        import PySheds.main as ps
        
        ps.delineate(output_dir=output_folder, output_fname=json_name, basins=basin)
        
    
    
        