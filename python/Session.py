from Gaming.Table import Table
from Gaming.Player import Player
from pandas import DataFrame
from pandas import Timestamp
import pandas as pd
from Gaming.Utilities import Log_Level
import numpy as np

# set display right
pd.set_option('display.width', 4000)
pd.set_option('max_colwidth', 4000)
pd.set_option('max_rows', 100)
pd.set_option('max_columns', 200)

"""
set up table
"""

report = []
table = Table("hellmuth", sex="m", colour="green", max_players=7, min_bet=50, max_bet=300, decks=8, dt=Timestamp("2018.01.01"))
table.shoe.shuffle()

if __name__ == "__main__":

    """
    set up table
    """

    report = []
    table = Table("hellmuth", sex="m", colour="green", max_players=7, min_bet=50, max_bet=300, decks=8, dt=Timestamp("2018.01.01"))
    table.shoe.shuffle()

    """
    set up player profiles
    """

    print("\033[4mcreating player pool\033[0m")

    number_of_sensible = 4
    number_of_risky = 40
    total_number_of_players = number_of_sensible + number_of_risky

    players = []

    [players.append(Player(id="s%s"%i, type=Player.SENSIBLE, report = report)) for i in range(number_of_sensible)]
    [players.append(Player(id="s%s"%i, type=Player.RISKY, report = report)) for i in range(number_of_risky)]

    print("total number of players:%s"%len(players))
    print("\033[4massembling tables\033[0m")
    table = Table("hellmuth0", sex="m", colour="green", max_players=7, min_bet=50, max_bet=300, decks=8, dt=Timestamp("2018.01.01"))
    table.shoe.shuffle()
    tables = [table]

    while players:
        player = players.pop()
        if not table.add_player(player):
            table = Table("hellmuth%s"%len(tables), sex="m", colour="green", max_players=7, min_bet=50, max_bet=300, decks=8, dt=Timestamp("2018.01.01"))
            table.shoe.shuffle()
            tables.append(table)
            table.add_player(player)

    """
    audit
    """
    [table.set_log_level(player_level=Log_Level.SESSION, dealer_level=Log_Level.NONE) for table in tables]

    """
    play
    """
    for table in tables:
        for player in table.players:
            player.start_table(table_id=table.id, table_start=table.time)
        while table.play_round() and table.games<200:
            pass

    df = DataFrame(data=report,columns="table player game_count action table_score bet bonus bonus_at win_amount table_balance leave".split())
    df = df.replace(np.nan, '', regex=True)
    # print(df.tail(150))


