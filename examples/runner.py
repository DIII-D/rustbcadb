#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 09:21:10 2023

@author: jeromeguterl
"""

from rustbcadb import *


directory = '/fusion/projects/boundary/guterlj/RustBCA/database/database_test'

params = {}
params["target"] = ["tungsten", ]
params["projectile"] = ["helium"]

options = {"num_samples": 20000, "path": directory,'N_energy':1, 'N_theta':1}

launcher = ParallelJobLauncher(directory, overwrite=True)
header_commands = ["module purge","module load conda","conda activate rust_bca"]

launcher.setup_array_runs(params, options=options, header_commands=header_commands)


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

