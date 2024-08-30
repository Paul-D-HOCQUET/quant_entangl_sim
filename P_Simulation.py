#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 20:07:35 2024

@author: jm
"""

from Sim_Construct           import Construct_Circuit
from Sim_Exec_Circuit        import Exec_Circuit

import math


MaxQubits = 10
Circuit   = './Exemples/Simple.txt'

(err, NbQubits, Desc) = Construct_Circuit (Circuit, MaxQubits)

A       = []
B       = []
Phis    = []

for i in range(math.floor(NbQubits / 2)):
    A.append(i)  

for i in range(math.floor(NbQubits / 2), NbQubits):
    B.append(i)  

(Phis, Rank_VN, Entropy_VN, Rank_SD, Entropy_SD, V_N_Partitions) = Exec_Circuit (NbQubits, Desc, A, B, True)

#print(Entropy_VN)
#print(Entropy_SD)
print(V_N_Partitions)