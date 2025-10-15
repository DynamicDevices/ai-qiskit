#!/usr/bin/env python3
"""
IBM Quantum Hardware Connection Example

Shows how to connect to real IBM quantum computers
and run circuits on actual quantum hardware.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from quantum_circuits import QuantumCircuitLibrary
from quantum_execution import analyze_results


def setup_ibm_quantum():
    """Setup connection to IBM Quantum."""
    
    print("🔗 IBM Quantum Hardware Setup")
    print("=" * 40)
    
    try:
        # Try to import IBM Quantum Runtime
        from qiskit_ibm_runtime import QiskitRuntimeService
        
        print("✅ qiskit-ibm-runtime is available")
        print("\n📋 Setup Instructions:")
        print("1. Create IBM Quantum account: https://quantum-computing.ibm.com/")
        print("2. Get your API token from the account dashboard")
        print("3. Install IBM Runtime: pip install qiskit-ibm-runtime")
        print("4. Save credentials:")
        print("   QiskitRuntimeService.save_account(channel='ibm_quantum', token='YOUR_TOKEN')")
        
        # Try to load saved account
        try:
            service = QiskitRuntimeService()
            backends = service.backends()
            
            print(f"\n🎯 Available Backends: {len(backends)}")
            for backend in backends[:5]:  # Show first 5
                status = "🟢 Available" if backend.status().operational else "🔴 Unavailable"
                print(f"  - {backend.name}: {backend.num_qubits} qubits {status}")
            
            return service
            
        except Exception as e:
            print(f"\n⚠️  No saved credentials found: {e}")
            print("Run: QiskitRuntimeService.save_account(channel='ibm_quantum', token='YOUR_TOKEN')")
            return None
            
    except ImportError:
        print("❌ qiskit-ibm-runtime not installed")
        print("Install with: pip install qiskit-ibm-runtime")
        return None


def run_on_quantum_hardware(service=None):
    """Run a circuit on real quantum hardware."""
    
    if service is None:
        print("⚠️  No IBM Quantum service available - using simulator")
        from quantum_execution import QuantumExecutor
        executor = QuantumExecutor()
        
        bell_circuit = QuantumCircuitLibrary.create_bell_state(measure=True)
        result = executor.execute_circuit(bell_circuit, shots=1024)
        
        if result['success']:
            analysis = analyze_results(result)
            print(f"\n📊 Simulator Results:")
            print(f"Entropy: {analysis['entropy']:.3f}")
            print(f"Most probable: |{analysis['most_probable_state']}⟩")
        
        return result
    
    print("\n🚀 Running on Quantum Hardware")
    print("-" * 40)
    
    try:
        # Get least busy backend
        backends = service.backends(operational=True, simulator=False)
        if not backends:
            print("❌ No quantum hardware available")
            return None
        
        # Sort by queue length and select least busy
        backend = min(backends, key=lambda b: b.status().pending_jobs)
        
        print(f"Selected backend: {backend.name}")
        print(f"Queue length: {backend.status().pending_jobs}")
        print(f"Qubits: {backend.num_qubits}")
        
        # Create a simple circuit
        bell_circuit = QuantumCircuitLibrary.create_bell_state(measure=True)
        
        # Transpile for hardware
        from qiskit import transpile
        transpiled = transpile(bell_circuit, backend, optimization_level=3)
        
        print(f"\nOriginal circuit depth: {bell_circuit.depth()}")
        print(f"Transpiled circuit depth: {transpiled.depth()}")
        
        # Submit job
        from qiskit_ibm_runtime import Sampler
        
        sampler = Sampler(backend)
        job = sampler.run([transpiled], shots=1024)
        
        print(f"\n📤 Job submitted: {job.job_id()}")
        print("⏳ Waiting for results (this may take several minutes)...")
        
        result = job.result()
        
        # Convert results
        counts = {}
        for i, prob in result.quasi_dists[0].items():
            bit_string = format(i, f'0{bell_circuit.num_clbits}b')
            counts[bit_string] = int(prob * 1024)
        
        hardware_result = {
            'counts': counts,
            'shots': 1024,
            'success': True,
            'backend': backend.name,
            'job_id': job.job_id()
        }
        
        analysis = analyze_results(hardware_result)
        
        print(f"\n🎯 Hardware Results from {backend.name}:")
        print(f"Job ID: {job.job_id()}")
        print(f"Entropy: {analysis['entropy']:.3f}")
        print(f"Most probable: |{analysis['most_probable_state']}⟩ ({analysis['most_probable_probability']:.3f})")
        
        print(f"\n📊 State Distribution:")
        for state, prob in analysis['probabilities'].items():
            print(f"  |{state}⟩: {prob:.3f}")
        
        return hardware_result
        
    except Exception as e:
        print(f"❌ Hardware execution failed: {e}")
        return None


def compare_simulator_vs_hardware():
    """Compare results between simulator and real hardware."""
    
    print("\n⚖️  Simulator vs Hardware Comparison")
    print("=" * 50)
    
    # Run on simulator
    from quantum_execution import QuantumExecutor
    executor = QuantumExecutor()
    bell_circuit = QuantumCircuitLibrary.create_bell_state(measure=True)
    
    sim_result = executor.execute_circuit(bell_circuit, shots=1024)
    sim_analysis = analyze_results(sim_result)
    
    print("🖥️  Simulator Results:")
    print(f"  Entropy: {sim_analysis['entropy']:.3f}")
    print(f"  Most probable: |{sim_analysis['most_probable_state']}⟩")
    
    # Setup hardware (if available)
    service = setup_ibm_quantum()
    hw_result = run_on_quantum_hardware(service)
    
    if hw_result and hw_result['success']:
        hw_analysis = analyze_results(hw_result)
        
        print(f"\n🔬 Hardware Results:")
        print(f"  Entropy: {hw_analysis['entropy']:.3f}")
        print(f"  Most probable: |{hw_analysis['most_probable_state']}⟩")
        
        # Compare entropies
        entropy_diff = abs(sim_analysis['entropy'] - hw_analysis['entropy'])
        print(f"\n📈 Comparison:")
        print(f"  Entropy difference: {entropy_diff:.3f}")
        print(f"  Hardware shows {'more' if hw_analysis['entropy'] > sim_analysis['entropy'] else 'less'} randomness")
        
        if entropy_diff > 0.1:
            print("  💡 Significant difference indicates quantum noise effects!")
        else:
            print("  ✅ Results are quite similar - good quantum fidelity!")


def main():
    """Main function to demonstrate IBM Quantum connection."""
    
    print("🌐 IBM Quantum Hardware Integration")
    print("=" * 50)
    
    # Setup and test connection
    service = setup_ibm_quantum()
    
    if service:
        print("\n✅ Successfully connected to IBM Quantum!")
        compare_simulator_vs_hardware()
    else:
        print("\n⚠️  Running in simulator mode only")
        print("\n🔧 To enable hardware access:")
        print("1. pip install qiskit-ibm-runtime")
        print("2. Create account at https://quantum-computing.ibm.com/")
        print("3. Save your API token:")
        print("   from qiskit_ibm_runtime import QiskitRuntimeService")
        print("   QiskitRuntimeService.save_account(channel='ibm_quantum', token='YOUR_TOKEN')")
        
        # Still show simulator comparison
        compare_simulator_vs_hardware()
    
    print("\n" + "=" * 50)
    print("🎯 Next Steps with IBM Quantum:")
    print("- Explore different quantum backends")
    print("- Run variational algorithms on hardware")
    print("- Study quantum error rates and noise")
    print("- Try quantum error mitigation techniques")


if __name__ == "__main__":
    main()
