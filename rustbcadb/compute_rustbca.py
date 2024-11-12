#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 11:23:07 2023

@author: jeromeguterl
"""
import sys, os
import numpy as np
from libRustBCA import *
from . import materials
from .materials import *
import argparse
mat_dic = dict((k,v) for (k,v) in vars(materials).items() if not k.startswith('_'))

def get_material(mat_name):
    mat = mat_dic.get(mat_name)
    if mat is None:
        for (k,v) in mat_dic.items():
            if mat_name == v['symbol']:
                mat = v
                break
    if mat is None:
        raise ValueError("Cannot find material {} in available materials:{}".format(mat_name,list_materials()))
    return mat

def show_materials():
    print("=== material available ===")
    for (k,v) in mat_dic.items():
        print(k, ":",' | '.join(("{}:{}".format(k_,v_) for (k_,v_)  in v.items())))
def list_materials():
    return ' | '.join("{} [{}]".format(k,v["symbol"]) for (k,v) in mat_dic.items())
def show_list_materials():
    print("=== material available ===")
    for (k,v) in mat_dic.items():
        print("{} [{}]".format(k,v["symbol"]))
        
    
def scan_energy_angle(projectile=None, target=None, path=None, Emin=1, Emax= 1e4, theta_max = 89, theta_min = 0.0, N_theta=40, N_energy=100, num_samples=10000):
    if path is None:
        parser = argparse.ArgumentParser("")
        parser.add_argument("--num_samples", help="number of samples", type=int, default=10000, required=False)
        parser.add_argument("--projectile", help="projectile", type=str, required=True)
        parser.add_argument("--target", help="target", type=str, required=True)
        parser.add_argument("--path", help="path", type=str, required=True)
        parser.add_argument("--Emax", help="maximum Energy for scan", type=float, default=1e4, required=False)
        parser.add_argument("--Emin", help="path", type=float, default=0.1, required=False)
        parser.add_argument("--theta_max", help="maximum Energy for scan", type=float, default=89.0, required=False)
        parser.add_argument("--theta_min", help="path", type=float, default=0, required=False)
        parser.add_argument("--N_theta", help="number of angle points", type=int, default=40, required=False)
        parser.add_argument("--N_energy", help="number of energy points", type=int, default=100, required=False)
        args = parser.parse_args()
        scan_energy_angle(**vars(args))
    else:
        assert projectile is not None
        assert target is not None
        print("target:", target)
        print("projectile:" ,projectile)
        t = get_material(target)
        p = get_material(projectile)
        energy = np.logspace(np.log10(Emin),np.log10(Emax),N_energy)
        angle = np.linspace(theta_min,theta_max,N_theta)
        data = {}
        data['target'] = t
        data['projectile'] = p
        data['num_samples'] = num_samples
        data['energy'] = energy
        data['angle'] = angle
        Y = np.zeros((N_energy,N_theta))
        R_p = np.zeros((N_energy,N_theta))
        R_E = np.zeros((N_energy,N_theta))
        data['R_E'] = R_E
        data['R_p'] = R_p
        data['Y'] = Y
        for i in range(N_energy):
            for j in range(N_theta):
                
                angle_ = angle[j]
                energy_ = energy[i]
                print("{} -> {} : energy={:2.2} [{}]/ angle = {:2.2} [{}]".format(p["symbol"],t["symbol"],energy_,i,angle_,j))
                Y[i,j] = sputtering_yield(p, t, energy_, angle_, num_samples)
                R_p[i,j], R_E[i,j] = reflection_coefficient(p, t, energy_, angle_, num_samples)
        if path is None:
            return data
        else:
            np.save(os.path.abspath(path+"/Y_R_{}_{}.npy".format(t["symbol"],p["symbol"])),data)
        return data

def postprocess_database(directory):
    log = np.load(os.path.join(directory, "log.npy"), allow_pickle=True).tolist()
    dic ={}
    dic['target'] = [p[0] for p in log['sims_param_array']]
    dic['projectile'] = [p[1] for p in log['sims_param_array']]
    dic['Y'] = {}
    for p in log['sims_param_array']:
        target_ = get_material(p[0])
        projectile_ = get_material(p[1])
        target = target_['name']
        projectile = projectile_['name']
        
        
        fp = os.path.join(directory,"Y_R_{}_{}.npy".format(target_['symbol'],projectile_['symbol']))
        if target not in dic['Y'].keys():
            dic['Y'][target] = {}
        if projectile not in dic['Y'][target].keys():
            dic['Y'][target][projectile] = {}
        print("reading {} ... : ".format(fp))
        try:
            dic['Y'][target][projectile] = np.load(fp, allow_pickle=True).tolist()
            print("success")
        except Exception as e:
            print(e)
            print("fail")
    file = os.path.join(directory,"processed_database.npy")
    np.save(file, dic)
    print("database postprocessed and  dump into {}".format(file))
    return dic
