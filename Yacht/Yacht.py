from Yacht.Player import Player
from Yacht.PointType import PointType


class Yacht:
    rounds: int = 0
    player: Player = Player()
    user_game: bool = False

    def set_user_game(self, is_user_game: bool):
        self.user_game = is_user_game

    def start(self):
        self.init()
        while self.rounds < 12:
            self.player.round_start()
            while self.play_round(0, 0) is False:
                pass
            self.rounds += 1

    def start_bot(self):
        self.init()

    def init(self):
        self.rounds = 0
        self.player = Player()

    def get_robot_input(self, robot_input: int):
        select = robot_input & 0xb11
        point_select = ((robot_input & 0b111100) >> 2)
        self.play_round(select, point_select)

    def play_round(self, bot_select: int, bot_point_select: int) -> bool:
        if self.user_game:
            self.print_round()
            self.player.print_dice()
        if self.player.roll_count == 0:
            return self.play_set_point(bot_point_select)
        else:
            if self.user_game:
                return self.play_user_round()
            else:
                return self.play_robot_round(bot_select, bot_point_select)

    def play_user_round(self) -> bool:
        print("0.Roll")
        print("1.Hold")
        print("2.Unhold")
        print("3.Set Point")
        user_input = int(input("="))
        return self.play_robot_round(user_input, 0)

    def play_robot_round(self, select: int, point_select: int) -> bool:
        select = (select % 4) + 1
        if select is 1:
            self.play_roll()
        elif select is 2:
            self.play_hold()
        elif select is 3:
            self.play_unhold()
        elif select is 4:
            return self.play_set_point(point_select)
        return False

    def play_set_point(self, bot_point_select: int) -> bool:
        if self.user_game:
            self.play_user_set_point()
        else:
            self.play_robot_set_point(bot_point_select)
        return True

    def play_user_set_point(self):
        user_input = int(input("Select point: "))
        self.play_robot_set_point(user_input)

    def play_robot_set_point(self, point_select: int):
        point_select = point_select % 12
        self.player.set_point(PointType(point_select))

    def print_round(self):
        print("Round: ", self.rounds)
        print("--------------------------------")
        self.player.print_point()

    def play_roll(self):
        self.player.roll()

    def play_hold(self):
        if self.user_game:
            user_input = int(input("Select dice: "))
        else:
            user_input = int(input())
        if (user_input >= 0) and (user_input < 5):
            self.player.hold(user_input)

    def play_unhold(self):
        if self.user_game:
            user_input = int(input("Select dice: "))
        else:
            user_input = int(input())
        if (user_input >= 0) and (user_input < 5):
            self.player.un_hold(user_input)
