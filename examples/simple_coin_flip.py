#!/usr/bin/env python3
"""
Simple Quantum Coin Flip Demonstration

Shows the difference between classical and quantum coin flips
without requiring user input.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from qiskit import QuantumCircuit
from quantum_execution import QuantumExecutor, analyze_results
import numpy as np


def classical_coin_flip():
    """Demonstrate a classical deterministic coin flip."""
    print("🪙 Classical Coin Flip (X gate)")
    print("-" * 30)
    
    # Classical coin: deterministic flip to |1⟩
    coin_circuit = QuantumCircuit(1, 1)
    coin_circuit.x(0)  # Flip to |1⟩ (heads)
    coin_circuit.measure(0, 0)
    
    print("Circuit:")
    print(coin_circuit.draw())
    
    # Execute 10 times
    executor = QuantumExecutor()
    results = []
    
    for i in range(10):
        result = executor.execute_circuit(coin_circuit, shots=1)
        if result['success']:
            outcome = list(result['counts'].keys())[0]
            results.append(int(outcome))
            print(f"Flip {i+1}: {'Heads' if outcome == '1' else 'Tails'}")
    
    print(f"\n📊 Results: Heads={results.count(1)}/10, Tails={results.count(0)}/10")
    print("🎪 Deterministic outcome - always the same!")
    
    return results


def quantum_superposition_coin():
    """Demonstrate a quantum coin in superposition."""
    print("\n🌊 Quantum Superposition Coin (H gate)")
    print("-" * 35)
    
    # Quantum coin: superposition |0⟩ + |1⟩
    coin_circuit = QuantumCircuit(1, 1)
    coin_circuit.h(0)  # Create superposition
    coin_circuit.measure(0, 0)
    
    print("Circuit:")
    print(coin_circuit.draw())
    
    # Execute 10 times
    executor = QuantumExecutor()
    results = []
    
    for i in range(10):
        result = executor.execute_circuit(coin_circuit, shots=1)
        if result['success']:
            outcome = list(result['counts'].keys())[0]
            results.append(int(outcome))
            print(f"Flip {i+1}: {'Heads' if outcome == '1' else 'Tails'}")
    
    print(f"\n📊 Results: Heads={results.count(1)}/10, Tails={results.count(0)}/10")
    print("🌊 Quantum randomness - truly random outcomes!")
    
    return results


def quantum_biased_coin():
    """Demonstrate a quantum coin with adjustable bias."""
    print("\n🎯 Quantum Biased Coin (RY rotation)")
    print("-" * 35)
    
    # Biased quantum coin using rotation
    angle = np.pi / 3  # 60 degrees - creates bias
    coin_circuit = QuantumCircuit(1, 1)
    coin_circuit.ry(angle, 0)  # Rotate on Bloch sphere
    coin_circuit.measure(0, 0)
    
    print("Circuit:")
    print(coin_circuit.draw())
    print(f"Rotation angle: {angle:.2f} radians ({np.degrees(angle):.1f}°)")
    
    # Calculate theoretical probabilities
    prob_0 = np.cos(angle/2)**2
    prob_1 = np.sin(angle/2)**2
    
    print(f"Theoretical: P(Tails)={prob_0:.3f}, P(Heads)={prob_1:.3f}")
    
    # Execute many times for statistics
    executor = QuantumExecutor()
    result = executor.execute_circuit(coin_circuit, shots=1000)
    
    if result['success']:
        analysis = analyze_results(result)
        
        print(f"\n📊 Experimental Results (1000 flips):")
        for state, prob in analysis['probabilities'].items():
            outcome = "Tails" if state == "0" else "Heads"
            print(f"  {outcome}: {prob:.3f}")
        
        # Compare with theory
        measured_prob_1 = analysis['probabilities'].get('1', 0)
        error = abs(measured_prob_1 - prob_1)
        print(f"\nError from theory: {error:.3f}")
        
        if error < 0.05:
            print("✅ Great match with quantum mechanics prediction!")
        else:
            print("⚠️  Some deviation - quantum noise or statistical fluctuation")
    
    return result


def compare_randomness():
    """Compare different types of randomness."""
    print("\n🔍 Randomness Comparison")
    print("=" * 30)
    
    # Test each coin type with many flips
    executor = QuantumExecutor()
    
    # Classical (deterministic)
    classical_circuit = QuantumCircuit(1, 1)
    classical_circuit.x(0)
    classical_circuit.measure(0, 0)
    
    classical_result = executor.execute_circuit(classical_circuit, shots=100)
    
    # Quantum (superposition)
    quantum_circuit = QuantumCircuit(1, 1)
    quantum_circuit.h(0)
    quantum_circuit.measure(0, 0)
    
    quantum_result = executor.execute_circuit(quantum_circuit, shots=100)
    
    if classical_result['success'] and quantum_result['success']:
        classical_analysis = analyze_results(classical_result)
        quantum_analysis = analyze_results(quantum_result)
        
        print("Classical coin entropy:", f"{classical_analysis['entropy']:.3f}")
        print("Quantum coin entropy:", f"{quantum_analysis['entropy']:.3f}")
        
        print("\n💡 Entropy measures randomness:")
        print("  - 0.0 = completely predictable")
        print("  - 1.0 = maximum randomness (for 2 outcomes)")
        
        if classical_analysis['entropy'] < 0.1:
            print("  ✅ Classical: Deterministic as expected")
        if quantum_analysis['entropy'] > 0.9:
            print("  ✅ Quantum: Highly random as expected")


def main():
    """Run quantum coin flip demonstrations."""
    
    print("🎮 Quantum Coin Flip Demonstration")
    print("=" * 40)
    print("Exploring different types of quantum 'coins'\n")
    
    # Run all demonstrations
    classical_results = classical_coin_flip()
    quantum_results = quantum_superposition_coin()
    biased_result = quantum_biased_coin()
    compare_randomness()
    
    print("\n" + "=" * 40)
    print("🎯 Key Quantum Concepts Demonstrated:")
    print("• Classical gates (X) create deterministic outcomes")
    print("• Hadamard gate (H) creates perfect superposition")
    print("• Rotation gates (RY) allow adjustable probabilities")
    print("• Quantum measurement collapses superposition")
    print("• True randomness emerges from quantum mechanics")
    
    print("\n🚀 Try the Interactive Version:")
    print("Run: python3 examples/quantum_games.py")
    print("Select option 1 for interactive coin flip game!")


if __name__ == "__main__":
    main()
