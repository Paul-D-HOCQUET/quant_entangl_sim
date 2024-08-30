#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: pdh
"""

from numpy.linalg import svd
import numpy as np
from math import sqrt
from numpy.linalg import svd, eig, inv
from scipy.linalg import logm
import pyqentangle

# -- NOTES --
#
# Qobj([]) declarer un etat
# tensor(etat1,etat2) obligatoire pour faire fonctionner les traces partielles
# U, D, VT = np.linalg.svd(matrice) decomposition de schmidt pour une matrice
# number_qubits = math.log2(Psi.dims[0][0])
# eigenvalues, eigenvectors = np.linalg.eig(matrice)

# Function to generate the B system depending on 
def Generator_System_B(nb_qbit, sysA) :
    sysB = []
    for q in range (nb_qbit) :
        if q not in sysA :
            sysB.append(q)
    return sysB

# Function to create binary strings with leading zeros
def Leading_Zero_Binary(num, length):
    return format(num, '0{}b'.format(length))

# Function to create matrixes of binary used to generate the initial matrix for the SVD
def Binary_Matrix(sys, nb_qbit_total) :
    # Definition of the number of qubits designated to the system
    nb_qbit_sys = len(sys)
    
    # Definition of an empty matrix
    M = np.empty(shape = (2**nb_qbit_sys, nb_qbit_total), dtype = str)

    # Because each qubit can be either 0 or 1, there is 2 power the number of qubits possible binary combination.
    # i.e for a 2 qubits system, there are 00, 01, 10 and 11 ==> 2**2 = 4 possible combinations
    for q in range (2**nb_qbit_sys) :

        # Generation of each binary combination
        binary = str(Leading_Zero_Binary(q,nb_qbit_sys))

        # Append the generated binary in the row
        for b in range (len(binary)) :
            M[q][sys[b]] = binary[b]
    return M

def Tensor_Matrix(state, sysA, sysB) :
    # Definition of a bunch of variables
    nb_qbit = int(np.log2(state.shape[0]))
    matA = Binary_Matrix(sysA, nb_qbit)
    matB = Binary_Matrix(sysB, nb_qbit)
    nb_qbit_A = len(sysA)
    nb_qbit_B = len(sysB)

    # Definition of an empty amtrix
    M = np.empty(shape = (2**nb_qbit_A, 2**nb_qbit_B), dtype = complex)

    # For each binary combination of the system A / row index
    for a in range (2**nb_qbit_A) :
        # Creation of a row for the matrix M
        row = []

        # For each binary combination of the system B / columns index
        for  b in range (2**nb_qbit_B) :
            
            # With both row and column index, each individual value in the matrix can be identify
            # Creation of a container for the index of the amplitude
            index = []

            # Concatenation of both A and B binary to generate the ket index
            for q in range (nb_qbit) :
                if matA[a][q] == '' :
                    index.append(matB[b][q])
                else :
                    index.append(matA[a][q])
            index = ''.join(index)

            # Search of the amplitude associated with the ket index
            #print(state)
            amp = state[int(index,2)]
            
            # Append it to the row
            M[a][b] = amp
    return M

# Function to generate the Schmidt decomposition of a state using SVD
def Schmidt_Decomposition(state, sysA, sysB) :
    M = Tensor_Matrix(state, sysA, sysB)
    U, sigma, VT = svd(M, full_matrices=False)
    return U, sigma, np.transpose(VT)

# Function to calculate the entanglement using the Von Neumann's entropy
def Von_Neumann_Entropy(NbQubits, state, sysA, sysB) :
    # Create variables for entanglement and Schmidt rank
    entnglmnt = 0
    schmidt_rank = 0

    nb_qbit_A = len(sysA)
    nb_qbit_B = len(sysB)
    sys_size = True

    if (nb_qbit_A + nb_qbit_B != NbQubits) :
        sys_size = False

    if nb_qbit_A != 0 and nb_qbit_B != 0 and sys_size == True :
        # Store the decomposition
        U, sigma, VT = Schmidt_Decomposition(state, sysA, sysB)

        # Setting the tolerance to avoid very low approximations due to computer calculations
        tolerance = 1e-10
        sigma.real[abs(sigma) < tolerance] = 0.0

        # For all Schmidt coefficients in Sigma
        for s in sigma :
            # A coefficient is not a Schmidt coefficient if equal to 0
            if s != 0 :
                schmidt_rank = schmidt_rank + 1

                # The entanglement is calculated with the Von Neumann entropy : -(sigma**2) x log_2(sigma**2)
                entnglmnt = round(entnglmnt + (-1)*(s**2)*np.log2(s**2),3)
                if entnglmnt < tolerance :
                    entnglmnt = 0.0
    return schmidt_rank, entnglmnt

def Schmidt_Decomposition_Pyqentangle(state, sysA, sysB) :
    M = Tensor_Matrix(state, sysA, sysB)
    Sch_Decomp = pyqentangle.schmidt_decomposition(M)
    return Sch_Decomp

def Von_Neumann_Entropy_Pyqentangle(NbQubits, state, sysA, sysB) :
    rank = 0
    entanglement = 0

    nb_qbit_A = len(sysA)
    nb_qbit_B = len(sysB)
    sys_size = True

    if (nb_qbit_A + nb_qbit_B != NbQubits) :
        sys_size = False

    if nb_qbit_A != 0 and nb_qbit_B != 0 and sys_size == True :
        decomposition = Schmidt_Decomposition_Pyqentangle(state, sysA, sysB)
        tolerance = 1e-10
        for s in range (len(decomposition)) :
            schmidt_coeff = decomposition[s][0].real
            if schmidt_coeff > tolerance : 
                entanglement = entanglement + ((-1)*(schmidt_coeff**2)*(np.log2(schmidt_coeff**2)))
                rank = rank + 1
    return rank, entanglement

# Function to calculate the density matrix of a vector-shaped matrix
def Density_Matrix(state) :
    # Store the length of the state
    nb = len(state)
    ket = state

    # A bra is defined to be the transposed conjugate of ket
    bra = np.conjugate(np.reshape(ket, (1, nb)))

    # The density matrix is the matrix product between ket and bra
    rho = np.dot(ket, bra)
    return rho

# Function to calculate the log2 of a matrix
def Mat_Log2(matrix) :
    P, D, P_inv = Diagonalize(matrix)
    #print(D)
    log2_D = where(D == 0, D, log2(D))
    M = dot(P, dot(log2_D, P_inv))
    return M

# Function to generate the partial traces of both systems A and B
def Partial_Traces(state, sysA, sysB) :
    # Definition of variables for the system A, system B, the Schmidt decomposition and the number of Schmidt coefficients
    A = sysA
    B = sysB
    U, sigma, VT = Schmidt_Decomposition(state, A, B)
    nb_sigma = len(sigma)

    #
    # Partial trace of the A system
    #

    # Creation of an empty array for the partial trace of A
    U_row = np.shape(U)[0]
    U_col = nb_sigma
    rho_A = np.empty(shape = (U_row, U_row), dtype = complex)

    # Each column is a state part of the tensor
    for c in range (U_col) :

        # Each tensor is multiplied by the associated Schmidt coefficient squared
        s = sigma[c]

        # Creation of an empty ket 
        ket_U = np.empty(shape = (U_row, 1), dtype = complex)

        # Filling the empty ket
        for r in range (U_row) :
            ket_U[r] = U[r][c]

        # Calculating the density matrix 
        ket_bra_U = Density_Matrix(ket_U)

        # Calculating the tensored density matrix
        sigma_ket_bra_U = (s**2)*ket_bra_U

        # Adding this part of the tensor to the partial trace
        rho_A = rho_A + sigma_ket_bra_U

    #
    # Partial trace of the B system
    #

    # Creation of an empty array for the partial trace of A
    VT_row = np.shape(VT)[0]
    rho_B = np.empty(shape = (VT_row, VT_row), dtype = complex)
    VT_col = nb_sigma

    # Each column is a state part of the tensor
    for c in range (VT_col) :

        # Each tensor is multiplied by the associated Schmidt coefficient squared
        s = sigma[c]

        # Creation of an empty ket 
        ket_V = np.empty(shape = (VT_row, 1), dtype = complex)

        # Filling the empty ket
        for r in range (VT_row) :
            ket_V[r] = VT[r][c]

        # Calculating the density matrix 
        ket_bra_VT = Density_Matrix(ket_V)

        # Calculating the tensored density matrix
        sigma_ket_bra_VT = (s**2)*ket_bra_VT

        # Adding this part of the tensor to the partial trace
        rho_B = rho_B + sigma_ket_bra_VT
    return rho_A, rho_B

def Diagonalize(matrix) :
    eigenvalues, eigenvectors = eig(matrix)
    #if not all(iscomplex(eigenvalues)) :
    D = diag(eigenvalues)
    P = eigenvectors
    P_inv = inv(eigenvectors)
    return P, D, P_inv

def Von_Neumann_Partial_Trace(ptrace) :
    log2_ptrace = Mat_Log2(ptrace)
    VN_trace = - trace(dot(ptrace, log2_ptrace))
    return VN_trace