#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 18:52:06 2024

@author: guterlj
"""
from libRustBCA import *
from materials import *
import matplotlib.pyplot as plt
# t = chromium

# chromium = {
#  'symbol': 'Cr',
#  'name': 'chromium',
#  'Z': 24.0,
#  'm': 51.9961,
#  'Es': 4.10,
#  'Ec': 0.1,
#  'Eb': 0.0,
#  'n': 8.327E28
# }

# deuterium = {
#     'symbol': 'D',
#     'name': 'deuterium',
#     'Z': 1.0,
#     'm': 2.0,
#     'Ec': 0.1,
#     'Es': 0.0,
# }
p = deuterium
t = chromium
E = np.logspace(0,3,100)
Y = [sputtering_yield(p, t, E_,0.0, 10000) for E_ in E]
plt.loglog(E,Y)

