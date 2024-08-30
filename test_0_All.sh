#!/bin/bash
echo "Pauli gates"
python3 ./test_1_X.py
python3 ./test_1_Y.py
python3 ./test_1_Z.py

echo "Classical one qubit gates"
python3 ./test_1_H.py
python3 ./test_1_P.py
python3 ./test_1_S.py
python3 ./test_1_T.py

echo "Classical square roots of the above"
python3 ./test_1_SRX.py
python3 ./test_1_SRY.py
python3 ./test_1_SRZ.py

echo "Classical Rotations - one qubit"
python3 ./test_1p_RTX.py
python3 ./test_1p_RTY.py
python3 ./test_1p_RTZ.py

echo "Simple Control one qubit gates"
python3 ./test_2_CH.py
python3 ./test_2_CX.py
python3 ./test_2_CY.py
python3 ./test_2_CZ.py

echo "SWAP gates and their square roots"
python3 ./test_2_SW.py
python3 ./test_2_SWr.py
python3 ./test_2_SWi.py
python3 ./test_2_SWir.py

echo "Ising gates"
python3 ./test_2p_XX.py
python3 ./test_2p_YY.py
python3 ./test_2p_ZZ.py
python3 ./test_2p_XY.py

echo "Special Control - CSWAP (Fredkin) & Toffoli"
python ./test_Ctrl_SWAP.py
python ./test_Ctrl_Toffoli.py
