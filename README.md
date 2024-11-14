# Quantum circuits simulator featuring entanglement measurement

This simulator is the result of a master's degree project.

## Another quantum circuit simulator ?

While learning quantum computing, I tinkered a lot with big compagnies' quantum simulators. They were all fancy and ergonomic but none of them actually introduced any data about entanglement. Yet, entanglement is fundamental to quantum computing that I was confused to have no information about it in existing simulators.
This simulator trades the Measurment gate for a gate-by-gate entanglement measure based on the Von Neumann entropy.

## Dissertation
This project is associated with a dissertation, redacted in French and available in the repository.

## Installation

Download the archive of the repository, extract it somewhere rememberable on your device and open it in the IDE of your choice.

## Usage
To start the simulator, excecute `P_Draw_Schmidt.py`.<br />
To edit the simulated circuit, modify the file path in `P_Simulation.py` to the `.txt` file of the circuit you want to simulate.<br />
The text file must respect a designated syntax :
### Initialization line
Starts with "N", then precises the number of qubits and their initial states. <br />
For example : `N 4 0 0 0 1` initializes a 4-qubits circuit where the three first are in the $\ket{0}$ state and the last one is in the $\ket{1}$ state.<br />
Supported initial states : 
- `0` = $\ket{0}$
- `1` = $\ket{1}$
- `+` = $\frac{1}{\sqrt{2}}\ket{0} + \frac{1}{\sqrt{2}}\ket{1}$
- `-` = $\frac{1}{\sqrt{2}}\ket{0} - \frac{1}{\sqrt{2}}\ket{1}$
- `i` = $\frac{1}{\sqrt{2}}\ket{0} + \frac{i}{\sqrt{2}}\ket{1}$
- `j` = $\frac{1}{\sqrt{2}}\ket{0} - \frac{i}{\sqrt{2}}\ket{1}$
### Gate line
After being initialized, indicate the gates that compose the circuit. <br />
A gate line is composed of the code letter of the designated gate and the target qubit(s).<br />
Supported gates :
#### Single qubit gates
- `I` : Identity gate
- `X` : NOT gate
- `Y` : Y gate
- `Z` : Z gate
- `H` : Hadamard gate
- `P`, `S`, `SRZ` : P gate (or S gate or $\sqrt{Z}$ gate)
- `T` : T gate
- `SRX` : $\sqrt{X}$ gate
- `SRY` : $\sqrt{Y}$ gate<br />
For example : `H 2` applies an Hadamard gate to the #2 qubit.
#### Controlled gates
- `CX` : Controlled-NOT gate
- `NC` : Not C-NOT gate
- `CY` : Controlled-Y gate
- `CZ` : Controlled-Z gate
- `CS` : Controlled-S gate
- `CT` : Controlled-T gate
- `CH` : Controlled Hadamard gate<br />
For example : `CX 0 3` applies a C-NOT gate to the #3 qubit controlled by the #0 qubit.
#### Two qubits gates
- `SW` : SWAP gate
- `SWr` : $\sqrt{SWAP}$ gate
- `SWi` : $i$ SWAP gate
- `SWir` : $\sqrt{iSWAP}$ gate<br />
For example : `SWi 0 1` applies a $i$ SWAP gate between the #0 and the #1 qubits.
#### Parameterized gates
- `RTX` : $R_{x}(\theta)$ X-rotation gate
- `RTY` : $R_{y}(\theta)$ Y-rotation gate
- `RTZ` : $R_{z}(\theta)$ Z-rotation gate 
- `XX` : $R_{xx}(\theta)$
- `YY` : $R_{yy}(\theta)$
- `XY` : $R_{xy}(\theta)$
- `ZZ` : $R_{zz}(\theta)$<br />
For example : `RTY 1 "3 * math.pi / 4"` applies a $R_{y}(\theta)$ gate on the #1 qubit where $\theta = \frac{3\pi}{4}$.

## Intellectual property rights
The simulator is the proprety of Mr. Paul Deschildre Hocquet and Mr. Jean-Marc Robert solely.<br />
The dissertation is the proprety of Mr. Paul Deschildre Hocquet, protected by l'Ecole de Technologie Supérieure.

## Additional notes
This program is far from being fully optimized and secured. As it is only a end-of-master's project, dedication was focused on the features rather than the code itself.
