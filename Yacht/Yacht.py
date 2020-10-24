from abc import abstractmethod

from Yacht.Player import Player
from Yacht.PointType import PointType


class Yacht:
    rounds: int = 0
    player: Player = Player()
    user_game: bool = False

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def play_round(self) -> bool:
        pass

    @abstractmethod
    def play_set_point(self) -> bool:
        pass

    def init(self):
        self.rounds = 0
        self.player = Player()

    def _select_round(self, select: int, point_select: int) -> bool:
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

    def _run_set_point(self, point_select: int):
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

    def set_user_game(self, is_user_game: bool):
        self.user_game = is_user_game
