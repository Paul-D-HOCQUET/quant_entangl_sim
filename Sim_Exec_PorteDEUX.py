#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 08:16:23 2023

@author: jm
"""

import math
import numpy as np
from   Sim_Tools import SWAPab, Mult

#
#       Portes a deux qubits et leur matrice
#       Attention les 4 premieres peuvent etre utilisees avec des Control-qubits.
#

DQ_Gates      = ["SW", "SWr", "SWi", "SWir", "CX", "NC", "CY", "CZ", "CS", "CT", "CH"]
CDQ_Gates     = 4  # seulement les quatre premières pourraient etre controlles -- PAS FAIT

G2 = np.array(
[         np.array ([[1. + 0j, 0. + 0j, 0. + 0j, 0. + 0j],   [0. + 0j, 0. + 0j, 1. + 0j, 0. + 0j],
                     [0. + 0j, 1. + 0j, 0. + 0j, 0. + 0j],   [0. + 0j, 0. + 0j, 0. + 0j, 1. + 0j]]),     # SW  - SWAP
          np.array ([[1. + 0j, 0. + 0j, 0. + 0j, 0. + 0j],   [0. + 0j, 0.5 + 0.5j, 0.5 -0.5j, 0. + 0j], 
                     [0. + 0j, 0.5 - 0.5j, 0.5 + 0.5j, 0. + 0j], [0. + 0j, 0. + 0j, 0. + 0j, 1. + 0j]]), # SWr - racine carre SWAP
          np.array ([[1. + 0j, 0. + 0j, 0. + 0j, 0. + 0j],   [0. + 0j, 0. + 0j, 0. + 1j, 0. + 0j],
                     [0. + 0j, 0. + 1j, 0. + 0j, 0. + 0j],   [0. + 0j, 0. + 0j, 0. + 0j, 1. + 0j]]),     # SWi - iSWAP
          np.array ([[1. + 0j, 0. + 0j, 0. + 0j, 0. + 0j],   [0. + 0j, 1/math.sqrt(2) + 0j, complex(0., 1/math.sqrt(2)), 0. + 0j],
                     [0. + 0j, complex(0., 1/math.sqrt(2)), 1/math.sqrt(2) + 0j, 0. + 0j], [0. + 0j, 0. + 0j, 0. + 0j, 1. + 0j]]),   # SWir - racine carre iSWAP
          np.array ([[1. + 0j, 0. + 0j, 0. + 0j, 0. + 0j],   [0. + 0j, 1. + 0j, 0. + 0j, 0. + 0j],
                     [0. + 0j, 0. + 0j, 0. + 0j, 1. + 0j],   [0. + 0j, 0. + 0j, 1. + 0j, 0. + 0j]]),     # CX
          np.array ([[0. + 0j, 1. + 0j, 0. + 0j, 0. + 0j],   [1. + 0j, 0. + 0j, 0. + 0j, 0. + 0j],
                     [0. + 0j, 0. + 0j, 1. + 0j, 0. + 0j],   [0. + 0j, 0. + 0j, 0. + 0j, 1. + 0j]]),     # NC  - Not CX
          np.array ([[1. + 0j, 0. + 0j, 0. + 0j, 0. + 0j],   [0. + 0j, 1. + 0j, 0. + 0j, 0. + 0j],
                     [0. + 0j, 0. + 0j, 0. + 0j, 0. - 1j],   [0. + 0j, 0. + 0j, 0. + 1j, 0. + 0j]]),     # CY
          np.array ([[1. + 0j, 0. + 0j, 0. + 0j, 0. + 0j],   [0. + 0j, 1. + 0j, 0. + 0j, 0. + 0j],
                     [0. + 0j, 0. + 0j, 1. + 0j, 0. + 0j],   [0. + 0j, 0. + 0j, 0. + 0j,-1. + 0j]]),     # CZ
          np.array ([[1. + 0j, 0. + 0j, 0. + 0j, 0. + 0j],   [0. + 0j, 1. + 0j, 0. + 0j, 0. + 0j],
                     [0. + 0j, 0. + 0j, 1. + 0j, 0. + 0j],   [0. + 0j, 0. + 0j, 0. + 0j, 0. + 1j]]),     # CS
          np.array ([[1. + 0j, 0. + 0j, 0. + 0j, 0. + 0j],   [0. + 0j, 1. + 0j, 0. + 0j, 0. + 0j],
                     [0. + 0j, 0. + 0j, 1. + 0j, 0. + 0j],   [0. + 0j, 0. + 0j, 0. + 0j, complex (math.cos(math.pi/4.0), math.sin(math.pi/4.0))]]),     # CT
          np.array ([[1. + 0j, 0. + 0j, 0. + 0j, 0. + 0j],   [0. + 0j, 1. + 0j, 0. + 0j, 0. + 0j],
                     [0. + 0j, 0. + 0j, 1/math.sqrt(2) + 0j, 1/math.sqrt(2) + 0j],   [0. + 0j, 0. + 0j, 1/math.sqrt(2) + 0j, -1/math.sqrt(2) + 0j]])]     # CH
       )
    
#
#   Executer la porte gate sur deux qubits (sans parametre sauf no qubits)
#

def Porte_DeuxQubits (N, Phi, gate, qa, qb):
 
   
    ind = DQ_Gates.index(gate) 
    
    #
    #   Swap entre les qubits pour que qa = N-2 (control) et qb = N-1. Appliquer alors la porte sur ces qubits 
    #
    
    if (qb == N-1):
        Phi = SWAPab (N, Phi, qa, N-2)
        Phi = Mult   (N, Phi, 0, 2, G2[ind])
        Phi = SWAPab (N, Phi, qa, N-2)
    elif (qa == N-1):
        Phi = SWAPab (N, Phi, qa, qb)
        Phi = SWAPab (N, Phi, qb, N-2)
        Phi = Mult   (N, Phi, 0, 2, G2[ind])
        Phi = SWAPab (N, Phi, qb, N-2)
        Phi = SWAPab (N, Phi, qa, qb)
    else:
        Phi = SWAPab (N, Phi, qb, N-1)
        Phi = SWAPab (N, Phi, qa, N-2)
        Phi = Mult   (N, Phi, 0, 2, G2[ind])
        Phi = SWAPab (N, Phi, qa, N-2)
        Phi = SWAPab (N, Phi, qb, N-1)
    return (Phi)
            

#
#   Executer la porte gate sur deux qubits avec parametre Theta (rotation)
#

def Porte_DeuxQubits_Param (N, Phi, gate, qa, qb, theta):
                
    sin = math.sin(theta)
    cos = math.cos(theta)
    
    match gate:
        case 'XX':
            G = np.array ([[ complex(cos, 0),   0. + 0j,   0. + 0j,   complex(0,-sin)], 
                           [ 0. + 0j,   complex(cos, 0),   complex(0,-sin),   0. + 0j],
                           [ 0. + 0j,   complex(0,-sin),   complex(cos, 0),   0. + 0j],
                           [ complex(0,-sin),   0. + 0j,   0. + 0j,   complex(cos, 0)]])

        case 'YY':
            G = np.array ([[ complex(cos, 0),   0. + 0j,   0. + 0j,   complex(0, sin)], 
                           [ 0. + 0j,   complex(cos, 0),   complex(0,-sin),   0. + 0j],
                           [ 0. + 0j,   complex(0,-sin),   complex(cos, 0),   0. + 0j],
                           [ complex(0, sin),   0. + 0j,   0. + 0j,   complex(cos, 0)]])
        case 'XY':
            G = np.array ([[ 1. + 0j,   0. + 0j,   0. + 0j,   0. + 0j], 
                           [ 0. + 0j,  complex(cos, 0),  complex(0, sin),   0. + 0j],
                           [ 0. + 0j,  complex(0, sin),  complex(cos, 0),   0. + 0j],
                           [ 0. + 0j,   0. + 0j,   0. + 0j,   1. + 0j]])
                
        case 'ZZ':
            G = np.array ([[ complex(cos, -sin),  0. + 0j,   0. + 0j,   0. + 0j], 
                           [ 0. + 0j,  complex(cos, sin),   0. + 0j,   0. + 0j],
                           [ 0. + 0j,   0. + 0j,  complex(cos, sin),   0. + 0j],
                           [ 0. + 0j,   0. + 0j,   0. + 0j,  complex(cos, -sin)]])

        #
        #   Swap entre les qubits pour que a = 0 et b = 1. Appliquer alors la porte sur ces qubits 
        #
        
    if (qb == N-1):
        Phi = SWAPab (N, Phi, qa, N-2)
        Phi = Mult   (N, Phi, 0, 2, G)
        Phi = SWAPab (N, Phi, qa, N-2)
    elif (qa == N-1):
        Phi = SWAPab (N, Phi, qa, qb)
        Phi = SWAPab (N, Phi, qb, N-2)
        Phi = Mult   (N, Phi, 0, 2, G)
        Phi = SWAPab (N, Phi, qb, N-2)
        Phi = SWAPab (N, Phi, qa, qb)
    else:
        Phi = SWAPab (N, Phi, qb, N-1)
        Phi = SWAPab (N, Phi, qa, N-2)
        Phi = Mult   (N, Phi, 0, 2, G)
        Phi = SWAPab (N, Phi, qa, N-2)
        Phi = SWAPab (N, Phi, qb, N-1)

    return (Phi)