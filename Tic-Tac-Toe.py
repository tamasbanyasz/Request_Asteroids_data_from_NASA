import numpy as np


class Map:
    def __init__(self):
        self.rows = 3
        self.cols = 3
        self.board = np.array([['-'] * self.cols] * self.rows)

    def print_map(self):
        for i in self.board:
            for j in i:
                print(j, end=' ')
            print()

    def valid_rows_n_cols(self, row_n_col, sign):
        if self.board[row_n_col[0] - 1, row_n_col[1] - 1] == '-':
            self.board[row_n_col[0] - 1, row_n_col[1] - 1] = sign
        elif self.board[row_n_col[0] - 1, row_n_col[1] - 1] != '-':
            return False

        return True


class Player:
    def __init__(self, signs):
        self.sign = signs

    def player_number(self, count):
        number_1 = int(input(f"Your turn {self.sign[count]}. Row: "))
        number_2 = int(input(f"Your turn {self.sign[count]}. Col: "))

        return [number_1, number_2]

    def player_sign(self, count):
        return self.sign[count]


class Game:
    def __init__(self, signs):
        self.signs = signs
        self.map = Map()
        self.plyr = Player(self.signs)
        self.count = 0

    def player_win(self, sign):
        idx = [i for i in range(len(self.map.board))]

        index = 0
        while index <= len(idx) - 1:
            rows = np.all(self.map.board[index, :] == sign)
            cols = np.all(self.map.board[:, index] == sign)
            diag1 = np.all(self.map.board[idx, idx] == sign)
            diag2 = np.all(self.map.board[idx[::-1], idx] == sign)

            index += 1

            if np.any([rows, cols, diag1, diag2]):
                return True

        return False

    def player_turn(self):
        if self.count < len(self.signs) - 1:
            self.count += 1
        else:
            self.count = 0

    def game_draw(self):
        for i in self.map.board:
            if '-' in i:
                return False

        return True

    def start_game(self):

        while True:

            self.map.print_map()

            if self.game_draw():
                print('DRAW!')
                break

            if not self.map.valid_rows_n_cols(self.plyr.player_number(self.count), self.plyr.player_sign(self.count)):
                print("WRONG!")
                self.count -= 1

            if self.player_win(self.plyr.player_sign(self.count)):
                self.map.print_map()
                print(f'Player {self.plyr.player_sign(self.count)} WON!')
                break

            self.player_turn()


tic_tac_toe = Game(['X', 'O'])
tic_tac_toe.start_game()
