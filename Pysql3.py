from pandas import DataFrame, concat, to_datetime
from Pysql2 import InsertInto
import plotly.express as px
from requests import get
import os.path
import ujson
from tkinter import *
from tkinter import messagebox
from datetime import datetime, date


class AsteroidsVisualization:
    def __init__(self, data_frame):
        self.data_frame = data_frame.drop(['asteroid_is_potentially_dangerous', 'close_approach_date_full'],
                                          axis=1)

        self.data_frame['asteroid_estimated_diameter_min_in_m'] = \
            self.data_frame['asteroid_estimated_diameter_min_in_m'].astype('float32')
        self.data_frame['relative_velocity_in_km/s'] = self.data_frame['relative_velocity_in_km/s'].astype('float32')

        self.fig = px.scatter(self.data_frame,
                              x="asteroid_miss_distance_in_km",
                              y="relative_velocity_in_km/s",
                              size="asteroid_estimated_diameter_min_in_m", color="asteroid_name",
                              hover_name="asteroid_name", log_x=True, size_max=80)

        self.fig.update_traces(marker=dict(line=dict(width=8, color='White')))
        self.fig.update_layout(plot_bgcolor='Black',
                               paper_bgcolor='Black',
                               font_color="White",
                               font_size=20,
                               yaxis=dict(titlefont=dict(size=30), gridcolor='Gray', linecolor='Red', linewidth=2),
                               xaxis=dict(titlefont=dict(size=30), gridcolor='Gray', linecolor='Red', linewidth=2),
                               legend_title=dict(font=dict(size=30)))

        self.fig.show()


class DataFrameOfAttributesOfAsteroids:
    def __init__(self):
        self.asteroids_df = DataFrame(columns=['asteroid_name',
                                               'close_approach_date_full',
                                               'asteroid_miss_distance_in_km',
                                               'relative_velocity_in_km/s',
                                               'asteroid_estimated_diameter_min_in_m',
                                               'asteroid_is_potentially_dangerous'
                                               ])

        self.asteroids_df['asteroid_is_potentially_dangerous'] = self.asteroids_df['asteroid_is_potentially_dangerous']\
            .astype('bool')

    def append_asteroid_attributes_to_dicts_in_list(self, list_of_asteroids):
        df = DataFrame(list_of_asteroids, columns=['name', 'close_approach_data', 'estimated_diameter',
                                                   'is_potentially_hazardous_asteroid'])
        self.asteroids_df['asteroid_name'] = [i.replace("'", "").strip('()').replace("(", "")
                                              for i in df['name'].values]
        self.asteroids_df['close_approach_date_full'] = [i[0]['close_approach_date_full']
                                                         for i in df['close_approach_data'].values]
        self.asteroids_df['asteroid_miss_distance_in_km'] = [round(float(i[0]['miss_distance']
                                                             ['kilometers']), 2)
                                                             for i in df['close_approach_data'].values]
        self.asteroids_df['relative_velocity_in_km/s'] = [round(float(i[0]
                                                          ['relative_velocity']['kilometers_per_second']), 2)
                                                          for i in df['close_approach_data'].values]
        self.asteroids_df['asteroid_estimated_diameter_min_in_m'] = [i['meters']
                                                                     ['estimated_diameter_min']
                                                                     for i in df['estimated_diameter'].values]
        self.asteroids_df['asteroid_is_potentially_dangerous'] = df['is_potentially_hazardous_asteroid'].values

        self.asteroids_df['asteroid_miss_distance_in_km'] = self.asteroids_df['asteroid_miss_distance_in_km'].\
            astype('float32')
        self.asteroids_df['asteroid_estimated_diameter_min_in_m'] = \
            self.asteroids_df['asteroid_estimated_diameter_min_in_m'].astype('float16')
        self.asteroids_df['relative_velocity_in_km/s'] = self.asteroids_df['relative_velocity_in_km/s'].astype('float16'
                                                                                                               )
        self.asteroids_df['close_approach_date_full'] = to_datetime(self.asteroids_df['close_approach_date_full'],
                                                                    format='%Y-%b-%d %H:%M')

        print(self.asteroids_df.to_string())
        print(self.asteroids_df.info())


class GetDatasFromNASA(DataFrameOfAttributesOfAsteroids):
    def __init__(self, api_key, selected_date):
        super().__init__()
        self.API_KEY = api_key
        self.DATE = selected_date
        self.today = date.today()

        self.is_valid_date()

    def is_valid_date(self):
        try:
            datetime.strptime(self.DATE, '%Y-%m-%d')
            year, month, day = self.DATE.split('-')
            self.DATE = date(int(year), int(month), int(day)).isoformat()

            if all([self.DATE < str(self.today), self.DATE >= '1960-01-01']):

                asteroids_data = get(f'https://api.nasa.gov/neo/rest/v1/feed?start_date={self.DATE}&'
                                     f'end_date={self.DATE}&api_key={self.API_KEY}')

                asteroids_data_in_json = asteroids_data.json()
                list_of_asteroids = asteroids_data_in_json['near_earth_objects'][self.DATE]

                self.append_asteroid_attributes_to_dicts_in_list(list_of_asteroids)

            else:
                messagebox.showerror("Invalid", "There is no such a date.")

        except ValueError:
            messagebox.showerror("Invalid", "Incorrect data format, should be 'YYYY-MM-DD'.")


class JSONFileFunctions:
    def __init__(self, file_name):
        self.file_name = file_name

    def is_json_exists(self):
        file_exists = os.path.exists(f'{self.file_name}.json')
        if file_exists:
            pass
        else:
            create_first_an_empty_dict = {'datas': []}

            with open(f'{self.file_name}.json', "w") as f:
                ujson.dump(create_first_an_empty_dict, f, indent=2, sort_keys=True, )

    def read_json(self, selected_date, data_frame):
        with open(f'{self.file_name}.json', 'r', encoding='utf-8') as f:
            json_file = ujson.load(f)
            new_dict = {selected_date: [data_frame]}
            json_file['datas'].append(new_dict)
            return json_file

    def write_to_json(self, json_file):
        with open(f'{self.file_name}.json', "w") as f:
            ujson.dump(json_file, f, indent=2, sort_keys=True)


class DataOperation:
    def __init__(self, listbox, db_file, api_key, name_of_json_file):
        self.json_functions = JSONFileFunctions(name_of_json_file)
        self.json_functions.is_json_exists()

        self.listbox = listbox
        self.api_key = api_key
        self.selected_date = None
        self.db_file_name = db_file

        self.asteroids_df_for_select = DataFrame()
        self.asteroids_df_for_visualization = DataFrame()
        self.selected_asteroid_name = None
        self.asteroid_index = 0
        self.selected_asteroid_in_df = DataFrame()

    def clear_listbox_and_selected_item(self):
        self.listbox.delete(0, END)
        self.asteroids_df_for_select = DataFrame()
        self.asteroids_df_for_visualization = DataFrame()

    def get_datas_from_nasa(self, selected_date):
        list_of_asteroids = GetDatasFromNASA(self.api_key, selected_date)
        self.store_selected_date_and_asteroids_temporarily(selected_date, list_of_asteroids)

    def store_selected_date_and_asteroids_temporarily(self, selected_date, list_of_asteroids):
        self.selected_date = selected_date
        self.asteroids_df_for_select = concat([list_of_asteroids.asteroids_df])
        self.asteroids_df_for_visualization = concat([list_of_asteroids.asteroids_df])

    def requesting_asteroids(self, selected_date):
        self.clear_listbox_and_selected_item()
        self.get_datas_from_nasa(selected_date)

    def insert_asteroids_name_into_listbox(self, selected_date):
        self.requesting_asteroids(selected_date)
        [self.listbox.insert(END, asteroid) for asteroid in self.asteroids_df_for_select['asteroid_name'].values]

    def selecting_asteroid(self):
        self.selected_asteroid_in_df = concat([self.asteroids_df_for_select.iloc[self.asteroid_index]])

    def refresh_temporary_dataframe(self, item):
        self.asteroids_df_for_select = self.asteroids_df_for_select.drop([item])
        self.asteroids_df_for_select.reset_index(drop=True, inplace=True)

    def send_selected_asteroid_to_json(self):
        self.selected_asteroid_in_df['close_approach_date_full'] = datetime.isoformat(self.selected_asteroid_in_df
                                                                                      ['close_approach_date_full'])
        data_frame = self.selected_asteroid_in_df.to_dict()
        readed_json = self.json_functions.read_json(self.selected_date, data_frame)
        self.json_functions.write_to_json(readed_json)

    def save_selected_asteroid_from_listbox(self):
        for item in self.listbox.curselection():
            self.selected_asteroid_name = self.listbox.get(item)
            self.asteroid_index = item
            self.selecting_asteroid()
            self.listbox.delete(item)
            self.refresh_temporary_dataframe(item)
            InsertInto(self.db_file_name, self.selected_asteroid_in_df).select_all_from_table()
            self.send_selected_asteroid_to_json()
            messagebox.showinfo("Information", "Asteroid sent.")

