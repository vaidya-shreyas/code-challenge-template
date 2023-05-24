from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Integer, Text, String, Numeric
from sqlalchemy import Column, Integer, Float, Date, DateTime, func, UniqueConstraint


Base = declarative_base()

# Data model declaration for weather data
class WeatherData(Base):

    __tablename__ = "WeatherData"

    uid = Column(Integer, primary_key=True, autoincrement="auto")
    station = Column(String, nullable=False)
    
    date = Column(Date)
    max_temperature = Column(Numeric( scale=1 ),nullable=True)
    min_temperature = Column(Numeric( scale=1 ),nullable=True)
    precipitation = Column(Numeric( scale=1 ),nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())

    __table_args__ = (UniqueConstraint('station', 'date', name='__station_date'),)

# Data model declaration for weather statistics
class WeatherStats(Base):

    __tablename__ = "WeatherStats"

    uid = Column(Integer, primary_key=True, autoincrement="auto")
    station = Column(String(255), nullable=False)
    
    year = Column(Integer)
    avg_max_temperature = Column(Numeric(scale=1), nullable=True)
    avg_min_temperature = Column(Numeric(scale=1), nullable=True)
    total_precipitation = Column(Numeric(scale=1), nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())

    __table_args__ = (UniqueConstraint('station', 'year', name='__station_year'),)