"""
Test suite for quantum circuits module.

These tests verify the correctness of quantum circuit implementations
following Qiskit best practices.
"""

import pytest
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, Operator

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from quantum_circuits import QuantumCircuitLibrary


class TestQuantumCircuitLibrary:
    """Test cases for QuantumCircuitLibrary."""
    
    def test_bell_state_creation(self):
        """Test Bell state circuit creation."""
        # Test without measurement
        bell_circuit = QuantumCircuitLibrary.create_bell_state(measure=False)
        
        assert bell_circuit.num_qubits == 2
        assert bell_circuit.num_clbits == 0
        assert bell_circuit.name == 'bell_state'
        
        # Verify the Bell state |00⟩ + |11⟩
        statevector = Statevector.from_instruction(bell_circuit)
        expected = np.array([1/np.sqrt(2), 0, 0, 1/np.sqrt(2)])
        np.testing.assert_allclose(statevector.data, expected, atol=1e-10)
    
    def test_bell_state_with_measurement(self):
        """Test Bell state circuit with measurements."""
        bell_circuit = QuantumCircuitLibrary.create_bell_state(measure=True)
        
        assert bell_circuit.num_qubits == 2
        assert bell_circuit.num_clbits == 2
        
        # Check that measurement operations are present
        has_measure = any(instr.operation.name == 'measure' 
                         for instr in bell_circuit.data)
        assert has_measure
    
    def test_ghz_state_creation(self):
        """Test GHZ state circuit creation."""
        # Test 3-qubit GHZ state
        ghz_circuit = QuantumCircuitLibrary.create_ghz_state(3, measure=False)
        
        assert ghz_circuit.num_qubits == 3
        assert ghz_circuit.name == 'ghz_3_state'
        
        # Verify the GHZ state |000⟩ + |111⟩
        statevector = Statevector.from_instruction(ghz_circuit)
        expected = np.zeros(8)
        expected[0] = 1/np.sqrt(2)  # |000⟩
        expected[7] = 1/np.sqrt(2)  # |111⟩
        np.testing.assert_allclose(statevector.data, expected, atol=1e-10)
    
    def test_ghz_state_invalid_qubits(self):
        """Test GHZ state with invalid number of qubits."""
        with pytest.raises(ValueError, match="GHZ state requires at least 3 qubits"):
            QuantumCircuitLibrary.create_ghz_state(2)
    
    def test_qft_creation(self):
        """Test Quantum Fourier Transform creation."""
        qft_circuit = QuantumCircuitLibrary.create_quantum_fourier_transform(3)
        
        assert qft_circuit.num_qubits == 3
        assert qft_circuit.name == 'qft_3'
        
        # QFT should be unitary
        operator = Operator(qft_circuit)
        assert operator.is_unitary(atol=1e-10)
    
    def test_variational_circuit_creation(self):
        """Test variational circuit creation."""
        var_circuit = QuantumCircuitLibrary.create_variational_circuit(
            n_qubits=3, depth=2, entanglement='linear'
        )
        
        assert var_circuit.num_qubits == 3
        assert var_circuit.num_parameters > 0
        
        # Check that parameters can be bound
        params = np.random.random(var_circuit.num_parameters) * 2 * np.pi
        bound_circuit = var_circuit.assign_parameters(params)
        assert bound_circuit.num_parameters == 0
    
    def test_grover_oracle_creation(self):
        """Test Grover oracle creation."""
        marked_items = ['101', '110']
        oracle = QuantumCircuitLibrary.create_grover_oracle(marked_items)
        
        assert oracle.num_qubits == 3
        assert oracle.name == 'grover_oracle'
    
    def test_grover_oracle_empty_items(self):
        """Test Grover oracle with empty marked items."""
        with pytest.raises(ValueError, match="At least one marked item required"):
            QuantumCircuitLibrary.create_grover_oracle([])
    
    def test_grover_oracle_inconsistent_length(self):
        """Test Grover oracle with inconsistent item lengths."""
        with pytest.raises(ValueError, match="All marked items must have same length"):
            QuantumCircuitLibrary.create_grover_oracle(['10', '101'])


class TestCircuitProperties:
    """Test quantum circuit properties and transformations."""
    
    def test_circuit_depth_calculation(self):
        """Test that circuit depth is calculated correctly."""
        bell_circuit = QuantumCircuitLibrary.create_bell_state(measure=False)
        
        # Bell state should have depth 2 (H gate, then CNOT)
        assert bell_circuit.depth() == 2
    
    def test_circuit_gate_count(self):
        """Test gate counting in circuits."""
        bell_circuit = QuantumCircuitLibrary.create_bell_state(measure=False)
        
        # Bell state has 2 gates: H and CNOT
        assert len(bell_circuit.data) == 2
    
    def test_qft_inverse_property(self):
        """Test that QFT followed by inverse QFT is identity."""
        n_qubits = 3
        qft = QuantumCircuitLibrary.create_quantum_fourier_transform(n_qubits)
        
        # Create circuit with QFT followed by inverse QFT
        test_circuit = QuantumCircuit(n_qubits)
        test_circuit.compose(qft, inplace=True)
        test_circuit.compose(qft.inverse(), inplace=True)
        
        # Should be close to identity
        operator = Operator(test_circuit)
        identity = Operator.from_label('I' * n_qubits)
        
        # Check if operators are approximately equal
        fidelity = np.abs(np.trace(operator.data @ identity.data.conj().T)) / (2 ** n_qubits)
        assert fidelity > 0.99  # Should be very close to 1


class TestCircuitValidation:
    """Test circuit validation and error handling."""
    
    def test_circuit_register_names(self):
        """Test that circuits have proper register names."""
        bell_circuit = QuantumCircuitLibrary.create_bell_state(measure=True)
        
        # Check quantum register name
        qreg_names = [reg.name for reg in bell_circuit.qregs]
        assert 'q' in qreg_names
        
        # Check classical register name
        creg_names = [reg.name for reg in bell_circuit.cregs]
        assert 'c' in creg_names
    
    def test_circuit_barriers(self):
        """Test that circuits use barriers appropriately."""
        from quantum_circuits import add_barrier_if_nonempty
        
        # Empty circuit should not get barrier
        empty_circuit = QuantumCircuit(2)
        add_barrier_if_nonempty(empty_circuit)
        assert len(empty_circuit.data) == 0
        
        # Non-empty circuit should get barrier
        circuit_with_gate = QuantumCircuit(2)
        circuit_with_gate.h(0)
        add_barrier_if_nonempty(circuit_with_gate)
        
        # Should have H gate + barrier
        assert len(circuit_with_gate.data) == 2
        assert circuit_with_gate.data[-1].operation.name == 'barrier'


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v"])
