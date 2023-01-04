from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import BOOLEAN
from sqlalchemy import DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Asteroids(Base):
    __tablename__ = "asteroids"

    id = Column(Integer, primary_key=True)
    asteroids_name = Column(String(50))
    close_approach_date_full = Column(DateTime)
    asteroids_miss_distance_in_km = Column(Float)
    relative_velocity_in_km_s = Column(Float)
    asteroids_estimated_diameter_min_in_m = Column(Float)
    asteroid_is_potentially_dangerous = Column(BOOLEAN)

    def __repr__(self):
        return f"Asteroid(id={self.id!r}, asteroid_name={self.asteroids_name!r}, " \
               f"close_approach_date_full={self.close_approach_date_full!r}," \
               f"miss_distance_in_km={self.asteroids_miss_distance_in_km!r}, " \
               f"relative_velocity_in_km/s={self.relative_velocity_in_km_s!r}," \
               f"estimated_diameter_min_in_m={self.asteroids_estimated_diameter_min_in_m!r}," \
               f"asteroid_is_potentially_dangerous={self.asteroid_is_potentially_dangerous!r})"
