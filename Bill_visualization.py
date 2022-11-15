import tkinter as tk
from tkinter import *
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import os.path
import json


class JsonFunctions:
    def __init__(self):
        pass

    @staticmethod
    def read_json():
        with open('bills.json', 'r', encoding='utf-8') as f:
            json_file = json.load(f)

            return json_file

    @staticmethod
    def json_exists():
        file_exists = os.path.exists('bills.json')
        if file_exists:
            pass
        else:
            python_dict = {
                'Years': ['2021.01', '2021.02', '2021.03', '2021.04', '2021.05', '2021.06', '2021.07', '2021.08',
                          '2021.09', '2021.10',
                          '2021.11', '2021.12', '2022.01', '2022.02', '2022.03', '2022.04', '2022.05', '2022.06',
                          '2022.07'],
                'Water': [2000, 1000, 250, 230, 207, 270, 230, 201, 250, 270, 204, 2800, 2008, 276, 211, 205, 204, 220,
                          501],
                'Electricity': [3000, 500, 300, 304, 302, 360, 300, 302, 305, 370, 355, 3060, 300, 309, 322, 306, 306,
                                320, 310],
                'Gas': [4000, 800, 401, 401, 450, 401, 400, 403, 450, 477, 402, 400, 490, 403, 440, 407, 401, 420, 410]
                }

            with open('bills.json', 'w', encoding='utf-8') as f:
                json.dump(python_dict, f, indent=2)

        return file_exists


class GetDataFrame:
    def __init__(self, json_object):
        self.df = pd.DataFrame.from_dict(json_object)
        self.years = self.df['Years']


class Visualization:
    def __init__(self):
        pass

    def visualization(self, dt):
        plt.figure(figsize=(8, 4))
        ax1 = plt.subplot(111)
        ax1.plot(dt.Years, dt.Water, 'o-', color='blue')
        ax1.plot(dt.Years, dt.Electricity, 'o-', color='yellow')
        ax1.plot(dt.Years, dt.Gas, 'o-', color='black')

        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)

        plt.legend(['Water', 'Electricity', 'Gas'], loc="upper right", shadow=True)
        plt.show()


class TkRoot:
    def __init__(self):
        self.window = tk.Tk()

        self.window.geometry("800x600")
        self.window.title("Bányász Tamás")
        self.window.resizable(False, False)


class DatetToDatesLabel(TkRoot):
    def __init__(self):
        super().__init__()
        self.date_to_dates_start = Entry(self.window)
        self.date_to_dates_end = Entry(self.window)

    def date_to_dates_label(self):
        date_to_dates_label = Label(self.window, text='Date to date :', fg='Black', font=('Ariel', 16))
        date_to_dates_label.place(x=400, y=167)

    def date_to_dates_start_place(self):
        self.date_to_dates_start.place(x=580, y=172)

    def date_to_dates_end_place(self):
        self.date_to_dates_end.place(x=580, y=194)


class BillsLabel(TkRoot):
    def __init__(self):
        super().__init__()

    def bills_place(self):
        bill_label = Label(self.window, text='Bills', fg='black', font=('Arial', 20))
        bill_label.pack()


class WaterLabel(TkRoot):
    def __init__(self):
        super().__init__()
        self.water_entry = Entry(self.window)

    def water_label_place(self):
        water_label = Label(self.window, text='Water :', fg='Blue', font=('Ariel', 16))
        water_label.place(x=80, y=60)

    def water_entry_place(self):
        self.water_entry.place(x=190, y=67)


class ElectricityLabel(TkRoot):
    def __init__(self):
        super().__init__()
        self.electricity_entry = Entry(self.window)

    def electricity_label_place(self):
        electricity_label = Label(self.window, text='Electricity :', fg='black', font=('Ariel', 16))
        electricity_label.place(x=80, y=113)

    def electricity_entry_place(self):
        self.electricity_entry.place(x=190, y=120)


class GasLabel(TkRoot):
    def __init__(self):
        super().__init__()
        self.gas_entry = Entry(self.window)

    def gas_label_place(self):
        gas_label = Label(self.window, text='Gas :', fg='Brown', font=('Ariel', 16))
        gas_label.place(x=80, y=166)

    def gas_entry_place(self):
        self.gas_entry.place(x=190, y=173)


class DateToDateBills(GetDataFrame, Visualization):
    def __init__(self, json_object):
        super().__init__(json_object)


class AllBills(GetDataFrame, Visualization):
    def __init__(self, json_object):
        super().__init__(json_object)

    def all_bills_visualization(self):
        self.visualization(self.df)


class YearlyBills(GetDataFrame, Visualization):
    def __init__(self, json_object):
        super().__init__(json_object)
        self.current_year = datetime.now().strftime("%Y")

    def select_year_of_indexes(self):
        index = []
        for i in json_object['Years']:
            if self.current_year in i:
                idx = json_object['Years'].index(i)
                index.append(idx)
        return index

    def get_year(self):
        return self.df.loc[self.select_year_of_indexes()[0]:self.select_year_of_indexes()[-1]]

    def yearly_vis(self):
        self.visualization(self.get_year())


class Submit(GetDataFrame, WaterLabel, ElectricityLabel, GasLabel):
    def __init__(self):
        super().__init__()


class DateToDatesButton(TkRoot):
    def __init__(self):
        super().__init__()
        self.date_to_dates_button = tk.Button(self.window, text='Show date to date',
                                              command=lambda: None,
                                              font=('Arial', 16))

    def date_to_dates_button_place(self):
        self.date_to_dates_button.place(x=550, y=230)


class AllBillsButton(TkRoot):
    def __init__(self):
        super().__init__()
        self.all_bills_button = tk.Button(self.window, text='All',
                                          command=lambda: AllBills(json_object).all_bills_visualization(),
                                          font=('Arial', 16))

    def all_bills_button_place(self):
        self.all_bills_button.place(x=210, y=480)


class YearlyButton(TkRoot):
    def __init__(self):
        super().__init__()
        self.yearly_button = tk.Button(self.window, text='Yearly',
                                       command=lambda: YearlyBills(json_object).yearly_vis(), font=('Arial', 16))

    def yearly_button_place(self):
        self.yearly_button.place(x=211, y=350)


class SubmitButton(TkRoot):
    def __init__(self):
        super().__init__()
        self.submit_button = tk.Button(self.window, text='Submit', command=lambda: None, font=('Arial', 16))

    def submit_button_place(self):
        self.submit_button.place(x=210, y=220)


class CalculatorLabels(DatetToDatesLabel, BillsLabel, WaterLabel, ElectricityLabel, GasLabel):
    def __init__(self):
        super().__init__()

        self.bills_place()

        self.date_to_dates_label()
        self.date_to_dates_start_place()
        self.date_to_dates_end_place()

        self.water_label_place()
        self.water_entry_place()

        self.electricity_label_place()
        self.electricity_entry_place()

        self.gas_label_place()
        self.gas_entry_place()


class CalculatorButtons(DateToDatesButton, AllBillsButton, YearlyButton, SubmitButton):
    def __init__(self):
        super().__init__()

        self.date_to_dates_button_place()
        self.all_bills_button_place()
        self.yearly_button_place()
        self.submit_button_place()


class CalculatorDisplay(CalculatorLabels, CalculatorButtons):
    def __init__(self):
        super().__init__()

        self.window.mainloop()


JsonFunctions().json_exists()

json_object = JsonFunctions().read_json()

GetDataFrame(json_object)

CalculatorDisplay()
