from Yacht.PointType import PointType
from Yacht.Yacht import Yacht


class RobotYacht(Yacht):
    # Step description
    # Step | Roll stage  | Play step    | Input
    # -------------------------------------------------
    #   0  | First roll  | Hold dice    | 5 bit integer
    #   1  | First roll  | Unhold dice  | 5 bit integer
    #   2  | Second roll | Hold dice    | 5 bit integer
    #   3  | Second roll | Unhold dice  | 5 bit integer
    #   4  | Third roll  | Select score | 0~11 integer
    current_step: int = 0

    def start(self):
        self.init()

    def play_round(self) -> bool:
        return True

    def play_set_point(self) -> bool:
        return True

    def play_robot_round(self, robot_input: int):
        if self.rounds < 12:
            self.get_input(robot_input)
            # Update round information
            self.current_step = (self.current_step + 1) % 5
            if self.current_step == 0:
                self.rounds += 1

    def get_game_status(self) -> []:
        # Build game status on list
        # round : integer 0 - 11
        # step  : integer 0 - 4
        # point [12] : bool, integer
        # dice [5] : integer 1 - 6
        # total point : integer
        status = [self.rounds, self.current_step]
        for point_type in PointType:
            status.append(self.player.point_table.table_set[point_type.value])
            status.append(self.player.point_table.table[point_type.value])
        for dice in range(5):
            status.append(self.player.dices[dice])
        status.append(self.player.get_point())
        return status

    def is_game_finish(self) -> bool:
        return self.rounds == 12

    def get_input(self, robot_input: int):
        if self.current_step == 0:
            self.__hold_dice(robot_input)
        elif self.current_step == 1:
            self.__unhold_dice(robot_input)
        elif self.current_step == 2:
            self.__hold_dice(robot_input)
        elif self.current_step == 3:
            self.__unhold_dice(robot_input)
        elif self.current_step == 4:
            self.__select_point(robot_input)

    def __hold_dice(self, hold_bit: int):
        for dice in range(5):
            if hold_bit & 0b1 == 1:
                self.player.hold(dice)
            hold_bit = hold_bit >> 1

    def __unhold_dice(self, unhold_bit: int):
        for dice in range(5):
            if unhold_bit & 0b1 == 1:
                self.player.un_hold(dice)
            unhold_bit = unhold_bit >> 1

    def __select_point(self, point_select: int):
        while not self.player.set_point(PointType(point_select)):
            point_select = (point_select + 1) % 12
