import random
import time

import numpy as np
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from keras.optimizer_v2.adam import Adam
from tensorflow.python.client import device_lib

from Player.PercentageBot import YachtPercentageBot
from Yacht.RobotYacht import RobotYacht


class YachtAiBot:
    # Input vector
    # Game status[56] = Integer[56] = Round(1) + Step(1) + Dices(30) + Score status(12) + Scores(12)
    # Round: Integer = 1 - 12
    # Step: Integer = 0 - 2
    # Dices: Boolean[30] = Boolean[6] * 5 = [0, 0, 0, 0, 0, 0] * 5
    # Score status: Boolean[12]
    #    = [one, two, three, four, five, six, choice, four card, full house, small straight, large straight, yacht]
    # Scores: Integer[12]
    #    = [one, two, three, four, five, six, choice, four card, full house, small straight, large straight, yacht]
    #
    # Output vector
    # Action[17] = Float[17] = Softmax[12] (Select scoreboard) + Sigmoid[5] (Select hold)
    # Softmax[12]: Put a score from the highest item and select the next highest one if it is already written.
    # Sigmoid[5]: Hold dice if x is larger than 0.5.

    __debug = False
    __yacht = RobotYacht()

    __avg_score = 0
    __max_score = 0
    __min_score = 400

    __learning_size = 1000

    __play_num = 1000
    __data_size = 100

    __input_size = 56
    __output_size = 17

    def start(self):
        print("Start AiBot")
        print("Tensorflow version ", tf.version)
        print(tf.config.list_logical_devices('GPU'))
        print(tf.test.gpu_device_name())
        print(device_lib.list_local_devices())
        self.__init_self()
        model = self.__build_model()

        YachtPercentageBot.build_score_array()

        def percentage_predictors(s):
            return YachtPercentageBot.expect_next_input(s)

        def random_predictor(s):
            output = []
            for score in range(17):
                output.append(random.random())
            sum = 0.0
            for index in range(12):
                sum += output[index] * 10000
            for index in range(12):
                output[index] = (output[index] * 10000) / sum
            return output

        t = time.time()
        training_set = \
            self.__data_preparation(100, 40, percentage_predictors)
        print("Execute time: " + str(time.time() - t))
        self.__train_model(model, training_set)

        def predictors(s):
            x_array = np.array(s).reshape(-1, self.__input_size)
            output_array = model(x_array, training=False)
            return np.append(output_array[0].numpy(), output_array[1].numpy())

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
            # print("Start play " + str(i))
            game_steps = []
            self.__yacht.start()

            while not self.__yacht.is_game_finish():
                # print("Start Round " + str(self.__yacht.get_game_status()[0]))
                while not self.__yacht.is_round_finish():
                    # print("Start step " + str(self.__yacht.current_step))
                    self.__yacht.start_step()
                    game_status = self.__yacht.get_game_status()
                    action = ai_func(game_status)
                    game_action = self.__yacht.play_robot_round(action)
                    game_steps.append((game_status, game_action[:12], game_action[12:]))
                self.__yacht.finish_round()

            score = self.__yacht.get_player_point()
            game_data.append((score, game_steps))

            self.__avg_score += score
            if score > self.__max_score:
                # self.__yacht.display_game_statistics()
                self.__max_score = score
            if score < self.__min_score:
                self.__min_score = score

        game_data.sort(key=lambda s: -s[0])

        training_set = []
        for i in range(data_size):
            print(str(i) + "th score :" + str(game_data[i][0]))
            for step in game_data[i][1]:
                # print("Step: " + str(step[1]) + " " + str(step[2]))
                training_set.append((step[0], step[1], step[2]))

        return training_set

    def __build_model(self):
        yacht_input = keras.Input(
            shape=56, name="yacht_status"
        )

        hidden1 = layers.Dense(256, name="hidden_1", activation='relu')(yacht_input)
        hidden2 = layers.Dense(256, name="hidden_2", activation='relu')(hidden1)
        hidden3 = layers.Dense(256, name="hidden_3", activation='relu')(hidden2)
        hidden4 = layers.Dense(128, name="hidden_4", activation='relu')(hidden3)
        score_selector = layers.Dense(12, name="output_score", activation='softmax')(hidden4)
        dice_hold_selector = layers.Dense(5, name="output_dice_hold", activation='sigmoid')(hidden4)

        model = keras.Model(
            inputs=[yacht_input],
            outputs=[score_selector, dice_hold_selector],
        )

        # keras.utils.plot_model(model, "yacht_predictor_model.png", show_shapes=True)

        model.compile(
            optimizer=Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999),
            loss={
                "output_score": keras.losses.CategoricalCrossentropy(),
                "output_dice_hold": keras.losses.MeanSquaredError(),
            },
        )

        return model

    def __train_model(self, model, training_set):
        x_array = np.array([i[0] for i in training_set]).reshape(-1, self.__input_size)
        y1_array = np.array([i[1] for i in training_set]).reshape(-1, 12)
        y2_array = np.array([i[2] for i in training_set]).reshape(-1, 5)
        t = time.time()
        hist = model.fit(x_array,
                         {"output_score": y1_array, "output_dice_hold": y2_array},
                         epochs=100, verbose=1, batch_size=128)
        print("Learning info: ")
        print(hist.history)
        print("Training time: " + str(time.time() - t))
