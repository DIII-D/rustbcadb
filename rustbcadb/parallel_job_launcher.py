#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 09:14:45 2023

@author: jeromeguterl
"""

import itertools
import numpy as np
import os

from .slurm_support import *
import subprocess

exec_path=os.path.dirname(os.path.dirname(__file__))
def chmodx_directory(directory):
    command = 'chmod -R u+x {}'.format(directory)
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print(output, error)


def tot_sim(params, tridyn_params={}):
    return np.prod([np.array(len(v)) for v in itertools.chain(params.values(), tridyn_params.values())])


def gnu_parallel_command(runner_exec_file, runner_input, njob):
    commands = ['module load parallel']
    commands += ['parallel -j {} {} {{}} < {}'.format(
        njob, runner_exec_file, runner_input)]
    return commands


def dump_log(filename, dic):
    np.save(filename, dic)


class ParallelJobLauncher():
    def __init__(self, directory,overwrite=False):
        self.sim_setup = {}
        self.njobs = 0
        self.directory = os.path.abspath(directory)
        if os.path.exists(directory) and not overwrite:
            raise Exception("the directory {} already exists ... use overwrite=True to use it".format(self.directory))
        if not os.path.exists(directory):
            os.mkdir(directory)
        if not os.path.isdir(self.directory):
            raise Exception(
                "Cannot find the directory {} ... ".format(self.directory))

    def setup_array_runs(self, params, options={}, header_commands=[],  casename='run', exec_command="poetry --directory {} run scan_energy_angle".format(exec_path)):

        dic = {}
        dic['exec_command'] = exec_command
        dic['directory'] = os.path.abspath(self.directory)
        dic['params'] = params
        dic['options'] = options

        dic['nsim'] = np.prod([np.array(len(v)) for v in params.values()])
        
        print(" === setup simulation array ===")
        for (k,v) in dic.items():
            print(k, " : ",v)
        sims = {}
        sim_param_array = np.empty(
            (dic['nsim'], len([k for k in params.values()])), dtype=object)

        for i, val in enumerate(itertools.product(*(v for v in params.values()))):
            print('Setup simulation # {} with :'.format(i), ';'.join(
                ['{}={}'.format(k, val) for k, val in zip(params.keys(), val)]))
            sim = {}
            val_params = val[0:len(list(params.keys()))]
            sim['exec_command'] = dic['exec_command']
            sim['params'] = dict((k, v)
                                 for k, v in zip(params.keys(), val_params))
            sim['options'] = options
            sim['casename'] = '{}_{}'.format(casename, i)
            sim_param_array[i, :] = np.array([v for v in val], dtype=object)
            self.make_command_line(sim, header_commands)
            sims[i] = sim

        dic['sims_param_array'] = sim_param_array
        dic['sims'] = sims
        self.sim_setup = dic
        self.njobs = len(list(self.sim_setup['sims'].keys()))



    @staticmethod
    def make_command_line(sim, header_commands=[]):
        args = " ".join(['--{}={}'.format(k, v) for (k, v) in sim['params'].items()] + [
                        '--{}={}'.format(k, v) for (k, v) in sim['options'].items()])
        command = sim['exec_command'] + " " + args
        sim['command'] = "\n".join(header_commands) + "\n" + command

    def setup_slurm_scripts(self, slurm_options):
        self.slurm_runners = []
        for (i, sim) in self.sim_setup['sims'].items():
            self.slurmscript_directory = os.path.join(
                self.sim_setup['directory'], 'sbatch_scripts')
            try:
                os.mkdir(self.slurmscript_directory)
            except:
                pass
            script_name = '{}.sbatch'.format(sim['casename'])
            slurm_options["J"] = sim['casename']
            slurm_options["o"] = os.path.join(
                self.slurmscript_directory, "{}.o".format(sim["casename"]))
            slurm_options["e"] = os.path.join(
                self.slurmscript_directory, "{}.e".format(sim["casename"]))
            logpath = os.path.join(
                self.slurmscript_directory, "{}.log".format(sim["casename"]))
            sim['logpath'] = logpath
            slurm_runner = SlurmSbatch(sim['command']+' >> {}'.format(
                logpath), **slurm_options, script_dir=self.slurmscript_directory, script_name=script_name, pyslurm=True)
            self.slurm_runners.append(slurm_runner)
            slurm_runner.write_job_file()

    def _sbatch(self):
        # chmodx_directory(self.directory)
        for s in self.slurm_runners:
            s.submit_job()

        # job_id = 0
        self.saveas(os.path.join(
            self.sim_setup['directory'], "log.npy"), self.sim_setup)

    def sbatch(self, slurm_options):
        self.setup_slurm_scripts(slurm_options)
        self._sbatch()

    def saveas(self, filename, obj):
        filename = os.path.join(filename)
        np.save(filename, obj)
