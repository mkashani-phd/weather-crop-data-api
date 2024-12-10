import os, time
import psycopg2
import pandas as pd

USER='moh'
PASSWORD='123456'

def create_database():
    """Create PostgreSQL database and tables."""
    conn = psycopg2.connect(
        database="postgres",
        user= USER,
        password=PASSWORD,
        host='127.0.0.1',
        port='5432'
    )
    cursor = conn.cursor()

    # Create Weather Data Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather (
            id SERIAL PRIMARY KEY,
            date TEXT NOT NULL,
            max_temp INTEGER,
            min_temp INTEGER,
            precipitation INTEGER
        )
    ''')

    # Create Yield Data Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS yield (
            id SERIAL PRIMARY KEY,
            year INTEGER NOT NULL,
            production INTEGER NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def ingest_weather_data(folder_path):
    """Ingest weather data into the database."""
    conn = psycopg2.connect(
        database="postgres",
        user= USER,
        password= PASSWORD,
        host='127.0.0.1',
        port='5432'
    )
    cursor = conn.cursor()

    # folder_path = os.path.join(os.path.dirname(__file__), folder_path)  # Adjust for relative path

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                for line in file:
                    data = line.strip().split()
                    if len(data) == 4:  # Ensure the correct number of columns
                        date, max_temp, min_temp, precipitation = data
                        cursor.execute('''
                            INSERT INTO weather (date, max_temp, min_temp, precipitation)
                            VALUES (%s, %s, %s, %s)
                        ''', (date, int(max_temp), int(min_temp), int(precipitation)))

    conn.commit()
    conn.close()
def ingest_yield_data(file_path):
    """Ingest yield data into the database."""
    conn = psycopg2.connect(
        database="postgres",
        user= USER,
        password= PASSWORD,
        host='127.0.0.1',
        port='5432'
    )
    cursor = conn.cursor()

    # file_path = os.path.join(os.path.dirname(__file__), file_path)  # Adjust for relative path

    with open(file_path, 'r') as file:
        for line in file:
            data = line.strip().split()
            if len(data) == 2:  # Ensure the correct number of columns
                year, production = data
                cursor.execute('''
                    INSERT INTO yield (year, production)
                    VALUES (%s, %s)
                ''', (int(year), int(production)))

    conn.commit()
    conn.close()

def main():
    # Paths to the data folders
    weather_folder = "wx_data"
    yield_file = "yld_data/US_corn_grain_yield.txt"  # Example file name

    # Create the database and tables
    create_database()

    # Ingest data
    ingest_weather_data(weather_folder)
    ingest_yield_data(yield_file)

    print("Data ingestion complete.")

if __name__ == "__main__":
    start = time.time()
    main()
    time_took = time.time() - start
    print("The time took to digest the data:", time_took)