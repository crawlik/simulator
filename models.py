from sqlalchemy import Column, DateTime, Float, Integer
from database import Base


class WeatherMetric(Base):
    __tablename__ = 'weather_metrics'

    id = Column(Integer, primary_key=True)
    collection_ts = Column(DateTime)
    temperature = Column(Float)
    humidity = Column(Float)
    precipitation = Column(Float)
    wind_speed = Column(Float)

    def __init__(self, collection_ts, temperature,
                 humidity, precipitation, wind_speed):
        self.collection_ts = collection_ts
        self.temperature = temperature
        self.humidity = humidity
        self.precipitation = precipitation
        self.wind_speed = wind_speed

    def __repr__(self):
        return '<Weather metrics ID %d>' % self.id
