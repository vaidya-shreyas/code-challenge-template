from sqlalchemy import exists, func
from sqlalchemy.sql import extract

from data_model import WeatherData, WeatherStats



# Function to compute weather statistics.
def analyze(s):

    # Computing the average statistics for given year and station.
    res = s.query(WeatherData.station, 
            extract('year', WeatherData.date).label('year'), 
            func.avg(WeatherData.max_temperature).label('avg_max_temp')/10,
            func.avg(WeatherData.min_temperature).label('avg_min_temp')/10,
            func.sum(WeatherData.precipitation).label('total_precip')/100) \
    .group_by(WeatherData.station, 'year').all()

    # Populating the result in the WeatherStats Table
    for row in res:
        weather_data = WeatherStats(
            station = row[0],
            year = row[1],
            avg_max_temperature = row[2],
            avg_min_temperature = row[3],
            total_precipitation = row[4]
        )
        # Checking for updates
        if s.query(exists().where(WeatherStats.station==weather_data.station, WeatherStats.year==weather_data.year)).scalar():
            existing_weather_data: WeatherStats = s.query(WeatherStats).filter_by(station=weather_data.station, year=weather_data.year).first()
            existing_weather_data.avg_max_temperature = weather_data.avg_max_temperature
            existing_weather_data.avg_min_temperature = weather_data.avg_min_temperature
            existing_weather_data.total_precipitation = weather_data.total_precipitation
        else:
            s.add(weather_data)
    s.commit()