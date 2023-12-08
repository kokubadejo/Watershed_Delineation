#!/bin/bash

# submit with:
#       sbatch submit-job-to-graham.sh

#SBATCH --account=rpp-julemai                      # your group
#SBATCH --mem-per-cpu=4G                           # memory; default unit is megabytes
#SBATCH --mail-user=juliane.mai@uwaterloo.ca       # email address for notifications
#SBATCH --mail-type=FAIL                           # email send only in case of failure
#SBATCH --time=0-01:00:00                          # time (DD-HH:MM:SS);
#SBATCH --job-name=delineate                       # name of job in queque
#SBATCH --array=1-79




# 100 stations = 19 min

# job ID: 13527971        # Inorganic_nitrogen_(nitrate_and_nitrite)_obs.json
# ---> no of stations:  7870    (grep -c LatitudeNormalized "Inorganic_nitrogen_(nitrate_and_nitrite)_obs.json")
# ---> ntasks = 79
json_file="Inorganic_nitrogen_(nitrate_and_nitrite)_obs.json"

# job ID:        # Total_Phosphorus_mixed_forms_obs.json
# ---> no of stations: 14309    (grep -c LatitudeNormalized "Total_Phosphorus_mixed_forms_obs.json")
# ---> ntasks = 144
# json_file="Total_Phosphorus_mixed_forms_obs.json"





# load modules
module purge
module load StdEnv/2020 netcdf/4.7.4 gcc/9.3.0 gdal/3.5.1
module load mpi4py/3.1.3 proj/9.0.1
module load geos/3.10.2
module load nco/5.0.6
module load python/3.10.2

# change to right dir
cd /home/julemai/projects/rpp-julemai/julemai/Watershed_Delineation/src/Super\ Computer\ Scripts

# set Python env
source ../../env-3.10/bin/activate

# determine start and end index
nstations=$( grep -c LatitudeNormalized ${json_file} )
ntasks=${SLURM_ARRAY_TASK_COUNT}
nstations_per_task=$(( ${nstations} / ${ntasks} + 1 ))

start_idx=$(( (${SLURM_ARRAY_TASK_ID} - 1)*${nstations_per_task} + 1 ))
end_idx=$((   (${SLURM_ARRAY_TASK_ID}    )*${nstations_per_task}     ))
end_idx=$(( ${end_idx} < ${nstations} ? ${end_idx} : ${nstations} )) # make sure end_idx min(end_idx, nstations)

# run script
python spc5_delineate_basins.py -i ${json_file} -o "/scratch/julemai/delineation" -s ${start_idx} -e ${end_idx}
