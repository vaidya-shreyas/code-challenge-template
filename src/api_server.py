from datetime import datetime
import json
from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_restful import Resource, Api
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

from data_model import WeatherData, WeatherStats

engine = create_engine('sqlite:///csv_test.db', echo=True)
RECORDS_PER_PAGE=50

#Create the session
session = sessionmaker()
session.configure(bind=engine)
s = session()

app = Flask("API Server")
api = Api(app)

def paginate(q, page=1, records_per_page=RECORDS_PER_PAGE):
    result = {}
    total = (q.count() // records_per_page) + 1
    result["total"] = total
    if page <= total:
        result["items"] = q.all()[(page-1)*records_per_page:page*records_per_page]
    else:
        result["items"] = []
    return result


def query_and_paginate(request, database_model, filter, response):

    page = int(request.args.get("page", 1))
    q = s.query(database_model).filter_by(**filter)
    paginated_result = paginate(q, page, RECORDS_PER_PAGE)
    if not paginated_result["total"]:
        return response
    for row in paginated_result["items"]:
        response["records"] += [row.to_dict()]

    response["pages"] = paginated_result["total"]



@app.route("/api/weather")
def weather():
    response = {"records":[]}
    filter = {}
    if "date" in request.args:
        date = datetime.strptime(request.args["date"],"%Y%m%d").date()
        filter["date"] = date
    if "station" in request.args:
        filter["station"] = request.args["station"]
    

    query_and_paginate(request, WeatherData, filter, response)

    return response

@app.route("/api/weather/stats")
def weather_stats():
    response = {"records":[]}
    filter = {}
    if "year" in request.args:
        filter["year"] = request.args["year"]
    if "station" in request.args:
        filter["station"] = request.args["station"]

    query_and_paginate(request, WeatherStats, filter, response)
    

    return response


SWAGGER_URL = '/swagger'
API_URL = 'http://localhost:8000/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Weather data and stats and APIs"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/swagger.json')
def swagger():
    with open('weather_api.json', 'r') as f:
        return jsonify(json.load(f))


def start_server():
    CORS(app)
    app.run(host="0.0.0.0", port=8000)

if __name__ == "__main__":
    start_server()
