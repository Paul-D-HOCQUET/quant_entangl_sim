#!/usr/bin/env python3
from   Sim_Exec_PorteUN   import Porte_UnQubit
from   Sim_Exec_PorteDEUX import Porte_DeuxQubits
import pennylane as qml
import numpy     as np
import math

#
#   Pennylane setup
#

Nbq = 3
dev = qml.device("default.qubit", wires=Nbq)

@qml.qnode(dev)

def Circuit(Nbq):
    qml.BasisState([0, 0, 0], wires=[0, 1, 2])
    
    qml.Hadamard(wires=1)
    
    # qml.CNOT(wires=[3, 2])

    # qml.PauliX(wires=1)
    
    # qml.PauliX(wires=0)

    return qml.state()

#
#   Preparation d'un état très asymétrique normalisé
#

etat_my = np.array([complex(1,0), complex(0,0)])
etat_my = np.kron(etat_my, [complex(1,0), complex(0,0)])
etat_my = np.kron(etat_my, [complex(1,0), complex(0,0)])

etat_penny      = Circuit (Nbq)   
print("Penny")
print(etat_penny)

#
#   Somme sur tous les tests
#

etat_my      = Porte_UnQubit (Nbq, etat_my, 'H', 1)
print("MY")
print(etat_my)
    
# q1 = 0
# q2 = 1     
# etat_simul      = Porte_DeuxQubits (Nbq, etat_simul, 'CX', 0, 1)
# print(etat_simul)

# q = 2   
# etat_simul      = Porte_UnQubit (Nbq, etat_simul, 'X', 2)
# print(etat_simul)

# q = 3     
# etat_simul      = Porte_UnQubit (Nbq, etat_simul, 'X', 3)
# print(etat_simul)

    
# som      = 0.0
# for i in range(2**Nbq):
#     som = som + abs(etat_penny[i] - etat_simul[i])**2

# print("Circuit: ", som)