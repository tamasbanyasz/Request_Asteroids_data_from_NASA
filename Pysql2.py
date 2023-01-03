from sqlalchemy import create_engine
from Pysql1 import Base, Asteroids
from sqlalchemy.orm import Session
from sqlalchemy import select


class InsertInto:
    def __init__(self, file_name,  datas):
        self.file_name = file_name
        self.engine = create_engine(f"sqlite:///{self.file_name}.db", echo=True, future=True)
        Base.metadata.create_all(self.engine)

        self.asteroid = Asteroids(
            asteroids_name=datas['asteroid_name'],
            close_approach_date_full=datas['close_approach_date_full'],
            asteroids_miss_distance_in_km=datas['asteroid_miss_distance_in_km'],
            relative_velocity_in_km_s=datas['relative_velocity_in_km/s'],
            asteroids_estimated_diameter_min_in_m=datas['asteroid_estimated_diameter_min_in_m'],
            asteroid_is_potentially_dangerous=datas['asteroid_is_potentially_dangerous']

        )

        with Session(self.engine) as session:
            session.add_all([self.asteroid])
            session.commit()

    def select_all_from_table(self):
        session = Session(self.engine)

        stmt = select(Asteroids)
        print('\nAsteroids data in DB:\n')
        for user in session.scalars(stmt):
            print(user)
