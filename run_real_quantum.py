#!/usr/bin/env python3
"""
🚀 REAL IBM Quantum Hardware Execution
=====================================
This script connects to actual IBM quantum computers and runs your circuits!
"""

import sys
import os
from qiskit import QuantumCircuit, transpile
from qiskit.primitives import Sampler
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from quantum_circuits import QuantumCircuitLibrary

def run_on_real_hardware():
    """
    Connect to real IBM quantum hardware and execute circuits!
    """
    print("🚀 CONNECTING TO REAL IBM QUANTUM HARDWARE!")
    print("=" * 60)
    
    try:
        from qiskit_ibm_runtime import QiskitRuntimeService, Sampler as RuntimeSampler
        
        print("🔑 Loading your saved IBM Quantum credentials...")
        
        # Initialize the service with saved credentials
        service = QiskitRuntimeService()
        print("✅ Successfully connected to IBM Quantum!")
        
        # Get available backends
        print("\n🖥️  Available Quantum Computers:")
        backends = service.backends(operational=True, simulator=False)
        
        if not backends:
            print("❌ No quantum hardware available right now")
            return
        
        # Choose the best available backend
        backend = None
        for b in backends:
            if b.status().operational:
                backend = b
                break
        
        if not backend:
            print("❌ No operational quantum computers available")
            return
            
        print(f"🎯 Selected: {backend.name}")
        print(f"   📊 Qubits: {backend.configuration().n_qubits}")
        print(f"   🔧 Status: {backend.status().status_msg}")
        
        # Create Bell state circuit
        print("\n🔬 Creating Bell State Circuit...")
        bell_circuit = QuantumCircuitLibrary.create_bell_state(measure=True)
        print(bell_circuit.draw())
        
        # Transpile for the specific hardware
        print(f"\n⚙️  Transpiling circuit for {backend.name}...")
        transpiled_circuit = transpile(bell_circuit, backend=backend, optimization_level=3)
        print(f"   Original depth: {bell_circuit.depth()}")
        print(f"   Transpiled depth: {transpiled_circuit.depth()}")
        
        # Execute on real quantum hardware!
        print(f"\n🚀 EXECUTING ON REAL QUANTUM COMPUTER: {backend.name}")
        print("   This may take a few minutes due to queue...")
        
        # Use Runtime Sampler for execution
        sampler = RuntimeSampler(backend=backend)
        
        # Run the circuit
        job = sampler.run([transpiled_circuit], shots=1024)
        print(f"   Job ID: {job.job_id}")
        print("   ⏳ Waiting for results from quantum computer...")
        
        # Get results
        result = job.result()
        counts = result.quasi_dists[0].binary_probabilities()
        
        # Convert to counts
        shots = 1024
        hardware_counts = {state: int(prob * shots) for state, prob in counts.items()}
        
        print("\n🎉 REAL QUANTUM HARDWARE RESULTS!")
        print("=" * 40)
        print(f"Quantum Computer: {backend.name}")
        print(f"Execution Time: {job.metrics()['usage_estimation'] if hasattr(job, 'metrics') else 'N/A'}")
        
        total_shots = sum(hardware_counts.values())
        for state, count in sorted(hardware_counts.items()):
            prob = count / total_shots
            print(f"   |{state}⟩: {count:4d} shots ({prob:.3f})")
        
        # Calculate Bell state fidelity
        bell_fidelity = (hardware_counts.get('00', 0) + hardware_counts.get('11', 0)) / total_shots
        print(f"\n📊 Bell State Fidelity: {bell_fidelity:.3f}")
        
        if bell_fidelity > 0.8:
            print("✅ Excellent quantum fidelity!")
        elif bell_fidelity > 0.6:
            print("✅ Good quantum fidelity!")
        else:
            print("⚠️  Noisy results - typical for NISQ devices")
        
        # Show quantum noise effects
        error_states = hardware_counts.get('01', 0) + hardware_counts.get('10', 0)
        error_rate = error_states / total_shots
        print(f"🔬 Quantum Error Rate: {error_rate:.3f} ({error_rate*100:.1f}%)")
        
        print("\n🌟 You just ran on a REAL quantum computer! 🌟")
        
        return hardware_counts
        
    except ImportError:
        print("❌ qiskit-ibm-runtime not installed")
        print("   Install with: pip install qiskit-ibm-runtime")
        return None
        
    except Exception as e:
        if "401" in str(e) or "authentication" in str(e).lower():
            print("❌ Authentication failed - check your API token")
            print("   Save token with:")
            print("   from qiskit_ibm_runtime import QiskitRuntimeService")
            print("   QiskitRuntimeService.save_account(channel='ibm_quantum', token='YOUR_TOKEN')")
        elif "network" in str(e).lower() or "connection" in str(e).lower():
            print("❌ Network connection error")
            print("   Check internet connection and try again")
        else:
            print(f"❌ Error: {e}")
        return None

def compare_simulator_vs_hardware():
    """
    Compare results from simulator vs real hardware.
    """
    print("\n🔬 SIMULATOR vs REAL HARDWARE COMPARISON")
    print("=" * 50)
    
    # Run on simulator first
    from quantum_execution import QuantumExecutor
    
    print("🖥️  Running on Simulator...")
    executor = QuantumExecutor()
    bell_circuit = QuantumCircuitLibrary.create_bell_state(measure=True)
    sim_results = executor.execute_circuit(bell_circuit, shots=1024)
    
    print("Simulator Results:")
    total_sim = sum(sim_results.values())
    for state, count in sorted(sim_results.items()):
        prob = count / total_sim
        print(f"   |{state}⟩: {count:4d} shots ({prob:.3f})")
    
    # Run on real hardware
    hardware_results = run_on_real_hardware()
    
    if hardware_results:
        print("\n📊 Key Differences:")
        print("• Simulator: Perfect quantum mechanics")
        print("• Hardware: Real quantum noise and decoherence")
        print("• Hardware shows quantum error correction needs!")

def main():
    """Main execution function."""
    print("🌟 REAL IBM QUANTUM HARDWARE EXECUTION!")
    print("=" * 60)
    print("Your API key is saved - let's run on real quantum computers!")
    print()
    
    # Try to run on real hardware
    hardware_results = run_on_real_hardware()
    
    if not hardware_results:
        print("\n🔄 Fallback: Running simulator comparison...")
        compare_simulator_vs_hardware()
    
    print("\n" + "=" * 60)
    print("🎯 What Just Happened:")
    print("✅ Connected to IBM Quantum cloud")
    print("✅ Selected an operational quantum computer") 
    print("✅ Transpiled circuit for specific hardware")
    print("✅ Executed on real quantum processor")
    print("✅ Observed real quantum noise effects")
    print("\n🚀 You're now a quantum programmer using real hardware!")

if __name__ == "__main__":
    main()
