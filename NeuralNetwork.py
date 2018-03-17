from Matrix import Matrix
import math
import random


def sigmoid(val):
    return 1 / (1 + math.exp(-val))


def dsigmoid(val):
    return sigmoid(val) * (1 - sigmoid(val))


def tanh(val):
    return (math.exp(val) - math.exp(-val)) / (math.exp(val) + math.exp(-val))


def dtanh(val):
    return 1 - (tanh(val) * tanh(val))


class NeuralNetwork:
    def __init__(self, nodes):
        if isinstance(nodes, NeuralNetwork):
            self.nodes_arr = nodes.nodes_arr
            self.weights_arr = []
            self.function = sigmoid
            self.dfunction = dsigmoid
            self.bias_arr = []
            self.layers = len(nodes.nodes_arr) - 1
            self.lr = nodes.lr

            for i in range(len(nodes.weights_arr)):
                self.weights_arr.append(nodes.weights_arr[i].copy())
                self.bias_arr.append(nodes.bias_arr[i].copy())

        else:
            self.nodes_arr = nodes
            self.weights_arr = []
            self.function = sigmoid
            self.dfunction = dsigmoid
            self.bias_arr = []
            self.layers = len(nodes) - 1
            self.lr = 0.1

            for i in range(1, self.layers + 1):
                m = Matrix(nodes[i], nodes[i - 1])
                m.randomize()
                self.weights_arr.append(m)
                b = Matrix(nodes[i], 1)
                b.randomize()
                self.bias_arr.append(b)

    def feedforward(self, input_arr):
        input_matrix = Matrix.fromArray(input_arr)

        cur_matrix = input_matrix
        for i in range(self.layers):
            next_matrix = Matrix.multiply(self.weights_arr[i], cur_matrix)
            next_matrix += self.bias_arr[i]
            next_matrix.map(self.function)

            cur_matrix = next_matrix

        return cur_matrix

    def train(self, input_arr, output_arr):
        input_matrix = Matrix.fromArray(input_arr)

        cur_matrix = input_matrix
        activations = [cur_matrix]
        zs = [cur_matrix]
        for i in range(self.layers):
            z = Matrix.multiply(self.weights_arr[i], cur_matrix)
            z += self.bias_arr[i]
            zs.append(z)
            activation = Matrix.mapMatrix(z, self.function)
            activations.append(activation)
            cur_matrix = activation

        answer_matrix = Matrix.fromArray(output_arr)
        error_matrix = answer_matrix - activations[-1]

        cur_err = error_matrix
        for i in reversed(range(0, self.layers)):
            # adjusting weights and bias, with the current error and the current index

            gradients = Matrix.mapMatrix(zs[i + 1], self.dfunction)
            gradients *= cur_err
            gradients *= self.lr

            hidden_T = Matrix.transpose(activations[i])
            weights_deltas = Matrix.multiply(gradients, hidden_T)

            self.weights_arr[i] += weights_deltas

            self.bias_arr[i] += gradients

            # recalculating current error
            h_T = Matrix.transpose(self.weights_arr[i])
            next_error = Matrix.multiply(h_T, cur_err)
            cur_err = next_error

    def train_epoch(self, trainingData):
        for item in trainingData:
            self.train(item["inputs"], item["outputs"])

    def setLearningRate(self, val):
        self.lr = val

    def setActivationFunction(self, func, dfunc):
        self.function = func
        self.dfunction = dfunc

    def copy(self):
        return NeuralNetwork(self)

    def mutate(self, mr, change):
        for i in range(self.layers):
            self.weights_arr[i].mutate(mr, change)
            self.bias_arr[i].mutate(mr, change)

    def __str__(self):
        string = ""
        string += "Neural Network with {} layers, containing {} nodes".format(self.layers + 1, self.nodes_arr)
        string += "\n"
        string += "weights: \n"
        for m in self.weights_arr:
            string += str(m)
            string += "\n"
        string += "bias: \n"
        for b in self.bias_arr:
            string += str(b)
            string += "\n"

        return string
