#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Provenance and third-party notices: see LICENSE, NOTICE, and LICENSING.md.
"""
🚀 DIRECT IBM QUANTUM HARDWARE TEST
==================================
Simple, direct connection to real quantum computers!
"""

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
import sys

def test_real_quantum_hardware():
    """Test connection and execution on real IBM quantum hardware."""
    
    print("🚀 REAL IBM QUANTUM HARDWARE TEST")
    print("=" * 50)
    
    # Create simple Bell state circuit
    print("🔬 Creating Bell State Circuit...")
    qr = QuantumRegister(2, 'q')
    cr = ClassicalRegister(2, 'c')
    circuit = QuantumCircuit(qr, cr, name='Bell_Test')
    
    # Build Bell state: |00⟩ + |11⟩
    circuit.h(qr[0])        # Put qubit 0 in superposition
    circuit.cx(qr[0], qr[1]) # Entangle qubits 0 and 1
    circuit.measure(qr, cr)  # Measure both qubits
    
    print(circuit.draw())
    print("Expected ideal: 50% |00⟩, 50% |11⟩")
    
    try:
        print("\n🔑 Connecting to IBM Quantum...")
        from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
        
        # Load saved credentials
        service = QiskitRuntimeService()
        print("✅ Credentials loaded successfully!")
        
        # Find available quantum computers
        print("\n🖥️  Searching for quantum computers...")
        backends = service.backends(operational=True, simulator=False)
        
        if not backends:
            print("❌ No quantum computers available")
            print("   (All may be in maintenance or queue full)")
            return False
            
        # Select best backend
        backend = backends[0]
        print(f"🎯 Selected: {backend.name}")
        print(f"   Qubits: {backend.configuration().n_qubits}")
        print(f"   Queue: {backend.status().pending_jobs} jobs")
        
        # Transpile for hardware
        print(f"\n⚙️  Optimizing circuit for {backend.name}...")
        optimized = transpile(circuit, backend=backend, optimization_level=3)
        print(f"   Original gates: {circuit.count_ops()}")
        print(f"   Optimized depth: {optimized.depth()}")
        
        # Execute on real quantum computer!
        print(f"\n🚀 EXECUTING ON QUANTUM COMPUTER: {backend.name}")
        print("   Submitting to real quantum hardware...")
        
        sampler = Sampler(backend=backend)
        job = sampler.run([optimized], shots=1024)
        
        print(f"   Job ID: {job.job_id}")
        print(f"   Status: {job.status()}")
        print("   ⏳ Waiting for quantum execution...")
        
        # Get results from quantum computer
        result = job.result()
        quasi_dist = result.quasi_dists[0]
        
        print("\n🎉 REAL QUANTUM COMPUTER RESULTS!")
        print("=" * 45)
        
        # Convert to readable format
        total_shots = 1024
        for bitstring, probability in quasi_dist.binary_probabilities().items():
            count = int(probability * total_shots)
            if count > 0:
                print(f"   |{bitstring}⟩: {count:4d} shots ({probability:.3f})")
        
        # Analyze quantum performance
        bell_states = quasi_dist.get(0, 0) + quasi_dist.get(3, 0)  # |00⟩ + |11⟩
        error_states = quasi_dist.get(1, 0) + quasi_dist.get(2, 0)  # |01⟩ + |10⟩
        
        print(f"\n📊 Quantum Analysis:")
        print(f"   Bell Fidelity: {bell_states:.3f}")
        print(f"   Error Rate: {error_states:.3f} ({error_states*100:.1f}%)")
        
        if bell_states > 0.85:
            print("✅ Excellent quantum fidelity!")
        elif bell_states > 0.70:
            print("✅ Good quantum performance!")
        else:
            print("⚠️  High noise - typical for NISQ era")
            
        print(f"\n🌟 SUCCESS: Executed on {backend.name}!")
        print("🔬 You just used a real quantum computer!")
        
        return True
        
    except ImportError:
        print("❌ qiskit-ibm-runtime not installed")
        return False
        
    except Exception as e:
        error_msg = str(e).lower()
        
        if "network" in error_msg or "connection" in error_msg:
            print("❌ Network Error: Cannot reach IBM Quantum servers")
            print("   Need internet connection for quantum hardware")
        elif "401" in str(e) or "authentication" in error_msg:
            print("❌ Authentication Error: Invalid API token")
            print("   Check your IBM Quantum credentials")
        elif "timeout" in error_msg:
            print("❌ Timeout: Quantum computer queue may be full")
        else:
            print(f"❌ Error: {str(e)[:100]}...")
            
        return False

def show_quantum_hardware_info():
    """Show information about IBM quantum computers."""
    
    print("\n🖥️  IBM QUANTUM COMPUTERS (2024)")
    print("=" * 40)
    
    processors = [
        ("ibm_brisbane", 127, "Heron processor, latest generation"),
        ("ibm_kyoto", 127, "High-fidelity Heron processor"),
        ("ibm_osaka", 127, "Utility-scale quantum computer"),
        ("ibm_sherbrooke", 127, "Advanced Heron architecture")
    ]
    
    for name, qubits, desc in processors:
        print(f"🔹 {name}: {qubits} qubits")
        print(f"   {desc}")
    
    print(f"\n🎯 What makes them special:")
    print(f"• Real quantum superposition and entanglement")
    print(f"• Quantum error correction research")
    print(f"• Cryogenic cooling (~0.01 Kelvin)")
    print(f"• Superconducting qubit technology")

def main():
    """Main test execution."""
    
    print("🌟 IBM QUANTUM HARDWARE CONNECTION TEST")
    print("=" * 55)
    
    # Test hardware connection
    success = test_real_quantum_hardware()
    
    if not success:
        print("\n📚 While we wait for connection...")
        show_quantum_hardware_info()
        
        print("\n🔄 Next Steps:")
        print("• Ensure internet connection")
        print("• Try again when online")
        print("• Your credentials are ready!")
    
    print("\n" + "=" * 55)
    print("🚀 Ready for quantum computing!")

if __name__ == "__main__":
    main()
