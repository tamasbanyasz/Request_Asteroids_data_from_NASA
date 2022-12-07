from sqlalchemy import create_engine
from Pysql import Base, Asteroids
from sqlalchemy.orm import Session
from sqlalchemy import select


class INSERTINTO:
    def __init__(self, file_name,  datas):
        self.file_name = file_name
        self.engine = create_engine(f"sqlite:///{self.file_name}.db", echo=True, future=True)
        Base.metadata.create_all(self.engine)

        self.data = datas
        self.index_of_asteroid = 0

        while self.index_of_asteroid < len(self.data[0]):
            self.asteroid = Asteroids(
                asteroids_name=self.data[0][self.index_of_asteroid],
                close_approach_date_full=self.data[1][self.index_of_asteroid],
                asteroids_miss_distance_in_km=self.data[2][self.index_of_asteroid],
                relative_velocity_in_km_s=self.data[3][self.index_of_asteroid],
                asteroids_estimated_diameter_min_in_m=self.data[4][self.index_of_asteroid],
                asteroid_is_potentially_dangerous=self.data[5][self.index_of_asteroid]
            )

            with Session(self.engine) as session:
                session.add_all([self.asteroid])
                session.commit()
            self.index_of_asteroid += 1

    def select_all_from_table(self):
        session = Session(self.engine)

        stmt = select(Asteroids)
        print('\nAsteroids data in DB:\n')
        for user in session.scalars(stmt):
            print(user)
