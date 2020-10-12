import random


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

    def print_dice(self):
        print("Is Hold: ", self.isHold, ", Eye: ", self.eye)