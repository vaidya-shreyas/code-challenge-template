from data_analysis import analyze
from data_model import WeatherData, Base
from api_server import start_server
from data_ingestion import ingest_data

from numpy import genfromtxt
from time import time
from datetime import datetime
from sqlalchemy import Column, Integer, Float, Date, exists
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os





# Initialise SQLite engine for given session
engine = create_engine('sqlite:///csv_test.db')
Base.metadata.create_all(engine)

# Create the session
session = sessionmaker()
session.configure(bind=engine)
s = session()

if __name__ == "__main__":

    ingest_data(s)
    analyze(s)

    start_server()