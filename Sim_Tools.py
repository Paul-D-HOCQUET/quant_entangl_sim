#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 08:16:23 2023

@author: jm
"""

import numpy as np
import math

def ParseParam_Integers (N, param, NbLign):
    
    Hash = np.zeros(N, dtype=int)
    Liste = []
    err   = False
    
    for i in range(len(param)):
        if param[i].isdigit():
            val = int(param[i])
            if (val < N):
                if (Hash[val] != 0):
                    print ('Erreur - Entier deja utilise - Ligne %d' % (NbLign))
                    err = True
                else:
                    Hash[val] = 1
                    Liste.append( val )
            else:
                print ('Erreur - Entier trop grand - Ligne %d' % (NbLign))
                err = True
                break
        else:
            print ('Erreur - Parametre non entier - Ligne %d' % (NbLign))
            err = True
            break
    
    return (err, Liste)

def ParseParam_NbInt_OneReal (N, Nb, param, NbLign):
    
    Liste = []
    err   = False
    
    if (len(param) != Nb+1):
        print ('Erreur - Nombre de parametres attendus DEUX - Ligne %d' % (NbLign))
        err = True
    else:
        for i in range(Nb):
            if param[i].isdigit():
                if (int(param[i]) < N):
                    Liste.append( int(param[i]) )
                else:
                    print ('Erreur - Entier trop grand - Ligne %d' % (NbLign))
                    err = True
                    break
            else:
                print ('Erreur - Parametre non entier - Ligne %d' % (NbLign))
                err = True
                break
            
        if Nb == 2:
            if Liste[0] == Liste[1]:
                 print ('Erreur - deux qubits egaux - Ligne %d' % (NbLign))
                 err = True
        
        if not err:
            try:
                str_theta = param[Nb]
                theta = eval(str_theta[1:-1])
                Liste.append (theta )
            except ValueError:
                print ('Erreur - Un numero de qubit (entier) et theta (reel) - Ligne %d' % (NbLign))
                err = True
    
    return (err, Liste)

#
#   Permuter les qubits a et b -- parametres a < b sont valides. 
#

def SWAPab (N, Phi, a, b):
    
    a = N-1-a
    b = N-1-b
    if (a == b):
        return Phi
    else:
        Perm = np.zeros(2**N, dtype=int)
        PhiP = np.zeros(2**N, dtype=complex)
        
        da = 2**a
        db = 2**b       
        
        for i in range (2**N):
            ba = 1 if (i & da != 0) else 0
            bb = 1 if (i & db != 0) else 0           
            if (ba == bb):
                Perm[i] = i
            else:
                Perm[i] = i + (-1)**ba * da + (-1)**bb * db
         
        for i in range(2**N):
            PhiP[i] = Phi[ Perm[i] ]
            
        return PhiP
    
#
#   Multiplier (I x I x ... x I x P) |Phi> ou P est une porte sur les d derniers qubits.
#   P est definie par une matrice 2^d x 2^d complexes. Peu de gain si d est tres grand.
#
#   Cas particulier: k indique le nombre de qubits controlant la porte P. 
#   Ces qubits precedent les derniers qubits transformes par la porte P.
#   Si k = 0, pas de qubit de controle.  Maximum k = N - d.
#  

def Mult (N, Phi, k, d, P):
    
    PhiP = np.zeros(2**N, dtype=complex)
    for i in range (2**N):
        PhiP[i] = Phi[i]

    for i in range (2**(N-(d+k))):
        #
        #   Multiplication de la matrice de P et du sous-vecteur de Phi (2^d positions)
        #
        for l in range (2**d):
            somme = 0 + 0j
            for c in range (2**d):
                somme = somme + P[l][c] * Phi[(i+1) * 2**(d+k) - 2**d + c]
            
            PhiP [(i+1) * 2**(d+k) - 2**d + l] = somme
            
    return PhiP