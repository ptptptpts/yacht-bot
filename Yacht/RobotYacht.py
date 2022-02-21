from Yacht.PointType import PointType
from Yacht.Yacht import Yacht


class RobotYacht(Yacht):
    # Step description
    # Step | Roll stage  | Input
    # -------------------------------------------------
    #   0  | First roll  | Softmax[12] (Select scoreboard) + Softmax[5] (Select hold)
    #   1  | Second roll | Softmax[12] (Select scoreboard) + Softmax[5] (Select hold)
    #   2  | Third roll  | Softmax[12] (Select scoreboard) + Softmax[5] (Select hold)
    current_step: int = 0
    select_history: list
    hold_history: list
    current_hold_history: list

    def start(self):
        self.init()
        self.current_step = 0
        self.select_history = []
        self.hold_history = []
        self.current_hold_history = []

    def play_round(self) -> bool:
        return True

    def play_set_point(self) -> bool:
        return True

    def play_robot_round(self, robot_input: list[float]):
        if self.rounds < 12:
            self.get_input(robot_input)
            # Update round information
            self.current_step = self.current_step + 1

    def get_game_status(self) -> []:
        # Game status[56] = Round(1) + Step(1) + Dices(30) + Score status(12) + Scores(12)
        # Round: Integer = 1 - 12
        # Step: Integer = 0 - 2
        # Dices: Boolean[30] = Boolean[6] * 5 = [0, 0, 0, 0, 0, 0] * 5
        # Score status: Boolean[12]
        #    = [one, two, three, four, five, six, choice, four card, full house, small straight, large straight, yacht]
        # Scores: Integer[12]
        #    = [one, two, three, four, five, six, choice, four card, full house, small straight, large straight, yacht]
        status = []

        # Round: Integer = 1 - 12
        status.append(self.rounds)

        # Step: Integer = 0 - 2
        status.append(self.current_step)

        # Score status: Boolean(0/1)[12]
        #    = [one, two, three, four, five, six, choice, four card, full house, small straight, large straight, yacht]
        # Scores: Integer[12]
        #    = [one, two, three, four, five, six, choice, four card, full house, small straight, large straight, yacht]
        table = self.player.point_table
        for i in range(12):
            if table.table_set[i]:
                status.append(1)
            else:
                status.append(0)
        for i in range(12):
            status.append(table.table[i])

        # Dices: Boolean(0/1)[30] = Boolean[6] * 5 = [0, 0, 0, 0, 0, 0] * 5
        for dice in range(5):
            current_dice = self.player.dices[dice]
            for eye in range(1, 7):
                current_eye = current_dice.get_eye()
                if eye == current_eye:
                    status.append(1)
                else:
                    status.append(0)

        return status

    def get_game_status_float(self) -> []:
        status = self.get_game_status()
        return status

    def get_player_point(self) -> int:
        return self.player.get_point()

    def is_game_finish(self) -> bool:
        return self.rounds == 12

    def is_round_finish(self) -> bool:
        return self.current_step == 3

    def start_step(self):
        if self.current_step == 0:
            self.player.round_start()
        else:
            self.play_roll()

    def finish_round(self):
        if self.current_step == 3:
            self.current_step = 0
            self.rounds = self.rounds + 1

    def get_input(self, robot_input: list[float]):
        current_hold = []
        use_input = []
        for idx in range(17):
            use_input.append(robot_input[idx])
        for dice in range(5):
            if use_input[12 + dice] > 0.5:
                self.player.hold(dice)
                current_hold.append(dice)
            else:
                self.player.un_hold(dice)
        self.current_hold_history.append(current_hold)
        if self.current_step == 2:
            current_highest_score = 0
            for score_type in range(12):
                if self.player.is_point_setable(PointType(score_type)):
                    if use_input[score_type] > use_input[current_highest_score]:
                        current_highest_score = score_type
            self.player.set_point(PointType(current_highest_score))
            self.select_history.append(PointType(current_highest_score))
            self.hold_history.append(self.current_hold_history)
            self.current_hold_history = []

    def display_game_statistics(self):
        for round in range(12):
            message = "Round " + str(round)\
                      + ": Select score " + str(self.select_history[round])\
                      + ", Hold " + str(self.hold_history[round])
            print(message)
