from Yacht.RobotYacht import RobotYacht
import random


class YachtRandomBot:
    __debug = False
    __yacht = RobotYacht()

    __avg_score = 0
    __max_score = 0
    __min_score = 400

    def start(self, total_run: int):
        for i in range(total_run):
            print("================================")
            print("Start", i, "run")
            score = self.__run_one_round()
            print("Run ", i, " finished. Score: ", score)
            print("================================")
            self.__avg_score += score
            if score > self.__max_score:
                self.__max_score = score
            if score < self.__min_score:
                self.__min_score = score
        self.__avg_score = self.__avg_score / total_run
        print("================================")
        print("Average score: ", self.__avg_score)
        print("Max score: ", self.__max_score)
        print("Min score: ", self.__min_score)

    def __run_one_round(self) -> int:
        self.__yacht.start()
        while not self.__yacht.is_game_finish():
            game_status = self.__yacht.get_game_status()
            if self.__debug:
                self.__yacht.print_round()
                self.__yacht.print_dice()
            self.__yacht.play_robot_round(random.randrange(0, 100))
        return self.__yacht.get_player_point()
