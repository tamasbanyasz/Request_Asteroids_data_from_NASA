
class NumberSystemCalculator:
    def __init__(self):
        self.number = 0
        self.decimal_number = 0

    def calculate_decimal_into_binary_system(self, decimal_number):
        self.number = decimal_number

        binary_numbers = []

        while self.number != 0:
            binary_numbers.append(self.number % 2)
            self.number = self.number // 2

        binary_numbers = int(''.join(map(str, reversed(binary_numbers))))
        print(f'\nThe selected decimal number in binary system: {binary_numbers}')
        return binary_numbers

    def calculate_octal_to_decimal(self, octal_number):
        self.number = octal_number
        list_of_digits = list(map(int, str(self.number)))

        decimal_number = 0

        for index, value in enumerate(reversed(list_of_digits)):
            decimal_number = decimal_number + value * 8 ** index

        print(f'\nThe selected octal number in decimal: {decimal_number}')
        return decimal_number

    def calculate_hexa_to_decimal(self, hexa_value):
        self.number = hexa_value

        list_of_hexa_values = [i for i in self.number]
        formatted_list_of_hexa_values = []

        for item in list_of_hexa_values:
            formatted_list_of_hexa_values.append(item.upper())
            if item.isdigit():
                formatted_list_of_hexa_values.append(int(item))

        hexa_numbers = {"A": 10, "B": 11, "C": 12, "D": 13, "E": 14, "F": 15}

        for index, value in enumerate(reversed(formatted_list_of_hexa_values)):
            if type(value) == int:
                self.decimal_number = self.decimal_number + value * 16 ** index
            self.value_equals_to_one_of_key_in_hexa_numbers_dict(hexa_numbers, index, value)

        print(f'\nThe selected hexa value in decimal: {self.decimal_number}')
        return self.decimal_number

    def value_equals_to_one_of_key_in_hexa_numbers_dict(self, hexa_numbers, index, value):
        for key, item in hexa_numbers.items():
            if value == key:
                self.decimal_number = self.decimal_number + item * 16 ** index


number = NumberSystemCalculator()

number.calculate_decimal_into_binary_system(27)
number.calculate_octal_to_decimal(2034)
number.calculate_hexa_to_decimal("a5f")
