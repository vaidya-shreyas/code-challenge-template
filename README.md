# Code-Challenge-Template

This repository is developed in response to the Corteva Code Challenge. The primary objective of this exercise is to create a data model for given weather details, ingest data into a dataabase and demonstrate some priliminary statistics for the same using a simple Rest API.



## Table of Contents

- [Experimental Setup](#Experimental-Setup)
- [Data Model](#Data-Model)
- [Data Ingestion](#Data-Ingestion)
- [Data Analysis](#Data-Analysis)
- [API Server](#API-Server)
- [Deployment](#Deployment)




## Experimental Setup


### Files Structure

- `wx_data/*`: Weather Dataset from 1985-01-01 to 2014-12-31. Each file corresponds to a particular weather station from Nebraska, Iowa, Illinois, Indiana, or Ohio.

- `src/data_model.py`: Python script for all the data loading and preprocessing routines.
- `src/data_ingestion.py`: Python script for training process orchestration.
- `src/data_analysis.py`: Python script to define model architectures.
- `src/api_server.py`: Python script where the API server is implemented.
- `requirements.txt`: Listing of Python requirements

### Usage
1. Create a virtual environment to install all required dependencies: `python -m venv venv`
2. Activate the virtual environment: `source venv/bin/activate`
3. Make sure you are in the directory where this README is located.
4. Install dependencies: `pip install -r requirements.txt`
5. Run the driver script, `python main.py`. This will initiate data ingestion, analysis and finally start the API server.
6. Once the API server is running you should be able to access the Swagger documentation at `http://localhost:8000/swagger`



## Data Model

- Data Model for the ORM may be found in src/data_model.py. 
- There are primarily two tables maintained here, namely, WeatherData and WeatherStats. WeatherData stores data for all the stations, with unique combination of station and date. WeatherStats store required statistics from the weather data. 
- All the corresponding model and attribute definitions can be found in [data_model.py](https://github.com/vaidya-shreyas/code-challenge-template/blob/main/src/data_model.py).

## Data Ingestion
- Data ingestion pipeline ensures that only new records are inserted and existing records are updated.
- Missing data (with values -9999) is inserted with null values.
- Timestamps for creation and updates are maintained for future reference.
- The script will indicate the number of records inserted per input file. If the records already exist in the database, the script will indicate that zero records were inserted.
- Data ingestion script to populate the weather data from files to models can be found in [data_ingestion.py](https://github.com/vaidya-shreyas/code-challenge-template/blob/main/src/data_ingestion.py).


## Data Analysis
- Data Statistics will be stored in WeatherStats table with average min and max temperatures and total precipitation for given year and staion.
- Unit conversions for these are handled while calculating statistics. For example, average maximum temperature is in degrees Celsius, converted from max_temperature in WeatherData that is in tenths of a degree Celsius. Similar conversions for average minimum temperature and precipitation are implementated.
- If ingested data gets updated for a station for given year, for which the statistics are computed previously, they will be updated accordingly in WeatherStats.
- It is assumed that station id is populated from filename and hence will never be empty.
- Data analysis script can be found in [data_analysis.py](https://github.com/vaidya-shreyas/code-challenge-template/blob/main/src/data_analysis.py).


## API Server
- The API server provides three API endpoints. All endpoints return pages containing maximum 50 records.
1. The first one allows the user to query weather data in a paginated manner. The path is `/api/weather`. The query parameters for the GET API call are `date`, `station` and `page`. `date` is expected in "YYYYMMDD" format. `page` is the requested page number. If a page number beyond the total number of pages for the query is requested the response contains no records. The response also returns the total number of pages for the query. None of the query paramters are required.
2. The path for the second one is `/api/weather/stats`. This API allows querying weather statistics. The query parameters for the GET API call are `year`, `station` and `page`. The "year" and "station" params specify the query and "page" specifies the requested page.
3. The third API at `/api/swagger` serves the Swagger documentation page. You can experiment with the API directly from that page.

- Sample request and response:
```
http://localhost:8000/api/weather?date=19850112&station=USC00257715&page=1

{
  "pages": 1,
  "records": [
    {
      "date": "1985-01-12",
      "max_temperature": "-61.0",
      "min_temperature": "-239.0",
      "precipitation": "0.0",
      "station": "USC00257715"
    }
  ]
}


http://localhost:8000/api/weather/stats?year=1985&station=USC00257715&page=1

{
  "pages": 1,
  "records": [
    {
      "avg_max_temperature": "15.8",
      "avg_min_temperature": "4.3",
      "station": "USC00257715",
      "total_precipiation": "70.6",
      "year": 1985
    }
  ]
}
```

## Deployment
Following process can be implemented to deploy given pipeline on AWS.

- Raw data can be hosted on Amazon S3, in partitioned buckets for every year.
- This service can be deployed on two Amazon EC2 instances, one serving as the database, and the other as the application.
- Create AWS Glue or cron jobs for data ingestion. Same can be scheduled to be triggered at desired frequency.
- Create a CI/CD pipeline using Jenkins for continuous deployment.
- PostgreSQL can be used as database along with Amazon RDS
- To keep an eye on the application logs, we can configure Cloudwatch alerts.
- Docker and Amazon EKS can be use for deployment and containerisation. 


## End Notes

[Back to Top](#Code-Challenge-Template)