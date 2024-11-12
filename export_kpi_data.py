import pandas as pd
import psycopg2
import psycopg2
import config


# Database connection details
rds_endpoint = config.RDS_ENDPOINT
db_name = config.DB_NAME
username = config.DB_USER
password = config.DB_PASSWORD
port = config.DB_PORT

# File path for the exported CSV
output_csv_path = 'data/kpi_ev_charging_data.csv'

# Connect to PostgreSQL and export data
try:
    # Establish the connection
    conn = psycopg2.connect(
        host=rds_endpoint,
        database=db_name,
        user=username,
        password=password,
        port=port
    )
    cursor = conn.cursor()
    print("Connected to PostgreSQL successfully.")

    # SQL query to extract relevant columns for KPI analysis
    query = """
    SELECT
        id, station_name, city, state,
        ev_level1_evse_num, ev_level2_evse_num, ev_dc_fast_count,
        latitude, longitude
    FROM ev_charging_stations;
    """

    # Execute the query and load the result into a pandas DataFrame
    df = pd.read_sql(query, conn)

    # Save the DataFrame to a local CSV file
    df.to_csv(output_csv_path, index=False)
    print(f"Data exported to '{output_csv_path}' successfully.")

    # Close the connection
    cursor.close()
    conn.close()
    print("Disconnected from PostgreSQL.")

except Exception as e:
    print(f"Error exporting data: {e}")
