#!/usr/bin/env python3
"""
Real Quantum Hardware Example

This script demonstrates running quantum circuits on actual IBM quantum computers
and compares results with simulators to show real quantum effects.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from quantum_circuits import QuantumCircuitLibrary
from quantum_execution import QuantumExecutor, analyze_results
import numpy as np


def setup_ibm_quantum_runtime():
    """Setup IBM Quantum Runtime service."""
    
    print("🌐 Setting up IBM Quantum Runtime")
    print("=" * 40)
    
    try:
        # Install IBM Quantum Runtime if not available
        try:
            from qiskit_ibm_runtime import QiskitRuntimeService
        except ImportError:
            print("📦 Installing qiskit-ibm-runtime...")
            import subprocess
            subprocess.run([sys.executable, "-m", "pip", "install", "qiskit-ibm-runtime"], 
                         capture_output=True)
            from qiskit_ibm_runtime import QiskitRuntimeService
        
        print("✅ qiskit-ibm-runtime is available!")
        
        # Try to load existing credentials
        try:
            service = QiskitRuntimeService()
            print("✅ Found saved IBM Quantum credentials!")
            return service
        except Exception:
            print("\n🔑 No saved credentials found.")
            print("\n📋 To connect to real quantum hardware:")
            print("1. Create account: https://quantum-computing.ibm.com/")
            print("2. Get your API token from the dashboard")
            print("3. Run this command:")
            print("   from qiskit_ibm_runtime import QiskitRuntimeService")
            print("   QiskitRuntimeService.save_account(channel='ibm_quantum', token='YOUR_TOKEN')")
            return None
            
    except Exception as e:
        print(f"❌ Error setting up IBM Quantum: {e}")
        return None


def run_bell_state_comparison():
    """Compare Bell state results between simulator and quantum hardware."""
    
    print("\n🔬 Bell State: Simulator vs Quantum Hardware")
    print("=" * 50)
    
    # Create Bell state circuit
    bell_circuit = QuantumCircuitLibrary.create_bell_state(measure=True)
    
    print("Bell State Circuit:")
    print(bell_circuit.draw())
    print("\nExpected: Only |00⟩ and |11⟩ outcomes with ~50% each")
    
    # Run on simulator
    print("\n🖥️  Running on Simulator...")
    simulator_executor = QuantumExecutor('aer_simulator')
    sim_result = simulator_executor.execute_circuit(bell_circuit, shots=1024)
    
    if sim_result['success']:
        sim_analysis = analyze_results(sim_result)
        print(f"Simulator Results:")
        for state, prob in sim_analysis['probabilities'].items():
            print(f"  |{state}⟩: {prob:.3f}")
        print(f"Entropy: {sim_analysis['entropy']:.3f}")
    
    # Try quantum hardware
    service = setup_ibm_quantum_runtime()
    
    if service:
        print("\n🔬 Running on Quantum Hardware...")
        
        try:
            # Get available backends
            backends = service.backends(operational=True, simulator=False)
            
            if not backends:
                print("❌ No quantum hardware currently available")
                return sim_result, None
            
            # Find least busy backend
            backend = min(backends, key=lambda b: b.status().pending_jobs)
            
            print(f"Selected backend: {backend.name}")
            print(f"Qubits: {backend.num_qubits}")
            print(f"Queue length: {backend.status().pending_jobs}")
            
            # Transpile for hardware
            from qiskit import transpile
            transpiled = transpile(bell_circuit, backend, optimization_level=3)
            
            print(f"Circuit depth after transpilation: {transpiled.depth()}")
            
            # Execute on hardware using Sampler
            from qiskit_ibm_runtime import Sampler
            
            sampler = Sampler(backend)
            print("📤 Submitting job to quantum computer...")
            
            job = sampler.run([transpiled], shots=1024)
            print(f"Job ID: {job.job_id()}")
            print("⏳ Waiting for quantum computer... (this may take several minutes)")
            
            # Wait for results
            result = job.result()
            
            # Process hardware results
            hw_counts = {}
            for i, prob in result.quasi_dists[0].items():
                bit_string = format(i, f'0{bell_circuit.num_clbits}b')
                hw_counts[bit_string] = int(prob * 1024)
            
            hw_result = {
                'counts': hw_counts,
                'shots': 1024,
                'success': True,
                'backend': backend.name,
                'job_id': job.job_id()
            }
            
            hw_analysis = analyze_results(hw_result)
            
            print(f"\n🎯 Quantum Hardware Results ({backend.name}):")
            for state, prob in hw_analysis['probabilities'].items():
                print(f"  |{state}⟩: {prob:.3f}")
            print(f"Entropy: {hw_analysis['entropy']:.3f}")
            
            # Compare results
            print(f"\n📊 Comparison:")
            print(f"Simulator entropy: {sim_analysis['entropy']:.3f}")
            print(f"Hardware entropy:  {hw_analysis['entropy']:.3f}")
            
            entropy_diff = abs(sim_analysis['entropy'] - hw_analysis['entropy'])
            print(f"Entropy difference: {entropy_diff:.3f}")
            
            if entropy_diff > 0.1:
                print("💡 Significant difference - quantum noise effects visible!")
            else:
                print("✅ Similar results - good quantum fidelity!")
            
            # Check for unexpected states
            unexpected_states = [state for state in hw_counts.keys() 
                               if state not in ['00', '11'] and hw_counts[state] > 10]
            
            if unexpected_states:
                print(f"🔍 Quantum errors detected in states: {unexpected_states}")
                print("   This shows real quantum decoherence and gate errors!")
            
            return sim_result, hw_result
            
        except Exception as e:
            print(f"❌ Hardware execution failed: {e}")
            print("💡 This is normal - quantum computers have limited availability")
            return sim_result, None
    
    else:
        print("\n💡 To run on real quantum hardware:")
        print("1. Create IBM Quantum account: https://quantum-computing.ibm.com/")
        print("2. Install: pip install qiskit-ibm-runtime")
        print("3. Save credentials as shown above")
        
        return sim_result, None


def demonstrate_quantum_noise():
    """Show how quantum noise affects different circuits."""
    
    print("\n🌊 Quantum Noise Demonstration")
    print("=" * 40)
    
    circuits = {
        "Single Qubit (|0⟩)": QuantumCircuit(1, 1),
        "Superposition (H)": QuantumCircuit(1, 1),
        "Bell State": QuantumCircuitLibrary.create_bell_state(measure=True)
    }
    
    # Prepare circuits
    circuits["Superposition (H)"].h(0)
    circuits["Superposition (H)"].measure(0, 0)
    
    circuits["Single Qubit (|0⟩)"].measure(0, 0)
    
    simulator_executor = QuantumExecutor()
    
    print("Circuit sensitivity to quantum noise:")
    print("(Lower entropy = more sensitive to errors)")
    
    for name, circuit in circuits.items():
        result = simulator_executor.execute_circuit(circuit, shots=1000)
        if result['success']:
            analysis = analyze_results(result)
            print(f"\n{name}:")
            print(f"  Entropy: {analysis['entropy']:.3f}")
            print(f"  Most probable: |{analysis['most_probable_state']}⟩ ({analysis['most_probable_probability']:.3f})")


def quantum_hardware_tutorial():
    """Interactive tutorial for quantum hardware."""
    
    print("🎓 Quantum Hardware Tutorial")
    print("=" * 35)
    
    print("\n🔬 What makes quantum hardware special?")
    print("• Real quantum effects: superposition, entanglement, interference")
    print("• Quantum noise: decoherence, gate errors, measurement errors") 
    print("• Limited coherence time: quantum states decay quickly")
    print("• NISQ era: Noisy Intermediate-Scale Quantum devices")
    
    print("\n⚡ Current quantum computers:")
    print("• IBM: Up to 1000+ qubits (e.g., Condor, Heron processors)")
    print("• Google: Sycamore (70 qubits)")  
    print("• IonQ: Trapped ion systems (32+ qubits)")
    print("• Rigetti: Superconducting qubits")
    
    print("\n🎯 Why use real hardware?")
    print("• Test quantum algorithms under realistic conditions")
    print("• Study quantum error patterns") 
    print("• Develop error mitigation techniques")
    print("• Prepare for fault-tolerant quantum computing")
    
    print("\n📈 Quantum advantage experiments:")
    print("• Google's quantum supremacy (2019)")
    print("• IBM's quantum volume benchmarks")
    print("• Quantum error correction demonstrations")


def main():
    """Run quantum hardware examples."""
    
    print("🚀 Real Quantum Hardware Examples")
    print("=" * 40)
    
    # Educational content
    quantum_hardware_tutorial()
    
    # Demonstrate noise effects
    demonstrate_quantum_noise()
    
    # Try to run on real hardware
    sim_result, hw_result = run_bell_state_comparison()
    
    print("\n" + "=" * 50)
    print("🎯 Key Takeaways:")
    
    if hw_result:
        print("✅ Successfully ran on quantum hardware!")
        print("• Real quantum computers show noise effects")
        print("• Results differ from perfect simulators")
        print("• This demonstrates genuine quantum physics")
    else:
        print("🖥️  Ran on quantum simulator")
        print("• Simulators give 'perfect' quantum results")
        print("• Real hardware would show additional noise")
        print("• Set up IBM account to try real hardware")
    
    print("\n🔬 Next Steps:")
    print("• Set up IBM Quantum account for hardware access")
    print("• Try quantum error mitigation techniques")
    print("• Explore different quantum processors")
    print("• Study quantum error correction codes")
    
    return sim_result, hw_result


if __name__ == "__main__":
    from qiskit import QuantumCircuit
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Quantum exploration interrupted!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nThis is normal if you don't have IBM Quantum credentials set up.")
        print("The example still demonstrates quantum concepts using simulators!")
