from Player.AiBot import YachtAiBot
from Player.PercentageBot import YachtPercentageBot
from Player.PlayerOne import YachtGamePlayerOne
from Player.RandomBot import YachtRandomBot


# print("1. Play Self")
# print("2. Play Random Bot")
# print("3. Play AI Bot")
# select = int(input(":"))
# if select == 1:
#     YachtGamePlayerOne().start()
# elif select == 2:
#     YachtRandomBot().start(100)
# elif select == 3:
#     YachtAiBot().start()
YachtPercentageBot().start(100)
