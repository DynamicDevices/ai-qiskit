# SPDX-License-Identifier: Apache-2.0
"""
Basic Quantum Algorithm Examples

This module demonstrates fundamental quantum algorithms implemented
following Qiskit best practices.
"""

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import GroverOperator, MCMT, ZGate
import numpy as np
from typing import List, Optional, Tuple


def deutsch_jozsa_algorithm(oracle_function: str) -> QuantumCircuit:
    """
    Implement Deutsch-Jozsa algorithm.
    
    Args:
        oracle_function: Binary string representing the oracle function
                        (e.g., '0000' for constant 0, '1010' for balanced)
    
    Returns:
        QuantumCircuit: Deutsch-Jozsa circuit
    """
    n_qubits = len(oracle_function)
    
    # Create quantum registers
    qreg_input = QuantumRegister(n_qubits, 'input')
    qreg_ancilla = QuantumRegister(1, 'ancilla')
    creg = ClassicalRegister(n_qubits, 'c')
    
    circuit = QuantumCircuit(qreg_input, qreg_ancilla, creg, 
                           name=f'deutsch_jozsa_{n_qubits}')
    
    # Initialize ancilla qubit to |1⟩
    circuit.x(qreg_ancilla[0])
    
    # Apply Hadamard to all qubits
    circuit.h(qreg_input)
    circuit.h(qreg_ancilla[0])
    
    circuit.barrier()
    
    # Oracle implementation
    for i, bit in enumerate(oracle_function):
        if bit == '1':
            circuit.cx(qreg_input[i], qreg_ancilla[0])
    
    circuit.barrier()
    
    # Apply Hadamard to input qubits
    circuit.h(qreg_input)
    
    # Measure input qubits
    circuit.measure(qreg_input, creg)
    
    return circuit


def bernstein_vazirani_algorithm(secret_string: str) -> QuantumCircuit:
    """
    Implement Bernstein-Vazirani algorithm to find a secret string.
    
    Args:
        secret_string: Binary secret string (e.g., '1011')
    
    Returns:
        QuantumCircuit: Bernstein-Vazirani circuit
    """
    n_qubits = len(secret_string)
    
    qreg_input = QuantumRegister(n_qubits, 'input')
    qreg_ancilla = QuantumRegister(1, 'ancilla')
    creg = ClassicalRegister(n_qubits, 'c')
    
    circuit = QuantumCircuit(qreg_input, qreg_ancilla, creg,
                           name=f'bernstein_vazirani_{secret_string}')
    
    # Initialize ancilla to |1⟩
    circuit.x(qreg_ancilla[0])
    
    # Apply Hadamard to all qubits
    circuit.h(qreg_input)
    circuit.h(qreg_ancilla[0])
    
    circuit.barrier()
    
    # Oracle: apply CNOT for each '1' in secret string
    for i, bit in enumerate(reversed(secret_string)):  # Reverse for correct bit order
        if bit == '1':
            circuit.cx(qreg_input[i], qreg_ancilla[0])
    
    circuit.barrier()
    
    # Apply Hadamard to input qubits
    circuit.h(qreg_input)
    
    # Measure
    circuit.measure(qreg_input, creg)
    
    return circuit


def simon_algorithm(secret_string: str) -> QuantumCircuit:
    """
    Implement Simon's algorithm to find the secret string s such that f(x) = f(x ⊕ s).
    
    Args:
        secret_string: Binary secret string
    
    Returns:
        QuantumCircuit: Simon's algorithm circuit
    """
    n = len(secret_string)
    
    qreg_input = QuantumRegister(n, 'input')
    qreg_output = QuantumRegister(n, 'output')
    creg = ClassicalRegister(n, 'c')
    
    circuit = QuantumCircuit(qreg_input, qreg_output, creg,
                           name=f'simon_{secret_string}')
    
    # Apply Hadamard to input register
    circuit.h(qreg_input)
    
    circuit.barrier()
    
    # Oracle implementation (simplified for demonstration)
    # Copy input to output
    for i in range(n):
        circuit.cx(qreg_input[i], qreg_output[i])
    
    # Apply secret string transformation
    for i, bit in enumerate(secret_string):
        if bit == '1':
            circuit.cx(qreg_input[0], qreg_output[i])
    
    circuit.barrier()
    
    # Apply Hadamard to input register
    circuit.h(qreg_input)
    
    # Measure input register
    circuit.measure(qreg_input, creg)
    
    return circuit


def grover_algorithm(marked_items: List[str], num_iterations: Optional[int] = None) -> QuantumCircuit:
    """
    Implement Grover's search algorithm.
    
    Args:
        marked_items: List of binary strings representing marked items
        num_iterations: Number of Grover iterations (auto-calculated if None)
    
    Returns:
        QuantumCircuit: Grover's algorithm circuit
    """
    if not marked_items:
        raise ValueError("At least one marked item required")
    
    n_qubits = len(marked_items[0])
    N = 2 ** n_qubits  # Total number of items
    M = len(marked_items)  # Number of marked items
    
    # Calculate optimal number of iterations
    if num_iterations is None:
        num_iterations = int(np.pi / 4 * np.sqrt(N / M))
    
    qreg = QuantumRegister(n_qubits, 'q')
    creg = ClassicalRegister(n_qubits, 'c')
    
    circuit = QuantumCircuit(qreg, creg, name=f'grover_{n_qubits}_{M}')
    
    # Initialize superposition
    circuit.h(qreg)
    
    # Grover iterations
    for iteration in range(num_iterations):
        circuit.barrier(label=f'iteration_{iteration}')
        
        # Oracle: mark the target items
        for item in marked_items:
            # Apply X gates to flip qubits that should be 0
            for i, bit in enumerate(item):
                if bit == '0':
                    circuit.x(qreg[i])
            
            # Multi-controlled Z gate
            if n_qubits == 1:
                circuit.z(qreg[0])
            elif n_qubits == 2:
                circuit.cz(qreg[0], qreg[1])
            else:
                # Use multi-controlled Z gate
                mcz = MCMT(ZGate(), n_qubits - 1, 1)
                circuit.append(mcz, qreg)
            
            # Undo X gates
            for i, bit in enumerate(item):
                if bit == '0':
                    circuit.x(qreg[i])
        
        # Diffusion operator (inversion about average)
        circuit.h(qreg)
        circuit.x(qreg)
        
        if n_qubits == 1:
            circuit.z(qreg[0])
        elif n_qubits == 2:
            circuit.cz(qreg[0], qreg[1])
        else:
            mcz = MCMT(ZGate(), n_qubits - 1, 1)
            circuit.append(mcz, qreg)
        
        circuit.x(qreg)
        circuit.h(qreg)
    
    # Final measurement
    circuit.barrier()
    circuit.measure(qreg, creg)
    
    return circuit


def quantum_phase_estimation(unitary_circuit: QuantumCircuit, 
                           eigenstate_prep: QuantumCircuit,
                           precision_qubits: int = 4) -> QuantumCircuit:
    """
    Implement Quantum Phase Estimation algorithm.
    
    Args:
        unitary_circuit: Unitary operator U
        eigenstate_prep: Circuit to prepare eigenstate |ψ⟩
        precision_qubits: Number of qubits for phase precision
    
    Returns:
        QuantumCircuit: QPE circuit
    """
    n_state_qubits = eigenstate_prep.num_qubits
    
    # Create registers
    qreg_phase = QuantumRegister(precision_qubits, 'phase')
    qreg_state = QuantumRegister(n_state_qubits, 'state')
    creg_phase = ClassicalRegister(precision_qubits, 'c_phase')
    
    circuit = QuantumCircuit(qreg_phase, qreg_state, creg_phase, name='qpe')
    
    # Prepare eigenstate
    circuit.compose(eigenstate_prep, qreg_state, inplace=True)
    
    # Initialize phase register in superposition
    circuit.h(qreg_phase)
    
    circuit.barrier()
    
    # Controlled unitary operations
    for i in range(precision_qubits):
        # Apply U^(2^i) controlled by phase qubit i
        for _ in range(2 ** i):
            controlled_u = unitary_circuit.control()
            circuit.compose(controlled_u, [qreg_phase[i]] + list(qreg_state), inplace=True)
    
    circuit.barrier()
    
    # Inverse QFT on phase register
    qft_inv = QuantumCircuit(precision_qubits, name='qft_inv')
    
    # Reverse qubit order
    for i in range(precision_qubits // 2):
        qft_inv.swap(i, precision_qubits - 1 - i)
    
    # Apply inverse QFT
    for i in range(precision_qubits):
        for j in range(i):
            qft_inv.cp(-np.pi / (2 ** (i - j)), j, i)
        qft_inv.h(i)
    
    circuit.compose(qft_inv, qreg_phase, inplace=True)
    
    # Measure phase register
    circuit.measure(qreg_phase, creg_phase)
    
    return circuit


def shor_period_finding(N: int, a: int) -> QuantumCircuit:
    """
    Implement the quantum part of Shor's algorithm for period finding.
    
    Args:
        N: Number to factor
        a: Base for modular exponentiation (gcd(a, N) = 1)
    
    Returns:
        QuantumCircuit: Shor's period finding circuit
    """
    # This is a simplified version for educational purposes
    # A full implementation would require modular arithmetic circuits
    
    n_count = 8  # Number of counting qubits
    n_reg = int(np.ceil(np.log2(N)))  # Register size for N
    
    qreg_count = QuantumRegister(n_count, 'count')
    qreg_reg = QuantumRegister(n_reg, 'register')
    creg_count = ClassicalRegister(n_count, 'c_count')
    
    circuit = QuantumCircuit(qreg_count, qreg_reg, creg_count, 
                           name=f'shor_N{N}_a{a}')
    
    # Initialize register to |1⟩
    circuit.x(qreg_reg[0])
    
    # Initialize counting register in superposition
    circuit.h(qreg_count)
    
    circuit.barrier()
    
    # Controlled modular exponentiation (simplified)
    # In practice, this would implement a^(2^j) mod N for each j
    for j in range(n_count):
        # Placeholder for controlled modular exponentiation
        # This would be replaced with actual modular arithmetic
        circuit.barrier(label=f'c_mod_exp_2^{j}')
    
    circuit.barrier()
    
    # Inverse QFT on counting register
    qft_inv = QuantumCircuit(n_count, name='qft_inv')
    for i in range(n_count // 2):
        qft_inv.swap(i, n_count - 1 - i)
    
    for i in range(n_count):
        for j in range(i):
            qft_inv.cp(-np.pi / (2 ** (i - j)), j, i)
        qft_inv.h(i)
    
    circuit.compose(qft_inv, qreg_count, inplace=True)
    
    # Measure counting register
    circuit.measure(qreg_count, creg_count)
    
    return circuit
