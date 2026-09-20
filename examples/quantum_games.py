#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Provenance and third-party notices: see LICENSE, NOTICE, and LICENSING.md.
"""
Quantum Visualization and Interactive Examples

Create interactive quantum state visualizations and quantum games
to better understand quantum mechanics principles.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector, plot_state_qsphere

from quantum_circuits import QuantumCircuitLibrary
from quantum_execution import QuantumExecutor


def quantum_coin_flip_game():
    """Interactive quantum coin flip game."""
    
    print("🎮 Quantum Coin Flip Game")
    print("=" * 30)
    print("Can you predict the quantum coin?")
    
    # Create quantum coin circuit
    coin_circuit = QuantumCircuit(1, 1)
    
    # Ask user for quantum operations
    print("\nChoose your quantum operations:")
    print("1. Classical coin (X gate)")
    print("2. Quantum superposition (H gate)")
    print("3. Quantum rotation (RY gate)")
    
    try:
        choice = input("Enter choice (1-3): ").strip()
        
        if choice == "1":
            coin_circuit.x(0)  # Flip to |1⟩
            print("Applied X gate - deterministic flip!")
        elif choice == "2":
            coin_circuit.h(0)  # Superposition
            print("Applied H gate - quantum superposition!")
        elif choice == "3":
            angle = float(input("Enter rotation angle (0-π): ") or "1.57")
            coin_circuit.ry(angle, 0)
            print(f"Applied RY({angle:.2f}) gate!")
        else:
            print("Invalid choice, using H gate")
            coin_circuit.h(0)
        
        # Add measurement
        coin_circuit.measure(0, 0)
        
        # Execute multiple times
        executor = QuantumExecutor()
        results = []
        
        for _ in range(10):
            result = executor.execute_circuit(coin_circuit, shots=1)
            if result['success']:
                outcome = list(result['counts'].keys())[0]
                results.append(int(outcome))
        
        print(f"\n🎯 Results: {results}")
        print(f"Heads (1): {results.count(1)}/10")
        print(f"Tails (0): {results.count(0)}/10")
        
        if len(set(results)) == 1:
            print("🎪 Deterministic outcome!")
        else:
            print("🌊 Quantum randomness observed!")
            
    except (ValueError, KeyboardInterrupt):
        print("Game cancelled!")


def visualize_quantum_states():
    """Visualize different quantum states on Bloch sphere."""
    
    print("\n🌐 Quantum State Visualization")
    print("=" * 40)
    
    # Create different quantum states
    states = {
        "|0⟩ (North pole)": QuantumCircuit(1),
        "|1⟩ (South pole)": QuantumCircuit(1),
        "|+⟩ (Equator)": QuantumCircuit(1),
        "|-⟩ (Equator)": QuantumCircuit(1),
        "|i⟩ (Y-axis)": QuantumCircuit(1),
        "Custom rotation": QuantumCircuit(1)
    }
    
    # Prepare states
    states["|1⟩ (South pole)"].x(0)
    states["|+⟩ (Equator)"].h(0)
    states["|-⟩ (Equator)"].x(0)
    states["|-⟩ (Equator)"].h(0)
    states["|i⟩ (Y-axis)"].h(0)
    states["|i⟩ (Y-axis)"].s(0)
    states["Custom rotation"].ry(np.pi/3, 0)
    states["Custom rotation"].rz(np.pi/4, 0)
    
    print("Quantum states to visualize:")
    for i, name in enumerate(states.keys(), 1):
        print(f"{i}. {name}")
    
    try:
        choice = input("\nSelect state to visualize (1-6): ").strip()
        state_names = list(states.keys())
        
        if choice.isdigit() and 1 <= int(choice) <= 6:
            selected_name = state_names[int(choice) - 1]
            selected_circuit = states[selected_name]
            
            # Get statevector
            statevector = Statevector.from_instruction(selected_circuit)
            
            print(f"\n📊 State: {selected_name}")
            print(f"Statevector: {statevector}")
            print(f"Probabilities: |0⟩={abs(statevector[0])**2:.3f}, |1⟩={abs(statevector[1])**2:.3f}")
            
            # Plot Bloch vector
            try:
                plot_bloch_multivector(statevector, title=f"Quantum State: {selected_name}")
                plt.show()
            except ImportError:
                print("⚠️  Visualization requires matplotlib and additional packages")
                print("Install with: pip install matplotlib qiskit[visualization]")
        
    except (ValueError, KeyboardInterrupt):
        print("Visualization cancelled!")


def quantum_interference_demo():
    """Demonstrate quantum interference effects."""
    
    print("\n🌊 Quantum Interference Demonstration")
    print("=" * 45)
    
    # Create Mach-Zehnder interferometer analog
    interferometer = QuantumCircuit(1, 1)
    
    # First beam splitter (superposition)
    interferometer.h(0)
    
    # Phase shift in one path
    print("Add phase shift to demonstrate interference:")
    try:
        phase = float(input("Enter phase (0 to 2π): ") or "0")
        interferometer.p(phase, 0)  # Phase gate
        
        # Second beam splitter
        interferometer.h(0)
        
        # Measure
        interferometer.measure(0, 0)
        
        print(f"\nInterferometer circuit with phase {phase:.2f}:")
        print(interferometer.draw())
        
        # Run multiple shots
        executor = QuantumExecutor()
        result = executor.execute_circuit(interferometer, shots=1000)
        
        if result['success']:
            counts = result['counts']
            prob_0 = counts.get('0', 0) / 1000
            prob_1 = counts.get('1', 0) / 1000
            
            print(f"\n📊 Interference Results:")
            print(f"|0⟩ probability: {prob_0:.3f}")
            print(f"|1⟩ probability: {prob_1:.3f}")
            
            # Theoretical prediction
            theoretical_prob_0 = np.cos(phase/2)**2
            print(f"\n🎯 Theoretical |0⟩ probability: {theoretical_prob_0:.3f}")
            print(f"Difference: {abs(prob_0 - theoretical_prob_0):.3f}")
            
            if abs(phase - np.pi) < 0.1:
                print("🌟 Perfect destructive interference!")
            elif abs(phase) < 0.1 or abs(phase - 2*np.pi) < 0.1:
                print("✨ Perfect constructive interference!")
            else:
                print("🌊 Partial interference effect")
        
    except (ValueError, KeyboardInterrupt):
        print("Demo cancelled!")


def quantum_entanglement_game():
    """Interactive game to explore quantum entanglement."""
    
    print("\n🔗 Quantum Entanglement Explorer")
    print("=" * 40)
    
    print("Create entangled states and test Bell's inequality!")
    
    # Create Bell states
    bell_states = {
        "Φ⁺": QuantumCircuitLibrary.create_bell_state(measure=False),
        "Φ⁻": QuantumCircuit(2),
        "Ψ⁺": QuantumCircuit(2),
        "Ψ⁻": QuantumCircuit(2)
    }
    
    # Prepare different Bell states
    # Φ⁻ = |00⟩ - |11⟩
    bell_states["Φ⁻"].h(0)
    bell_states["Φ⁻"].cx(0, 1)
    bell_states["Φ⁻"].z(0)
    
    # Ψ⁺ = |01⟩ + |10⟩
    bell_states["Ψ⁺"].h(0)
    bell_states["Ψ⁺"].cx(0, 1)
    bell_states["Ψ⁺"].x(1)
    
    # Ψ⁻ = |01⟩ - |10⟩
    bell_states["Ψ⁻"].h(0)
    bell_states["Ψ⁻"].cx(0, 1)
    bell_states["Ψ⁻"].x(1)
    bell_states["Ψ⁻"].z(0)
    
    print("Available Bell states:")
    for i, name in enumerate(bell_states.keys(), 1):
        print(f"{i}. {name}")
    
    try:
        choice = input("Choose Bell state (1-4): ").strip()
        state_names = list(bell_states.keys())
        
        if choice.isdigit() and 1 <= int(choice) <= 4:
            selected_name = state_names[int(choice) - 1]
            selected_circuit = bell_states[selected_name]
            
            # Add measurements
            test_circuit = selected_circuit.copy()
            test_circuit.add_register(QuantumRegister(0, 'c'))  # Add classical register
            test_circuit.measure_all()
            
            # Execute
            executor = QuantumExecutor()
            result = executor.execute_circuit(test_circuit, shots=1000)
            
            if result['success']:
                print(f"\n🔗 Bell State: {selected_name}")
                print(f"Circuit depth: {selected_circuit.depth()}")
                
                counts = result['counts']
                print(f"\n📊 Measurement Results:")
                for state, count in sorted(counts.items()):
                    prob = count / 1000
                    print(f"|{state}⟩: {count:4d} ({prob:.3f})")
                
                # Check for perfect correlations
                correlated_states = counts.get('00', 0) + counts.get('11', 0)
                anticorrelated_states = counts.get('01', 0) + counts.get('10', 0)
                
                print(f"\n🎯 Entanglement Analysis:")
                print(f"Correlated (00,11): {correlated_states/1000:.3f}")
                print(f"Anti-correlated (01,10): {anticorrelated_states/1000:.3f}")
                
                if correlated_states > 900:
                    print("🌟 Strong positive correlation - typical entanglement!")
                elif anticorrelated_states > 900:
                    print("🌟 Strong anti-correlation - entangled state!")
                else:
                    print("🌊 Mixed correlations")
        
    except (ValueError, KeyboardInterrupt):
        print("Entanglement exploration cancelled!")


def main():
    """Run interactive quantum demonstrations."""
    
    print("🎮 Interactive Quantum Playground")
    print("=" * 50)
    
    demos = {
        "1": ("Quantum Coin Flip Game", quantum_coin_flip_game),
        "2": ("Quantum State Visualization", visualize_quantum_states),
        "3": ("Quantum Interference Demo", quantum_interference_demo),
        "4": ("Quantum Entanglement Explorer", quantum_entanglement_game)
    }
    
    print("\nAvailable demonstrations:")
    for key, (name, _) in demos.items():
        print(f"{key}. {name}")
    
    try:
        choice = input("\nSelect demonstration (1-4): ").strip()
        
        if choice in demos:
            name, demo_func = demos[choice]
            print(f"\nStarting: {name}")
            demo_func()
        else:
            print("Invalid choice!")
            
    except KeyboardInterrupt:
        print("\nGoodbye! Keep exploring quantum mechanics! 🚀")
    
    print("\n" + "=" * 50)
    print("🎯 Learning Outcomes:")
    print("- Quantum superposition creates probabilistic outcomes")
    print("- Phase relationships enable interference effects")
    print("- Entanglement creates non-local correlations")
    print("- Measurement collapses quantum states")
    
    print("\n🔬 Next Steps:")
    print("- Try different parameters and observe changes")
    print("- Create your own quantum circuits")
    print("- Explore quantum algorithms in detail")
    print("- Study quantum error correction")


if __name__ == "__main__":
    main()
