#!/usr/bin/env python3
"""
Quick IBM Quantum Setup Script

Run this after getting your API token from IBM Quantum website.
"""

def setup_ibm_credentials():
    """Interactive setup for IBM Quantum credentials."""
    
    print("🔑 IBM Quantum API Setup")
    print("=" * 30)
    
    print("\n📋 You should have:")
    print("1. ✅ IBM Quantum account created")
    print("2. ✅ API token copied from IBM Quantum dashboard")
    print("3. 🔄 Ready to save credentials")
    
    try:
        # Get token from user
        token = input("\n🔑 Paste your IBM Quantum API token here: ").strip()
        
        if not token:
            print("❌ No token provided. Please try again.")
            return False
        
        # Save the token
        from qiskit_ibm_runtime import QiskitRuntimeService
        
        QiskitRuntimeService.save_account(
            channel='ibm_quantum',
            token=token,
            overwrite=True
        )
        
        print("\n✅ IBM Quantum credentials saved successfully!")
        
        # Test the connection
        print("\n🔬 Testing connection...")
        service = QiskitRuntimeService()
        backends = service.backends()
        
        print(f"✅ Connection successful! Found {len(backends)} quantum backends.")
        
        # Show available backends
        print("\n🚀 Available Quantum Computers:")
        for backend in backends[:5]:  # Show first 5
            status = "🟢 Available" if backend.status().operational else "🔴 Unavailable"
            print(f"  - {backend.name}: {backend.num_qubits} qubits {status}")
        
        print(f"\n🎯 Ready to run quantum circuits on real hardware!")
        print("Try: python3 examples/quantum_hardware_demo.py")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please check your token and try again.")
        return False


if __name__ == "__main__":
    success = setup_ibm_credentials()
    
    if success:
        print("\n🎉 Setup complete! You can now:")
        print("• Run circuits on real quantum computers")
        print("• Access IBM's quantum processors") 
        print("• Compare simulator vs hardware results")
    else:
        print("\n🔧 Setup incomplete. Please:")
        print("• Double-check your API token")
        print("• Ensure you have an IBM Quantum account")
        print("• Try running this script again")
