#!/usr/bin/env python3
"""
Quantum Backend Comparison: Ideal vs Noisy

This demonstrates different types of quantum backends and their effects
on quantum circuit execution.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from qiskit import QuantumCircuit, transpile
from quantum_circuits import QuantumCircuitLibrary
from quantum_execution import QuantumExecutor, analyze_results
import numpy as np


def create_noise_model():
    """Create a simple noise model to simulate real quantum hardware."""
    
    try:
        from qiskit_aer.noise import NoiseModel, depolarizing_error, thermal_relaxation_error
        
        # Create noise model
        noise_model = NoiseModel()
        
        # Add depolarizing error to gates
        error_1q = 0.001  # 0.1% error rate for single-qubit gates
        error_2q = 0.01   # 1% error rate for two-qubit gates
        
        depolarizing_1q = depolarizing_error(error_1q, 1)
        depolarizing_2q = depolarizing_error(error_2q, 2)
        
        # Add errors to all single-qubit gates
        noise_model.add_all_qubit_quantum_error(depolarizing_1q, ['h', 'x', 'y', 'z', 's', 't', 'ry', 'rz'])
        
        # Add errors to all two-qubit gates
        noise_model.add_all_qubit_quantum_error(depolarizing_2q, ['cx', 'cy', 'cz'])
        
        # Add thermal relaxation (T1 and T2 times)
        t1 = 50e-6  # 50 microseconds
        t2 = 70e-6  # 70 microseconds
        gate_time = 0.1e-6  # 100 nanoseconds
        
        thermal_error = thermal_relaxation_error(t1, t2, gate_time)
        noise_model.add_all_qubit_quantum_error(thermal_error, ['h', 'x', 'cx'])
        
        return noise_model
        
    except ImportError:
        print("⚠️  qiskit-aer not available - using basic simulator")
        return None


def compare_backends_bell_state():
    """Compare Bell state on different backends."""
    
    print("🔬 Backend Comparison: Bell State")
    print("=" * 40)
    
    # Create Bell state
    bell_circuit = QuantumCircuitLibrary.create_bell_state(measure=True)
    
    print("Bell State Circuit:")
    print(bell_circuit.draw())
    print("Expected: Only |00⟩ and |11⟩ with ~50% probability each")
    
    # Test on different backends
    backends = {
        "Ideal Simulator": QuantumExecutor('aer_simulator'),
        "Basic Simulator": QuantumExecutor('aer_simulator')  # Will fallback to basic
    }
    
    # Add noisy simulator if available
    noise_model = create_noise_model()
    if noise_model:
        backends["Noisy Simulator"] = ("noisy", noise_model)
    
    results = {}
    
    for backend_name, executor in backends.items():
        print(f"\n🎯 Running on {backend_name}...")
        
        if isinstance(executor, tuple):
            # Special handling for noisy simulator
            try:
                from qiskit_aer import AerSimulator
                from qiskit import execute
                
                backend_type, noise = executor
                backend = AerSimulator(noise_model=noise)
                
                # Transpile and execute
                transpiled = transpile(bell_circuit, backend)
                job = execute(transpiled, backend, shots=1024)
                qiskit_result = job.result()
                
                result = {
                    'counts': qiskit_result.get_counts(transpiled),
                    'shots': 1024,
                    'success': True,
                    'backend': backend_name
                }
                
            except ImportError:
                print("  Skipping noisy simulator (qiskit-aer not available)")
                continue
        else:
            # Regular executor
            result = executor.execute_circuit(bell_circuit, shots=1024)
        
        if result['success']:
            analysis = analyze_results(result)
            results[backend_name] = analysis
            
            print(f"  Results:")
            for state, prob in analysis['probabilities'].items():
                print(f"    |{state}⟩: {prob:.3f}")
            print(f"  Entropy: {analysis['entropy']:.3f}")
            
            # Check for errors (non-Bell states)
            error_states = [state for state in analysis['probabilities'].keys() 
                          if state not in ['00', '11']]
            
            if error_states:
                error_prob = sum(analysis['probabilities'][state] for state in error_states)
                print(f"  ❌ Error probability: {error_prob:.3f}")
            else:
                print("  ✅ Perfect Bell state!")
    
    return results


def test_circuit_depth_effects():
    """Show how circuit depth affects noise."""
    
    print("\n📏 Circuit Depth vs Quantum Errors")
    print("=" * 40)
    
    # Create circuits of different depths
    circuits = {}
    
    # Shallow circuit: single Hadamard
    shallow = QuantumCircuit(1, 1)
    shallow.h(0)
    shallow.measure(0, 0)
    circuits["Shallow (H)"] = shallow
    
    # Medium circuit: multiple gates
    medium = QuantumCircuit(1, 1)
    for _ in range(5):
        medium.h(0)
        medium.s(0)
    medium.measure(0, 0)
    circuits["Medium (5 layers)"] = medium
    
    # Deep circuit: many gates
    deep = QuantumCircuit(1, 1)
    for _ in range(20):
        deep.ry(np.pi/4, 0)
        deep.rz(np.pi/6, 0)
    deep.measure(0, 0)
    circuits["Deep (20 layers)"] = deep
    
    executor = QuantumExecutor()
    
    print("Effect of circuit depth on quantum fidelity:")
    print("(Deeper circuits are more susceptible to errors)")
    
    for name, circuit in circuits.items():
        result = executor.execute_circuit(circuit, shots=1000)
        
        if result['success']:
            analysis = analyze_results(result)
            
            print(f"\n{name}:")
            print(f"  Circuit depth: {circuit.depth()}")
            print(f"  Gate count: {len(circuit.data)}")
            print(f"  Entropy: {analysis['entropy']:.3f}")
            print(f"  Most probable: |{analysis['most_probable_state']}⟩ ({analysis['most_probable_probability']:.3f})")


def quantum_volume_test():
    """Simple quantum volume-like test."""
    
    print("\n📊 Quantum Volume Test (Simplified)")
    print("=" * 40)
    
    print("Quantum Volume measures the largest random circuit a quantum computer can reliably execute")
    
    # Create random quantum circuits of increasing size
    from qiskit.circuit.random import random_circuit
    
    executor = QuantumExecutor()
    
    for n_qubits in [1, 2, 3]:
        for depth in [2, 4, 8]:
            
            # Create random circuit
            circuit = random_circuit(
                num_qubits=n_qubits,
                depth=depth,
                measure=True,
                seed=42  # For reproducibility
            )
            
            result = executor.execute_circuit(circuit, shots=100)
            
            if result['success']:
                analysis = analyze_results(result)
                
                # Simplified fidelity measure
                fidelity = analysis['most_probable_probability']
                
                print(f"  {n_qubits} qubits, depth {depth}: fidelity ≈ {fidelity:.3f}")


def demonstrate_quantum_backends():
    """Main demonstration function."""
    
    print("🚀 Quantum Backend Demonstration")
    print("=" * 45)
    
    print("\n🎯 What are quantum backends?")
    print("• Simulators: Perfect quantum mechanics simulation")
    print("• Noisy simulators: Include realistic quantum errors")  
    print("• Real hardware: Actual quantum computers with physical noise")
    
    print("\n⚡ Types of quantum noise:")
    print("• Gate errors: Imperfect quantum gate operations")
    print("• Decoherence: Quantum states decay over time (T1, T2)")
    print("• Measurement errors: Incorrect qubit state readout")
    print("• Cross-talk: Unwanted interactions between qubits")
    
    # Run demonstrations
    bell_results = compare_backends_bell_state()
    test_circuit_depth_effects()
    quantum_volume_test()
    
    print("\n" + "=" * 45)
    print("🎯 Key Insights:")
    
    if len(bell_results) > 1:
        print("✅ Different backends show different results")
        print("• Ideal simulators give perfect quantum results")
        print("• Noisy simulators show realistic quantum errors")
        print("• Real hardware would show even more complex noise")
    
    print("\n🔬 Why this matters:")
    print("• NISQ devices have limited fidelity")
    print("• Error mitigation is crucial for quantum algorithms")
    print("• Quantum error correction will enable fault-tolerant computing")
    
    print("\n🚀 Next steps:")
    print("• Set up IBM Quantum account for real hardware")
    print("• Try quantum error mitigation techniques")
    print("• Explore quantum error correction codes")
    print("• Study noise characterization methods")


if __name__ == "__main__":
    try:
        demonstrate_quantum_backends()
    except KeyboardInterrupt:
        print("\n\n👋 Backend exploration interrupted!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("This demonstrates quantum concepts even with basic simulators!")
