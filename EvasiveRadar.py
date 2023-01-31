import numpy as np
import time


class EvasiveRadar:
    def __init__(self, size):
        self.matrix_col = size
        self.matrix_row = self.matrix_col

        self.return_pos = size // 2
        self.own_row = self.return_pos

        self.row_step = 0
        self.obj_col = 0

    def display_radar(self):

        while True:
            radar_map = np.zeros((self.matrix_row, self.matrix_col), dtype=int)

            self.get_incoming_number_position(radar_map)

            self.dodge_when_number_incoming(radar_map)

            self.get_dodging_number_position(radar_map)

            time.sleep(1)

            self.row_step += 1
            print(f"\n{radar_map}\n")

            self.change_column_of_moving_number()

            if self.obj_col == len(radar_map):
                break

            self.return_back_when_number_gone_to_next_column(radar_map)

    def dodge_when_number_incoming(self, radar_map):
        if radar_map[self.matrix_col // 2 - 1, self.own_row] != 0:
            self.own_row -= 1

    def return_back_when_number_gone_to_next_column(self, radar_map):
        if all(radar_map[-self.matrix_col:, self.return_pos] == 0):
            self.own_row += 1

    def change_column_of_moving_number(self):
        if self.row_step == self.matrix_col:
            self.obj_col += 1
            self.row_step = 0

    def get_incoming_number_position(self, radar_map):
        radar_map[self.row_step, self.obj_col] = 4

    def get_dodging_number_position(self, radar_map):
        radar_map[self.matrix_col // 2, self.own_row] = 1


obj = EvasiveRadar(4)
obj.display_radar()
