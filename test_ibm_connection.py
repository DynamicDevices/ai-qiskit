#!/usr/bin/env python3
"""
Test IBM Quantum Connection

Run this script when you have internet access to test your 
IBM Quantum hardware connection.
"""

def test_ibm_quantum_connection():
    """Test connection to IBM Quantum hardware."""
    
    print("🔬 Testing IBM Quantum Connection")
    print("=" * 40)
    
    try:
        from qiskit_ibm_runtime import QiskitRuntimeService
        
        # Load saved credentials
        service = QiskitRuntimeService()
        print("✅ IBM Quantum credentials loaded successfully!")
        
        # Get available backends
        backends = service.backends()
        print(f"🚀 Found {len(backends)} quantum backends available!")
        
        # Show quantum computers
        print(f"\n🔬 Available Quantum Computers:")
        for i, backend in enumerate(backends):
            status = "🟢 Available" if backend.status().operational else "🔴 Unavailable"
            queue_length = backend.status().pending_jobs
            
            print(f"{i+1:2d}. {backend.name}")
            print(f"     Qubits: {backend.num_qubits}")
            print(f"     Status: {status}")
            print(f"     Queue: {queue_length} jobs")
            print()
        
        # Find least busy backend
        operational_backends = [b for b in backends if b.status().operational]
        
        if operational_backends:
            least_busy = min(operational_backends, key=lambda b: b.status().pending_jobs)
            print(f"🎯 Recommended backend: {least_busy.name}")
            print(f"   Qubits: {least_busy.num_qubits}")
            print(f"   Queue: {least_busy.status().pending_jobs} jobs")
        else:
            print("⚠️  No quantum computers currently operational")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection error: {e}")
        
        if "No active account" in str(e):
            print("\n🔧 Solution: Run the API key setup again")
        elif "Name or service not known" in str(e):
            print("\n🌐 Network issue: Check internet connection")
        elif "Unauthorized" in str(e):
            print("\n🔑 Authentication issue: Check your API key")
        else:
            print(f"\n🔍 Debug info: {str(e)[:200]}")
        
        return False


def run_simple_quantum_test():
    """Run a simple test on quantum hardware."""
    
    print("\n🧪 Running Simple Quantum Test")
    print("-" * 30)
    
    try:
        from qiskit import QuantumCircuit
        from qiskit_ibm_runtime import Sampler
        import sys
        import os
        sys.path.append('src')
        
        from quantum_circuits import QuantumCircuitLibrary
        
        # Create simple Bell state
        bell_circuit = QuantumCircuitLibrary.create_bell_state(measure=True)
        print("Created Bell state circuit for testing")
        
        # Get service and select backend
        service = QiskitRuntimeService()
        backends = [b for b in service.backends() if b.status().operational]
        
        if not backends:
            print("❌ No operational quantum computers available")
            return False
        
        # Use least busy backend
        backend = min(backends, key=lambda b: b.status().pending_jobs)
        print(f"Selected backend: {backend.name} ({backend.num_qubits} qubits)")
        
        # Create sampler and submit job
        sampler = Sampler(backend)
        print("Submitting job to quantum computer...")
        
        job = sampler.run([bell_circuit], shots=1024)
        print(f"Job ID: {job.job_id()}")
        print("⏳ Waiting for results (this may take several minutes)...")
        
        # Get results
        result = job.result()
        
        # Process results
        counts = {}
        for i, prob in result.quasi_dists[0].items():
            bit_string = format(i, f'0{bell_circuit.num_clbits}b')
            counts[bit_string] = int(prob * 1024)
        
        print(f"\n🎯 Quantum Hardware Results:")
        for state, count in sorted(counts.items()):
            prob = count / 1024
            print(f"  |{state}⟩: {count:4d} ({prob:.3f})")
        
        # Check for quantum effects
        expected_states = counts.get('00', 0) + counts.get('11', 0)
        error_states = sum(count for state, count in counts.items() 
                          if state not in ['00', '11'])
        
        print(f"\n📊 Analysis:")
        print(f"Expected Bell states (00, 11): {expected_states/1024:.3f}")
        print(f"Quantum errors: {error_states/1024:.3f}")
        
        if error_states > 50:  # More than 5% error
            print("🌊 Quantum noise effects visible!")
        else:
            print("✨ High fidelity quantum execution!")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def main():
    """Main test function."""
    
    print("🚀 IBM Quantum Hardware Test")
    print("=" * 50)
    
    # Test connection
    connected = test_ibm_quantum_connection()
    
    if connected:
        print("\n" + "="*50)
        choice = input("Run quantum circuit on hardware? (y/N): ").strip().lower()
        
        if choice in ['y', 'yes']:
            run_simple_quantum_test()
        else:
            print("Skipping hardware test.")
    
    print("\n" + "="*50)
    print("🎯 Next Steps:")
    print("• Your IBM Quantum credentials are saved and ready")
    print("• Run quantum circuits on real hardware when connected")
    print("• Try: python3 examples/quantum_hardware_demo.py")
    print("• Explore different quantum processors and their capabilities")


if __name__ == "__main__":
    main()
