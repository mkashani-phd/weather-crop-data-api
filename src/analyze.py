import psycopg2

def create_analysis_table():
    """Create a table to store analysis results."""
    conn = psycopg2.connect(
        database="postgres",
        user='moh',
        password='123456',
        host='127.0.0.1',
        port='5432'
    )
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather_stats (
            id SERIAL PRIMARY KEY,
            year INTEGER NOT NULL,
            avg_max_temp FLOAT,
            avg_min_temp FLOAT,
            total_precipitation FLOAT
        )
    ''')

    conn.commit()
    conn.close()

def calculate_statistics_in_db():
    """Perform aggregation in the database and insert results into the weather_stats table."""
    conn = psycopg2.connect(
        database="postgres",
        user='moh',
        password='123456',
        host='127.0.0.1',
        port='5432'
    )
    cursor = conn.cursor()

    # SQL query to calculate yearly statistics
    query = '''
        INSERT INTO weather_stats (year, avg_max_temp, avg_min_temp, total_precipitation)
        SELECT
            EXTRACT(YEAR FROM TO_DATE(date, 'YYYYMMDD')) AS year,
            AVG(NULLIF(max_temp, -9999)) / 10 AS avg_max_temp,  -- Convert to Celsius
            AVG(NULLIF(min_temp, -9999)) / 10 AS avg_min_temp,  -- Convert to Celsius
            SUM(NULLIF(precipitation, -9999)) / 100 AS total_precipitation  -- Convert to cm
        FROM weather
        GROUP BY year
        ORDER BY year;
    '''

    cursor.execute(query)
    conn.commit()
    conn.close()

def main():
    # Step 1: Create the analysis table if it doesn't exist
    create_analysis_table()

    # Step 2: Perform the calculations in the database
    calculate_statistics_in_db()

    print("Yearly weather statistics have been calculated and stored in the database.")

if __name__ == "__main__":
    main()
