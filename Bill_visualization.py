import tkinter as tk
from tkinter import *
from tkinter import messagebox
import plotly.express as px
from datetime import datetime
import pandas as pd
import os.path
import orjson


class Visualization:
    def __init__(self, df, title):
        self.fig = px.line(df, x=df.Years, y=df.columns, hover_data={"Years": "|%B, %Y"},
                           title=title, labels={"variable": "Bills", "value": "Amount", "Years": "Date"})
        self.fig.update_traces(mode="markers+lines")
        self.fig.update_xaxes(
            dtick="M1",
            tickformat="%b\n%Y"
        )

        self.fig.show()


class JsonFunctions:
    def __init__(self, file_name):
        self.file_name = file_name

    def write_to_json(self, new_jsonfile):
        with open(f"{self.file_name}.json", "wb") as f:
            f.write(orjson.dumps(new_jsonfile, option=orjson.OPT_INDENT_2))

    def read_json(self):
        with open(f"{self.file_name}.json", "rb") as f:
            json_data = orjson.loads(f.read())

            return json_data

    def json_exists(self):
        file_exists = os.path.exists(f"{self.file_name}.json")
        if file_exists:
            pass
        else:
            test_dict = {
                'Years': ['2021-01', '2021-01', '2021-02', '2021-03', '2021-04', '2021-04', '2021-05', '2021-06',
                          '2021-07', '2021-08', '2021-09', '2021-10',
                          '2021-11', '2021-12', '2022-01', '2022-01', '2022-02', '2022-03', '2022-04', '2022-04',
                          '2022-05', '2022-06', '2022-07', '2022-08', '2022-09', '2022-10', '2022-11'],
                'Water': [2000, 1467, 1000, 250, 770, 330, 601, 920, 230, 550, 1200, 1500, 204, 2800, 2008, 800, 150,
                          205, 340, 400, 501, 600, 800, 500, 386, 777, 1300],

                'Electricity': [3000, 1777, 2000, 1500, 1100, 800, 501, 700, 600, 800, 900, 1000, 1100, 3060, 300, 500,
                                600, 900, 850, 320, 310, 450, 550, 600, 999, 1300, 1000],
                'Gas': [4000, 2100, 800, 401, 401, 450, 301, 401, 400, 403, 450, 477, 402, 400, 490, 403, 440, 407, 401,
                        420, 410, 500, 1000, 1255, 1500, 1790, 1100]
            }

            self.write_to_json(test_dict)

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
        jsonfile = pd.DataFrame(jsonfile)
        start_date = self.date_to_date.get_start_date()
        end_date = self.date_to_date.get_end_date()
        years = set(i for i in jsonfile['Years'])

        if not years.__contains__(start_date and end_date):
            messagebox.showerror("Invalid", "There is no such date.")
            return window.mainloop()

        start_date_index = jsonfile.index[jsonfile['Years'] == start_date]
        end_date_index = jsonfile.index[jsonfile['Years'] == end_date]

        if start_date_index[0] > end_date_index[-1:][0]:
            messagebox.showerror("Invalid", "Incorrect date format.")
            return window.mainloop()

        selected_bills = jsonfile[start_date_index[0]:end_date_index[-1:][0] + 1]
        Visualization(selected_bills, "Date to date")


class SubmitAmounts(JsonFunctions):
    def __init__(self, tk_window, file_name):
        super().__init__(file_name)
        self.water = WaterLabel(tk_window)
        self.electricity = ElectricityLabel(tk_window)
        self.gas = GasLabel(tk_window)
        self.date_now = datetime.now().strftime("%Y-%m")

    def send_amounts(self, jsonfile):
        water = self.water.get_water_amount()
        electricity = self.electricity.get_electricity_amount()
        gas = self.gas.get_gas_amount()

        if not water.isnumeric() and not electricity.isnumeric() and not gas.isnumeric():
            messagebox.showerror("Invalid", "Incorrect input.")
            return window.mainloop()

        jsonfile['Years'].append(self.date_now)
        jsonfile['Water'].append(int(water))
        jsonfile['Electricity'].append(int(electricity))
        jsonfile['Gas'].append(int(gas))

        self.write_to_json(jsonfile)
        messagebox.showinfo("Information", "Amounts sent.")


class YearlyBills:
    def __init__(self, jsonfile):
        self.index = []
        self.jsonfile = pd.DataFrame(jsonfile)

        for index, value in enumerate(self.jsonfile['Years']):
            if datetime.now().strftime("%Y") in value:
                self.index.append(index)

        self.yearly_bills = self.jsonfile.loc[self.index[0]:self.index[-1]]

        Visualization(self.yearly_bills, "Yearly bills")


class AllBills:
    def __init__(self, jsonfile):
        Visualization(pd.DataFrame(jsonfile), "All Bills")


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
    def __init__(self, tk_window, jsonfile, name_of_json_file):
        self.s = SubmitAmounts(tk_window, name_of_json_file)

        self.submit_button = tk.Button(tk_window, text='Submit',
                                       command=lambda: self.s.send_amounts(jsonfile),
                                       font=('Arial', 16))

        self.submit_button.place(x=210, y=220)


json_file_name = "bills"

window = tk.Tk()
window.geometry("800x600")
window.title("Bányász Tamás")
window.resizable(False, False)

json_functions = JsonFunctions(json_file_name)
json_functions.json_exists()

datas_in_dict = json_functions.read_json()

BillsLabel(window)
WaterLabel(window)
ElectricityLabel(window)
GasLabel(window)
DatetToDatesLabel(window)

DateToDatesButton(window, datas_in_dict)
YearlyButton(window, datas_in_dict)
AllBillsButton(window, datas_in_dict)
SubmitButton(window, datas_in_dict, json_file_name)

window.mainloop()
