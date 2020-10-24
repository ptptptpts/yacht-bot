from Yacht.HumanYacht import HumanYacht


class YachtGamePlayerOne:
    yacht = HumanYacht()

    def start(self):
        self.yacht.set_user_game(True)
        self.yacht.start()
