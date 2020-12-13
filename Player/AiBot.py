from Yacht.RobotYacht import RobotYacht
import random


class YachtAiBot:
    __debug = False
    __yacht = RobotYacht()

    __avg_score = 0
    __max_score = 0
    __min_score = 400

    __learning_size = 10

    __play_num = 100
    __data_size = 10

    def start(self):
        for i in range(self.__learning_size):
            self.__init_self()
            print("================================")
            training_set = self.__data_preparation(self.__play_num, self.__data_size, lambda s: random.randrange(0, 100))
            self.__avg_score = self.__avg_score / self.__play_num
            print("Average score: ", self.__avg_score)
            print("Max score: ", self.__max_score)
            print("Min score: ", self.__min_score)

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

        print("0th score: {0}".format(game_data[0][0]))
        print("{0}th score: {1}".format(data_size, game_data[data_size-1][0]))

        return training_set
