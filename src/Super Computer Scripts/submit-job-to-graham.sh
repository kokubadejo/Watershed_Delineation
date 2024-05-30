#!/bin/bash

# submit with:
#       sbatch submit-job-to-graham.sh

#SBATCH --account=rpp-julemai                      # your group
#SBATCH --mem-per-cpu=4G                           # memory; default unit is megabytes
#SBATCH --mail-user=juliane.mai@uwaterloo.ca       # email address for notifications
#SBATCH --mail-type=FAIL                           # email send only in case of failure
#SBATCH --time=0-03:00:00                          # time (DD-HH:MM:SS);
#SBATCH --job-name=delineate                       # name of job in queque
#SBATCH --array=1-63




# 100 stations = 19 min

# job ID: 15946951              # Inorganic_nitrogen_(nitrate_and_nitrite)_obs.json
#         CHECKED
# ---> no of stations:  5816    (grep -c Latitude "Inorganic_nitrogen_(nitrate_and_nitrite)_obs.json")
# ---> ntasks = 59
json_file="Inorganic_nitrogen_(nitrate_and_nitrite)_obs.json"

# job ID: 15948818              # Nitrate_obs.json
#         CHECKED
# ---> no of stations:  5826    (grep -c Latitude "Nitrate_obs.json")
# ---> ntasks = 59
json_file="Nitrate_obs.json"

# job ID: 15949799              # Nitrite_obs.json
#         CHECKED
# ---> no of stations:  4490    (grep -c Latitude "Nitrite_obs.json")
# ---> ntasks = 45
json_file="Nitrite_obs.json"

# job ID: 15950413              # Total_Nitrogen_mixed_forms_obs.json
#         CHECKED
# ---> no of stations:  4129    (grep -c Latitude "Total_Nitrogen_mixed_forms_obs.json")
# ---> ntasks = 42
json_file="Total_Nitrogen_mixed_forms_obs.json"

# job ID: 15950831              # Organic_Nitrogen_obs.json
#         CHECKED
# ---> no of stations:  1921    (grep -c Latitude "Organic_Nitrogen_obs.json")
# ---> ntasks = 20
json_file="Organic_Nitrogen_obs.json"

# job ID: 15950926              # Inorganic_nitrogen_(ammonia_nitrate_and_nitrite)_obs.json
#         CHECKED
# ---> no of stations:  21    (grep -c Latitude "Inorganic_nitrogen_(ammonia_nitrate_and_nitrite)_obs.json")
# ---> ntasks = 10
json_file="Inorganic_nitrogen_(ammonia_nitrate_and_nitrite)_obs.json"



# job ID: 15954741       # Total_Phosphorus_mixed_forms_obs.json
#         15958060
#         15959961
# ---> no of stations: 7700    (grep -c Latitude "Total_Phosphorus_mixed_forms_obs.json")
# ---> ntasks = 78
json_file="Total_Phosphorus_mixed_forms_obs.json"

# job ID: 15954857       # Orthophosphate_obs.json
#         15958177
#         CHECKED
# ---> no of stations: 5568    (grep -c Latitude "Orthophosphate_obs.json")
# ---> ntasks = 56
# json_file="Orthophosphate_obs.json"

# job ID: 15954949       # Soluble_Reactive_Phosphorus_(SRP)_obs.json
#         CHECKED
# ---> no of stations: 141    (grep -c Latitude "Soluble_Reactive_Phosphorus_(SRP)_obs.json")
# ---> ntasks = 30
#json_file="Soluble_Reactive_Phosphorus_(SRP)_obs.json"

# job ID: 21112411       # hydat_stations_w_area.json
#         CHECKED
# ---> no of stations: 6257   
# ---> ntasks = 63
json_file="hydat_stations_w_area.json"




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
ntasks=63 #${SLURM_ARRAY_TASK_COUNT}
nstations_per_task=$(( ${nstations} / ${ntasks} + 1 ))

start_idx=$(( (${SLURM_ARRAY_TASK_ID} - 1)*${nstations_per_task} + 1 ))
end_idx=$((   (${SLURM_ARRAY_TASK_ID}    )*${nstations_per_task}     ))
end_idx=$(( ${end_idx} < ${nstations} ? ${end_idx} : ${nstations} )) # make sure end_idx min(end_idx, nstations)

# run script
python spc5_delineate_basins.py -i ${json_file} -o "/scratch/julemai/delineation" -s ${start_idx} -e ${end_idx}


# cd /home/julemai/projects/rpp-julemai/julemai/Watershed_Delineation/src/Super\ Computer\ Scripts/
# cnn=0 ; for (( ii=1 ; ii<=79 ; ii++ )) ; do nn=$(grep "Writing output for watershed" slurm-13891389_${ii}.out | wc -l) ; start=$(( (ii-1)*100+1)) ; end=$(( ii*100 )); echo "Indexes: ${start} to ${end} --> delineated ${nn} watersheds (should be 100)" ; cnn=$(( cnn + nn )) ; done ; echo "Total number of matches: ${cnn}"

# cnn=0 ; for (( ii=1 ; ii<=79 ; ii++ )) ; do nn=$(grep "KO: COASTAL BASIN?" slurm-13891389_${ii}.out | wc -l) ; start=$(( (ii-1)*100+1)) ; end=$(( ii*100 )); echo "Indexes: ${start} to ${end} --> ${nn} coastal watersheds (hopefully 0)" ; cnn=$(( cnn + nn )) ; done ; echo "Total number of coastal watersheds: ${cnn}"

# slurmid="15948818" ; ntasks=59 ; nstations_per_task=99 ; cnn1=0 ; cnn2=0 ; for (( ii=1 ; ii<=59 ; ii++ )) ; do nn1=$(grep "KO: COASTAL BASIN?" slurm-${slurmid}_${ii}.out | wc -l) ; nn2=$(grep "Writing output for watershed" slurm-${slurmid}_${ii}.out | wc -l) ; start=$(( (${ii} - 1)*${nstations_per_task} + 1 )) ; end=$(((${ii})*${nstations_per_task})); echo "Indexes: ${start} to ${end} --> ${nn1} coastal watersheds and ${nn2} delineated = $(( nn1 + nn2 ))" ; cnn1=$(( cnn1 + nn1 )) ; cnn2=$(( cnn2 + nn2 )) ; done ; echo "Total number of coastal watersheds: ${cnn1}" ; echo "Total number of matches: ${cnn2}"

# find /scratch/julemai/delineation/ -name Inorg*.geojson | wc -l
# find /scratch/julemai/delineation/ -name Total*.geojson | wc -l
