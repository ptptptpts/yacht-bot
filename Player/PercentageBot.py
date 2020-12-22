from typing import List

import numpy as np

from Yacht.RobotYacht import RobotYacht
import random


class YachtPercentageBot:
    __debug = False
    __yacht = RobotYacht()

    __avg_score = 0
    __max_score = 0
    __min_score = 400

    __score_array = []

    def start(self, total_run: int):
        self.__build_score_array()
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

    def __build_score_array(self):
        dices = [0, 0, 0, 0, 0]
        for a in range(6):
            dices[0] = a
            for b in range(6):
                dices[1] = b
                for c in range(6):
                    dices[2] = c
                    for d in range(6):
                        dices[3] = d
                        for e in range(6):
                            dices[4] = e
                            self.__score_array.append(self.__get_point_list(dices))

    @staticmethod
    def __get_point_list(dices: List[int]) -> []:
        point_table = []
        counts: [int] = [0, 0, 0, 0, 0, 0]

        for dice in dices:
            counts[dice] += 1

        point_table.append(counts[0])
        point_table.append(counts[1] * 2)
        point_table.append(counts[2] * 3)
        point_table.append(counts[3] * 4)
        point_table.append(counts[4] * 5)
        point_table.append(counts[5] * 6)

        choice = 0
        for eye in range(1, 7):
            choice += counts[eye - 1] * eye
        point_table.append(choice)

        is_two_matched: bool = False
        is_three_matched: bool = False
        is_four_matched: bool = False
        is_five_matched: bool = False
        for eye in range(1, 7):
            if counts[eye - 1] == 2:
                is_two_matched = True
            elif counts[eye - 1] == 3:
                is_three_matched = True
            elif counts[eye - 1] == 4:
                is_four_matched = True
            elif counts[eye - 1] == 5:
                is_two_matched = True
                is_three_matched = True
                is_four_matched = True
                is_five_matched = True

        if is_four_matched is True:
            for eye in range(1, 7):
                point_table.append(counts[eye - 1] * eye)
        else:
            point_table.append(0)

        if (is_three_matched is True) and (is_two_matched is True):
            for eye in range(1, 7):
                point_table.append(counts[eye - 1] * eye)
        else:
            point_table.append(0)

        is_four_line: bool = False
        if (counts[2] > 0) and (counts[3] > 0):
            if (counts[0] > 0) and (counts[1] > 0):
                is_four_line = True
            elif (counts[1] > 0) and (counts[4] > 0):
                is_four_line = True
            elif (counts[4] > 0) and (counts[5] > 0):
                is_four_line = True
        if is_four_line is True:
            point_table.append(15)
        else:
            point_table.append(0)

        is_five_line: bool = False
        if (counts[1] > 0) and (counts[2] > 0) and (counts[3] > 0) and (counts[4] > 0):
            if counts[0] > 0:
                is_five_line = True
            elif counts[5] > 0:
                is_five_line = True
        if is_five_line is True:
            point_table.append(30)
        else:
            point_table.append(0)

        if is_five_matched:
            point_table.append(50)
        else:
            point_table.append(0)

        return point_table

    def __run_one_round(self) -> int:
        self.__yacht.start()
        while not self.__yacht.is_game_finish():
            for round in range(5):
                game_status = self.__yacht.get_game_status_float()
                dices = self.__read_dice(game_status)
                point_status = self.__read_point_status(game_status)

                if round < 4:
                    self.__yacht.play_robot_round(random.randrange(0, 100))
                else:
                    self.__yacht.play_robot_round(self.__select_max_point(dices, point_status))

        return self.__yacht.get_player_point()

    @staticmethod
    def __read_dice(game_status: List[float]) -> []:
        # Build game status on list[37]
        # round_bit[1] : integer 0 - 11
        # step_bit[1]  : integer 0 - 4
        # total point_bit[1] : integer 0-512
        # point_bit[24] (MAX 50)
        #   point [12] : bool, integer
        # dice_bit[10] (MAX 6)
        #   dice [5] : integer 1 - 6
        dices = [int(game_status[27] * 6) - 1,
                 int(game_status[29] * 6) - 1,
                 int(game_status[31] * 6) - 1,
                 int(game_status[33] * 6) - 1,
                 int(game_status[35] * 6) - 1]
        return dices

    @staticmethod
    def __read_point_status(game_status: List[float]) -> []:
        point_status = [game_status[4] == 1, game_status[6] == 1, game_status[8] == 1, game_status[10] == 1,
                        game_status[12] == 1, game_status[14] == 1, game_status[16] == 1, game_status[18] == 1,
                        game_status[20] == 1, game_status[22] == 1, game_status[24] == 1, game_status[26] == 1]
        return point_status

    def __select_max_point(self, dices: List[int], point_status: List[bool]) -> int:
        max_point = 0
        max_type = 0

        dice_pos = 0
        for i in range(5):
            dice_pos = dice_pos * 6 + dices[i]

        point_list = self.__score_array[dice_pos]

        for i in range(11):
            if not point_status[i]:
                if point_list[i] > max_point:
                    max_point = point_list[i]
                    max_type = i

        return max_type
