# rustbcadb
rustbcadb is a python package permitting the generation of a database of sputtering yield and reflection coefficients with rustbca on HPC clusters using slurm.

## Install rustbcadb

1. Install poetry systemwide

See instructions here: https://python-poetry.org/docs/

2. Create a new conda environment

Create a new conda/mamba environment named `rust_bca` with the package rust
```bash
  mamba create -n rust_bca python=3.10 rust
  mamba activate rust_bca
```

3. Install rustbcadb

```
git clone https://github.com/DIII-D/rustbcadb
cd rustbcadb
poetry install
cd ..
```
## Use rustbcadb to create a database

An example on how to submit a slurm job on the GA cluster Omega to scan sputtering yield and reflection coefficients as a function of energy and angle for various combinations of projectiles and targets is given in `examples/runner.py'. The example must executed in a python session started in the `rust_bca` conda environment

```python
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
```

