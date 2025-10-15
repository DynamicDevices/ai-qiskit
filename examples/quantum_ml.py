#!/usr/bin/env python3
"""
Quantum Machine Learning Example

Demonstrates quantum neural networks and quantum feature maps
using Qiskit Machine Learning.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

from qiskit import QuantumCircuit
from qiskit.circuit.library import ZZFeatureMap, RealAmplitudes
from qiskit.primitives import Sampler
from qiskit_machine_learning.neural_networks import SamplerQNN
from qiskit_machine_learning.algorithms.classifiers import NeuralNetworkClassifier

from quantum_execution import QuantumExecutor


def create_quantum_feature_map(num_features=2, num_qubits=2):
    """Create a quantum feature map for data encoding."""
    feature_map = ZZFeatureMap(
        feature_dimension=num_features,
        reps=2,
        entanglement='linear'
    )
    return feature_map


def create_quantum_neural_network():
    """Create a quantum neural network for binary classification."""
    
    # Generate synthetic dataset
    X, y = make_classification(
        n_samples=100,
        n_features=2,
        n_redundant=0,
        n_informative=2,
        n_clusters_per_class=1,
        random_state=42
    )
    
    # Normalize features to [0, 1] range for quantum encoding
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.3, random_state=42
    )
    
    print("📊 Dataset Information:")
    print(f"Training samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")
    print(f"Feature range: [{X_scaled.min():.2f}, {X_scaled.max():.2f}]")
    
    return X_train, X_test, y_train, y_test, scaler


def build_quantum_classifier():
    """Build and train a quantum neural network classifier."""
    
    print("\n🧠 Building Quantum Neural Network")
    print("-" * 40)
    
    # Create quantum circuits
    num_qubits = 2
    feature_map = create_quantum_feature_map(num_features=2, num_qubits=num_qubits)
    ansatz = RealAmplitudes(num_qubits=num_qubits, reps=3)
    
    # Combine feature map and ansatz
    qc = QuantumCircuit(num_qubits)
    qc.compose(feature_map, inplace=True)
    qc.compose(ansatz, inplace=True)
    
    print(f"Quantum circuit depth: {qc.depth()}")
    print(f"Number of parameters: {qc.num_parameters}")
    
    # Create quantum neural network
    sampler = Sampler()
    
    # Define output shape for binary classification
    qnn = SamplerQNN(
        circuit=qc,
        input_params=feature_map.parameters,
        weight_params=ansatz.parameters,
        sampler=sampler,
        output_shape=2  # Binary classification
    )
    
    print(f"QNN input dimension: {qnn.num_inputs}")
    print(f"QNN weight dimension: {qnn.num_weights}")
    
    return qnn


def train_quantum_classifier():
    """Train the quantum classifier on synthetic data."""
    
    print("\n🚀 Quantum Machine Learning Demo")
    print("=" * 50)
    
    # Prepare data
    X_train, X_test, y_train, y_test, scaler = create_quantum_neural_network()
    
    # Build quantum neural network
    qnn = build_quantum_classifier()
    
    # Create classifier
    classifier = NeuralNetworkClassifier(
        neural_network=qnn,
        optimizer='COBYLA',  # Classical optimizer
        loss='cross_entropy'
    )
    
    print("\n🎯 Training Quantum Classifier...")
    print("This may take a few minutes...")
    
    # Train the classifier
    classifier.fit(X_train, y_train)
    
    # Evaluate on test set
    train_score = classifier.score(X_train, y_train)
    test_score = classifier.score(X_test, y_test)
    
    print(f"\n📈 Results:")
    print(f"Training accuracy: {train_score:.3f}")
    print(f"Test accuracy: {test_score:.3f}")
    
    # Make predictions
    y_pred = classifier.predict(X_test)
    
    print(f"\n🔍 Sample Predictions:")
    for i in range(min(5, len(X_test))):
        print(f"Sample {i+1}: True={y_test[i]}, Predicted={y_pred[i]}")
    
    return classifier, X_test, y_test, y_pred


def visualize_quantum_feature_map():
    """Visualize how quantum feature map encodes classical data."""
    
    print("\n🎨 Quantum Feature Map Visualization")
    print("-" * 40)
    
    # Create simple 2D data points
    data_points = np.array([
        [0.0, 0.0],
        [0.5, 0.5], 
        [1.0, 1.0],
        [0.2, 0.8]
    ])
    
    feature_map = create_quantum_feature_map(num_features=2, num_qubits=2)
    
    print("Data encoding in quantum feature map:")
    for i, point in enumerate(data_points):
        # Bind parameters
        bound_circuit = feature_map.bind_parameters(point)
        
        print(f"Point {i+1}: {point} -> {bound_circuit.num_parameters} quantum parameters")
        print(f"  Circuit depth: {bound_circuit.depth()}")
    
    print("\n💡 The feature map encodes classical data into quantum states")
    print("   Higher-dimensional quantum Hilbert space enables quantum advantage!")


def main():
    """Run quantum machine learning examples."""
    
    try:
        # Visualize feature encoding
        visualize_quantum_feature_map()
        
        # Train quantum classifier
        classifier, X_test, y_test, y_pred = train_quantum_classifier()
        
        print("\n" + "=" * 50)
        print("✅ Quantum Machine Learning Demo Completed!")
        print("\n🎯 Key Concepts Demonstrated:")
        print("- Quantum feature maps for data encoding")
        print("- Variational quantum circuits as neural networks") 
        print("- Hybrid classical-quantum optimization")
        print("- Binary classification with quantum advantage potential")
        
        print("\n🔬 Next Steps:")
        print("- Try different datasets and feature maps")
        print("- Experiment with deeper quantum circuits")
        print("- Compare with classical ML performance")
        print("- Explore quantum kernels and QSVMs")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure qiskit-machine-learning is installed!")
        print("pip install qiskit-machine-learning")


if __name__ == "__main__":
    main()
