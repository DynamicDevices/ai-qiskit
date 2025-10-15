#!/usr/bin/env python3
"""
🚀 QUANTUM ALGORITHM SHOWCASE
============================
Amazing quantum algorithms you can run on real IBM hardware!
"""

def quantum_algorithms_menu():
    """Interactive menu of quantum algorithms for real hardware."""
    
    print("🌟 QUANTUM ALGORITHMS FOR REAL IBM HARDWARE")
    print("=" * 60)
    print()
    
    algorithms = [
        {
            "name": "🪙 Quantum Coin Flip",
            "description": "Perfect 50/50 randomness from superposition",
            "complexity": "Beginner",
            "qubits": 1,
            "advantage": "True quantum randomness",
            "runtime": "~30 seconds"
        },
        {
            "name": "🔔 Bell State Creation", 
            "description": "Quantum entanglement between two qubits",
            "complexity": "Beginner",
            "qubits": 2,
            "advantage": "Demonstrates quantum entanglement",
            "runtime": "~30 seconds"
        },
        {
            "name": "🎲 Quantum Dice (3-qubit)",
            "description": "8-sided quantum dice with true randomness", 
            "complexity": "Beginner",
            "qubits": 3,
            "advantage": "Uniform random distribution",
            "runtime": "~45 seconds"
        },
        {
            "name": "🔍 Grover's Search",
            "description": "Quantum database search with quadratic speedup",
            "complexity": "Intermediate", 
            "qubits": "2-4",
            "advantage": "√N speedup over classical",
            "runtime": "~60 seconds"
        },
        {
            "name": "🌊 Quantum Fourier Transform",
            "description": "Quantum version of classical FFT",
            "complexity": "Intermediate",
            "qubits": "3-5", 
            "advantage": "Exponential speedup for some problems",
            "runtime": "~90 seconds"
        },
        {
            "name": "📡 Quantum Teleportation",
            "description": "Transfer quantum state without moving particles",
            "complexity": "Advanced",
            "qubits": 3,
            "advantage": "Quantum communication protocol", 
            "runtime": "~120 seconds"
        },
        {
            "name": "📐 Quantum Phase Estimation",
            "description": "Estimate eigenvalues of quantum operators",
            "complexity": "Advanced",
            "qubits": "3-5",
            "advantage": "Core of Shor's algorithm",
            "runtime": "~120 seconds"
        },
        {
            "name": "🛡️ Quantum Error Correction",
            "description": "3-qubit bit-flip error correction code",
            "complexity": "Advanced", 
            "qubits": 5,
            "advantage": "Fault-tolerant quantum computing",
            "runtime": "~150 seconds"
        },
        {
            "name": "🚀 Random Quantum Circuit",
            "description": "Complex circuit for quantum supremacy",
            "complexity": "Expert",
            "qubits": "4-8",
            "advantage": "Demonstrates quantum complexity",
            "runtime": "~180 seconds"
        },
        {
            "name": "🧠 Quantum Neural Network",
            "description": "Variational quantum classifier",
            "complexity": "Expert",
            "qubits": "4-6", 
            "advantage": "Quantum machine learning",
            "runtime": "~300 seconds"
        }
    ]
    
    print("📚 Available Quantum Algorithms:")
    print()
    
    for i, alg in enumerate(algorithms, 1):
        print(f"{i:2d}. {alg['name']}")
        print(f"    📝 {alg['description']}")
        print(f"    🎯 Advantage: {alg['advantage']}")
        print(f"    🔧 Complexity: {alg['complexity']} | Qubits: {alg['qubits']} | Runtime: {alg['runtime']}")
        print()
    
    print("🎯 RECOMMENDED NEXT STEPS:")
    print("=" * 30)
    print("✅ You've mastered: Bell States (97.9% fidelity)")
    print("✅ You've mastered: Quantum Coin Flips (0.9% bias)")
    print()
    print("🚀 Try next:")
    print("• Quantum Dice (#3) - Multi-qubit randomness")
    print("• Grover's Search (#4) - Quantum search advantage") 
    print("• Quantum Teleportation (#6) - Quantum communication")
    print()
    print("🌟 ADVANCED CHALLENGES:")
    print("• Quantum Fourier Transform (#5)")
    print("• Quantum Error Correction (#8)")
    print("• Quantum Neural Networks (#10)")
    
    return algorithms

def show_quantum_hardware_capabilities():
    """Show what your IBM quantum computers can do."""
    
    print("\n🖥️  YOUR IBM QUANTUM HARDWARE CAPABILITIES")
    print("=" * 55)
    
    capabilities = {
        "IBM Torino (133 qubits)": {
            "processor": "Heron R1", 
            "topology": "Heavy-hex lattice",
            "gate_time": "~100 ns",
            "coherence": "~100 μs",
            "fidelity": "99.5%+ (1-2 qubit gates)",
            "specialties": ["Large circuits", "Error correction", "Optimization"]
        },
        "IBM Brisbane (127 qubits)": {
            "processor": "Eagle R3",
            "topology": "Heavy-hex lattice", 
            "gate_time": "~100 ns",
            "coherence": "~80 μs",
            "fidelity": "99%+ (1-2 qubit gates)",
            "specialties": ["Algorithm research", "Quantum advantage", "Benchmarking"]
        }
    }
    
    for name, specs in capabilities.items():
        print(f"🖥️  {name}")
        print(f"   Processor: {specs['processor']}")
        print(f"   Topology: {specs['topology']}")
        print(f"   Gate Speed: {specs['gate_time']}")
        print(f"   Coherence: {specs['coherence']}")
        print(f"   Fidelity: {specs['fidelity']}")
        print(f"   Best for: {', '.join(specs['specialties'])}")
        print()
    
    print("🎯 WHAT THIS MEANS FOR YOU:")
    print("• Run circuits up to ~50-100 gates deep")
    print("• Use 10-20 qubits effectively (NISQ era)")
    print("• Demonstrate quantum advantage in specific problems")
    print("• Research quantum error correction")
    print("• Explore quantum machine learning")

def quantum_algorithm_templates():
    """Provide ready-to-run quantum algorithm templates."""
    
    print("\n🛠️  READY-TO-RUN QUANTUM ALGORITHMS")
    print("=" * 45)
    
    templates = {
        "Quantum Dice": """
# 3-qubit quantum dice (8 outcomes)
from qiskit import QuantumCircuit
qc = QuantumCircuit(3, 3)
for i in range(3):
    qc.h(i)  # Superposition
qc.measure_all()
# Run on hardware: python3 -c "exec(open('quantum_dice.py').read())"
""",
        
        "Deutsch Algorithm": """
# Determine if function is constant or balanced
qc = QuantumCircuit(2, 1)
qc.x(1)  # Ancilla qubit
qc.h(0)  # Input qubit  
qc.h(1)  # Ancilla qubit
qc.cx(0, 1)  # Oracle (for balanced function)
qc.h(0)  # Interference
qc.measure(0, 0)
# Result: 0 = constant, 1 = balanced
""",
        
        "Quantum Walk": """
# 1D quantum walk on 4 positions
qc = QuantumCircuit(3, 2)  # 2 position qubits + 1 coin
qc.h(0)  # Initialize coin
for step in range(3):
    qc.ch(0, 1)  # Conditional walk
    qc.cx(0, 2)   # Move based on coin
    qc.h(0)      # Flip coin
qc.measure([1,2], [0,1])  # Measure position
""",
        
        "Bernstein-Vazirani": """
# Find hidden bit string in one query
secret = '101'  # Hidden string
qc = QuantumCircuit(len(secret)+1, len(secret))
qc.x(-1)  # Ancilla
qc.h(range(len(secret)+1))  # Superposition
for i, bit in enumerate(secret):
    if bit == '1':
        qc.cx(i, -1)  # Oracle
qc.h(range(len(secret)))  # Interference  
qc.measure(range(len(secret)), range(len(secret)))
"""
    }
    
    print("📋 Copy-paste these algorithms:")
    print()
    
    for name, code in templates.items():
        print(f"🔬 {name}:")
        print("```python")
        print(code.strip())
        print("```")
        print()

def main():
    """Main showcase function."""
    algorithms = quantum_algorithms_menu()
    show_quantum_hardware_capabilities() 
    quantum_algorithm_templates()
    
    print("\n🚀 NEXT STEPS:")
    print("=" * 20)
    print("1. Choose an algorithm from the menu above")
    print("2. Run: python3 advanced_quantum_algorithms.py")
    print("3. Select the algorithm number to execute")
    print("4. Watch it run on real quantum hardware!")
    print()
    print("🌟 You're now ready for advanced quantum computing!")

if __name__ == "__main__":
    main()
