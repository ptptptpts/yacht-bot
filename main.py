import random
from enum import Enum
from typing import List


class Dice:
    isHold: bool = False
    eye: int = 0

    def reset(self):
        self.eye = 0
        self.isHold = False

    def roll(self) -> int:
        if self.isHold is False:
            self.eye = random.randrange(1, 7)
        return self.eye

    def set_hold(self) -> bool:
        self.isHold = True
        return self.isHold

    def unset_hold(self) -> bool:
        self.isHold = False
        return self.isHold

    def get_eye(self) -> int:
        return self.eye

    def get_hold_state(self) -> bool:
        return self.isHold


class PointType(Enum):
    ONE = 0
    TWO = 1
    THREE = 2
    FOUR = 3
    FIVE = 4
    SIX = 5
    CHOICE = 6
    FOUR_OF_KINDS = 7
    FULL_HOUSE = 8
    SMALL_STRAIGHT = 9
    LARGE_STRAIGHT = 10
    YACHT = 11


class PointTable:
    table: List[int] = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

    def set_point(self, point_type: PointType, dices: List[Dice]) -> bool:
        if self.table[point_type.value] is -1:
            self.table[point_type.value] = 0
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
                    if counts[eye - 1] is 3:
                        is_three_matched = True
                    elif counts[eye - 1] is 2:
                        is_two_matched = True
                    elif counts[eye - 1] is 5:
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
                    if counts[eye - 1] is 5:
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


class Player:
    point_table: PointTable = PointTable()
    dices: List[Dice] = [Dice(), Dice(), Dice(), Dice(), Dice()]
    roll_count: int

    def round_start(self):
        for dice in self.dices:
            dice.reset()
            dice.roll()
        self.roll_count = 2

    def roll(self) -> bool:
        if self.roll_count > 0:
            self.roll_count -= 1
            for dice in self.dices:
                dice.roll()
            return True
        else:
            return False

    def hold(self, number: int):
        self.dices[number].set_hold()

    def un_hold(self, number: int):
        self.dices[number].unset_hold()

    def set_point(self, point_type: PointType):
        self.point_table.set_point(point_type, self.dices)

    def get_point(self) -> int:
        return self.point_table.get_total_point()

    def get_roll_count(self) -> int:
        return self.roll_count

    def get_dices(self) -> List[Dice]:
        return self.dices

    def get_point_table(self) -> PointTable:
        return self.point_table


class Yacht:
    is_two_player: bool = False
    rounds: int = 0
    currentPlayer: int = 0
    players: List[Player] = [Player(), Player()]

    def init(self):
        self.rounds = 0
        self.currentPlayer = 0
        self.players = [Player(), Player()]

    def start(self):
        pass

    def print_round(self):
        pass


yacht = Yacht()
yacht.init()
yacht.start()
