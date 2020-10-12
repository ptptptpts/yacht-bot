from Player.AiBot import YachtAiBot
from Player.PlayerOne import YachtGamePlayerOne
from Player.RandomBot import YachtRandomBot


def data_preparation(N, K, f, print_data=False):
    game_data = []
    for i in range(N):
        score = 0
        game_steps = []

print("1. Play Self")
print("2. Play Random Bot")
print("3. Play AI Bot")
select = int(input(":"))
if select == 1:
    YachtGamePlayerOne().start()
elif select == 2:
    YachtRandomBot().start()
elif select == 3:
    YachtAiBot().start()
