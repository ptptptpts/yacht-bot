import random
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
    __data_size = 10

    __input_size = 5

    def start(self):
        self.__init_self()
        model = self.__build_model()
        training_set = \
            self.__data_preparation(self.__play_num, self.__data_size, lambda s: random.randrange(0, 100))
        self.__train_model(model, training_set)

        def predictors(s):
            x_array = np.array(s).reshape(-1, self.__input_size)
            x_array = np.asarray(x_array).astype('float32')
            return int(model.predict(x_array)[0])

        for i in range(self.__learning_size):
            self.__init_self()
            print("================================")
            training_set = \
                self.__data_preparation(self.__play_num, self.__data_size, predictors)
            # self.__train_model(model, training_set)
            self.__avg_score = self.__avg_score / self.__play_num
            print("Average score: ", self.__avg_score)
            print("Max score: ", self.__max_score)
            print("Min score: ", self.__min_score)

    def __init_self(self):
        print(tf.test.is_gpu_available())
        print(tf.test.gpu_device_name())
        print(device_lib.list_local_devices())
        self.__avg_score = 0
        self.__max_score = 0
        self.__min_score = 400

    def __data_preparation(self, play_num, data_size, ai_func):
        game_data = []
        for i in range(play_num):
            print("Play " + str(i) + " round")
            score = 0
            game_steps = []
            self.__yacht.start()
            while not self.__yacht.is_game_finish():
                game_status = self.__yacht.get_game_status()
                action = ai_func(game_status)
                game_steps.append((game_status, action))
                self.__yacht.play_robot_round(action)
            score = self.__yacht.get_player_point()
            game_data.append((score, game_steps))

            self.__avg_score += score
            if score > self.__max_score:
                self.__max_score = score
            if score < self.__min_score:
                self.__min_score = score

        game_data.sort(key=lambda s: -s[0])

        training_set = []
        for i in range(data_size):
            for step in game_data[i][1]:
                training_set.append((step[0], step[1]))

        return training_set

    def __build_model(self):
        model = Sequential()
        model.add(Dense(128, input_dim=self.__input_size, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(1, activation='softmax'))
        model.compile(loss='mse', optimizer=Adam())
        return model

    def __train_model(self, model, training_set):
        x_array = np.array([i[0] for i in training_set]).reshape(-1, self.__input_size)
        x_array = np.asarray(x_array).astype('float32')
        y_array = np.array([i[1] for i in training_set]).reshape(-1, 1)
        y_array = np.asarray(y_array).astype('float32')
        model.fit(x_array, y_array, epochs=10, verbose=0)
