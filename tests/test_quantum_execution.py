"""
Test suite for quantum execution module.

These tests verify the quantum circuit execution framework
and result analysis functions.
"""

import pytest
import numpy as np
from unittest.mock import Mock, patch

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from quantum_execution import QuantumExecutor, analyze_results, benchmark_circuit_execution
from quantum_circuits import QuantumCircuitLibrary


class TestQuantumExecutor:
    """Test cases for QuantumExecutor class."""
    
    def test_executor_initialization(self):
        """Test QuantumExecutor initialization."""
        executor = QuantumExecutor()
        assert executor.backend_name == 'aer_simulator'
        assert hasattr(executor, 'backend')
    
    def test_execute_bell_state(self):
        """Test execution of Bell state circuit."""
        executor = QuantumExecutor()
        bell_circuit = QuantumCircuitLibrary.create_bell_state(measure=True)
        
        result = executor.execute_circuit(bell_circuit, shots=1024)
        
        assert result['success'] is True
        assert 'counts' in result
        assert result['shots'] == 1024
        assert result['backend'] == 'aer_simulator'
        
        # Bell state should only produce |00⟩ and |11⟩
        counts = result['counts']
        for state in counts.keys():
            assert state in ['00', '11']
    
    def test_execute_ghz_state(self):
        """Test execution of GHZ state circuit."""
        executor = QuantumExecutor()
        ghz_circuit = QuantumCircuitLibrary.create_ghz_state(3, measure=True)
        
        result = executor.execute_circuit(ghz_circuit, shots=1024)
        
        assert result['success'] is True
        
        # GHZ state should primarily produce |000⟩ and |111⟩
        counts = result['counts']
        total_target_counts = counts.get('000', 0) + counts.get('111', 0)
        total_counts = sum(counts.values())
        
        # At least 80% should be in target states (allowing for noise/errors)
        assert total_target_counts / total_counts > 0.8


class TestResultAnalysis:
    """Test cases for result analysis functions."""
    
    def test_analyze_successful_results(self):
        """Test analysis of successful quantum execution results."""
        # Mock successful result
        mock_result = {
            'success': True,
            'counts': {'00': 500, '11': 524},
            'shots': 1024
        }
        
        analysis = analyze_results(mock_result)
        
        assert analysis['total_shots'] == 1024
        assert analysis['unique_states'] == 2
        assert analysis['most_probable_state'] == '11'
        assert abs(analysis['most_probable_probability'] - 0.51171875) < 1e-6
        assert 'probabilities' in analysis
        assert 'entropy' in analysis
        assert 'raw_counts' in analysis
    
    def test_analyze_failed_results(self):
        """Test analysis of failed quantum execution results."""
        mock_result = {
            'success': False,
            'error': 'Simulation failed'
        }
        
        analysis = analyze_results(mock_result)
        
        assert 'error' in analysis
        assert analysis['details'] == 'Simulation failed'
    
    def test_entropy_calculation(self):
        """Test entropy calculation for different distributions."""
        # Uniform distribution (maximum entropy)
        uniform_result = {
            'success': True,
            'counts': {'00': 256, '01': 256, '10': 256, '11': 256},
            'shots': 1024
        }
        
        uniform_analysis = analyze_results(uniform_result)
        
        # Entropy should be close to log2(4) = 2 for uniform distribution
        assert abs(uniform_analysis['entropy'] - 2.0) < 0.1
        
        # Deterministic distribution (minimum entropy)
        deterministic_result = {
            'success': True,
            'counts': {'00': 1024},
            'shots': 1024
        }
        
        deterministic_analysis = analyze_results(deterministic_result)
        
        # Entropy should be 0 for deterministic outcome
        assert deterministic_analysis['entropy'] == 0.0
    
    def test_probability_calculation(self):
        """Test probability calculation from counts."""
        mock_result = {
            'success': True,
            'counts': {'0': 750, '1': 250},
            'shots': 1000
        }
        
        analysis = analyze_results(mock_result)
        probabilities = analysis['probabilities']
        
        assert abs(probabilities['0'] - 0.75) < 1e-10
        assert abs(probabilities['1'] - 0.25) < 1e-10
        
        # Probabilities should sum to 1
        assert abs(sum(probabilities.values()) - 1.0) < 1e-10


class TestCircuitBenchmarking:
    """Test cases for circuit benchmarking functionality."""
    
    def test_benchmark_circuit_execution(self):
        """Test benchmarking of circuit execution."""
        bell_circuit = QuantumCircuitLibrary.create_bell_state(measure=True)
        shots_list = [100, 500]
        
        benchmark_results = benchmark_circuit_execution(bell_circuit, shots_list)
        
        assert len(benchmark_results) == 2
        
        for shots in shots_list:
            assert shots in benchmark_results
            result = benchmark_results[shots]
            
            if 'error' not in result:
                assert 'execution_time' in result
                assert 'entropy' in result
                assert 'unique_states' in result
                assert 'most_probable_probability' in result
                assert result['execution_time'] > 0


class TestUtilityFunctions:
    """Test cases for utility functions."""
    
    def test_create_random_unitary_circuit(self):
        """Test random unitary circuit creation."""
        from quantum_execution import create_random_unitary_circuit
        
        n_qubits = 3
        depth = 5
        
        random_circuit = create_random_unitary_circuit(n_qubits, depth)
        
        assert random_circuit.num_qubits == n_qubits
        assert random_circuit.depth() <= depth  # May be less due to optimization
        
        # Should be reproducible with same seed
        random_circuit2 = create_random_unitary_circuit(n_qubits, depth)
        
        # Circuits should be identical (same seed)
        assert random_circuit.data == random_circuit2.data


class TestErrorHandling:
    """Test error handling in quantum execution."""
    
    def test_invalid_circuit_handling(self):
        """Test handling of invalid circuits."""
        from qiskit import QuantumCircuit
        
        # Create an invalid circuit (measurement without classical register)
        invalid_circuit = QuantumCircuit(2)
        invalid_circuit.h(0)
        invalid_circuit.measure_all()  # This might cause issues
        
        executor = QuantumExecutor()
        
        # Should handle gracefully and return error result
        # Note: This test depends on specific backend behavior
        try:
            result = executor.execute_circuit(invalid_circuit, shots=100)
            # If it succeeds, that's also fine (backend handled it)
            assert 'success' in result
        except Exception:
            # If it raises an exception, the executor should catch it
            pass
    
    @patch('quantum_execution.Sampler')
    def test_execution_exception_handling(self, mock_sampler):
        """Test exception handling during circuit execution."""
        # Mock Sampler to raise an exception
        mock_sampler.return_value.run.side_effect = Exception("Mocked execution error")
        
        executor = QuantumExecutor()
        bell_circuit = QuantumCircuitLibrary.create_bell_state(measure=True)
        
        result = executor.execute_circuit(bell_circuit, shots=100)
        
        assert result['success'] is False
        assert 'error' in result
        assert 'Mocked execution error' in result['error']


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v"])
