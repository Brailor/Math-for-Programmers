import numpy as np
from math import exp

def sigmoid(x):
    return 1 / (1 + exp(-x))

class MLP:
    # layer_sizes => [3, 4, 4, 2]
    # each number is the number of neurons in that particular layer
    def __init__(self, layer_sizes) -> None:
        self.layer_sizes = layer_sizes
        self.weights = [
            # rows, columns
            np.random.rand(n,m)
            for m,n in zip(layer_sizes[:-1], layer_sizes[1:])
        ]
        self.biases = [
            np.random.random(n)
            for n in layer_sizes[1:]
        ]

    def feedforward(self, v):
        val = v
        activations = []
        activations.append(val)

        for weight,bias in zip(self.weights, self.biases):
            z = weight @ val + bias
            val = [sigmoid(a) for a in z]
            activations.append(val)
        
        return activations
    
    def eval(self, v):
        return np.array(self.feedforward(v)[-1])