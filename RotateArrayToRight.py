from numpy import array, concatenate


class ArrayRotate:
    def __init__(self, length, number_of_rotate):
        self.array_length = length
        self.k = number_of_rotate
        self.mylist = array([item for item in range(1, self.array_length+1)])

    def to_right(self):
        print(f'Original array --> {self.mylist}')
        return concatenate([self.mylist[self.array_length - self.k:self.array_length], self.mylist[self.array_length - self.array_length:self.array_length - self.k]])


array_rotate = ArrayRotate(10, 1)

rotated_array = array_rotate.to_right()

print(f'Rotated array --> {rotated_array}')
