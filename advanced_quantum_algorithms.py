#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Provenance and third-party notices: see LICENSE, NOTICE, and LICENSING.md.
"""
🚀 Advanced Quantum Algorithms for Real Hardware
===============================================
Explore cutting-edge quantum algorithms on IBM quantum computers!
"""

from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
import numpy as np
import matplotlib.pyplot as plt

def quantum_random_number_generator():
    """Generate truly random numbers using quantum superposition."""
    print("🎲 Quantum Random Number Generator")
    print("=" * 40)
    
    # Create circuit for true quantum randomness
    n_bits = 8  # Generate 8-bit random numbers
    qc = QuantumCircuit(n_bits, n_bits, name='Quantum_RNG')
    
    # Put all qubits in superposition
    for i in range(n_bits):
        qc.h(i)
    
    # Measure all qubits
    qc.measure_all()
    
    print(f"Circuit for {n_bits}-bit quantum random numbers:")
    print(qc.draw())
    
    return qc

def grovers_search_algorithm(target_item='11'):
    """Grover's algorithm for searching unsorted databases."""
    print("🔍 Grover's Search Algorithm")
    print("=" * 40)
    
    n_qubits = len(target_item)
    qc = QuantumCircuit(n_qubits, n_qubits, name='Grovers_Search')
    
    # Initialize superposition
    for i in range(n_qubits):
        qc.h(i)
    
    # Oracle: mark the target item
    # For target '11', apply Z gates to both qubits when both are |1⟩
    if target_item == '11':
        qc.cz(0, 1)
    elif target_item == '01':
        qc.x(0)
        qc.cz(0, 1) 
        qc.x(0)
    elif target_item == '10':
        qc.x(1)
        qc.cz(0, 1)
        qc.x(1)
    # '00' needs no oracle for this simple case
    
    # Diffusion operator (amplitude amplification)
    for i in range(n_qubits):
        qc.h(i)
        qc.x(i)
    
    qc.cz(0, 1)  # Multi-controlled Z
    
    for i in range(n_qubits):
        qc.x(i)
        qc.h(i)
    
    qc.measure_all()
    
    print(f"Searching for item: |{target_item}⟩")
    print(qc.draw())
    
    return qc

def quantum_fourier_transform():
    """Quantum Fourier Transform - basis for many quantum algorithms."""
    print("🌊 Quantum Fourier Transform")
    print("=" * 40)
    
    n_qubits = 3
    qc = QuantumCircuit(n_qubits, n_qubits, name='QFT')
    
    # Prepare initial state |001⟩
    qc.x(2)
    qc.barrier()
    
    # QFT implementation
    for j in range(n_qubits):
        qc.h(j)
        for k in range(j + 1, n_qubits):
            qc.cp(np.pi / (2**(k - j)), k, j)
    
    # Swap qubits to get correct order
    for i in range(n_qubits // 2):
        qc.swap(i, n_qubits - 1 - i)
    
    qc.barrier()
    qc.measure_all()
    
    print("QFT transforms |001⟩ → frequency domain")
    print(qc.draw())
    
    return qc

def quantum_phase_estimation():
    """Estimate eigenvalues of quantum operators."""
    print("📐 Quantum Phase Estimation")
    print("=" * 40)
    
    # 2 counting qubits + 1 eigenstate qubit
    counting_qubits = 2
    total_qubits = counting_qubits + 1
    qc = QuantumCircuit(total_qubits, counting_qubits, name='Phase_Estimation')
    
    # Prepare eigenstate |1⟩ (eigenstate of Z gate)
    qc.x(2)
    
    # Initialize counting qubits in superposition
    for i in range(counting_qubits):
        qc.h(i)
    
    # Controlled unitary operations (powers of Z gate)
    # Z^1 controlled by qubit 1
    qc.cz(1, 2)
    
    # Z^2 controlled by qubit 0 (Z^2 = I, so no operation needed)
    
    # Inverse QFT on counting qubits
    qc.swap(0, 1)
    qc.h(1)
    qc.cp(-np.pi/2, 0, 1)
    qc.h(0)
    
    # Measure counting qubits
    for i in range(counting_qubits):
        qc.measure(i, i)
    
    print("Estimating phase of Z gate eigenvalue")
    print(qc.draw())
    
    return qc

def quantum_teleportation():
    """Quantum teleportation protocol."""
    print("📡 Quantum Teleportation")
    print("=" * 40)
    
    qc = QuantumCircuit(3, 3, name='Quantum_Teleportation')
    
    # Prepare state to teleport |+⟩ = (|0⟩ + |1⟩)/√2
    qc.h(0)
    qc.barrier()
    
    # Create Bell pair between Alice (qubit 1) and Bob (qubit 2)
    qc.h(1)
    qc.cx(1, 2)
    qc.barrier()
    
    # Alice's measurements
    qc.cx(0, 1)  # Entangle message with Alice's half
    qc.h(0)      # Rotate message qubit
    qc.barrier()
    
    # Measure Alice's qubits
    qc.measure(0, 0)
    qc.measure(1, 1)
    
    # Bob's corrections (would be conditional in real protocol)
    qc.cx(1, 2)  # Correct based on Alice's measurement
    qc.cz(0, 2)  # Correct based on Alice's measurement
    
    # Measure Bob's qubit
    qc.measure(2, 2)
    
    print("Teleporting |+⟩ state from Alice to Bob")
    print(qc.draw())
    
    return qc

def quantum_error_correction():
    """3-qubit bit-flip error correction code."""
    print("🛡️ Quantum Error Correction")
    print("=" * 40)
    
    qc = QuantumCircuit(5, 3, name='Error_Correction')
    
    # Prepare logical |0⟩ = |000⟩
    # (Start with |000⟩ - no operations needed)
    
    # Encode into 3-qubit repetition code
    qc.cx(0, 1)
    qc.cx(0, 2)
    qc.barrier()
    
    # Simulate bit-flip error on qubit 1
    qc.x(1)  # This is the "error"
    qc.barrier()
    
    # Error syndrome measurement
    qc.cx(0, 3)  # Ancilla qubit 3
    qc.cx(1, 3)
    qc.cx(1, 4)  # Ancilla qubit 4  
    qc.cx(2, 4)
    
    # Measure syndrome
    qc.measure(3, 0)  # Syndrome bit 1
    qc.measure(4, 1)  # Syndrome bit 2
    
    # Error correction (simplified - normally conditional)
    qc.x(1)  # Correct the error we introduced
    
    # Measure final state
    qc.measure(0, 2)
    
    print("3-qubit error correction detecting bit-flip on qubit 1")
    print(qc.draw())
    
    return qc

def quantum_supremacy_circuit():
    """Random quantum circuit for supremacy demonstration."""
    print("🚀 Quantum Supremacy Circuit")
    print("=" * 40)
    
    n_qubits = 4
    depth = 8
    qc = QuantumCircuit(n_qubits, n_qubits, name='Supremacy_Circuit')
    
    # Random quantum circuit with alternating layers
    np.random.seed(42)  # For reproducibility
    
    for layer in range(depth):
        # Single qubit gates
        for i in range(n_qubits):
            gate_choice = np.random.choice(['h', 'rx', 'ry', 'rz'])
            if gate_choice == 'h':
                qc.h(i)
            elif gate_choice == 'rx':
                qc.rx(np.random.uniform(0, 2*np.pi), i)
            elif gate_choice == 'ry':
                qc.ry(np.random.uniform(0, 2*np.pi), i)
            else:  # rz
                qc.rz(np.random.uniform(0, 2*np.pi), i)
        
        # Two-qubit gates
        if layer % 2 == 0:
            # Even layers: (0,1), (2,3)
            for i in range(0, n_qubits-1, 2):
                qc.cx(i, i+1)
        else:
            # Odd layers: (1,2), (3,0) if n_qubits > 3
            for i in range(1, n_qubits-1, 2):
                qc.cx(i, i+1)
            if n_qubits > 3:
                qc.cx(n_qubits-1, 0)
        
        qc.barrier()
    
    qc.measure_all()
    
    print(f"Random circuit: {n_qubits} qubits, depth {depth}")
    print("Designed to be hard for classical computers")
    print(qc.draw())
    
    return qc

def run_algorithm_on_hardware(circuit, algorithm_name):
    """Execute any quantum algorithm on real IBM hardware."""
    print(f"\n🚀 EXECUTING {algorithm_name.upper()} ON REAL QUANTUM HARDWARE!")
    print("=" * 60)
    
    try:
        # Connect to quantum hardware
        service = QiskitRuntimeService(name='my_quantum_cloud')
        backends = service.backends(operational=True, simulator=False)
        
        # Select backend with shortest queue
        backend = min(backends, key=lambda b: b.status().pending_jobs)
        print(f"🎯 Selected: {backend.name} ({backend.status().pending_jobs} jobs in queue)")
        
        # Transpile for hardware
        transpiled = transpile(circuit, backend=backend, optimization_level=3)
        print(f"⚙️  Transpiled: {circuit.depth()} → {transpiled.depth()} depth")
        
        # Execute on quantum hardware
        sampler = Sampler(backend)
        job = sampler.run([transpiled], shots=1024)
        
        print(f"📋 Job ID: {job.job_id}")
        print("⏳ Executing on quantum hardware...")
        
        # Get results
        result = job.result()
        counts = result[0].data.c.get_counts()
        
        print(f"\n🎉 RESULTS FROM {backend.name}:")
        print("=" * 40)
        
        # Show top results
        sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        for state, count in sorted_counts[:8]:  # Top 8 results
            prob = count / 1024
            bar = '█' * int(prob * 30)
            print(f"   |{state}⟩: {count:4d} shots ({prob:.3f}) {bar}")
        
        return counts
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    """Showcase advanced quantum algorithms."""
    print("🌟 ADVANCED QUANTUM ALGORITHMS FOR REAL HARDWARE")
    print("=" * 60)
    print("Choose from these cutting-edge quantum algorithms:\n")
    
    algorithms = {
        "1": ("Quantum Random Number Generator", quantum_random_number_generator),
        "2": ("Grover's Search Algorithm", grovers_search_algorithm),
        "3": ("Quantum Fourier Transform", quantum_fourier_transform),
        "4": ("Quantum Phase Estimation", quantum_phase_estimation),
        "5": ("Quantum Teleportation", quantum_teleportation),
        "6": ("Quantum Error Correction", quantum_error_correction),
        "7": ("Quantum Supremacy Circuit", quantum_supremacy_circuit)
    }
    
    for key, (name, _) in algorithms.items():
        print(f"{key}. {name}")
    
    print("\n🎯 Each algorithm demonstrates different quantum phenomena:")
    print("• Superposition, entanglement, interference")
    print("• Quantum speedups and advantages")
    print("• Error correction and fault tolerance")
    print("• Quantum communication protocols")
    
    print(f"\n🚀 Ready to run on your IBM quantum computers!")
    print("💡 Tip: Try algorithm #2 (Grover's) for quantum search!")

if __name__ == "__main__":
    main()
