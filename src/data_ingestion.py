from data_analysis import analyze
from data_model import WeatherData, Base
#from database import session

from numpy import genfromtxt
from time import time
from datetime import datetime
from sqlalchemy import Column, Integer, Float, Date, exists
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os


path=  os.getcwd()
weather_files_path = 'wx_data' #path + '/wx_data'
print(weather_files_path)
files= os.listdir('wx_data')
print(files)


# This function loads the data for given file, using genfromtxt() functio of numpy. 
def load_data(file_path, file_name):
    data = genfromtxt(file_path + '/' + file_name, delimiter='\t', skip_header=0, converters={0: lambda s: s.decode('utf-8')})
    #print(data)
    return data.tolist()


# This function is to check for missing rows indicated by -9999 in the original data.
def validate_row(tuple_row):

    # Check for the records with -9999
    row = list(tuple_row)
    if row[0] == "-9999":
        row[0] = None
    for i in range(1, len(row)):
        if row[i] == -9999:
            row[i] = None
    return row


# This function is to ingest data to SQLite.
def ingest_data():

    t = time()

    # Initialise SQLite engine for given session
    engine = create_engine('sqlite:///csv_test.db')
    Base.metadata.create_all(engine)

    # Create the session
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()

    # Inserting data
    try:

        analyze(s)
        # For each file in the given folder
        for i, each_file in enumerate(files):
            if i >= 0:
                break
            print(f"{each_file} {i+1} of {len(files)}")
            data = load_data('wx_data', each_file)

            # Extracting station from filename.
            station = each_file[:-4]

            # Iterating over each record in the file.
            for row in data:

                # Validation for missing values
                row = validate_row(row)
                
                # Date formating
                date = datetime.strptime(row[0],"%Y%m%d").date()
                
                # Checking if given record exists, populating otherwise.
                if s.query(exists().where(WeatherData.station==station, WeatherData.date==date)).scalar():
                    continue
                weather_data = WeatherData(
                                            station = station,
                                            date = date, #'%d-%b-%y'
                                            max_temperature = row[1],
                                            min_temperature = row[2],
                                            precipitation = row[3]
                                        )
                # Add all the records
                s.add(weather_data) 

        # Commiting the records
        s.commit()

    except Exception as e:
        s.rollback()
        print(e)
        raise e

    finally:
        # Close the connection
        s.close()

    print ("Time elapsed: " + str(time() - t) + " s.") #0.091s






if __name__ == "__main__":

    ingest_data()