#
# Copyright (c) 2019. Asutosh Nayak (nayak.asutosh@ymail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#


"""
Individual class represents each individual in a population that participate in reproduction.
In this project each Neural Network model is represented as Individual.
"""
import sys

import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout
from utils import *
import uuid


class Individual:
    def __init__(self, nn_prams: dict, **kwargs):
        self.__nn_params = nn_prams
        self.func_model = kwargs['func_create_model'] if 'func_create_model' in kwargs and kwargs[
            'func_create_model'] else self.create_model
        self.__model = self.func_model(nn_prams)
        self.__fitness_score = 0.0
        self.mt_dna = uuid.uuid4().hex

    def create_model(self, params: dict = None):
        """
        Creates a Keras NeuralNet model using parameters in 'params' dict.
        :param params: expects a dict with hyper parameters for NN.
        format of 'params' {'batch_size': 100, 'nodes_1': 500, 'do_1': 0.0, 'activation_1': 'sigmoid', 'lr': 1e-07,
        'epochs': 3000, 'optimizer': 'sgd', 'output_nodes': 10, 'output_activation: 'softmax',
        'loss': ['categorical_crossentropy']}
        :return: Keras Sequential model
        """

        if not params:
            params = self.__nn_params

        num_layers = 0
        for key in params.keys():
            if key.startswith('nodes_layer_'):
                num_layers = num_layers + 1

        if num_layers == 0:
            raise Exception("Please specify number of nodes for each layer using format nodes_layer_{layer_number}")

        try:
            model = Sequential()
            for i in range(num_layers):
                i = str(i + 1)
                if i == '1':
                    model.add(
                        Dense(params["nodes_layer_" + i], input_shape=(params['input_size'],),
                              activation=params['activation_layer_' + i] if ('activation_layer_' + i) in params
                              else None))
                else:
                    model.add(
                        Dense(params["nodes_layer_" + i],
                              activation=params['activation_layer_' + i] if ('activation_layer_' + i) in params
                              else None))
                if 'do_layer_' + i in params:
                    model.add(Dropout(params['do_layer_' + i]))

            model.add(Dense(params['output_nodes'], activation=params['output_activation']))
            model.compile(loss=params['loss'], optimizer=params["optimizer"], metrics=['accuracy'])  # TODO metric
        except Exception as ex:
            log("problem params", params)
            log("exception:", str(ex))
            log_flush()
            sys.exit()
        return model

    def set_fitness_score(self, score):
        self.__fitness_score = score

    def get_fitness_score(self):
        return self.__fitness_score

    def get_model(self):
        return self.__model

    def set_model(self, params):
        self.__model = self.func_model(params)

    def set_nn_params(self, nn_params):
        self.__nn_params = nn_params
        self.__model = self.create_model()

    def get_nn_params(self):
        return self.__nn_params

    def __deepcopy__(self, memodict={}):
        copy = Individual(self.__nn_params.copy())
        copy.func_model = self.func_model
        copy.__model = self.__model
        copy.__fitness_score = self.__fitness_score
        return copy

    def reset_id(self):
        self.mt_dna = uuid.uuid4().hex

    # def __eq__(self, other):
    #     return self.__nn_params == other.get_nn_params() and self.__fitness_score == other.get_fitness_score()
