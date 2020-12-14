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
        self.current_step = 0

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
        # Build game status on list[5]
        # status_bit :
        #   round : integer 0 - 11
        #   step  : integer 0 - 4
        #   total point : integer
        # point_bit[3] :
        #   point [12] : bool, integer
        # dice_bit :
        #   dice [5] : integer 1 - 6
        status = []

        # status_bit = rounds(4bit, 0-11) + current step(3bit, 0-4) + point(10bit, 0-1023)
        status_bit = (self.rounds << 13) + (self.current_step << 10) + self.player.get_point()
        status.append(status_bit)

        # point_bit = ((point value(6bit, 0-50) + point status(1bit, 0-1)) * 4) * 3
        for i in range(3):
            point_bit = 0
            for j in range(4):
                table = self.player.point_table
                point_bit = (point_bit << 7) + table.table[i * 4 + j]
                if table.table_set[i * 4 + j]:
                    point_bit += 1
            status.append(point_bit)

        # dice_bit = (dice eye(3bit, 1-6) + dice status(1bit, 0-1)) * 5
        dice_bit = 0
        for dice in range(5):
            current_dice = self.player.dices[dice]
            dice_bit = (dice_bit << 4) + (current_dice.get_eye() << 1)
            if current_dice.get_hold_state():
                dice_bit += 1
        status.append(dice_bit)

        return status

    def get_player_point(self) -> int:
        return self.player.get_point()

    def is_game_finish(self) -> bool:
        return self.rounds == 12

    def get_input(self, robot_input: int):
        if self.current_step == 0:
            self.player.round_start()
            self.__hold_dice(robot_input)
        elif self.current_step == 1:
            self.__unhold_dice(robot_input)
        elif self.current_step == 2:
            self.play_roll()
            self.__hold_dice(robot_input)
        elif self.current_step == 3:
            self.__unhold_dice(robot_input)
        elif self.current_step == 4:
            self.play_roll()
            self.__select_point(robot_input)

    def __hold_dice(self, hold_bit: int):
        for dice in range(5):
            if (hold_bit & 0b1) == 1:
                self.player.hold(dice)
            hold_bit = hold_bit >> 1

    def __unhold_dice(self, unhold_bit: int):
        for dice in range(5):
            if unhold_bit & 0b1 == 1:
                self.player.un_hold(dice)
            unhold_bit = unhold_bit >> 1

    def __select_point(self, point_select: int):
        point_select = point_select % 12
        while not self.player.set_point(PointType(point_select)):
            point_select = (point_select + 1) % 12
