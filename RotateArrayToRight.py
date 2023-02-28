
class Line:

    def __init__(self, value):
        self.line = self.get_parameter(value)
        self.line_length = len(self.line)

    def get_array(self):
        return self.line

    def get_parameter(self, value):
        return self.generate_array_if_value_is_integer(value) or self.value_can_be_slicing(value)

    def generate_array_if_value_is_integer(self, value):
        if type(value) == int:
            return [i for i in range(value)]

    def value_can_be_slicing(self, value):
        if type(value) != int:
            return [i for i in value]

    def rotate_right_one_by_one(self, my_array):
        last_item_of_my_array = my_array.pop()
        my_array.insert(0, last_item_of_my_array)

        return my_array

    def rotate_left_one_by_one(self, my_array):
        first_item_of_my_array = my_array.pop(0)
        my_array.insert(self.line_length, first_item_of_my_array)

        return my_array

    def rotate_right_by_a_specific_number(self, my_array, selected_number):
        for i in range(selected_number):
            self.rotate_right_one_by_one(my_array)

        return my_array

    def rotate_left_by_a_specific_number(self, my_array, selected_number):
        for i in range(selected_number):
            self.rotate_left_one_by_one(my_array)

        return my_array


list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
number = 10
string = "Hello"

first_line = Line(string)

first_array = first_line.get_array()
print(f'\nOriginal array -- > {first_array}')

rotated_by_one = first_line.rotate_right_one_by_one(first_array)
print(f'\nRotated to right by one -- >{rotated_by_one}')

rotated_left_by_a_specific_index = first_line.rotate_left_by_a_specific_number(rotated_by_one, 3)
print(f'\nRotated to left by a specific index -- > {rotated_left_by_a_specific_index}')
