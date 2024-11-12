import psycopg2
import config

# Database connection details
rds_endpoint = config.RDS_ENDPOINT
db_name = config.DB_NAME
username = config.DB_USER
password = config.DB_PASSWORD
port = config.DB_PORT
# SQL query to drop the table if it exists
drop_table_query = "DROP TABLE IF EXISTS ev_charging_stations;"

# Connect to PostgreSQL and drop the table
try:
    conn = psycopg2.connect(
        host=rds_endpoint,
        database=db_name,
        user=username,
        password=password,
        port=port
    )
    cursor = conn.cursor()
    cursor.execute(drop_table_query)
    conn.commit()
    print("Table 'ev_charging_stations' dropped successfully.")

    cursor.close()
    conn.close()
except Exception as e:
    print(f"Error dropping table: {e}")
