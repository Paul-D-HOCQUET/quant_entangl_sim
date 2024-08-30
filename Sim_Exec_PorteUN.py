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
#       Portes a un qubit et leur matrice
#

UQ_Gates = ["I", "X", "Y", "Z", "H", "P", "S", "T",
            "SRX", "SRY", "SRZ"]

G1 = np.array(
        [ np.array ([[1 + 0j, 0 + 0j], [0 + 0j,  1 + 0j]]),         # I
          np.array ([[0 + 0j, 1 + 0j], [1 + 0j,  0 + 0j]]),         # X
          np.array ([[0 + 0j, 0 - 1j], [0 + 1j,  0 + 0j]]),         # Y
          np.array ([[1 + 0j, 0 + 0j], [0 + 0j, -1 + 0j]]),         # Z
          np.array ([[1/math.sqrt(2) + 0j, 1/math.sqrt(2) + 0j], [1/math.sqrt(2) + 0j, -1/math.sqrt(2) + 0j]]),  # H
          np.array ([[1 + 0j, 0 + 0j], [0 + 0j,  0 + 1j]]),         # P -- equiv S
          np.array ([[1 + 0j, 0 + 0j], [0 + 0j,  0 + 1j]]),         # S
          np.array ([[1 + 0j, 0 + 0j], [0 + 0j,  complex (math.cos(math.pi/4.0), math.sin(math.pi/4.0))]]),      # T
#          
          np.array ([[0.5 + 0.5j,  0.5 - 0.5j], [0.5 - 0.5j,  0.5 + 0.5j]]),   # SRX
          np.array ([[0.5 + 0.5j, -0.5 - 0.5j], [0.5 + 0.5j,  0.5 + 0.5j]]),   # SRY
          np.array ([[1   + 0j,      0 + 0j],   [0   + 0j,    0   + 1j ]])]    # SRZ -- equiv S
       )

#
#   Executer la porte gate sur un qubit (sans parametre sauf no qubit)
#

def Porte_UnQubit (N, Phi, gate, qbno):
            
    ind = UQ_Gates.index(gate) 

    #
    #   Swap entre le qubit sur lequel la porte doit etre appliquee avec le dernier qubit N-1 
    #  
    Phi = SWAPab(N, Phi, qbno, N-1)
    #               
    #   Appliquer la porte sur le dernier qubit
    #
    Phi = Mult (N, Phi, 0, 1, G1[ind])
    #
    #   Swap entre le premier qubit et le qubit original
    #
    Phi = SWAPab(N, Phi, qbno, N-1)

    return (Phi)

#
#   Executer la porte gate sur un qubit avec parametre Theta (rotation)
#

def Porte_UnQubit_Param (N, Phi, gate, qbno, theta):
            
    #
    #   Extraire le numero du qubit sur lequel la porte est appliquee
    #
    
    sin = math.sin(theta)
    cos = math.cos(theta)
    
    match gate:
        case "RTX":
            G = np.array ([[complex(cos, 0),  complex(0, -sin)], [ complex(0, -sin),  complex(cos, 0)]])
        case "RTY":
            G = np.array ([[complex(cos, 0),  complex(-sin, 0)], [complex(sin, 0),  complex(cos, 0)]])
        case "RTZ":
            G = np.array ([[ complex(cos, -sin),  0. + 0j], [0. + 0j,  complex(cos, sin)]])

    #
    #   Swap entre le qubit sur lequel la porte doit etre appliquee avec le dernier qubit. 
    #
    Phi = SWAPab(N, Phi, qbno, N-1)
    #
    #   Appliquer la porte sur le dernier qubit
    #
    Phi = Mult (N, Phi, 0, 1, G)
    #
    #   Swap entre le dernier qubit et le qubit original
    #
    Phi = SWAPab(N, Phi, qbno, N-1)
    
    return (Phi)