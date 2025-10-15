#!/usr/bin/env python3
"""
Variational Quantum Eigensolver (VQE) Example

Demonstrates VQE algorithm for finding ground state energy
of the H2 molecule using Qiskit.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import Estimator
from qiskit_algorithms import VQE
from qiskit_algorithms.optimizers import SPSA
from quantum_circuits import QuantumCircuitLibrary


def create_h2_hamiltonian():
    """Create H2 molecule Hamiltonian in minimal basis."""
    # H2 molecule Hamiltonian coefficients (STO-3G basis)
    # This is a simplified version for demonstration
    
    coeffs = [-1.0523732, 0.39793742, -0.39793742, -0.01128010, 
              0.18093119, 0.18093119]
    
    operators = [
        "II", "IZ", "ZI", "ZZ", "XX", "YY"
    ]
    
    hamiltonian = SparsePauliOp.from_list(
        [(op, coeff) for op, coeff in zip(operators, coeffs)]
    )
    
    return hamiltonian


def run_vqe_example():
    """Run VQE algorithm for H2 molecule."""
    print("🧬 Variational Quantum Eigensolver (VQE)")
    print("=" * 50)
    
    # Create H2 Hamiltonian
    hamiltonian = create_h2_hamiltonian()
    print(f"H2 Hamiltonian: {hamiltonian}")
    
    # Create ansatz circuit
    ansatz = QuantumCircuitLibrary.create_variational_circuit(
        n_qubits=2, depth=2, entanglement='linear'
    )
    print(f"Ansatz parameters: {ansatz.num_parameters}")
    
    # Set up VQE
    optimizer = SPSA(maxiter=100)
    estimator = Estimator()
    
    vqe = VQE(estimator, ansatz, optimizer)
    
    # Run VQE
    print("\nRunning VQE optimization...")
    result = vqe.compute_minimum_eigenvalue(hamiltonian)
    
    print(f"\n📊 VQE Results:")
    print(f"Ground state energy: {result.eigenvalue:.6f} Hartree")
    print(f"Optimal parameters: {result.optimal_parameters}")
    print(f"Function evaluations: {result.cost_function_evals}")
    
    # Compare with exact result (for H2 at equilibrium)
    exact_energy = -1.137270  # Known exact value
    error = abs(result.eigenvalue - exact_energy)
    print(f"Exact energy: {exact_energy:.6f} Hartree")
    print(f"Error: {error:.6f} Hartree")
    
    return result


if __name__ == "__main__":
    try:
        result = run_vqe_example()
        print("\n✅ VQE example completed successfully!")
        print("\nNext: Try optimizing different molecules or ansatz circuits!")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure qiskit-algorithms is installed: pip install qiskit-algorithms")
