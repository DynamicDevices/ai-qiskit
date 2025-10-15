"""
Quantum Circuit Library

This module contains reusable quantum circuits following Qiskit best practices.
"""

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import TwoLocal, EfficientSU2
from typing import Optional, List
import numpy as np


class QuantumCircuitLibrary:
    """
    A collection of common quantum circuits following Qiskit best practices.
    """
    
    @staticmethod
    def create_bell_state(measure: bool = True) -> QuantumCircuit:
        """
        Create a Bell state (maximally entangled two-qubit state).
        
        Args:
            measure: Whether to add measurement operations
            
        Returns:
            QuantumCircuit: Bell state circuit
        """
        # Use QuantumRegister and ClassicalRegister for clarity
        qreg = QuantumRegister(2, 'q')
        creg = ClassicalRegister(2, 'c') if measure else None
        
        # Create circuit with descriptive name
        if measure:
            circuit = QuantumCircuit(qreg, creg, name='bell_state')
        else:
            circuit = QuantumCircuit(qreg, name='bell_state')
        
        # Create Bell state |00⟩ + |11⟩
        circuit.h(qreg[0])  # Hadamard on first qubit
        circuit.cx(qreg[0], qreg[1])  # CNOT gate
        
        if measure:
            circuit.measure(qreg, creg)
            
        return circuit
    
    @staticmethod
    def create_ghz_state(n_qubits: int, measure: bool = True) -> QuantumCircuit:
        """
        Create a GHZ (Greenberger-Horne-Zeilinger) state.
        
        Args:
            n_qubits: Number of qubits (minimum 3)
            measure: Whether to add measurement operations
            
        Returns:
            QuantumCircuit: GHZ state circuit
        """
        if n_qubits < 3:
            raise ValueError("GHZ state requires at least 3 qubits")
            
        qreg = QuantumRegister(n_qubits, 'q')
        creg = ClassicalRegister(n_qubits, 'c') if measure else None
        
        if measure:
            circuit = QuantumCircuit(qreg, creg, name=f'ghz_{n_qubits}_state')
        else:
            circuit = QuantumCircuit(qreg, name=f'ghz_{n_qubits}_state')
        
        # Create GHZ state |000...⟩ + |111...⟩
        circuit.h(qreg[0])  # Hadamard on first qubit
        for i in range(1, n_qubits):
            circuit.cx(qreg[0], qreg[i])  # CNOT gates
            
        if measure:
            circuit.measure(qreg, creg)
            
        return circuit
    
    @staticmethod
    def create_quantum_fourier_transform(n_qubits: int) -> QuantumCircuit:
        """
        Create a Quantum Fourier Transform circuit.
        
        Args:
            n_qubits: Number of qubits
            
        Returns:
            QuantumCircuit: QFT circuit
        """
        qreg = QuantumRegister(n_qubits, 'q')
        circuit = QuantumCircuit(qreg, name=f'qft_{n_qubits}')
        
        # QFT implementation
        for i in range(n_qubits):
            circuit.h(qreg[i])
            for j in range(i + 1, n_qubits):
                circuit.cp(np.pi / (2 ** (j - i)), qreg[j], qreg[i])
        
        # Reverse the order of qubits
        for i in range(n_qubits // 2):
            circuit.swap(qreg[i], qreg[n_qubits - 1 - i])
            
        return circuit
    
    @staticmethod
    def create_variational_circuit(n_qubits: int, depth: int = 3, 
                                 entanglement: str = 'linear') -> TwoLocal:
        """
        Create a variational quantum circuit (ansatz).
        
        Args:
            n_qubits: Number of qubits
            depth: Circuit depth (number of layers)
            entanglement: Entanglement pattern ('linear', 'full', 'circular')
            
        Returns:
            TwoLocal: Parameterized variational circuit
        """
        # Use Qiskit's built-in efficient ansatz
        ansatz = EfficientSU2(
            num_qubits=n_qubits,
            reps=depth,
            entanglement=entanglement,
            insert_barriers=True
        )
        
        return ansatz
    
    @staticmethod
    def create_grover_oracle(marked_items: List[str]) -> QuantumCircuit:
        """
        Create an oracle for Grover's algorithm.
        
        Args:
            marked_items: List of binary strings representing marked items
            
        Returns:
            QuantumCircuit: Oracle circuit
        """
        if not marked_items:
            raise ValueError("At least one marked item required")
            
        n_qubits = len(marked_items[0])
        qreg = QuantumRegister(n_qubits, 'q')
        circuit = QuantumCircuit(qreg, name='grover_oracle')
        
        for item in marked_items:
            if len(item) != n_qubits:
                raise ValueError("All marked items must have same length")
                
            # Apply X gates to qubits that should be 0 in the marked state
            for i, bit in enumerate(item):
                if bit == '0':
                    circuit.x(qreg[i])
            
            # Multi-controlled Z gate
            if n_qubits == 1:
                circuit.z(qreg[0])
            elif n_qubits == 2:
                circuit.cz(qreg[0], qreg[1])
            else:
                # Use multi-controlled Z gate from circuit library
                from qiskit.circuit.library import MCMT, ZGate
                mcz = MCMT(ZGate(), n_qubits - 1, 1)
                circuit.append(mcz, qreg)
            
            # Undo X gates
            for i, bit in enumerate(item):
                if bit == '0':
                    circuit.x(qreg[i])
                    
        return circuit


def add_barrier_if_nonempty(circuit: QuantumCircuit) -> None:
    """
    Add a barrier to the circuit if it's not empty.
    
    Args:
        circuit: Quantum circuit to add barrier to
    """
    if len(circuit.data) > 0:
        circuit.barrier()


def optimize_circuit_depth(circuit: QuantumCircuit) -> QuantumCircuit:
    """
    Apply basic circuit optimization to reduce depth.
    
    Args:
        circuit: Input quantum circuit
        
    Returns:
        QuantumCircuit: Optimized circuit
    """
    from qiskit.transpiler import PassManager
    from qiskit.transpiler.passes import Optimize1qGatesDecomposition, CXCancellation
    
    # Create optimization pass manager
    pass_manager = PassManager([
        Optimize1qGatesDecomposition(),
        CXCancellation()
    ])
    
    return pass_manager.run(circuit)
