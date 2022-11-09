import numpy as np
from random import randint
import plotly.express as px


class FrontRadar:
    def __init__(self):
        self.map_size = 0

        self.front_value = 0
        self.value_from_right = 0
        self.value_from_left = 0

    def calc_only_front_row(self, front_map):
        if self.front_value:
            front_map[self.front_value] = self.front_value

    def calc_front_row_and_right_col_from_right(self, front_map):
        if self.value_from_right:
            front_map[0:self.front_value, -self.value_from_right - 1] = self.value_from_right
            front_map[self.front_value, -self.value_from_right - 1] = self.front_value + self.value_from_right

    def calc_front_row_and_left_col_from_left(self, front_map):
        if self.value_from_left:
            front_map[0:self.front_value, self.value_from_left] = self.value_from_left
            front_map[self.front_value, self.value_from_left] = self.front_value + self.value_from_left

    def front_view_radar(self):

        front_map = np.zeros((self.map_size, self.map_size), dtype=int)

        self.calc_only_front_row(front_map)

        self.calc_front_row_and_right_col_from_right(front_map)

        self.calc_front_row_and_left_col_from_left(front_map)

        return front_map[::-1]


class HindRadar:
    def __init__(self):
        self.map_size = 0

        self.lower_value = 0
        self.value_from_right = 0
        self.value_from_left = 0

    def calc_only_lower_row(self, hind_map):
        if self.lower_value:
            hind_map[self.lower_value] = self.lower_value

    def calc_hind_and_right_row(self, hind_map):
        if self.value_from_right:
            hind_map[0:self.lower_value, self.value_from_right] = self.value_from_right
            hind_map[self.lower_value, self.value_from_right] = self.lower_value + self.value_from_right

    def calc_hind_and_left_row(self, hind_map):
        if self.value_from_left:
            hind_map[0:self.lower_value, -self.value_from_left - 1] = self.value_from_left
            hind_map[self.lower_value, -self.value_from_left - 1] = self.lower_value + self.value_from_left

    def hind_view_radar(self):

        hind_map = np.zeros((self.map_size, self.map_size), dtype=int)

        self.calc_only_lower_row(hind_map)

        self.calc_hind_and_right_row(hind_map)

        self.calc_hind_and_left_row(hind_map)

        return hind_map


class RightRadar:
    def __init__(self):
        self.map_size = 0

        self.value_from_right = 0

    def calc_only_righter_col(self, right_map):
        if self.value_from_right:
            right_map[:, self.value_from_right] = self.value_from_right

    def calc_right_row_from_up(self, right_map):
        if self.value_from_right:
            right_map[self.value_from_right, self.value_from_right:] = self.value_from_right
            right_map[self.value_from_right, self.value_from_right] = self.value_from_right + self.value_from_right

    def right_side_radar(self):

        right_map = np.zeros((self.map_size, self.map_size), dtype=int)

        self.calc_only_righter_col(right_map)

        self.calc_right_row_from_up(right_map)

        print(f'Right radar: \n\n{right_map}\n\n')
        return right_map


class LeftRadar:
    def __init__(self):
        self.map_size = 0

        self.value_from_right = 0
        self.value_from_left = 0

    def calc_only_left_col(self, left_map):
        if self.value_from_left:
            left_map[:, -1 - self.value_from_left] = self.value_from_left

    def calc_left_row_from_up(self, left_map):
        if self.value_from_right:
            left_map[self.value_from_left, :-self.value_from_left] = self.value_from_left
            left_map[self.value_from_left, -self.value_from_left - 1] = self.value_from_left + self.value_from_left

    def left_side_radar(self):

        left_map = np.zeros((self.map_size, self.map_size), dtype=int)

        self.calc_only_left_col(left_map)

        self.calc_left_row_from_up(left_map)

        print(f'Left radar: \n\n{left_map}\n\n')
        return left_map


class GetRadarsAttributes:
    def __init__(self):
        self.front = FrontRadar()
        self.hind = HindRadar()
        self.right = RightRadar()
        self.left = LeftRadar()
        

    def get_attributes_to_front_view_radar(self, map_size=0, front_value=0, value_from_right=0, value_from_left=0):
        self.front.map_size = map_size
        self.front.front_value = front_value
        self.front.value_from_right = value_from_right
        self.front.value_from_left = value_from_left

    def get_attributes_to_hind_view_radar(self, map_size=0, lower_value=0, value_from_right=0, value_from_left=0):
        self.hind.map_size = map_size
        self.hind.lower_value = lower_value
        self.hind.value_from_right = value_from_right
        self.hind.value_from_left = value_from_left

    def get_attributes_to_right_view_radar(self, map_size=0, value_from_right=0):
        self.right.map_size = map_size
        self.right.value_from_right = value_from_right

    def get_attributes_to_left_view_radar(self, map_size=0, value_from_right=0, value_from_left=0):
        self.left.map_size = map_size
        self.left.value_from_right = value_from_right
        self.left.value_from_left = value_from_left


class GetRadarsCoordinates(GetRadarsAttributes):
    def __init__(self):
        super().__init__()

    def get_coordinates_from_front_radar(self):
        return np.array(self.front.front_view_radar())

    def get_coordinates_from_hind_radar(self):
        return np.array(self.hind.hind_view_radar())

    def get_coordinates_from_right_radar(self):
        return np.array(self.right.right_side_radar())

    def get_coordinates_from_left_radar(self):
        return np.array(self.left.left_side_radar())


class SetRadarsDatas(GetRadarsCoordinates):
    def __init__(self):
        super().__init__()
        self.front_datas = 0
        self.hind_datas = 0
        self.right_datas = 0
        self.left_datas = 0

    def set_front_radar_datas(self):
        self.front_datas += self.get_coordinates_from_front_radar()

    def set_hind_radar_datas(self):
        self.hind_datas += self.get_coordinates_from_hind_radar()

    def set_right_radar_datas(self):
        self.right_datas += self.get_coordinates_from_right_radar()

    def set_left_radar_datas(self):
        self.left_datas += self.get_coordinates_from_left_radar()


class GetRadarsDatas(SetRadarsDatas):
    def __init__(self):
        super().__init__()

    def get_front_radar_datas(self):
        return self.front_datas

    def get_hind_radar_datas(self):
        return self.hind_datas

    def get_right_radar_datas(self):
        return self.right_datas

    def get_left_radar_datas(self):
        return self.left_datas

    def print(self):
        print(self.front_datas)
        print(type(self.front_datas))


class RadarVisualisation:
    def __init__(self):
        pass

    def visualization_settings(self):
        pass

    @staticmethod
    def data_visualization(data=0):
        fig = px.imshow(data, text_auto=True)
        fig.show()


obj = GetRadarsDatas()
for i in range(3):
    obj.get_attributes_to_front_view_radar(15, randint(1, 14), randint(1, 14), randint(1, 14))
    obj.get_coordinates_from_front_radar()
    obj.set_front_radar_datas()

obj.print()

RadarVisualisation().data_visualization(obj.get_front_radar_datas())

