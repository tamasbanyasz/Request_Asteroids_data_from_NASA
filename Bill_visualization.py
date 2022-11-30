import tkinter as tk
from tkinter import *
from tkinter import messagebox
import plotly.express as px
from datetime import datetime
import pandas as pd
import os.path
import json


class Visualization:
    def __init__(self, df, title):
        tf = px.data.gapminder()
        print(tf)

        self.fig = px.line(df, x=df.Years, y=df.columns, hover_data={"Years": "|#%B,%Y"},
                           title=title, labels={"variable": "Bills", "value": "Amount", "Years": "Date", })

        self.fig.update_xaxes(
            dtick="M1",
            tickformat="%b\n%Y"
        )

        self.fig.show()


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
                'Years': ['2021-01', '2021-02', '2021-03', '2021-04', '2021-05', '2021-06', '2021-07', '2021-08',
                          '2021-09', '2021-10',
                          '2021-11', '2021-12', '2022-01', '2022-02', '2022-03', '2022-04', '2022-05', '2022-06',
                          '2022-07', '2022-08', '2022-09', '2022-10'],
                'Water': [2000, 1000, 250, 770, 330, 920, 230, 550, 1200, 1500, 204, 2800, 2008, 800, 150, 205, 340,
                          400, 501, 600, 800, 500],

                'Electricity': [3000, 2000, 1500, 1100, 800, 700, 600, 800, 900, 1000, 1100, 3060, 300, 500, 600, 900,
                                850, 320, 310, 450, 550, 600],
                'Gas': [4000, 800, 401, 401, 450, 401, 400, 403, 450, 477, 402, 400, 490, 403, 440, 407, 401, 420, 410,
                        500, 1000, 1255]
                }

            with open('bills.json', 'w', encoding='utf-8') as f:
                json.dump(python_dict, f, indent=2)

        return file_exists


class BillsLabel:
    def __init__(self, tk_window):
        self.bill_label = Label(tk_window, text='Bills', fg='black', font=('Arial', 20))
        self.bill_label.pack()


class WaterLabel:
    def __init__(self, tk_window):
        self.water_entry = Entry(tk_window)

        self.water_label = Label(tk_window, text='Water :', fg='Blue', font=('Ariel', 16))
        self.water_label.place(x=80, y=60)

        self.water_entry.place(x=190, y=67)

    def get_water_amount(self):
        water_amount = self.water_entry.get()
        self.water_entry.delete(0, END)

        return water_amount


class ElectricityLabel:
    def __init__(self, tk_window):
        self.electricity_entry = Entry(tk_window)

        self.electricity_label = Label(tk_window, text='Electricity :', fg='black', font=('Ariel', 16))
        self.electricity_label.place(x=80, y=113)

        self.electricity_entry.place(x=190, y=120)

    def get_electricity_amount(self):
        electricity_amount = self.electricity_entry.get()
        self.electricity_entry.delete(0, END)

        return electricity_amount


class GasLabel:
    def __init__(self, tk_window):
        self.gas_entry = Entry(tk_window)

        self.gas_label = Label(tk_window, text='Gas :', fg='Brown', font=('Ariel', 16))
        self.gas_label.place(x=80, y=166)

        self.gas_entry.place(x=190, y=173)

    def get_gas_amount(self):
        gas_amount = self.gas_entry.get()
        self.gas_entry.delete(0, END)

        return gas_amount


class DatetToDatesLabel:
    def __init__(self, tk_window):
        self.date_to_dates_start = Entry(tk_window)
        self.date_to_dates_end = Entry(tk_window)

        self.date_to_dates_label = Label(tk_window, text='Date to date :', fg='Black', font=('Ariel', 16))

        self.date_to_dates_label.place(x=400, y=167)
        self.date_to_dates_start.place(x=580, y=172)
        self.date_to_dates_end.place(x=580, y=194)

    def get_start_date(self):
        start_date = self.date_to_dates_start.get()
        self.date_to_dates_start.delete(0, END)

        return start_date

    def get_end_date(self):
        end_date = self.date_to_dates_end.get()
        self.date_to_dates_end.delete(0, END)

        return end_date


class DateToDateBills:
    def __init__(self, tk_window):
        self.date_to_date = DatetToDatesLabel(tk_window)

    def selected_dates(self, jsonfile):
        start_date = self.date_to_date.get_start_date()
        end_date = self.date_to_date.get_end_date()
        years = [i for i in jsonfile['Years']]

        if not years.__contains__(start_date and end_date):
            messagebox.showerror("Invalid", "There is no such date.")
            return window.mainloop()

        start_date_index = jsonfile.index[jsonfile['Years'] == start_date]
        end_date_index = jsonfile.index[jsonfile['Years'] == end_date]

        if start_date_index > end_date_index:
            messagebox.showerror("Invalid", "Incorrect date format.")
            return window.mainloop()

        selected_bills = jsonfile[start_date_index[0]:end_date_index[0] + 1]
        Visualization(selected_bills, "Date to date")


class YearlyBills:
    def __init__(self, jsonfile):
        self.index = []

        for index, value in enumerate(jsonfile['Years']):
            if datetime.now().strftime("%Y") in value:
                self.index.append(index)

        self.yearly_bills = jsonfile.loc[self.index[0]:self.index[-1]]

        Visualization(self.yearly_bills, "Yearly bills")


class AllBills:
    def __init__(self, jsonfile):
        pass

        Visualization(jsonfile, "All Bills")


class DateToDatesButton:
    def __init__(self, tk_window, jsonfile):
        self.date_to_date_bills = DateToDateBills(tk_window)
        self.date_to_dates_button = tk.Button(tk_window, text='Show date to date',
                                              command=lambda: self.date_to_date_bills.selected_dates(jsonfile),
                                              font=('Arial', 16))

        self.date_to_dates_button.place(x=550, y=230)


class AllBillsButton:
    def __init__(self, tk_window, jsonfile):
        self.all_bills_button = tk.Button(tk_window, text='All',
                                          command=lambda: AllBills(jsonfile),
                                          font=('Arial', 16))

        self.all_bills_button.place(x=210, y=480)


class YearlyButton:
    def __init__(self, tk_window, jsonfile):

        self.yearly_button = tk.Button(tk_window, text='Yearly',
                                       command=lambda: YearlyBills(jsonfile), font=('Arial', 16))

        self.yearly_button.place(x=211, y=350)


class SubmitButton:
    def __init__(self, tk_window, jsonfile):
        self.submit_button = tk.Button(tk_window, text='Submit', command=lambda: None,
                                       font=('Arial', 16))

        self.submit_button.place(x=210, y=220)


window = tk.Tk()
window.geometry("800x600")
window.title("Bányász Tamás")
window.resizable(False, False)

JsonFunctions().json_exists()

json_obj = JsonFunctions().read_json()
json_object = pd.DataFrame(json_obj)

BillsLabel(window)
WaterLabel(window)
ElectricityLabel(window)
GasLabel(window)
DatetToDatesLabel(window)

DateToDatesButton(window, json_object)
SubmitButton(window, json_object)
YearlyButton(window, json_object)
AllBillsButton(window, json_object)

window.mainloop()
