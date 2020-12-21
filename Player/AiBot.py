import random
import time

import numpy as np
import tensorflow as tf

from keras.layers import Dense
from keras.models import Sequential
from keras.optimizers import Adam
from tensorflow.python.client import device_lib

from Yacht.RobotYacht import RobotYacht


class YachtAiBot:
    __debug = False
    __yacht = RobotYacht()

    __avg_score = 0
    __max_score = 0
    __min_score = 400

    __learning_size = 100

    __play_num = 100
    __data_size = 100

    __input_size = 20
    __output_size = 5

    __bit_size = 5

    def start(self):
        print(tf.config.list_logical_devices('GPU'))
        print(tf.test.gpu_device_name())
        print(device_lib.list_local_devices())
        self.__init_self()
        model = self.__build_model()
        training_set = \
            self.__data_preparation(self.__play_num, self.__data_size, lambda s: random.randrange(0, 100))
        self.__train_model(model, training_set)

        def predictors(s):
            x_array = np.array(s).reshape(-1, self.__input_size)
            x_array = np.asarray(x_array).astype('float32')
            output_array = model(x_array, training=False)
            output = 0
            for bit in range(self.__bit_size):
                output = (output << 1) + int(output_array[0][bit])
            return output

        for i in range(self.__learning_size):
            t = time.time()
            self.__init_self()
            print("================================")
            training_set = \
                self.__data_preparation(self.__play_num, self.__data_size, predictors)
            self.__train_model(model, training_set)
            self.__avg_score = self.__avg_score / self.__play_num
            print("Average score: ", self.__avg_score)
            print("Max score: ", self.__max_score)
            print("Min score: ", self.__min_score)
            print("Execute time: " + str(time.time() - t))

    def __init_self(self):
        self.__avg_score = 0
        self.__max_score = 0
        self.__min_score = 400

    def __data_preparation(self, play_num, data_size, ai_func):
        game_data = []
        for i in range(play_num):
            score = 0
            game_steps = []
            self.__yacht.start()
            while not self.__yacht.is_game_finish():
                round_score = self.__yacht.get_player_point()
                for round in range(5):
                    game_status = self.__yacht.get_game_status_float()
                    action = ai_func(game_status)
                    bit_action = [0, 0, 0, 0, 0]
                    for bit in range(self.__bit_size):
                        bit_action[self.__bit_size - 1 - bit] = action % 2
                        action = action >> 1
                    game_steps.append((game_status, bit_action))
                    self.__yacht.play_robot_round(action)
                round_score = self.__yacht.get_player_point() - round_score
            score = self.__yacht.get_player_point()
            game_data.append((score, game_steps))

            self.__avg_score += score
            if score > self.__max_score:
                self.__max_score = score
            if score < self.__min_score:
                self.__min_score = score

        game_data.sort(key=lambda s: -s[0])

        for i in range(10):
            print(str(i) + "th score :" + str(game_data[i][0]))

        training_set = []
        for i in range(data_size):
            for step in game_data[i][1]:
                training_set.append((step[0], step[1]))

        return training_set

    def __build_model(self):
        model = Sequential()
        model.add(Dense(128, input_dim=self.__input_size, activation='sigmoid'))
        model.add(Dense(32, activation='sigmoid'))
        model.add(Dense(5, activation='sigmoid'))
        model.compile(loss='mse', optimizer=Adam())
        return model

    def __train_model(self, model, training_set):
        x_array = np.array([i[0] for i in training_set]).reshape(-1, self.__input_size)
        y_array = np.array([i[1] for i in training_set]).reshape(-1, self.__output_size)
        t = time.time()
        hist = model.fit(x_array, y_array, epochs=1000, verbose=0)
        print("Learning info: ")
        print(hist.history)
        print("Training time: " + str(time.time() - t))
