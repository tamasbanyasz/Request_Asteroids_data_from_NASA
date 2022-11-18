import matplotlib.pyplot as plt
import numpy as np


class ResultVisualization:
    def __init__(self, players_name, player_res):
        super().__init__()
        self.players_name = players_name
        self.players_result = player_res
        self.colors = ("red", "green", "brown")

        self.index_of_max_result = np.argmax(self.players_result)
        self.explode_values_in_array = np.array([0.] * len(self.players_result))
        self.explode_values_in_array[self.index_of_max_result] = 0.3

        self.explode = tuple(self.explode_values_in_array)

        self.wp = {'linewidth': 2, 'edgecolor': "black"}

        self.fig, self.ax = plt.subplots(figsize=(10, 7))

        self.wedges, self.tx, self.autotexts = plt.pie(self.players_result, labels=self.players_name,
                                                       explode=self.explode, autopct="",
                                                       wedgeprops=self.wp, shadow=True, colors=self.colors)

        for i, a in enumerate(self.autotexts):
            a.set_text("{}".format(self.players_result[i]))

        self.ax.legend(self.wedges, self.players_name,
                       title="Players name",
                       loc="upper right",
                       fontsize=16,
                       bbox_to_anchor=(0.8, 0, 0.5, 1))

        plt.setp(self.autotexts, size=22, weight="bold")

        self.ax.set_title("Rock-Paper-Scissors Game")
        plt.show()


class Player:
    def __init__(self, name):
        self.name = name
        self.win = 0

    def __iadd__(self, other):
        if type(other) == int:
            self.win += other

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        elif isinstance(other, int):
            return self.win == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f'{self.name}'


class Battle:
    def __init__(self):
        self.won = ""

    def __call__(self, players):
        if (players[0] == 'Rock' and players[1] == 'Scissors') or (players[0] == 'Scissors' and players[1] == 'Rock'):
            self.won = 'Rock'

        if (players[0] == 'Scissors' and players[1] == 'Paper') or (players[0] == 'Paper' and players[1] == 'Scissors'):
            self.won = 'Scissors'

        if (players[0] == 'Paper' and players[1] == 'Rock') or (players[0] == 'Rock' and players[1] == 'Paper'):
            self.won = 'Paper'

        return self.won


class Game:
    def __init__(self):
        self.rock = Player('Rock')
        self.paper = Player('Paper')
        self.scissors = Player('Scissors')
        self.battle = Battle()
        self.players = np.array([self.rock, self.scissors, self.paper])

    def battle_result(self):
        return self.battle(np.random.choice(self.players, 2, False))

    def add_win_number_to_player(self):
        for player in self.players:
            if player == self.battle_result():
                player += 1

    def end_of_the_game(self):
        for player in self.players:
            if player == 1000:
                print(f'\n{player} has won the battle')
                return True
        return False

    def game_loop(self):
        while True:
            self.add_win_number_to_player()
            if self.end_of_the_game():
                print(f'\n{self.rock.name}: {self.rock.win}\n{self.paper.name}: {self.paper.win}\n{self.scissors.name}:'
                      f' {self.scissors.win}')
                break

    def display_pie_chart(self):
        self.game_loop()
        ResultVisualization(self.players, np.array([self.rock.win, self.scissors.win, self.paper.win]))


game = Game()
game.display_pie_chart()
