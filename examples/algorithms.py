#!/usr/bin/env python3
"""
Quantum Algorithms Examples

This script demonstrates fundamental quantum algorithms
implemented with Qiskit following best practices.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from quantum_algorithms import (
    deutsch_jozsa_algorithm,
    bernstein_vazirani_algorithm,
    grover_algorithm,
    quantum_phase_estimation
)
from quantum_execution import QuantumExecutor, analyze_results
import numpy as np


def run_deutsch_jozsa_examples():
    """Demonstrate Deutsch-Jozsa algorithm."""
    print("\n🔍 Deutsch-Jozsa Algorithm")
    print("-" * 40)
    
    executor = QuantumExecutor()
    
    # Test constant function (all 0s)
    print("Testing constant function f(x) = 0:")
    constant_oracle = '0000'  # 4-bit constant function
    dj_circuit = deutsch_jozsa_algorithm(constant_oracle)
    
    result = executor.execute_circuit(dj_circuit, shots=1024)
    if result['success']:
        analysis = analyze_results(result)
        print(f"Most frequent result: {analysis['most_probable_state']}")
        print("Expected: 0000 (all zeros indicates constant function)")
    
    # Test balanced function
    print("\nTesting balanced function:")
    balanced_oracle = '1010'  # 4-bit balanced function
    dj_circuit = deutsch_jozsa_algorithm(balanced_oracle)
    
    result = executor.execute_circuit(dj_circuit, shots=1024)
    if result['success']:
        analysis = analyze_results(result)
        print(f"Most frequent result: {analysis['most_probable_state']}")
        print("Expected: Non-zero result indicates balanced function")


def run_bernstein_vazirani_example():
    """Demonstrate Bernstein-Vazirani algorithm."""
    print("\n🎯 Bernstein-Vazirani Algorithm")
    print("-" * 40)
    
    executor = QuantumExecutor()
    
    secret_string = '1011'
    print(f"Finding secret string: {secret_string}")
    
    bv_circuit = bernstein_vazirani_algorithm(secret_string)
    
    result = executor.execute_circuit(bv_circuit, shots=1024)
    if result['success']:
        analysis = analyze_results(result)
        print(f"Measured result: {analysis['most_probable_state']}")
        print(f"Success: {'✅' if analysis['most_probable_state'] == secret_string else '❌'}")


def run_grover_example():
    """Demonstrate Grover's search algorithm."""
    print("\n🔎 Grover's Search Algorithm")
    print("-" * 40)
    
    executor = QuantumExecutor()
    
    # Search for '101' in a 3-qubit space
    marked_items = ['101']
    print(f"Searching for: {marked_items[0]} in 3-qubit space (8 total items)")
    
    grover_circuit = grover_algorithm(marked_items)
    
    result = executor.execute_circuit(grover_circuit, shots=1024)
    if result['success']:
        analysis = analyze_results(result)
        print(f"Most frequent result: {analysis['most_probable_state']}")
        print(f"Probability of success: {analysis['probabilities'].get('101', 0):.3f}")
        
        # Show top 3 results
        sorted_probs = sorted(analysis['probabilities'].items(), 
                            key=lambda x: x[1], reverse=True)
        print("\nTop 3 measurement outcomes:")
        for i, (state, prob) in enumerate(sorted_probs[:3]):
            marker = "🎯" if state in marked_items else "  "
            print(f"  {i+1}. |{state}⟩: {prob:.3f} {marker}")


def run_quantum_phase_estimation_example():
    """Demonstrate Quantum Phase Estimation."""
    print("\n📐 Quantum Phase Estimation")
    print("-" * 40)
    
    from qiskit import QuantumCircuit
    
    # Create a simple unitary (Z rotation)
    phase = np.pi / 4  # π/4 rotation
    unitary = QuantumCircuit(1, name='U')
    unitary.rz(2 * phase, 0)  # RZ(2φ) gives phase φ
    
    # Eigenstate preparation (|+⟩ state is eigenstate of RZ)
    eigenstate_prep = QuantumCircuit(1, name='eigenstate')
    eigenstate_prep.h(0)  # |+⟩ = (|0⟩ + |1⟩)/√2
    
    print(f"Estimating phase: π/4 ≈ {phase:.4f}")
    print("Using 4 precision qubits")
    
    qpe_circuit = quantum_phase_estimation(unitary, eigenstate_prep, precision_qubits=4)
    
    executor = QuantumExecutor()
    result = executor.execute_circuit(qpe_circuit, shots=1024)
    
    if result['success']:
        analysis = analyze_results(result)
        
        # Convert binary result to phase estimate
        most_frequent = analysis['most_probable_state']
        binary_fraction = int(most_frequent, 2) / (2 ** len(most_frequent))
        estimated_phase = 2 * np.pi * binary_fraction
        
        print(f"Most frequent measurement: {most_frequent}")
        print(f"Estimated phase: {estimated_phase:.4f}")
        print(f"True phase: {phase:.4f}")
        print(f"Error: {abs(estimated_phase - phase):.4f}")


def demonstrate_circuit_properties():
    """Show quantum circuit analysis and properties."""
    print("\n📊 Circuit Analysis")
    print("-" * 40)
    
    from quantum_circuits import QuantumCircuitLibrary
    
    circuits = {
        'Bell State': QuantumCircuitLibrary.create_bell_state(measure=False),
        'GHZ State (3)': QuantumCircuitLibrary.create_ghz_state(3, measure=False),
        'QFT (3)': QuantumCircuitLibrary.create_quantum_fourier_transform(3),
    }
    
    for name, circuit in circuits.items():
        print(f"\n{name}:")
        print(f"  Qubits: {circuit.num_qubits}")
        print(f"  Depth: {circuit.depth()}")
        print(f"  Gate count: {len(circuit.data)}")
        
        # Count gate types
        gate_counts = {}
        for instruction in circuit.data:
            gate_name = instruction.operation.name
            gate_counts[gate_name] = gate_counts.get(gate_name, 0) + 1
        
        print(f"  Gate types: {dict(gate_counts)}")


def main():
    """Run quantum algorithm examples."""
    print("🚀 Quantum Algorithms Examples")
    print("=" * 50)
    
    try:
        run_deutsch_jozsa_examples()
        run_bernstein_vazirani_example()
        run_grover_example()
        run_quantum_phase_estimation_example()
        demonstrate_circuit_properties()
        
        print("\n" + "=" * 50)
        print("✅ All algorithm examples completed!")
        print("\nKey Takeaways:")
        print("- Deutsch-Jozsa: Exponential speedup for function classification")
        print("- Bernstein-Vazirani: Finds hidden bit string in one query")
        print("- Grover's: Quadratic speedup for unstructured search")
        print("- QPE: Estimates eigenvalue phases of unitary operators")
        
    except Exception as e:
        print(f"❌ Error running examples: {e}")
        print("Make sure all dependencies are installed and working correctly.")


if __name__ == "__main__":
    main()
