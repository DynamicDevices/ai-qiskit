"""
Quantum Simulators and Execution

This module provides utilities for running quantum circuits on simulators
and real quantum hardware following Qiskit best practices.
"""

from qiskit import QuantumCircuit, transpile
from qiskit.primitives import Sampler, Estimator
from qiskit.quantum_info import SparsePauliOp
from typing import Dict, List, Optional, Union, Tuple
import numpy as np
from collections import Counter


class QuantumExecutor:
    """
    Quantum circuit execution with best practices for error handling and optimization.
    """
    
    def __init__(self, backend_name: str = 'aer_simulator'):
        """
        Initialize quantum executor.
        
        Args:
            backend_name: Name of the backend to use
        """
        self.backend_name = backend_name
        self._setup_backend()
    
    def _setup_backend(self):
        """Setup the quantum backend."""
        if self.backend_name == 'aer_simulator':
            # Try to use AerSimulator, fallback to basic simulator
            try:
                from qiskit_aer import AerSimulator
                self.backend = AerSimulator()
            except ImportError:
                # Fallback to basic simulator if Aer not available
                from qiskit.providers.basic_provider import BasicProvider
                provider = BasicProvider()
                self.backend = provider.get_backend('basic_simulator')
                print("Warning: qiskit-aer not available, using basic simulator")
        else:
            # For real quantum hardware, would connect to IBM Quantum
            # This requires IBM Quantum account setup
            raise NotImplementedError("Real hardware execution requires IBM Quantum setup")
    
    def execute_circuit(self, circuit: QuantumCircuit, shots: int = 1024) -> Dict:
        """
        Execute a quantum circuit with proper error handling.
        
        Args:
            circuit: Quantum circuit to execute
            shots: Number of measurement shots
            
        Returns:
            Dict: Execution results
        """
        try:
            # Transpile circuit for the target backend
            transpiled_circuit = transpile(circuit, self.backend, optimization_level=2)
            
            # Execute using Sampler primitive (recommended approach)
            sampler = Sampler()
            job = sampler.run([transpiled_circuit], shots=shots)
            result = job.result()
            
            # Convert to counts format for compatibility
            counts = {}
            if hasattr(result, 'quasi_dists') and result.quasi_dists:
                # New Sampler format
                for i, prob in result.quasi_dists[0].items():
                    bit_string = format(i, f'0{circuit.num_clbits}b')
                    counts[bit_string] = int(prob * shots)
            else:
                # Fallback for basic simulator - execute directly
                from qiskit import execute
                job = execute(transpiled_circuit, self.backend, shots=shots)
                result = job.result()
                counts = result.get_counts(transpiled_circuit)
            
            return {
                'counts': counts,
                'shots': shots,
                'success': True,
                'backend': self.backend_name,
                'transpiled_circuit': transpiled_circuit
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'backend': self.backend_name
            }
    
    def estimate_expectation_value(self, circuit: QuantumCircuit, 
                                 observable: SparsePauliOp, 
                                 shots: int = 1024) -> Dict:
        """
        Estimate expectation value of an observable.
        
        Args:
            circuit: Quantum circuit (without measurements)
            observable: Pauli operator to measure
            shots: Number of measurement shots
            
        Returns:
            Dict: Expectation value results
        """
        try:
            # Transpile circuit
            transpiled_circuit = transpile(circuit, self.backend, optimization_level=2)
            
            # Use Estimator primitive
            estimator = Estimator()
            job = estimator.run([transpiled_circuit], [observable], shots=shots)
            result = job.result()
            
            return {
                'expectation_value': result.values[0],
                'standard_error': result.metadata[0].get('standard_error', 0),
                'shots': shots,
                'success': True,
                'backend': self.backend_name
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'backend': self.backend_name
            }


class QuantumNoiseModel:
    """
    Noise modeling for realistic quantum simulations.
    """
    
    @staticmethod
    def create_basic_noise_model(error_rate: float = 0.01) -> object:
        """
        Create a basic noise model for simulation.
        
        Args:
            error_rate: Basic error rate for gates
            
        Returns:
            NoiseModel: Qiskit noise model
        """
        try:
            from qiskit_aer.noise import NoiseModel, depolarizing_error
            
            noise_model = NoiseModel()
            
            # Add depolarizing error to all single-qubit gates
            single_qubit_error = depolarizing_error(error_rate, 1)
            noise_model.add_all_qubit_quantum_error(single_qubit_error, ['h', 'x', 'y', 'z', 's', 't'])
            
            # Add depolarizing error to all two-qubit gates
            two_qubit_error = depolarizing_error(error_rate * 2, 2)
            noise_model.add_all_qubit_quantum_error(two_qubit_error, ['cx', 'cy', 'cz'])
            
            return noise_model
            
        except ImportError:
            print("Warning: qiskit-aer not available, returning None for noise model")
            return None


def analyze_results(results: Dict) -> Dict:
    """
    Analyze quantum execution results.
    
    Args:
        results: Results from quantum execution
        
    Returns:
        Dict: Analysis of results
    """
    if not results.get('success', False):
        return {'error': 'Execution failed', 'details': results.get('error', 'Unknown error')}
    
    counts = results['counts']
    total_shots = sum(counts.values())
    
    # Calculate probabilities
    probabilities = {state: count / total_shots for state, count in counts.items()}
    
    # Find most probable state
    most_probable = max(counts.items(), key=lambda x: x[1])
    
    # Calculate entropy (measure of randomness)
    entropy = -sum(p * np.log2(p) for p in probabilities.values() if p > 0)
    
    return {
        'total_shots': total_shots,
        'unique_states': len(counts),
        'probabilities': probabilities,
        'most_probable_state': most_probable[0],
        'most_probable_probability': most_probable[1] / total_shots,
        'entropy': entropy,
        'raw_counts': counts
    }


def visualize_results(results: Dict, title: str = "Quantum Circuit Results") -> None:
    """
    Visualize quantum execution results.
    
    Args:
        results: Results from quantum execution
        title: Plot title
    """
    try:
        import matplotlib.pyplot as plt
        
        if not results.get('success', False):
            print(f"Cannot visualize failed execution: {results.get('error', 'Unknown error')}")
            return
        
        counts = results['counts']
        states = list(counts.keys())
        values = list(counts.values())
        
        plt.figure(figsize=(12, 6))
        plt.bar(states, values)
        plt.xlabel('Quantum States')
        plt.ylabel('Measurement Counts')
        plt.title(title)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
        
    except ImportError:
        print("Matplotlib not available for visualization")
    except Exception as e:
        print(f"Visualization error: {e}")


# Utility functions for common quantum operations
def create_random_unitary_circuit(n_qubits: int, depth: int = 10) -> QuantumCircuit:
    """
    Create a random unitary circuit for testing.
    
    Args:
        n_qubits: Number of qubits
        depth: Circuit depth
        
    Returns:
        QuantumCircuit: Random unitary circuit
    """
    from qiskit.circuit.random import random_circuit
    
    return random_circuit(
        num_qubits=n_qubits,
        depth=depth,
        measure=False,
        seed=42  # For reproducibility
    )


def benchmark_circuit_execution(circuit: QuantumCircuit, 
                              shots_list: List[int] = [100, 1000, 10000]) -> Dict:
    """
    Benchmark circuit execution with different shot counts.
    
    Args:
        circuit: Circuit to benchmark
        shots_list: List of shot counts to test
        
    Returns:
        Dict: Benchmark results
    """
    executor = QuantumExecutor()
    benchmark_results = {}
    
    for shots in shots_list:
        import time
        start_time = time.time()
        
        result = executor.execute_circuit(circuit, shots=shots)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        if result['success']:
            analysis = analyze_results(result)
            benchmark_results[shots] = {
                'execution_time': execution_time,
                'entropy': analysis['entropy'],
                'unique_states': analysis['unique_states'],
                'most_probable_probability': analysis['most_probable_probability']
            }
        else:
            benchmark_results[shots] = {
                'execution_time': execution_time,
                'error': result['error']
            }
    
    return benchmark_results
