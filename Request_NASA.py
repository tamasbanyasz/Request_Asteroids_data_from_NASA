from pandas import DataFrame, Series
from PYsql2 import INSERTINTO
import plotly.express as px
from requests import get
import os.path
import ujson


class AsteroidsVisualization:
    def __init__(self, data_frame):
        self.data_frame = DataFrame(data_frame).drop(['asteroid_is_potentially_dangerous', 'close_approach_date_full'],
                                                     axis=1)
        
        self.fig = px.scatter(self.data_frame,
                              x="asteroid_miss_distance_in_km",
                              y="relative_velocity_in_km/s",
                              size="asteroid_estimated_diameter_min_in_m", color="asteroid_name",
                              hover_name="asteroid_name", log_x=True, size_max=80)

        self.fig.show()


class GetDatasFromNASA:
    def __init__(self, api_key, date):
        self.API_KEY = api_key
        self.DATE = date
        self.asteroids_data = get(f'https://api.nasa.gov/neo/rest/v1/feed?start_date={self.DATE}&'
                                  f'end_date={self.DATE}&api_key={self.API_KEY}')
        self.asteroids_data_in_json = self.asteroids_data.json()
        print(self.asteroids_data_in_json)
        self.list_of_asteroids = self.asteroids_data_in_json['near_earth_objects'][self.DATE]

    def get_list_of_asteroids(self):
        return self.list_of_asteroids


class DictOfAttributesOfAsteroids:
    def __init__(self):
        self.dict = {'asteroid_name': [],
                     'close_approach_date_full': [],
                     'asteroid_miss_distance_in_km': [],
                     'relative_velocity_in_km/s': [],
                     'asteroid_estimated_diameter_min_in_m': [],
                     'asteroid_is_potentially_dangerous': []
                     }
        self.index_of_asteroid = 0

    def append_asteroid_attributes_to_lists_in_dict(self, list_of_asteroids):
        while self.index_of_asteroid < len(list_of_asteroids):
            asteroid = list_of_asteroids[self.index_of_asteroid]
            asteroids_approach_data = asteroid['close_approach_data'][0]
            asteroids_estimated_diameter = asteroid['estimated_diameter']

            self.dict['asteroid_name'].append(asteroid['name'].replace("'", "").strip('()').replace("(", ""))
            self.dict['close_approach_date_full'].append(asteroids_approach_data['close_approach_date_full']),
            self.dict['asteroid_miss_distance_in_km'].append(float(asteroids_approach_data['miss_distance']
                                                                   ['kilometers']))
            self.dict['relative_velocity_in_km/s'].append(float(asteroids_approach_data['relative_velocity']
                                                          ['kilometers_per_second']))
            self.dict['asteroid_estimated_diameter_min_in_m'].append(asteroids_estimated_diameter['meters']
                                                                     ['estimated_diameter_min'])
            self.dict['asteroid_is_potentially_dangerous'].append(bool(asteroid['is_potentially_hazardous_asteroid']))

            self.index_of_asteroid += 1


class JSONFileFunctions:
    def __init__(self, file_name):
        self.file_name = file_name

    def is_json_exists(self):
        file_exists = os.path.exists(f'{self.file_name}.json')
        if file_exists:
            pass
        else:
            create_first_an_empty_dict = {}

            with open(f'{self.file_name}.json', "w") as f:
                ujson.dump(create_first_an_empty_dict, f, indent=2, sort_keys=True, )

    def read_json(self, date, data_frame):
        with open(f'{self.file_name}.json', 'r', encoding='utf-8') as f:
            json_file = ujson.load(f)
            print(f"In JSON File:\n{json_file}\n")
            new_dict = {date: data_frame.to_dict()}
            json_file.update(new_dict)
            return json_file

    def write_to_json(self, json_file):
        with open(f'{self.file_name}.json', "w") as f:
            ujson.dump(json_file, f, indent=2, sort_keys=True)


class AsteroidsSeries:
    def __init__(self, api_key, date):
        self.datas = GetDatasFromNASA(api_key, date)
        self.values = DictOfAttributesOfAsteroids()
        self.values.append_asteroid_attributes_to_lists_in_dict(self.datas.get_list_of_asteroids())
        self.json_functions = JSONFileFunctions(json_file_name)

    def get_asteroids_in_pd_series(self):
        return Series(self.values.dict)

    def read_json(self, date, data_frame):
        return self.json_functions.read_json(date, data_frame)

    def save_to_json(self, json_file):
        self.json_functions.write_to_json(json_file)


API_KEY = 'diHl0LviLAVDsFhiQQBFeVhGzaypOchuTneOJWXI'
DATE = '2022-12-07'
json_file_name = "asteroids"
db_file_name = "asteroids"

JSONFileFunctions(json_file_name).is_json_exists()

asteroids_df = AsteroidsSeries(API_KEY, DATE)
asteroids_data = asteroids_df.get_asteroids_in_pd_series()
print(f'{asteroids_data}\n')
readed_json = asteroids_df.read_json(DATE, asteroids_data)
asteroids_df.save_to_json(readed_json)

insert_into = INSERTINTO(db_file_name, asteroids_data)
insert_into.select_all_from_table()

AsteroidsVisualization(asteroids_df.values.dict)
