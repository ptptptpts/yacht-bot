from Yacht.Yacht import Yacht


class HumanYacht (Yacht):

    def start(self):
        self.init()
        while self.rounds < 12:
            while self.play_round() is False:
                pass
            self.rounds += 1

    def play_round(self) -> bool:
        self.print_round()
        self.player.print_dice()
        if self.player.roll_count == 0:
            return self.play_set_point()
        else:
            return self._play_round()

    def _play_round(self) -> bool:
        print("0.Roll")
        print("1.Hold")
        print("2.Unhold")
        print("3.Set Point")
        user_input = int(input("="))
        return self._select_round(user_input, 0)

    def play_set_point(self) -> bool:
        self._play_set_point()
        return True

    def _play_set_point(self):
        user_input = int(input("Select point: "))
        self._run_set_point(user_input)