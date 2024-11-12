import psycopg2
import pandas as pd
import config

# Database connection details
rds_endpoint = config.RDS_ENDPOINT
db_name = config.DB_NAME
username = config.DB_USER
password = config.DB_PASSWORD
port = config.DB_PORT

# Connect to PostgreSQL
try:
    conn = psycopg2.connect(
        host=rds_endpoint,
        database=db_name,
        user=username,
        password=password,
        port=port
    )
    cursor = conn.cursor()
    print("Connected to PostgreSQL successfully.")

    # Query to check the data
    query = """
    SELECT id, station_name, city, state, latitude, longitude, open_date, date_last_confirmed, updated_at
    FROM ev_charging_stations
    LIMIT 10;
    """
    cursor.execute(query)

    # Fetch the data and display it
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['ID', 'Station Name', 'City', 'State', 'Latitude', 'Longitude', 'Open Date', 'Date Last Confirmed', 'Updated At'])
    print(df)

    cursor.close()
    conn.close()
except Exception as e:
    print(f"Error querying data from PostgreSQL: {e}")
