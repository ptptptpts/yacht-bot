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
                            self.__score_array.append(self.__build_point_table(dices))

    def __run_one_round(self) -> int:
        self.__yacht.start()
        while not self.__yacht.is_game_finish():
            while not self.__yacht.is_round_finish():
                self.__yacht.start_step()

                game_status = self.__yacht.get_game_status()
                print(game_status)
                dices = self.__read_dice(game_status)
                point_status = self.__read_point_status(game_status)
                next_dices_status = self.__find_max_available_point(dices, point_status)
                selected_score_type = self.__select_max_point(dices, point_status)[0]

                next_input = [0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0,  # Score type
                              0, 0, 0, 0, 0]  # Dice
                next_input[selected_score_type] = 1
                for dice in range(5):
                    if next_dices_status[dice]:
                        next_input[12 + dice] = 1

                self.__yacht.play_robot_round(next_input)
            self.__yacht.finish_round()
        return self.__yacht.get_player_point()

    def __find_max_available_point(self, dices: List[int], point_status: List[bool]) -> []:
        current_max = self.__select_max_point(dices, point_status)[1]
        is_hold_dice = [False, False, False, False, False]
        current_max_state = [False, False, False, False, False]

        for a_hold in range(2):
            is_hold_dice[0] = a_hold == 1
            for b_hold in range(2):
                is_hold_dice[1] = b_hold == 1
                for c_hold in range(2):
                    is_hold_dice[2] = c_hold == 1
                    for d_hold in range(2):
                        is_hold_dice[3] = d_hold == 1
                        for e_hold in range(2):
                            if (a_hold + b_hold + c_hold + d_hold + e_hold) == 5:
                                break
                            is_hold_dice[4] = e_hold == 1

                            expected_point = self.__get_expected_point(dices, is_hold_dice, point_status)

                            if expected_point > current_max:
                                current_max = expected_point
                                for i in range(5):
                                    current_max_state[i] = is_hold_dice[i]

        return current_max_state

    def __get_expected_point(self, dices, is_hold_dice, point_status):
        current_dice = [0, 0, 0, 0, 0]
        multiplier = 1
        current_point_sum = 0

        for i in range(5):
            if not is_hold_dice[i]:
                multiplier = multiplier * 6

        for a in range(6):
            if is_hold_dice[0]:
                current_dice[0] = dices[0]
                a = 5
            else:
                current_dice[0] = a

            for b in range(6):
                if is_hold_dice[1]:
                    current_dice[1] = dices[1]
                    b = 5
                else:
                    current_dice[1] = b

                for c in range(6):
                    if is_hold_dice[2]:
                        current_dice[2] = dices[2]
                        c = 5
                    else:
                        current_dice[2] = c

                    for d in range(6):
                        if is_hold_dice[3]:
                            current_dice[3] = dices[3]
                            d = 5
                        else:
                            current_dice[3] = d

                        for e in range(6):
                            if is_hold_dice[4]:
                                current_dice[4] = dices[4]
                                e = 5
                            else:
                                current_dice[4] = e

                            # print(current_dice)
                            max_point = self.__select_max_point(current_dice, point_status)[1]
                            current_point_sum = current_point_sum + (float(max_point) / float(multiplier))

        return current_point_sum

    def __select_max_point(self, dices: List[int], point_status: List[bool]) -> []:
        max_point = 0
        max_type = 0

        point_list = self.__get_point_list(dices)

        for i in range(12):
            if not point_status[i]:
                if point_list[i] > max_point:
                    max_point = point_list[i]
                    max_type = i

        return [max_type, max_point]

    def __get_point_list(self, dices):
        dice_pos = 0
        for i in range(5):
            dice_pos = dice_pos * 6 + dices[i]
        point_list = self.__score_array[dice_pos]
        return point_list

    @staticmethod
    def __build_point_table(dices: List[int]) -> []:
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

    @staticmethod
    def __read_dice(game_status: []) -> []:
        dices = []
        for i in range(5):
            if game_status[2 + i * 6] == 1:  # 1
                dices.append(0)
            elif game_status[2 + i * 6 + 1] == 1:  # 2
                dices.append(1)
            elif game_status[2 + i * 6 + 2] == 1:  # 3
                dices.append(2)
            elif game_status[2 + i * 6 + 3] == 1:  # 4
                dices.append(3)
            elif game_status[2 + i * 6 + 4] == 1:  # 5
                dices.append(4)
            elif game_status[2 + i * 6 + 5] == 1:  # 6
                dices.append(5)
        print(dices)
        return dices

    @staticmethod
    def __read_point_status(game_status: []) -> []:
        point_status = [game_status[32] == 1, game_status[33] == 1, game_status[34] == 1, game_status[35] == 1,
                        game_status[36] == 1, game_status[37] == 1, game_status[38] == 1, game_status[39] == 1,
                        game_status[40] == 1, game_status[41] == 1, game_status[42] == 1, game_status[43] == 1]
        return point_status
