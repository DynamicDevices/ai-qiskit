#!/usr/bin/env python3
"""
IBM Quantum Setup Helper

This script helps you connect to real IBM quantum computers.
"""

def setup_ibm_quantum_credentials():
    """Interactive setup for IBM Quantum credentials."""
    
    print("🌐 IBM Quantum Setup Helper")
    print("=" * 35)
    
    print("\n📋 Step-by-Step Setup:")
    print("1. 🌍 Go to: https://quantum-computing.ibm.com/")
    print("2. 📝 Create a free account (or log in)")
    print("3. 🔑 Copy your API token from the dashboard")
    print("4. 💾 Save it using the code below")
    
    print("\n" + "="*50)
    print("🔧 COPY AND RUN THIS CODE:")
    print("="*50)
    
    code = """
# Run this in Python to save your IBM Quantum credentials
from qiskit_ibm_runtime import QiskitRuntimeService

# Replace 'YOUR_TOKEN_HERE' with your actual token
QiskitRuntimeService.save_account(
    channel='ibm_quantum', 
    token='YOUR_TOKEN_HERE'
)

print("✅ IBM Quantum credentials saved!")
"""
    
    print(code)
    print("="*50)
    
    print("\n🎯 After setup, you can:")
    print("• Run circuits on real quantum computers")
    print("• Access IBM's quantum processors")
    print("• See real quantum noise effects")
    print("• Compare simulator vs hardware results")
    
    print("\n🚀 Test your setup:")
    print("python3 examples/quantum_hardware_demo.py")


def check_ibm_quantum_status():
    """Check if IBM Quantum is already set up."""
    
    try:
        from qiskit_ibm_runtime import QiskitRuntimeService
        
        try:
            service = QiskitRuntimeService()
            backends = service.backends()
            
            print("✅ IBM Quantum is set up!")
            print(f"Available backends: {len(backends)}")
            
            # Show a few backends
            print("\n🔬 Available Quantum Computers:")
            for backend in backends[:5]:
                status = "🟢" if backend.status().operational else "🔴"
                print(f"  {status} {backend.name}: {backend.num_qubits} qubits")
            
            return True
            
        except Exception:
            print("❌ IBM Quantum credentials not found")
            return False
            
    except ImportError:
        print("📦 Installing qiskit-ibm-runtime...")
        import subprocess
        import sys
        
        subprocess.run([
            sys.executable, "-m", "pip", "install", "qiskit-ibm-runtime"
        ], capture_output=True)
        
        print("✅ qiskit-ibm-runtime installed!")
        return False


def main():
    """Main setup function."""
    
    print("🚀 IBM Quantum Backend Setup")
    print("=" * 40)
    
    # Check current status
    is_setup = check_ibm_quantum_status()
    
    if not is_setup:
        setup_ibm_quantum_credentials()
    else:
        print("\n🎉 You're ready to use quantum hardware!")
        print("\nTry running:")
        print("python3 examples/quantum_hardware_demo.py")
        print("python3 examples/ibm_quantum_hardware.py")


if __name__ == "__main__":
    main()
