import psycopg2
import config

# Database connection details
rds_endpoint = config.RDS_ENDPOINT
db_name = config.DB_NAME
username = config.DB_USER
password = config.DB_PASSWORD
port = config.DB_PORT

# Connect to PostgreSQL and get the table schema
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

    # Query to get table schema details
    query = """
    SELECT column_name, data_type, character_maximum_length
    FROM information_schema.columns
    WHERE table_name = 'ev_charging_stations';
    """
    cursor.execute(query)
    schema = cursor.fetchall()

    print("Table Schema for 'ev_charging_stations':")
    for column in schema:
        print(f"Column: {column[0]}, Data Type: {column[1]}, Max Length: {column[2]}")

    cursor.close()
    conn.close()
except Exception as e:
    print(f"Error verifying table schema: {e}")
