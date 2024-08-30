#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 21:31:15 2024

@author: jm
"""

from   Sim_Tools import SWAPab

def Porte_Mesure (N, Phi, gate, qbno):
    
    #
    #   Swap entre le qubit sur lequel la masure doit etre appliquee avec le premier qubit 0 
    #  
   
    Phi = SWAPab(N, Phi, qbno, 0)
    
    #               
    #   Mesurer le premier qubit
    #
    
    
    
    
    #
    #   Swap entre le qubit sur lequel la masure doit etre appliquee avec le premier qubit 0 
    #  
    
    Phi = SWAPab(N, Phi, qbno, 0)
    
    return (Phi)