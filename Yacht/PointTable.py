from typing import List

from Yacht.Dice import Dice
from Yacht.PointType import PointType


class PointTable:
    table_set: List[bool] = [False, False, False, False, False, False, False, False, False, False, False, False]
    table: List[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def __init__(self):
        for i in range(0, len(self.table_set)):
            self.table_set[i] = False
        for i in range(0, len(self.table)):
            self.table[i] = 0

    def is_point_setable(self, point_type: PointType) -> bool:
        return self.table_set[point_type.value] == False

    def set_point(self, point_type: PointType, dices: List[Dice]) -> bool:
        if self.table_set[point_type.value] is False:
            self.table[point_type.value] = 0
            self.table_set[point_type.value] = True

            counts: List[int] = [0, 0, 0, 0, 0, 0]

            for dice in dices:
                counts[dice.get_eye() - 1] += 1

            if point_type == PointType.ONE:
                self.table[point_type.value] = counts[0]

            elif point_type == PointType.TWO:
                self.table[point_type.value] = counts[1] * 2

            elif point_type == PointType.THREE:
                self.table[point_type.value] = counts[2] * 3

            elif point_type == PointType.FOUR:
                self.table[point_type.value] = counts[3] * 4

            elif point_type == PointType.FIVE:
                self.table[point_type.value] = counts[4] * 5

            elif point_type == PointType.SIX:
                self.table[point_type.value] = counts[5] * 6

            elif point_type == PointType.CHOICE:
                for eye in range(1, 7):
                    self.table[point_type.value] += counts[eye - 1] * eye

            elif point_type == PointType.FOUR_OF_KINDS:
                is_matched: bool = False
                for eye in range(1, 7):
                    if counts[eye - 1] >= 4:
                        is_matched = True
                if is_matched is True:
                    for eye in range(1, 7):
                        self.table[point_type.value] += counts[eye - 1] * eye

            elif point_type == PointType.FULL_HOUSE:
                is_three_matched: bool = False
                is_two_matched: bool = False

                for eye in range(1, 7):
                    if counts[eye - 1] == 3:
                        is_three_matched = True
                    elif counts[eye - 1] == 2:
                        is_two_matched = True
                    elif counts[eye - 1] == 5:
                        is_three_matched = True
                        is_two_matched = True
                if (is_three_matched is True) and (is_two_matched is True):
                    for eye in range(1, 7):
                        self.table[point_type.value] += counts[eye - 1] * eye

            elif point_type == PointType.SMALL_STRAIGHT:
                is_matched: bool = False

                if (counts[2] > 0) and (counts[3] > 0):
                    if (counts[0] > 0) and (counts[1] > 0):
                        is_matched = True
                    elif (counts[1] > 0) and (counts[4] > 0):
                        is_matched = True
                    elif (counts[4] > 0) and (counts[5] > 0):
                        is_matched = True

                if is_matched is True:
                    self.table[point_type.value] = 15

            elif point_type == PointType.LARGE_STRAIGHT:
                is_matched: bool = False

                if (counts[1] > 0) and (counts[2] > 0) and (counts[3] > 0) and (counts[4] > 0):
                    if counts[0] > 0:
                        is_matched = True
                    elif counts[5] > 0:
                        is_matched = True

                if is_matched is True:
                    self.table[point_type.value] = 15

            elif point_type == PointType.YACHT:
                for eye in range(1, 7):
                    if counts[eye - 1] == 5:
                        self.table[point_type.value] = eye * 5

            return True
        else:
            return False

    def get_total_point(self) -> int:
        point: int = 0

        for p in self.table:
            point += p

        temp_sum = 0
        for i in range(0, 6):
            temp_sum += i
        if temp_sum >= 63:
            point += 35

        return point

    def print_table(self):
        print("==== PointTable ====")
        for point_type in PointType:
            print(point_type, ": ", self.table[point_type.value])
