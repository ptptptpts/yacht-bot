from typing import List

from Yacht.Dice import Dice
from Yacht.PointTable import PointTable
from Yacht.PointType import PointType


class Player:
    point_table: PointTable = PointTable()
    dices: List[Dice] = [Dice(), Dice(), Dice(), Dice(), Dice()]
    roll_count: int = 0

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

    def set_point(self, point_type: PointType) -> bool:
        return self.point_table.set_point(point_type, self.dices)

    def get_point(self) -> int:
        return self.point_table.get_total_point()

    def is_point_setable(self, point_type: PointType) -> bool:
        return self.point_table

    def get_roll_count(self) -> int:
        return self.roll_count

    def get_dices(self) -> List[Dice]:
        return self.dices

    def get_point_table(self) -> PointTable:
        return self.point_table

    def print_point(self):
        print("Total Point: ", self.point_table.get_total_point())
        self.point_table.print_table()

    def print_dice(self):
        print("Roll Count: ", self.roll_count)
        for dice in self.dices:
            dice.print_dice()
