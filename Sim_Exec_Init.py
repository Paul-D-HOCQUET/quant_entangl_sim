#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 08:16:23 2023

@author: jm
"""

import math
import numpy as np

#
#   Definir le nombre de qubits et l'etat quantique du systeme |Phi>
#

def Qubit_Setting (Values):
    
    q0    = np.array([1 + 0j,  0 + 0j])
    q1    = np.array([0 + 0j,  1 + 0j])
    qp    = np.array([1/math.sqrt(2) + 0j, 1/math.sqrt(2) + 0j])
    qm    = np.array([1/math.sqrt(2) + 0j, -1/math.sqrt(2) + 0j])
    qpi   = np.array([1/math.sqrt(2) + 0j,  complex (0,  1/math.sqrt(2)) ])
    qmi   = np.array([1/math.sqrt(2) + 0j,  complex (0, -1/math.sqrt(2)) ])
    
    match Values[0]:
        case '0':
            KP = q0.copy()
        case '1':
            KP = q1.copy()
        case '+':
            KP = qp.copy()
        case '-':
            KP = qm.copy()
        case 'i':
            KP = qpi.copy()
        case 'j':
            KP = qmi.copy()
    
        
    for i in range (1, len(Values)):
        match Values[i]:
            case '0':
                KP = np.kron(KP, q0)
            case '1':
                KP = np.kron(KP, q1)
            case '+':
                KP = np.kron(KP, qp)
            case '-':
                KP = np.kron(KP, qm)
            case 'i':
                KP = np.kron(KP, qpi)
            case 'j':
                KP = np.kron(KP, qmi)
            
    return (KP)