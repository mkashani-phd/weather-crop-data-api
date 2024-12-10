from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
import psycopg2
from psycopg2.extras import RealDictCursor

# Initialize Flask app and Flask-RESTX API
app = Flask(__name__)
api = Api(app, version="1.0", title="Weather API", description="A RESTful API for Weather Data and Statistics")

# Database connection settings
DB_CONFIG = {
    "database": "postgres",
    "user": "moh",
    "password": "123456",
    "host": "127.0.0.1",
    "port": "5432"
}

# API models for documentation
weather_model = api.model("Weather", {
    "date": fields.String(required=True, description="Date in YYYYMMDD format"),
    "max_temp": fields.Float(description="Maximum temperature in Celsius"),
    "min_temp": fields.Float(description="Minimum temperature in Celsius"),
    "precipitation": fields.Float(description="Precipitation in cm")
})

stats_model = api.model("WeatherStats", {
    "year": fields.Integer(required=True, description="Year of the statistics"),
    "avg_max_temp": fields.Float(description="Average maximum temperature in Celsius"),
    "avg_min_temp": fields.Float(description="Average minimum temperature in Celsius"),
    "total_precipitation": fields.Float(description="Total precipitation in cm")
})

# Utility function to query the database
def query_db(query, params=None):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(query, params or [])
    results = cursor.fetchall()
    conn.close()
    return results

# Weather data endpoint
@api.route('/api/weather')
class WeatherResource(Resource):
    @api.doc(params={"date": "Filter by date (YYYYMMDD)", "station_id": "Filter by station ID"})
    @api.marshal_list_with(weather_model)
    def get(self):
        """Fetch weather data with optional filters"""
        date = request.args.get("date")
        station_id = request.args.get("station_id")

        query = "SELECT * FROM weather WHERE 1=1"
        params = []

        if date:
            query += " AND date = %s"
            params.append(date)
        if station_id:
            query += " AND station_id = %s"
            params.append(station_id)

        data = query_db(query, params)
        return data, 200

# Weather statistics endpoint
@api.route('/api/weather/stats')
class WeatherStatsResource(Resource):
    @api.doc(params={"year": "Filter by year"})
    @api.marshal_list_with(stats_model)
    def get(self):
        """Fetch weather statistics with optional filters"""
        year = request.args.get("year")

        query = "SELECT * FROM weather_stats WHERE 1=1"
        params = []

        if year:
            query += " AND year = %s"
            params.append(year)

        data = query_db(query, params)
        return data, 200

# Swagger documentation endpoint
@api.route('/api/docs')
class SwaggerDocs(Resource):
    def get(self):
        """Provides automatic Swagger/OpenAPI documentation"""
        return jsonify(api.__schema__)

# Main entry point
if __name__ == "__main__":
    app.run(host = "0.0.0.0" , port= 5000, debug=True)
