#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 11:01:55 2024

@author: jm
"""

import math
import numpy         as np
from   numpy.linalg  import eigh
from   Sim_Exec_Init import Qubit_Setting

Tolerance = 1e-10

def Schmidt_Decomp_Entropy (NbQubits, Phi, A, B, Trace):

    M    = 2**len(A)
    N    = 2**len(B)
    Mat  = np.zeros((M, N), dtype=np.complex128)
    
    for i in range (M):
        for j in range (N):
            ba = bin(i)[2:]
            ba = ba.zfill(len(A))
            bb = bin(j)[2:]
            bb = bb.zfill(len(B))
            
            Vect = np.zeros(M + N,  dtype=str)
            
            for k in range(len(A)):
                Vect[A[k]] = str(ba[k])
            for k in range(len(B)):
                Vect[B[k]] = str(bb[k])
                
            KP = Qubit_Setting (Vect)
            
            Mat[i][j] = KP @ Phi
            
    MatDag                      = np.conj(Mat).T
    (Eigenvalues, eigenvectors) = eigh (Mat @ MatDag)
    Eigenvalues                 = sorted(Eigenvalues, reverse=True)
    
    Entropy   = 0.0
    Rank      = 0
    
    for i in range(len(Eigenvalues)):
        if Eigenvalues[i] < Tolerance:
            Eigenvalues[i] = 0.0
        else:
            if (1-Eigenvalues[i]) < Tolerance:
                Eigenvalues[i] = 1.0
            Entropy = Entropy - Eigenvalues[i] * math.log2(Eigenvalues[i])
            Rank    = Rank + 1
    
    return (Rank, Entropy) 