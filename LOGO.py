import numpy as np
import time


class TLetterBackgroundSettings:
    def __init__(self, t_background, t_background_value):
        self.t_background = t_background
        self.t_background_value = t_background_value

    def is_backgrounded_reversed_t_letter(self, t_matrix):
        if self.t_background:
            t_matrix = np.where(t_matrix == 0, self.t_background_value, 1)
            return t_matrix

        if not self.t_background:
            return t_matrix


class TLetterMatrix(TLetterBackgroundSettings):
    def __init__(self, t_size, t_background, t_background_value):
        super().__init__(t_background, t_background_value)
        self.timer = 1

        self.t_size = t_size
        self.t_rows = 1
        self.t_shape = self.t_size
        self.t_cols = self.t_size

    def calc_column_in_t_letter(self, t_matrix):
        if len(t_matrix) >= 2:
            if self.t_size % 2 == 0:
                t_col_idx1 = self.t_size // 2
                t_col_idx2 = t_col_idx1 - 1
                t_matrix[:, t_col_idx1] = 1
                t_matrix[:, t_col_idx2] = 1

            if self.t_size % 2 != 0:
                t_col_idx3 = self.t_size // 2
                t_matrix[:, t_col_idx3] = 1

    def get_t_letter_map(self):
        t_matrix = np.zeros(self.t_shape, dtype=int)
        t_matrix[:self.t_size] = 1

        return t_matrix

    def set_t_letter_matrix_map(self):
        t_matrix = np.reshape(self.get_t_letter_map(), (self.t_rows, self.t_cols))
        t_matrix = np.roll(t_matrix, -1, axis=0)

        t_matrix = self.is_backgrounded_reversed_t_letter(t_matrix)

        return t_matrix

    def t_matrix_loop_counts(self):
        self.t_shape += self.t_cols
        self.t_rows += 1

    def is_reversed_mirrored_t_letter(self, t_matrix):
        if len(t_matrix) >= self.t_size:
            t_matrix = t_matrix[::-1, :]
            print(f'\n Reversed T: \n\n{t_matrix}')
            return True

        return False

    def letter_t_matrix(self):

        print('\n Print mirrored T: \n')
        while True:

            t_matrix = self.set_t_letter_matrix_map()

            self.calc_column_in_t_letter(t_matrix)

            print(f'\n{t_matrix}')
            self.t_matrix_loop_counts()
            time.sleep(self.timer)

            if self.is_reversed_mirrored_t_letter(t_matrix):
                break


class OLetterBackgroundSettings:
    def __init__(self, o_background, o_background_value):
        self.o_background = o_background
        self.o_background_value = o_background_value

    def is_backgrounded_reversed_o_letter(self, o_matrix):
        if self.o_background:
            o_matrix = np.where(o_matrix == 0, self.o_background_value, 1)
            return o_matrix

        if not self.o_background:
            return o_matrix


class OLetterMatrix(OLetterBackgroundSettings):
    def __init__(self, o_size, o_background, o_background_value):
        super().__init__(o_background, o_background_value)
        self.timer = 1

        self.o_size = o_size
        self.o_rows = 1
        self.o_shape = self.o_size
        self.o_cols = self.o_size

    def calc_o_letter_sides_in_o_matrix(self, o_matrix):
        o_matrix[0, :] = 1
        if len(o_matrix) > 2:
            o_matrix[:, 0::self.o_size - 1] = 1

    def get_o_letter_map(self):
        o_matrix = np.zeros(self.o_shape, dtype=int)
        o_matrix[:self.o_size] = 1

        return o_matrix

    def set_o_matrix_map(self):
        o_matrix = np.reshape(self.get_o_letter_map(), (self.o_rows, self.o_cols))
        o_matrix = np.roll(o_matrix, -1, axis=0)
        o_matrix = self.is_backgrounded_reversed_o_letter(o_matrix)

        return o_matrix

    def o_matrix_loop_counts(self):
        self.o_shape += self.o_cols
        self.o_rows += 1

    def completed_bottom_line_of_o_letter(self, o_matrix):
        if len(o_matrix) == self.o_size:
            o_matrix[self.o_size - 1, :] = 1
            print(f'\n Print O: \n\n{o_matrix}')
            return True

        return False

    def letter_o_matrix(self):

        print('\n Print O: \n')
        while True:

            o_matrix = self.set_o_matrix_map()

            self.calc_o_letter_sides_in_o_matrix(o_matrix)

            print(f'\n{o_matrix}')
            self.o_matrix_loop_counts()
            time.sleep(self.timer)

            if self.completed_bottom_line_of_o_letter(o_matrix):
                break


class MLetterBackgroundSettings:
    def __init__(self, m_background, m_background_value):
        self.m_background = m_background
        self.m_background_value = m_background_value

    def is_backgrounded_reversed_m_letter(self, m_matrix):
        if self.m_background:
            m_matrix = np.where(m_matrix == 0, self.m_background_value, 1)
            return m_matrix

        if not self.m_background:
            return m_matrix


class MLetterMatrix(MLetterBackgroundSettings):
    def __init__(self, m_size, m_background, m_background_value):
        super().__init__(m_background, m_background_value)
        self.timer = 1

        self.m_size = m_size
        self.m_rows = 1
        self.m_shape = self.m_size
        self.m_cols = self.m_size

    def calc_mirrored_m_letter_pos(self, m_matrix):
        if len(m_matrix) == self.m_rows:
            m_matrix[:, 0::self.m_size - 1] = 1
        if self.m_size % 2 == 0:
            m_mid_bottom = self.m_size // 2

            np.fill_diagonal((m_matrix[m_mid_bottom:][::-1]), 1)
            m_matrix = np.fliplr(m_matrix)
            np.fill_diagonal((m_matrix[m_mid_bottom:][::-1]), 1)

        if self.m_size % 2 != 0:
            m_mid_bottom1 = self.m_size // 2

            np.fill_diagonal((m_matrix[m_mid_bottom1:][::-1]), 1)
            m_matrix = np.fliplr(m_matrix)
            np.fill_diagonal((m_matrix[m_mid_bottom1:][::-1]), 1)

    def get_m_letter_map(self):
        m_matrix = np.zeros(self.m_shape, dtype=int)
        m_matrix[0] = 1
        m_matrix[self.m_size - 1] = 1

        return m_matrix

    def set_m_matrix_map(self):
        m_matrix = np.reshape(self.get_m_letter_map(), (self.m_rows, self.m_cols))
        m_matrix = np.roll(m_matrix, -1, axis=0)
        m_matrix = self.is_backgrounded_reversed_m_letter(m_matrix)

        return m_matrix

    def m_matrix_loop_counts(self):
        self.m_shape += self.m_cols
        self.m_rows += 1

    def completed_reversed_mirrored_m_letter(self, m_matrix):
        if len(m_matrix) == self.m_size:
            m_matrix = m_matrix[::-1]
            print(f'\n Print reversed M: \n\n{m_matrix}')
            return True

        return False

    def letter_m_matrix(self):

        print('\n Print mirrored M: \n')
        while True:

            m_matrix = self.set_m_matrix_map()

            self.calc_mirrored_m_letter_pos(m_matrix)

            print(f'\n{m_matrix}')
            self.m_matrix_loop_counts()
            time.sleep(self.timer)

            if self.completed_reversed_mirrored_m_letter(m_matrix):
                break


class ILetterBackgroundSettings:
    def __init__(self, i_background, i_background_value):
        self.i_background = i_background
        self.i_background_value = i_background_value

    def is_backgrounded_reversed_i_letter(self, i_matrix):
        if self.i_background:
            i_matrix = np.where(i_matrix == 0, self.i_background_value, 1)
            return i_matrix

        if not self.i_background:
            return i_matrix


class ILetterMatrix(ILetterBackgroundSettings):
    def __init__(self, i_size, i_background, i_background_value):
        super().__init__(i_background, i_background_value)
        self.timer = 1

        self.i_size = i_size
        self.i_rows = 1
        self.i_shape = self.i_size
        self.i_cols = self.i_size

    def calc_i_letter_middle_pos_in_i_matix(self, i_matrix):
        if self.i_size % 2 == 0:
            i_mid_idx1 = self.i_size // 2
            i_mid_idx2 = i_mid_idx1 - 1
            i_matrix[i_mid_idx1] = 1
            i_matrix[i_mid_idx2] = 1

        if self.i_size % 2 != 0:
            i_mid_idx3 = self.i_size // 2
            i_matrix[i_mid_idx3] = 1

    def get_i_letter_map(self):
        i_matrix = np.zeros(self.i_shape, dtype=int)
        self.calc_i_letter_middle_pos_in_i_matix(i_matrix)

        return i_matrix

    def set_i_matrix_map(self):
        i_matrix = np.reshape(self.get_i_letter_map(), (self.i_rows, self.i_cols))
        i_matrix = np.roll(i_matrix, -1, axis=0)
        i_matrix = self.is_backgrounded_reversed_i_letter(i_matrix)

        return i_matrix

    def calc_i_letter_next_parts(self, i_matrix):
        if len(i_matrix) == self.i_rows:
            if self.i_size % 2 == 0:
                i_col_idx1 = self.i_size // 2
                i_col_idx2 = i_col_idx1 - 1
                i_matrix[:, i_col_idx1] = 1
                i_matrix[:, i_col_idx2] = 1

            if self.i_size % 2 != 0:
                i_col_idx3 = self.i_size // 2
                i_matrix[:, i_col_idx3] = 1

    def i_matrix_loop_counts(self):
        self.i_shape += self.i_cols
        self.i_rows += 1

    def completed_i_letter(self, i_matrix):
        if len(i_matrix) == self.i_size:
            print(f'\n Print I : \n\n{i_matrix}')
            return True

        return False

    def letter_i_matrix(self):

        print('\n Print I: \n')
        while True:

            i_matrix = self.set_i_matrix_map()

            self.calc_i_letter_next_parts(i_matrix)

            print(f'\n{i_matrix}')
            self.i_matrix_loop_counts()
            time.sleep(self.timer)

            if self.completed_i_letter(i_matrix):
                break


obj = TLetterMatrix(t_size=8, t_background=False, t_background_value=3)
obj.letter_t_matrix()

obj = OLetterMatrix(o_size=8, o_background=False, o_background_value=3)
obj.letter_o_matrix()

obj = MLetterMatrix(m_size=8, m_background=False, m_background_value=3)
obj.letter_m_matrix()

obj = ILetterMatrix(i_size=8, i_background=False, i_background_value=3)
obj.letter_i_matrix()
