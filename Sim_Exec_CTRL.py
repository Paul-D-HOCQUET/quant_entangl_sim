#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 08:16:23 2023

@author: jm
"""

from  Sim_Tools          import SWAPab, Mult
from  Sim_Exec_PorteUN   import UQ_Gates, G1
from  Sim_Exec_PorteDEUX import DQ_Gates, G2

    
#
#   Executer une porte gate sur le dernier qubit N-1 et controlee par k precedents qubits.
#

def CTRLk (N, Phi, k, d, gate):
       
    if (d == 1):
        ind = UQ_Gates.index(gate) 
        G   = G1[ind].copy()
        Phi = Mult (N, Phi, k, d, G)
        return (Phi)
    else:
        ind = DQ_Gates.index(gate)
        G   = G2[ind].copy()
        Phi = Mult (N, Phi, k, d, G)
        return (Phi)

def CTRL (N, Phi, StrG, control_list, on_Qubits):

    k     = len(control_list)
    d     = len(on_Qubits)
    stack = []
    
    on_Qubits.sort()
    
    minq = on_Qubits[0]
    
    if (minq > 0):
        Phi = SWAPab (N, Phi, N-1, minq)
        stack.append([0, minq])
        on_Qubits[0] = 0
        if (0 in control_list):
            control_list.remove(0)
            control_list.append(minq)
    
    if (d == 2):
        maxq = on_Qubits[1]
        
        if maxq > 1:
            Phi = SWAPab (N, Phi, N-2, maxq)
            stack.append([1, maxq])
            on_Qubits[1] = 1
            if (1 in control_list):
                control_list.remove(1)
                control_list.append(maxq)
    
    control_list.sort()
    
    for i in range( len(control_list) ):
        if control_list[i] != (i+d):
            Phi = SWAPab (N, Phi, N-1-d, control_list[i])
            stack.append([i+d, control_list[i]])
        
    Phi = CTRLk (N, Phi, k, d, StrG)
    
    while (stack):
        [a, b] = stack.pop()
        Phi = SWAPab (N, Phi, a, b)
    
    return (Phi)