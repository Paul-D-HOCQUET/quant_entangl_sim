#!/usr/bin/env python3
from   Sim_Exec_PorteDEUX   import Porte_DeuxQubits_Param
import pennylane as qml
import numpy     as np
import math

#
#   Pennylane setup
#

Nbq = 4
dev = qml.device("default.qubit", wires=Nbq)

@qml.qnode(dev)

def IsingYY(phi, q1, q2, State):
    qml.AmplitudeEmbedding(features=State, wires=range(Nbq))
    qml.IsingYY(phi, wires=[q1, q2])
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

for q1 in range(Nbq):
    for q2 in range(Nbq):
        if q1 != q2 :
            etat_penny      = IsingYY (2*(3 * math.pi / 4), q1, q2, State)    
            etat_simul      = Porte_DeuxQubits_Param (Nbq, State, 'YY', q1, q2, eval("3 * math.pi / 4"))
    
            for i in range(2**Nbq):
                som = som + abs(etat_penny[i] - etat_simul[i])**2

print("YY: ", som)