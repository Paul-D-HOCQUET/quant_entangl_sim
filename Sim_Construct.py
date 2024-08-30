#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 09:43:33 2024

@author: jm
"""

import re
from Sim_Tools import ParseParam_Integers, ParseParam_NbInt_OneReal

def Construct_Circuit(filename, MaxQubits):
    file    = open(filename,'r')
    
    NbQubits = 0
    NbLign   = 0
    Desc     = []
    err      = False
    
    while ((ligne := file.readline()) and (not err)):
        
        NbLign = NbLign + 1
    #
    # Ignorer les commentaires
    #
        if (ligne[0] != '#'): 
            pattern = re.compile(r'\w+|\+|\-|\"[A-Za-z0-9\s.\+\-\*\/\(\)]*\"' )
            param   = pattern.findall(ligne)
            #
            # Ignorer les lignes blanches.
            #
            if (param):
                gate = param.pop(0)
                if (NbQubits == 0):
                    if (gate != 'N'):
                        print('Erreur - Le nombre de qubits N doit etre defini sur la premiere ligne')
                        err = True 
                    else:
                        if (not param[0].isdigit()):
                                print('Erreur - Le nombre de qubits N doit etre entier')
                                err = True
                        else:
                            
                            if (int(param[0]) > MaxQubits):
                                print('Erreur - Le nombre de qubits N est trop grand - max %d' % MaxQubits)
                                err = True
                            else:
                                NbQubits = int(param[0])
                                param.pop(0)
                                
                                if len(param) != NbQubits:
                                    print('Erreur - Le nombre de valeurs de qubits pas equal a N')
                                    err = True
                                else:
                                    for i in range(len(param)):
                                        match param[i]:
                                            case '0' | '1' | '+' | '-' | 'i' | 'j' :
                                                pass
                                            case _:
                                                print('Erreur - Valeur initiale qubit erronée 0 1 + - i j (seulement --> j = -i)')
                                                err = True
                                                break
                                    if not err:
                                        Desc.append(['N', NbQubits, param])
                else:
                    match gate:                                
                        case 'HT':
                            #
                            #   Initialiser l'etat avec une tour de Hadamard.
                            #   all : tous les qubits
                            #
                            if len(param) == 0:
                                Liste = []
                                for i in range (NbQubits):
                                    Liste.append(i)
                                Desc.append(['H', Liste])
                            else:
                                print('Erreur - Aucun parametre pour cette porte - Ligne %d' % (NbLign))
                                err = True
                                
                        case 'I' | 'X'  | 'Y' | 'Z' | 'H' | 'S' | 'T' | 'SRX'  | 'SRY' | 'SRZ' :
                            #
                            #   Portes classiques à un qubit. Optimisation: Plusieurs portes independentes sur des qubits differents
                            #
                            
                            (err, Liste) = ParseParam_Integers(NbQubits, param, NbLign)
                            if not err:
                                Desc.append([gate, Liste])
                        
                        case 'RTX' | 'RTY' | 'RTZ':
                            #
                            #   Portes à un qubit avec parametre Theta (angle -- entre guillement)
                            #
                            
                            (err, Liste) = ParseParam_NbInt_OneReal (NbQubits, 1, param, NbLign)
                            if not err:
                                Desc.append([gate, Liste])
                            
                        case 'CX' | 'NC' | 'CY' | 'CZ' |'CS' | 'CT' | 'CH' | 'SW' | 'SWr' | 'SWi' | 'SWir':
                            #
                            #   Portes de controle a deux qubits (porte sur le deuxieme qubit)
                            #   Porte SWAP permutant deux qubits (et ses variantes)
                            #
                            
                            (err, Liste) = ParseParam_Integers(NbQubits, param, NbLign)
                            if not err:
                                if len(Liste) > 2:
                                    print('Erreur - Plus de deux parametres pour cette porte - Ligne %d' % (NbLign))
                                else:
                                    Desc.append([gate, Liste])
                        
                        case 'XX' | 'YY' | 'XY' | 'ZZ':
                            #
                            #   Portes a deux qubits avec un parametre Theta (angle -- real 3.0 ou 3.1415)
                            #
                            
                            (err, Liste) = ParseParam_NbInt_OneReal (NbQubits, 2, param, NbLign)
                            if not err:
                                Desc.append([gate, Liste])
                                
                        case 'C':
                            #
                            #   Portes de controle a k qubits sur d qubits (sans parametre)
                            #   Exemple: Porte Toffoli CCNOT 2 qubits de controle pour un CNOT sur 1 qubit  - VERIFIEE
                            #   Exemple: Porte Fredkin CSWAP 1 qubit  de controle pour un SWAP sur 2 qubits - VERIFIEE
                            #
                            
                            StrG = param.pop(0)
                            
                            match StrG:
                                case 'I' | 'X'  | 'Y' | 'Z' | 'H' | 'P' | 'S' | 'T' | 'SRX'  | 'SRY' | 'SRZ' :
                                    (err, Liste) = ParseParam_Integers(NbQubits, param, NbLign)
                                    if len(Liste) < 2:
                                        print('Erreur - Au moins DEUX parametres pour cette porte - Ligne %d' % (NbLign))
                                        err = True
                                    else:
                                        Desc.append(['C', StrG, Liste])
                                    
                                case 'SW' | 'SWr' | 'iSW' | 'iSWr' :
                                    (err, Liste) = ParseParam_Integers(NbQubits, param, NbLign)
                                    if len(Liste) < 3:
                                        print('Erreur - Au moins TROIS parametres pour cette porte - Ligne %d' % (NbLign))
                                        err = True
                                    else:
                                        Desc.append(['C', StrG, Liste])
                                    
                                case  _ :
                                    print('Erreur - Porte %s inconnue - Ligne %d' % (StrG, NbLign))
                                    err = True 

                        
                        case 'MX', 'MY', 'MZ':
                            #
                            #   Portes de mesure : MX, MY et MZ et un numéro de qubit
                            #
                            (err, Liste) = ParseParam_Integers(NbQubits, param, NbLign)
                            if not err:
                                if len(Liste) > 1:
                                    print('Erreur - Plus d un parametre pour cette porte - Ligne %d' % (NbLign))
                                else:
                                    Desc.append([gate, Liste])
                            
                        case  _:
                            print('Erreur - Porte %s inconnue - Ligne %d' % (gate, NbLign))
                            err = True 
    
    file.close()
    return (err, NbQubits, Desc)