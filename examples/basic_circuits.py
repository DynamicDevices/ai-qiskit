#!/usr/bin/env python3
"""
Basic Qiskit Examples

This script demonstrates basic quantum circuits and their execution
following Qiskit best practices.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from quantum_circuits import QuantumCircuitLibrary
from quantum_execution import QuantumExecutor, analyze_results, visualize_results
from qiskit.visualization import plot_histogram, circuit_drawer
import matplotlib.pyplot as plt


def main():
    """Run basic quantum circuit examples."""
    
    print("🔬 Qiskit Basic Examples")
    print("=" * 50)
    
    # Initialize quantum executor
    executor = QuantumExecutor()
    
    # Example 1: Bell State
    print("\n1. Bell State Example")
    print("-" * 30)
    
    bell_circuit = QuantumCircuitLibrary.create_bell_state(measure=True)
    print("Circuit:")
    print(bell_circuit.draw(output='text'))
    
    # Execute the circuit
    result = executor.execute_circuit(bell_circuit, shots=1024)
    
    if result['success']:
        analysis = analyze_results(result)
        print(f"\nResults:")
        print(f"Total shots: {analysis['total_shots']}")
        print(f"Unique states: {analysis['unique_states']}")
        print(f"Most probable state: {analysis['most_probable_state']} "
              f"({analysis['most_probable_probability']:.3f})")
        print(f"Entropy: {analysis['entropy']:.3f}")
        
        print("\nState probabilities:")
        for state, prob in analysis['probabilities'].items():
            print(f"  |{state}⟩: {prob:.3f}")
    else:
        print(f"Execution failed: {result['error']}")
    
    # Example 2: GHZ State
    print("\n\n2. GHZ State Example (3 qubits)")
    print("-" * 30)
    
    ghz_circuit = QuantumCircuitLibrary.create_ghz_state(3, measure=True)
    print("Circuit:")
    print(ghz_circuit.draw(output='text'))
    
    result = executor.execute_circuit(ghz_circuit, shots=1024)
    
    if result['success']:
        analysis = analyze_results(result)
        print(f"\nResults:")
        print(f"Most probable state: {analysis['most_probable_state']} "
              f"({analysis['most_probable_probability']:.3f})")
        print(f"Entropy: {analysis['entropy']:.3f}")
        
        # Show top 3 states
        sorted_probs = sorted(analysis['probabilities'].items(), 
                            key=lambda x: x[1], reverse=True)
        print("\nTop 3 states:")
        for i, (state, prob) in enumerate(sorted_probs[:3]):
            print(f"  {i+1}. |{state}⟩: {prob:.3f}")
    
    # Example 3: Quantum Fourier Transform
    print("\n\n3. Quantum Fourier Transform Example")
    print("-" * 30)
    
    qft_circuit = QuantumCircuitLibrary.create_quantum_fourier_transform(3)
    print("Circuit:")
    print(qft_circuit.draw(output='text'))
    
    # Add measurements for execution
    from qiskit import ClassicalRegister
    qft_with_measurement = qft_circuit.copy()
    creg = ClassicalRegister(3, 'c')
    qft_with_measurement.add_register(creg)
    qft_with_measurement.measure_all()
    
    result = executor.execute_circuit(qft_with_measurement, shots=1024)
    
    if result['success']:
        analysis = analyze_results(result)
        print(f"\nResults:")
        print(f"Entropy: {analysis['entropy']:.3f} (higher entropy indicates more uniform distribution)")
        print(f"Unique states observed: {analysis['unique_states']}/8")
    
    # Example 4: Variational Circuit
    print("\n\n4. Variational Circuit Example")
    print("-" * 30)
    
    var_circuit = QuantumCircuitLibrary.create_variational_circuit(3, depth=2)
    print("Parameterized circuit structure:")
    print(var_circuit.draw(output='text'))
    
    # Bind parameters for execution
    import numpy as np
    parameters = np.random.random(var_circuit.num_parameters) * 2 * np.pi
    bound_circuit = var_circuit.assign_parameters(parameters)
    
    # Add measurements
    from qiskit import ClassicalRegister
    bound_circuit.add_register(ClassicalRegister(3, 'c'))
    bound_circuit.measure_all()
    
    result = executor.execute_circuit(bound_circuit, shots=1024)
    
    if result['success']:
        analysis = analyze_results(result)
        print(f"\nResults with random parameters:")
        print(f"Entropy: {analysis['entropy']:.3f}")
        print(f"Most probable state: {analysis['most_probable_state']} "
              f"({analysis['most_probable_probability']:.3f})")
    
    print("\n" + "=" * 50)
    print("✅ All examples completed successfully!")
    print("\nNext steps:")
    print("- Explore the notebooks/ directory for interactive examples")
    print("- Check out quantum algorithms in examples/algorithms.py")
    print("- Run tests with: python -m pytest tests/")


if __name__ == "__main__":
    main()
