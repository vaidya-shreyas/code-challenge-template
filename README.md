# Code-Challenge-Template

This repository is developed in response to the Corteva Code Challenge. The primary objective of this exercise is to create a data model for given weather details, ingest data into a dataabase and demonstrate some priliminary statistics for the same using a simple Rest API.



## Table of Contents

- [Experimental Setup](#Experimental-Setup)
- [Data Model](#Data-Model)
- [Data Ingestion](#Data-Ingestion)
- [Data Analysis](#Data-Analysis)
- [API](#API)
- [Deployment](#Deployment)




## Experimental Setup


### Files Structure

- `wx_data/*`: Weather Dataset from 1985-01-01 to 2014-12-31. Each file corresponds to a particular weather station from Nebraska, Iowa, Illinois, Indiana, or Ohio.

- `src/data_model.py`: Python script for all the data loading and preprocessing routines.
- `src/data_ingestion.py`: Python script for training process orchestration.
- `src/data_analysis.py`: Python script to define model architectures.
- `requirements.txt`: Listing of Python requirements

### Usage

> *Execute run.sh on terminal as follows : bash run.sh*

Please note that the current version is tested on Twitter dataset with results attached. Provisional design and setup implemented for Wikipedia Dataset


## Data Model

- Data Model for the ORM may be found in src/data_model.py. 
- There are primarily two tables maintained here, namely, WeatherData and WeatherStats. WeatherData stores data for all the stations, with unique combination of station and date. WeatherStats store required statistics from the weather data. 
- All the corresponding model and attribute definitions can be found in [data_model.py](https://github.com/vaidya-shreyas/code-challenge-template/blob/main/src/data_model.py).

## Data Ingestion
- Data ingestion pipeline ensures that only new records are inserted and existing records are updated.
- Missing data (with values -9999) is inserted with null values.
- Timestamps for creation and updates are maintained for future reference.
- Data ingestion script to populate the weather data from files to models can be found in [data_ingestion.py](https://github.com/vaidya-shreyas/code-challenge-template/blob/main/src/data_ingestion.py).


## Data Analysis
- Data Statistics will be stored in WeatherStats table with average min and max temperatures and total precipitation for given year and staion.
- Unit conversions for these are handled while calculating statistics. For example, average maximum temperature is in degrees Celsius, converted from max_temperature in WeatherData that is in tenths of a degree Celsius. Similar conversions for average minimum temperature and precipitation are implementated.
- If ingested data gets updated for a station for given year, for which the statistics are computed previously, they will be updated accordingly in WeatherStats.
- It is assumed that station id is populated from filename and hence will never be empty.

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

Feel free to discuss your experiences on the [discussion page](https://github.com/vaidya-shreyas/Code-Challenge-Template/discussions).

[Back to Top](#Code-Challenge-Template)