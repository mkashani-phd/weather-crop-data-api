# Weather and Crop Yield Data Analysis Application

This document provides a comprehensive guide to using the application, including setup, running the components, and interacting with the API using `curl`.

---

## **Getting Started**

### **1. Prerequisites**
Ensure the following are installed on your system:
- Python 3
- Required Python libraries (`psycopg2`, `pandas`, `flask`, `flask-restx`)
- PostgreSQL database server

### **2. Initial Setup**
1. Start your PostgreSQL database server.
2. Ensure that the database credentials in the Python scripts (`digest.py`, `analyze.py`, and `app.py`) match your PostgreSQL setup.

---

## **Running the Application**

### **Step 1: Data Ingestion**
Run the `digest.py` script to ingest weather and crop yield data into the database:
```bash
python3 digest.py
```

**Description**: 
- Reads raw weather data from text files and inserts it into the `weather` table.
- Reads crop yield data and inserts it into the `yield` table.
- Ensures no duplicate entries during ingestion.

---

### **Step 2: Data Analysis**
Run the `analyze.py` script to calculate yearly statistics and store them in the `weather_stats` table:
```bash
python3 analyze.py
```

**Description**:
- Aggregates weather data by year.
- Calculates:
  - Average maximum temperature (in degrees Celsius).
  - Average minimum temperature (in degrees Celsius).
  - Total precipitation (in centimeters).
- Stores the results in the `weather_stats` table.

---

### **Step 3: Start the Flask API**
Run the `app.py` script to start the Flask server:
```bash
python3 app.py
```

**Description**:
- Launches a RESTful API to query weather and crop yield data.
- Provides endpoints for raw weather data and precomputed statistics.

---

## **Using the API**

### **Base URL**
The API runs at: `http://127.0.0.1:5000`

### **Endpoints**

#### **1. Get Raw Weather Data**
```bash
curl "http://127.0.0.1:5000/api/weather"
```

**Optional Query Parameters**:
- `date`: Filter by a specific date (e.g., `19850101`).
- `station_id`: Filter by a specific weather station ID (if applicable).

**Example**:
```bash
curl "http://127.0.0.1:5000/api/weather?date=19850101"
```

---

#### **2. Get Weather Statistics**
```bash
curl "http://127.0.0.1:5000/api/weather/stats"
```

**Optional Query Parameters**:
- `year`: Filter by a specific year (e.g., `1985`).

**Example**:
```bash
curl "http://127.0.0.1:5000/api/weather/stats?year=1985"
```

**Response Format**:
The response is a JSON object with the following structure:
```json
[
    {
        "year": 1985,
        "avg_max_temp": 20.5,
        "avg_min_temp": 5.3,
        "total_precipitation": 12.8
    },
    
]
```

---

#### **3. Access Swagger Documentation**
```bash
curl "http://127.0.0.1:5000/api/docs"
```

**Description**:
Provides automatic documentation of the API, including details about endpoints, query parameters, and response structures.

---

## **Troubleshooting**
1. **Unable to Connect to the Database**:
   - Verify PostgreSQL is running and the database credentials are correct.
   - Ensure the tables `weather`, `yield`, and `weather_stats` exist in the database.

2. **Flask Server Not Accessible**:
   - Ensure `app.py` is running.
   - Confirm the API is bound to `0.0.0.0` or `127.0.0.1`.

3. **Curl Command Fails**:
   - Verify the Flask server URL and endpoint paths.
   - Check if the database contains the required data.

---

## **Summary Workflow**
1. Ingest data:
   ```bash
   python3 digest.py
   ```
2. Analyze data:
   ```bash
   python3 analyze.py
   ```
3. Start the API:
   ```bash
   python3 app.py
   ```
4. Query data:
   ```bash
   curl "http://127.0.0.1:5000/api/weather/stats?year=1985"
   ```

This completes the setup and usage of the Weather and Crop Yield Data Analysis application.



# Problem 1 - Data Modeling

This document explains the database schema designed for **Problem 1**, which involves modeling weather and crop yield data for ingestion and storage.

---

## **1. Weather Data Table: `weather`**

The `weather` table stores raw weather data records from the provided text files.

### **Schema**
| Column Name     | Data Type | Description                                             |
|------------------|-----------|---------------------------------------------------------|
| `id`            | SERIAL    | Primary key, auto-incremented unique identifier.        |
| `date`          | TEXT      | Date in `YYYYMMDD` format (e.g., `19850101`).           |
| `max_temp`      | INTEGER   | Maximum temperature for the day (tenths of a degree Celsius). |
| `min_temp`      | INTEGER   | Minimum temperature for the day (tenths of a degree Celsius). |
| `precipitation` | INTEGER   | Precipitation for the day (tenths of a millimeter).     |

### **Notes**
- **Units**:
  - Maximum and minimum temperatures are stored in tenths of a degree Celsius.
  - Precipitation is stored in tenths of a millimeter.
- **Missing Data**:
  - Missing values are represented by `-9999`.

---

## **2. Crop Yield Data Table: `yield`**

The `yield` table stores annual crop yield data, specifically for corn grain production.

### **Schema**
| Column Name  | Data Type | Description                                       |
|--------------|-----------|---------------------------------------------------|
| `id`         | SERIAL    | Primary key, auto-incremented unique identifier.  |
| `year`       | INTEGER   | Year of the data (e.g., `1985`).                  |
| `production` | INTEGER   | Crop yield production for that year (units vary). |

### **Notes**
- This table links crop yield data to specific years for analysis alongside weather data.

---

## **Rationale for Design**

1. **Normalization**:
   - Each table represents a single type of data (`weather` or `yield`), simplifying relationships and queries.
2. **Flexibility**:
   - The schema allows efficient querying of weather and crop yield data for analysis and integration.
3. **Handling Missing Data**:
   - Missing weather data values are stored as `-9999` to ensure consistency with the raw data.
4. **Scalability**:
   - The schema is extensible to include additional metadata, such as station IDs or crop types, in future use cases.

---

## **Sample Data**
### **Weather Table:**
| `id` | `date`     | `max_temp` | `min_temp` | `precipitation` |
|------|------------|------------|------------|------------------|
| 1    | 19850101   | 200        | 50         | 12              |
| 2    | 19850102   | -9999      | -100       | 5               |

### **Yield Table:**
| `id` | `year` | `production` |
|------|--------|--------------|
| 1    | 1985   | 7000         |
| 2    | 1986   | 7200         |

---

## **Advantages**
- **Ease of Querying**: Simple and intuitive schema for joining weather and crop yield data.
- **Analysis Ready**: Prepares the data for aggregation and statistical analysis in subsequent steps.
- **Data Integrity**: Use of primary keys ensures unique records and prevents duplication.

--- 

This schema provides the foundation for efficient ingestion, storage, and querying of weather and crop yield data.


# Problem 3 - Data Analysis Tables

This document explains the database tables used in **Problem 3** to calculate and store yearly weather statistics.

## 1. Weather Data Table: `weather`

This table stores the raw weather data ingested from the files provided. It serves as the input for calculating statistics.

### Schema:
| Column Name     | Data Type | Description                                             |
|------------------|-----------|---------------------------------------------------------|
| `id`            | SERIAL    | Primary key.                                            |
| `date`          | TEXT      | Date in `YYYYMMDD` format.                              |
| `max_temp`      | INTEGER   | Maximum temperature for the day (tenths of a degree Celsius). |
| `min_temp`      | INTEGER   | Minimum temperature for the day (tenths of a degree Celsius). |
| `precipitation` | INTEGER   | Precipitation for the day (tenths of a millimeter).     |

### Notes:
- Missing values are indicated by `-9999`.
- This table contains data for multiple weather stations over a period of years.

---

## 2. Weather Statistics Table: `weather_stats`

This table stores the aggregated yearly statistics calculated from the `weather` table. It is designed to allow efficient querying and analysis of yearly weather trends.

### Schema:
| Column Name          | Data Type | Description                                                       |
|-----------------------|-----------|-------------------------------------------------------------------|
| `id`                 | SERIAL    | Primary key.                                                     |
| `station_id`         | TEXT      | Identifier for the weather station (optional for future use).    |
| `year`               | INTEGER   | The year for which the statistics are calculated.                |
| `avg_max_temp`       | FLOAT     | Average maximum temperature for the year (degrees Celsius).      |
| `avg_min_temp`       | FLOAT     | Average minimum temperature for the year (degrees Celsius).      |
| `total_precipitation`| FLOAT     | Total precipitation for the year (centimeters).                  |

### Notes:
- **Station ID**: Not used in the current implementation but included for scalability if data per station is needed.
- **Temperature Conversion**:
  - Max/Min temperatures are converted from tenths of degrees Celsius to degrees Celsius.
- **Precipitation Conversion**:
  - Precipitation is converted from tenths of a millimeter to centimeters.
- **Handling Missing Data**:
  - Missing values (`-9999`) are excluded from calculations.
- **Null Values**:
  - If no valid data exists for a statistic in a given year, the corresponding column is set to `NULL`.

---

## Data Flow Summary

1. **Input**: Raw weather data is stored in the `weather` table.
2. **Processing**: Yearly statistics (average max/min temperature, total precipitation) are calculated by grouping data by year.
3. **Output**: Results are stored in the `weather_stats` table for efficient analysis and API queries.

---

## Benefits of `weather_stats` Table

- **Simplified Queries**: Precomputed yearly statistics make it easier to serve API requests without recalculating values repeatedly.
- **Scalability**: Allows future enhancements, such as adding `station_id` for station-specific statistics.
- **Improved Performance**: Reduces computational overhead for frequent queries by precomputing statistics.

