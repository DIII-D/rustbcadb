#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 09:21:10 2023

@author: jeromeguterl
"""

from rustbcadb import *

#show a list of available materials
show_list_materials()

# directory where database will be built
directory = '/fusion/projects/boundary/guterlj/RustBCA/database/database_test'

# setup targets and projectiles
params = {}
params["target"] = ["tungsten", "carbon"]
params["projectile"] = ["helium", "deuterium"]

# simulation options
options = {"num_samples": 20000, "path": directory,'N_energy':5, 'Emax':1000, 'N_theta':2}

#Launcher
launcher = ParallelJobLauncher(directory, overwrite=True)
#setup header command to load conda environment in sbatch script
header_commands = ["module purge","module load conda","conda activate rust_bca"]

#setup runs
launcher.setup_array_runs(params, options=options, header_commands=header_commands)


#submit jobto slurm
slurm_options = {}
slurm_options['p'] = 'ga-ird'
# slurm_options['qos'] = 'debug'
# slurm_options['account'] = 'm3938'
# slurm_options['constraint'] = 'haswell'
slurm_options['J'] = ''
slurm_options['t'] = '02-00:00:00'
#slurm_options['t'] = '00-01:00:00'
slurm_options['cpus-per-task'] = '1'
slurm_options['mem-per-cpu'] = '4G'
slurm_options['o'] = '%j.o'
slurm_options['e'] = '%j.e'
# slurm_options['ntasks-per-node'] = 1
slurm_options['n'] = 1

launcher.sbatch(slurm_options)

##### to postprocess the database ####:
# from rustbcadb import *   
# postprocess_database(directory)

