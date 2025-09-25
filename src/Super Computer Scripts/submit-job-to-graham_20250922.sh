#!/bin/bash

# submit with:
#       sbatch submit-job-to-graham.sh

#SBATCH --account=rpp-caspar                       # rpp-julemai   # your group
#SBATCH --mem-per-cpu=4G                           # memory; default unit is megabytes
#SBATCH --mail-user=juliane.mai@uwaterloo.ca       # email address for notifications
#SBATCH --mail-type=FAIL                           # email send only in case of failure
#SBATCH --time=0-01:30:00                          # time (DD-HH:MM:SS);
#SBATCH --job-name=delineate                       # name of job in queque
#SBATCH --array=1-73




# 100 stations = 19 min

# job ID: XXX              # Inorganic_nitrogen_(nitrate_and_nitrite)_obs.json
# ---> no of stations:  7262    (grep -c Latitude "Inorganic_nitrogen_(nitrate_and_nitrite)_obs.json")
# ---> ntasks = 73
json_file="Inorganic_nitrogen_(nitrate_and_nitrite)_obs.json"

# job ID: XXX              # Nitrate_obs.json
# ---> no of stations:  6292    (grep -c Latitude "Nitrate_obs.json")
# ---> ntasks = 63
#json_file="Nitrate_obs.json"

# job ID: XXX              # Nitrite_obs.json
# ---> no of stations:  7056    (grep -c Latitude "Nitrite_obs.json")
# ---> ntasks = 71
#json_file="Nitrite_obs.json"

# job ID: XXX              # Total_Nitrogen_mixed_forms_obs.json
# ---> no of stations:  4899    (grep -c Latitude "Total_Nitrogen_mixed_forms_obs.json")
# ---> ntasks = 49
# SUBMITTED
#json_file="Total_Nitrogen_mixed_forms_obs.json"

# job ID: XXX              # Organic_Nitrogen_obs.json
# ---> no of stations:  1918    (grep -c Latitude "Organic_Nitrogen_obs.json")
# ---> ntasks = 20
#json_file="Organic_Nitrogen_obs.json"

# job ID: 2192740   # Total_Phosphorus_mixed_forms_obs.json
# ---> no of stations: 8872    (grep -c Latitude "Total_Phosphorus_mixed_forms_obs.json")
# ---> ntasks = 89
# SUBMITTED
#json_file="Total_Phosphorus_mixed_forms_obs.json"

# job ID: XXX       # Orthophosphate_obs.json
# ---> no of stations: 6386    (grep -c Latitude "Orthophosphate_obs.json")
# ---> ntasks = 64
# SUBMITTED
#json_file="Orthophosphate_obs.json"

# job ID: 2192732   # Soluble_Reactive_Phosphorus_(SRP)_obs.json
# ---> no of stations: 203    (grep -c Latitude "Soluble_Reactive_Phosphorus_(SRP)_obs.json")
# ---> ntasks = 3
# SUBMITTED
#json_file="Soluble_Reactive_Phosphorus_(SRP)_obs.json"

# job ID: XXX       # hydat_stations_all.json
#                   #     {
#                   #         "value": [
#                   #              {
#                   #             	"Id": "01AD002",
#            	    #		  	"Name": "SAINT JOHN RIVER AT FORT KENT",
#            	    #		  	"Latitude": 47.258060455322266,
#                   #    	  	"Longitude": -68.59583282470703,
#                   #              },
#                   #              ...
#                   #          ] 
#                   #     }
#                   #
# ---> no of stations: 7937   
# ---> ntasks = 80
#json_file="hydat_stations_all.json"





# load modules
# module purge
# module load StdEnv/2020 netcdf/4.7.4 gcc/9.3.0 gdal/3.5.1
# module load mpi4py/3.1.3 proj/9.0.1
# module load geos/3.10.2
# module load nco/5.0.6
# module load python/3.10.2

# load modules
module purge
module load StdEnv/2023 gcc/12.3 netcdf/4.9.2 gdal/3.7.2 mpi4py/3.1.4 proj/9.2.0 geos/3.12.0 nco/5.1.7 python/3.11.5

# change to right dir
cd /home/julemai/projects/rpp-julemai/julemai/Watershed_Delineation/src/Super\ Computer\ Scripts

# set Python env
source ../../env-3.11/bin/activate

# determine start and end index
# nstations=$( grep -c LatitudeNormalized ${json_file} )
nstations=$( grep -c Latitude ${json_file} )
ntasks=${SLURM_ARRAY_TASK_COUNT}
nstations_per_task=$(( ${nstations} / ${ntasks} + 1 ))

start_idx=$(( (${SLURM_ARRAY_TASK_ID} - 1)*${nstations_per_task} + 1 ))
end_idx=$((   (${SLURM_ARRAY_TASK_ID}    )*${nstations_per_task}     ))
end_idx=$(( ${end_idx} < ${nstations} ? ${end_idx} : ${nstations} )) # make sure end_idx min(end_idx, nstations)

# run script
#python spc5_delineate_basins.py -i ${json_file} -o "/scratch/julemai/delineation" -s ${start_idx} -e ${end_idx}
python spc5_delineate_basins.py -i ${json_file} -o "/project/6070465/julemai/Watershed_Delineation/output" -s ${start_idx} -e ${end_idx}

# cd /home/julemai/projects/rpp-julemai/julemai/Watershed_Delineation/src/Super\ Computer\ Scripts/
# cnn=0 ; for (( ii=1 ; ii<=79 ; ii++ )) ; do nn=$(grep "Writing output for watershed" slurm-13891389_${ii}.out | wc -l) ; start=$(( (ii-1)*100+1)) ; end=$(( ii*100 )); echo "Indexes: ${start} to ${end} --> delineated ${nn} watersheds (should be 100)" ; cnn=$(( cnn + nn )) ; done ; echo "Total number of matches: ${cnn}"

# cnn=0 ; for (( ii=1 ; ii<=79 ; ii++ )) ; do nn=$(grep "KO: COASTAL BASIN?" slurm-13891389_${ii}.out | wc -l) ; start=$(( (ii-1)*100+1)) ; end=$(( ii*100 )); echo "Indexes: ${start} to ${end} --> ${nn} coastal watersheds (hopefully 0)" ; cnn=$(( cnn + nn )) ; done ; echo "Total number of coastal watersheds: ${cnn}"

# slurmid="15948818" ; ntasks=59 ; nstations_per_task=99 ; cnn1=0 ; cnn2=0 ; for (( ii=1 ; ii<=59 ; ii++ )) ; do nn1=$(grep "KO: COASTAL BASIN?" slurm-${slurmid}_${ii}.out | wc -l) ; nn2=$(grep "Writing output for watershed" slurm-${slurmid}_${ii}.out | wc -l) ; start=$(( (${ii} - 1)*${nstations_per_task} + 1 )) ; end=$(((${ii})*${nstations_per_task})); echo "Indexes: ${start} to ${end} --> ${nn1} coastal watersheds and ${nn2} delineated = $(( nn1 + nn2 ))" ; cnn1=$(( cnn1 + nn1 )) ; cnn2=$(( cnn2 + nn2 )) ; done ; echo "Total number of coastal watersheds: ${cnn1}" ; echo "Total number of matches: ${cnn2}"

# find /scratch/julemai/delineation/ -name Inorg*.geojson | wc -l
# find /scratch/julemai/delineation/ -name Total*.geojson | wc -l
