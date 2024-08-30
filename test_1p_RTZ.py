#!/usr/bin/env python3
from   Sim_Exec_PorteUN   import Porte_UnQubit_Param
import pennylane as qml
import numpy     as np
import math

#
#   Pennylane setup
#

Nbq = 4
dev = qml.device("default.qubit", wires=Nbq)

@qml.qnode(dev)

def RZ(phi, q, State):
    qml.AmplitudeEmbedding(features=State, wires=range(Nbq))
    qml.RZ(phi, wires=q)
    return qml.state()

#
#   Preparation d'un état très asymétrique normalisé
#

State = np.array([complex(1, -2), complex(-3, 4)])
norm  = math.sqrt (abs(State[0])**2 + abs(State[1])**2)
State = State / norm

for i in range(1, Nbq):
    q     = np.array([complex(2*i, -2*i+1), complex(-3*i, 3*i+1)])
    State = np.kron(State, q)

som = 0.0   
for i in range(2**Nbq):
    som = som + abs(State[i])**2

State = State / math.sqrt(som)


#
#   Début des tests
#

#
#   Somme sur tous les tests
#

som      = 0.0

for q in range(Nbq):
    #
    #   Facteur 2 entre Pennylane et Simulateur
    #
    etat_penny      = RZ (2*(3 * math.pi / 4), q, State)       
    etat_simul      = Porte_UnQubit_Param (Nbq, State, 'RTZ', q, eval("3 * math.pi / 4"))
    
    for i in range(2**Nbq):
        som = som + abs(etat_penny[i] - etat_simul[i])**2

print("RTZ: ", som)