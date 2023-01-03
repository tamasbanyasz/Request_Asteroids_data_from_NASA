import tkinter as tk
from tkinter import *
from tkinter import messagebox
from Pysql3 import DataOperation, AsteroidsVisualization


class DateEntry:
    def __init__(self, tk_window):
        self.date_entry = Entry(tk_window)

        self.date_label = Label(tk_window, text='Date :', fg='Black', font=('Ariel', 16))
        self.date_label.place(x=117, y=166)

        self.date_entry.place(x=190, y=173)

    def get_date(self):
        selected_date = self.date_entry.get()
        self.date_entry.delete(0, END)

        return selected_date


class RequestGUI:
    def __init__(self, api_key, db_file, name_of_json_file):
        self.window = tk.Tk()
        self.frame = Frame(self.window)
        self.window.geometry("1024x768")
        self.window.title("Bányász Tamás")
        self.window.resizable(False, False)

        self.asteroid_label = Label(self.window, text='Asteroid name', fg='black', font=('Arial', 20))
        self.data_entry = DateEntry(self.window)
        self.scrollbar = Scrollbar(self.frame, orient=VERTICAL)
        self.listbox = Listbox(self.frame, yscrollcommand=self.scrollbar.set, height=15,
                               selectmode=EXTENDED,
                               width=25,
                               bd=4,
                               bg="White",
                               activestyle='dotbox',
                               font="Helvetica",
                               fg="Black")

        self.data_operating = DataOperation(self.listbox, db_file, api_key, name_of_json_file)

        self.select_date_button()
        self.save_button()
        self.bubble_chart_visualization_button()
        self.delete_all_button()

        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox.pack()
        self.asteroid_label.pack()
        self.frame.pack()

        self.window.mainloop()

    def display_visualization(self):
        if self.data_operating.asteroids_df.empty:
            messagebox.showerror("Invalid", "There is no requested asteroids.")
            return self.window.mainloop()

        AsteroidsVisualization(self.data_operating.asteroids_df)

    def select_date_button(self):
        select_date_button = tk.Button(self.window, text='Select date',
                                       command=lambda: self.data_operating.insert_asteroids_name_into_listbox
                                       (self.data_entry.get_date()),
                                       font=('Arial', 16))

        select_date_button.place(x=190, y=203)

    def save_button(self):
        save_item_button = tk.Button(self.window, text='Save asteroid',
                                     command=lambda: self.data_operating.save_selected_asteroid_from_listbox(),
                                     font=('Arial', 16))

        save_item_button.place(x=425, y=450)

    def bubble_chart_visualization_button(self):
        visualization_button = tk.Button(self.window, text='Display asteroids',
                                         command=lambda: self.display_visualization(),
                                         font=('Arial', 16))

        visualization_button.place(x=700, y=200)

    def delete_all_button(self):
        delete_all_button = tk.Button(self.window, text='Delete all',
                                      command=lambda: self.data_operating.clear_listbox_and_selected_item(),
                                      font=('Arial', 16))

        delete_all_button.place(x=445, y=500)


API_KEY = 'diHl0LviLAVDsFhiQQBFeVhGzaypOchuTneOJWXI'
json_file_name = "asteroids"
db_file_name = "asteroids"

asteroids_request = RequestGUI(API_KEY, db_file_name, json_file_name)
