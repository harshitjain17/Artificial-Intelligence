# Some potentially useful modules
import random
import numpy as np

class NeuralMMAgent(object):
    
    '''
    Class to for Neural Net Agents
    '''

    def __init__(self, num_in_nodes, num_hid_nodes, num_hid_layers, num_out_nodes,
                learning_rate = 0.2, max_epoch=10000, min_sse=.01, momentum=0,
                creation_function=None, activation_function=None, random_seed=1):
        '''
        Arguments:
            num_in_nodes -- total # of input nodes for Neural Net
            num_hid_nodes -- total # of hidden nodes for each hidden layer
                in the Neural Net
            num_hid_layers -- total # of hidden layers for Neural Net
            num_out_nodes -- total # of output layers for Neural Net
            learning_rate -- learning rate to be used when propogating error
            max_epoch -- maximum number of epochs for our NN to run during learning
            min_sse -- minimum SSE that we will use as a stopping point
            momentum -- Momentum term used for learning
            creation_function -- function that will be used to create the
                neural network given the input
            activation_function -- list of two functions:
                1st function will be used by network to determine activation given a weighted summed input
                2nd function will be the derivative of the 1st function
            random_seed -- used to seed object random attribute.
                This ensures that we can reproduce results if wanted
        '''
        assert num_in_nodes > 0 and num_hid_layers > 0 and num_hid_nodes > 0 and num_out_nodes > 0, "Illegal number of input, hidden, or output layers!"
        
        self.num_in_nodes = num_in_nodes
        self.num_hid_nodes = num_hid_nodes
        self.num_hid_layers = num_hid_layers
        self.num_out_nodes = num_out_nodes
        self.learning_rate = learning_rate
        self.max_epoch = max_epoch
        self.min_sse = min_sse
        self.momentum = momentum
        self.creation_function = creation_function
        self.activation_function = activation_function
        self.random_seed = random_seed

        if(activation_function is None):
            self.activation_function = [self.sigmoid_af , self.sigmoid_af_deriv]
        
        # create the neural network
        self.weights = []
        self.bias = []
        self.deltas = []
        self.random = random.Random(random_seed)
        
        if (self.creation_function is not None):
            creation_function()
            return

        # initialize input-hiddenLayer weights and biases
        weights_input_to_hidden = [np.random.uniform(-0.5, 0.5) for j in range(num_hid_nodes * num_in_nodes)]
        bias_hidden = [np.random.uniform(-0.5, 0.5) for i in range(num_in_nodes)]
        self.weights.append(weights_input_to_hidden)
        self.bias.append(bias_hidden)

        # initialize hidden layer weights and biases
        bias_hidden = [np.random.uniform(-0.5, 0.5) for i in range(num_hid_nodes)]
        self.bias.append(bias_hidden)
        for layer in range(num_hid_layers - 1):
            weights_hidden_to_hidden = [np.random.uniform(-0.5, 0.5) for j in range(num_hid_nodes * num_hid_nodes)]
            bias_hidden = [np.random.uniform(-0.5, 0.5) for i in range(num_hid_nodes)]
            self.weights.append(weights_hidden_to_hidden)
            self.bias.append(bias_hidden)

        # initialize hidden-output layer weights and biases
        weights_hidden_to_output = [np.random.uniform(-0.5, 0.5) for j in range(num_out_nodes * num_hid_nodes)]
        bias_out = [np.random.uniform(-0.5, 0.5) for i in range(num_out_nodes)]
        self.weights.append(weights_hidden_to_output)
        self.bias.append(bias_out)


    def train_net_incremental(self, input_list, output_list, max_num_epoch=None, min_sse=0.001):
        ''' Trains neural net using incremental learning
            (update once per input-output pair)
            Arguments:
                input_list -- 2D list of inputs
                output_list -- 2D list of outputs matching inputs
            Outputs:
                1d list of errors (total error each epoch) (e.g., [0.1])
        '''

        if(max_num_epoch is None):
            max_num_epoch = self.max_epoch
        self.max_epoch = max_num_epoch
        
        all_err = []
        weight_deltas = None
        for epoch in range(max_num_epoch):
            total_err = 0.0
            for row in range(len(input_list)):

                # feed forward and obtain the activations
                activations = self._feed_forward(input_list, row)
                
                # calculate the errors
                errors = []
                error_last_layer = []
                
                for i in range(len(output_list[row])):
                    error_last_layer.append((output_list[row][i] - activations[-1][i]) * self.activation_function[1](activations[-1][i]) * (-1))
                errors = [[0 for i in range(self.num_hid_nodes)]]

                for i in range(self.num_hid_layers):
                    errors.append([0 for i in range(self.num_hid_nodes)])
                errors.append(error_last_layer)

                total_err += sum([e ** 2 for e in errors[-1]])

                # calculate the deltas
                (little_deltas, weight_deltas, bias_deltas) = self._calculate_deltas(activations, errors, weight_deltas)
                
                # adjust the weights and biases
                (self.weights, self.bias) = self._adjust_weights_bias(weight_deltas, bias_deltas)
            
            all_err.append(total_err)
            if total_err < min_sse:
                break
        return all_err


    def _feed_forward(self, input_list, row):
        '''Used to feedforward input and calculate all activation values
            Arguments:
                input_list -- a list of possible input values
                row -- the row from that input_list that we should use
            Outputs:
                list of activation values
        '''    
        
        final_activation = [input_list[row]]
        
        for i in range(self.num_hid_layers + 1):
            activation_layer=[]
            
            for j in range(len(self.bias[i+1])):
                summation = 0

                for k in range(len(self.weights[i])):
                    if(k % len(self.bias[i+1]) == j):
                        summation += final_activation[i][k // len(self.bias[i+1])] * self.weights[i][k]
                activation_layer.append(self.activation_function[0](summation))

            final_activation.append(activation_layer)
        return final_activation
    
    def _calculate_deltas(self, activations, errors, prev_weight_deltas=None):
        '''Used to calculate all weight deltas for our neural net
            Parameters:
                activations -- a 2d list of activation values
                errors -- a 2d list of errors
                prev_weight_deltas [OPTIONAL] -- a 2d list of previous weight deltas
            Output:
                A tuple made up of 3 items:
                    A 2d list of little deltas (e.g., [[0, 0], [-0.1, 0.1], [0.1]])
                    A 2d list of weight deltas (e.g., [[-0.1, 0.1, -0.1, 0.1], [0.1, 0.1]])
                    A 2d list of bias deltas (e.g., [[0, 0], [-0.1, 0.1], [0]])
        '''

        # Calculate error gradient for each output node & propgate error
        # (calculate weight deltas going backward from output_nodes)

        little_deltas = []
        weight_deltas = []
        bias_deltas = []
        delta_layer = errors[-1]
        little_deltas.append(delta_layer)

        for i in range(self.num_hid_layers):
            delta_layer = []
            for j in range(self.num_hid_nodes):
                temp= 0
                for k in range(len(little_deltas[0])):
                    temp += self.weights[-1-i][k + (len(activations[-1-i]) * j)] * little_deltas[0][k]
                little_delta = self.activation_function[1](activations[-2-i][j]) * temp
                delta_layer.append(little_delta)
            little_deltas.insert(0, delta_layer)
        little_deltas.insert(0, self.num_in_nodes*[0])

        for i in range(len(little_deltas)):
            bias_layer = []
            for j in range(len(little_deltas[i])):
                bias_layer.append(little_deltas[i][j] * self.learning_rate)
            bias_deltas.append(bias_layer)

        for i in range(len(self.weights)):
            weight_layer = []
            for j in range(len(self.weights[i])):
                weight_layer.append(self.learning_rate * activations[i][j // int(len(activations[i+1]))] * little_deltas[i+1][j % len(activations[i+1])])
            weight_deltas.append(weight_layer)
        return (little_deltas, weight_deltas, bias_deltas)

    def _adjust_weights_bias(self, weight_deltas, bias_deltas):
        '''Used to apply deltas
        Parameters:
            weight_deltas -- 2d list of weight deltas
            bias_deltas -- 2d list of bias deltas
        Outputs:
            A tuple w/ the following items (in order):
            2d list of all weights after updating (e.g. [[-0.071, 0.078, 0.313, 0.323], [-0.34, 0.021]])
            list of all biases after updating (e.g., [[0, 0], [0, 0], [0]])
        '''
        bias = self.bias.copy()
        weights = self.weights.copy()
        
        for i in range(len(weights)):
            for j in range(len(weights[i])):
                weights[i][j]= self.weights[i][j] - weight_deltas[i][j]
        
        for i in range(len(bias)):
            for j in range(len(bias[i])):
                bias[i][j]= self.bias[i][j] - bias_deltas[i][j]
        
        return (weights, bias)
    

    #-----Begin ACCESSORS-----#
    def get_weights(self):
        return (self.weights)

    def set_weights(self, weights):
        self.weights = weights

    def get_biases(self):
        return (self.bias)

    def set_biases(self, biases):
        self.bias = biases
	#-----End ACCESSORS-----#

    @staticmethod
    def sigmoid_af(summed_input):

        # Sigmoid function
        return 1 / (1 + np.exp(-1 * summed_input))

    @staticmethod
    def sigmoid_af_deriv(sig_output):

        # The derivative of the sigmoid function
        return sig_output * (1 - sig_output)



# test_agent = NeuralMMAgent(2, 2, 1, 1,random_seed=5, max_epoch=1000000, learning_rate=0.2, momentum=0)
# test_in = [[1,0],[0,0],[1,1],[0,1]]
# test_out = [[1],[0],[0],[1]]
# test_agent.set_weights([[-.37,.26,.1,-.24],[-.01,-.05]])
# test_agent.set_biases([[0,0],[0,0],[0]])
# test_agent.train_net_incremental(test_in, test_out, max_num_epoch = 1000, min_sse = test_agent.min_sse )