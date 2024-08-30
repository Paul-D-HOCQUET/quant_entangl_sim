#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 20:07:35 2024

@author: jm
"""

from Sim_Exec_PorteUN        import Porte_UnQubit, Porte_UnQubit_Param
from Sim_Exec_PorteDEUX      import Porte_DeuxQubits, Porte_DeuxQubits_Param
from Sim_Exec_CTRL           import CTRL
from Sim_Exec_Init           import Qubit_Setting
from Sim_Exec_Measure        import Porte_Mesure
from Sim_Comp_Intrication    import Von_Neumann_Entropy
from Sim_Comp_Schmidt        import Schmidt_Decomp_Entropy
from A_Partition_Generator   import Von_Neumann_Partitions

import numpy as np

def sumprob (N, Phi):
    s = 0.0
    for i in range(2**N):
        s  = s + abs(Phi[i])**2
    return s
    
def Exec_Circuit (NbQubits, Desc, A, B, Trace):
    global Phis
    Phis = []
    Rank_VN    = np.zeros(len(Desc), dtype=int)
    Entropy_VN = np.zeros(len(Desc), dtype=float)
    Rank_SD    = np.zeros(len(Desc), dtype=int)
    Entropy_SD = np.zeros(len(Desc), dtype=float)
    Max_Schmidt_Ranks = []
    Min_Schmidt_Ranks = []
    Max_VN_Entropy = []
    Min_VN_Entropy = []
    
    for i in range (len(Desc)):
        gate = Desc[i][0]
        match gate:  
            case 'N' :  
                Values = Desc[i][2]
                Phi    = Qubit_Setting (Values)  
                
            case 'I' | 'X'  | 'Y' | 'Z' | 'H' | 'S' | 'T' | 'SRX'  | 'SRY' | 'SRZ' :
                Liste = Desc[i][1]
                for j in range(len(Liste)):
                    Phi = Porte_UnQubit (NbQubits, Phi, gate, Liste[j])
                    
            case 'RTX' | 'RTY' | 'RTZ' :
                Liste = Desc[i][1]
                Phi   = Porte_UnQubit_Param (NbQubits, Phi, gate, Liste[0], Liste[1])
                
            case 'CX' | 'NC' | 'CY' | 'CZ' |'CS' | 'CT' | 'CH' | 'SW' | 'SWr' | 'iSW' | 'iSWr' :
                Liste = Desc[i][1]
                Phi   = Porte_DeuxQubits (NbQubits, Phi, gate, Liste[0], Liste[1])
                
            case 'XX' | 'YY' | 'XY' | 'ZZ' :
                Liste = Desc[i][1]
                Phi   = Porte_DeuxQubits_Param (NbQubits, Phi, gate, Liste[0], Liste[1], Liste[2])
            
            case 'C':
                controlled_gate = Desc[i][1]
                match controlled_gate:
                    case 'X'  | 'Y' | 'Z' | 'H' | 'P' | 'S' | 'T' | 'SRX'  | 'SRY' | 'SRZ' :
                        Liste = Desc[i][2]
                        CTRL (NbQubits, Phi, controlled_gate, Liste[0:len(Liste)-1], Liste[len(Liste)-1:])
                    case 'SW' | 'SWr' | 'SWi' | 'SWir' :
                        Liste = Desc[i][2]
                        CTRL (NbQubits, Phi, controlled_gate, Liste[0:len(Liste)-2], Liste[len(Liste)-2:])
            
            case 'MX', 'MY', 'MZ':
                Liste = Desc[i][1]
                Phi   = Porte_Mesure (NbQubits, Phi, gate, Liste[0])
        
        if (Trace):
            print("No %3d  Gate %5s  Sum prob %4.2f " % (i, gate, sumprob (NbQubits, Phi)))
                        
        (Rank_VN[i], Entropy_VN[i]) = Von_Neumann_Entropy    (NbQubits, Phi, A, B)  
        (Rank_SD[i], Entropy_SD[i]) = Schmidt_Decomp_Entropy (NbQubits, Phi, A, B, False)
        Phis.append(Phi)
        V_N_Partitions = Von_Neumann_Partitions(Phi)
        #print(V_N_Partitions)
        max_schmidt    = max(partition[2][0] for partition in V_N_Partitions)
        min_schmidt    = min(partition[2][0] for partition in V_N_Partitions)
        max_vn_entropy    = max(partition[2][1] for partition in V_N_Partitions)
        min_vn_entropy    = min(partition[2][1] for partition in V_N_Partitions)
        Max_Schmidt_Ranks.append(max_schmidt)
        Min_Schmidt_Ranks.append(min_schmidt)
        Max_VN_Entropy.append(max_vn_entropy)
        Min_VN_Entropy.append(min_vn_entropy)
        #print(V_N_Partitions)
        #print("Entangled : ", entangled, "| Separable : ", separable)
        
    #print('end exec : ', len(Phis))
        #print("|----------------------------------------------|")
    return (Phis, Rank_VN, Entropy_VN, Rank_SD, Entropy_SD, Max_Schmidt_Ranks, Min_Schmidt_Ranks, Max_VN_Entropy, Min_VN_Entropy)