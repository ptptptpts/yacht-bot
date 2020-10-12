from Yacht.Yacht import Yacht


class YachtAiBot:
    yacht = Yacht()

    def start(self):
        self.yacht.set_user_game(True)
        self.yacht.start()
