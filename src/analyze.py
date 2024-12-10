import psycopg2
import pandas as pd

USER='moh'
PASSWORD='123456'

def create_analysis_table():
    """Create a table to store analysis results."""
    conn = psycopg2.connect(
        database="postgres",
        user=USER,
        password=PASSWORD,
        host='127.0.0.1',
        port='5432'
    )
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather_stats (
            id SERIAL PRIMARY KEY,
            station_id TEXT,
            year INTEGER,
            avg_max_temp FLOAT,
            avg_min_temp FLOAT,
            total_precipitation FLOAT
        )
    ''')

    conn.commit()
    conn.close()

def calculate_statistics():
    """Calculate yearly weather statistics and store them in the database."""
    conn = psycopg2.connect(
        database="postgres",
        user=USER,
        password=PASSWORD,
        host='127.0.0.1',
        port='5432'
    )
    cursor = conn.cursor()

    # Retrieve weather data
    query = '''
        SELECT date, max_temp, min_temp, precipitation
        FROM weather
    '''
    cursor.execute(query)
    rows = cursor.fetchall()

    # Convert to pandas DataFrame
    df = pd.DataFrame(rows, columns=['date', 'max_temp', 'min_temp', 'precipitation'])

    # Extract year and station_id from date (assuming station_id is part of data)
    df['year'] = df['date'].str[:4].astype(int)
    df['max_temp'] = df['max_temp'].replace(-9999, None) / 10  # Convert to Celsius
    df['min_temp'] = df['min_temp'].replace(-9999, None) / 10  # Convert to Celsius
    df['precipitation'] = df['precipitation'].replace(-9999, None) / 100  # Convert to cm

    # Group by year and station_id
    grouped = df.groupby(['year'])

    # Calculate statistics
    stats = grouped.agg(
        avg_max_temp=('max_temp', 'mean'),
        avg_min_temp=('min_temp', 'mean'),
        total_precipitation=('precipitation', 'sum')
    ).reset_index()

    # Insert stats into the database
    for _, row in stats.iterrows():
        cursor.execute('''
            INSERT INTO weather_stats (year, avg_max_temp, avg_min_temp, total_precipitation)
            VALUES (%s, %s, %s, %s)
        ''', (row['year'], row['avg_max_temp'], row['avg_min_temp'], row['total_precipitation']))

    conn.commit()
    conn.close()

def main():
    # Create analysis table
    create_analysis_table()

    # Calculate and store statistics
    calculate_statistics()

    print("Weather statistics calculation and storage complete.")

if __name__ == "__main__":
    main()
