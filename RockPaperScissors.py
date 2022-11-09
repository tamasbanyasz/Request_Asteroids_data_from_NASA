import numpy as np


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
        return f'{self.name}: {self.win}'


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

    def __str__(self):
        return f'\n{self.won} has won the battle'


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
            if player == 10000:
                return True
        return False

    def display_game(self):
        self.add_win_number_to_player()
        if self.end_of_the_game():
            return True
        return False

    def __str__(self):
        return f'\n{self.rock}\n{self.paper}\n{self.scissors}\n{self.battle}'


game = Game()
while True:
    if game.display_game():
        print(game)
        break

print(vars(game))
