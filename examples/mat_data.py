#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 09:00:20 2024

@author: guterlj
"""
from rustbcadb.compute_rustbca import mat_dic

mat_dic
m = [mat_dic[k]['m'] for k in mat_dic.keys()]
s = [mat_dic[k]['symbol'] for k in mat_dic.keys()]
Es = [mat_dic[k].get('Es') for k in mat_dic.keys()]
with open("data_mat.txt", "w") as f:
    for (a,b,c) in zip(s,m,Es):
        f.write("{} {} {} \n".format(a,b,c))
    