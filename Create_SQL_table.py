from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import VARCHAR
from sqlalchemy import Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Asteroids(Base):
    __tablename__ = "asteroids"

    id = Column(Integer, primary_key=True)
    asteroids_name = Column(VARCHAR(50))
    asteroids_close_date = Column(VARCHAR(20))
    asteroids_miss_distance_in_km = Column(Float)
    velocitys_in_km_s = Column(Float)
    asteroids_estimated_diameter_min_in_m = Column(Float)

    def __repr__(self):
        return f"Asteroid(id={self.id!r}, asteroid_name={self.asteroids_name!r}, " \
               f"close_date={self.asteroids_close_date!r}," \
               f"miss_distance_in_km={self.asteroids_miss_distance_in_km!r}, " \
               f"velocitys_in_km/s={self.velocitys_in_km_s!r}," \
               f"estimated_diameter_min_inm={self.asteroids_estimated_diameter_min_in_m!r})"
