import psycopg2

# Database connection details
rds_endpoint = "ev-db.cpimwkoa8o4d.us-east-2.rds.amazonaws.com"
db_name = "postgres"
username = "mjcolon218"
password = "Bronxnyc86!"
port = "5432"

# SQL query to create the table with updated schema
create_table_query = """
CREATE TABLE IF NOT EXISTS ev_charging_stations (
    id BIGINT PRIMARY KEY,
    fuel_type_code VARCHAR(10),
    station_name VARCHAR(200),
    street_address VARCHAR(200),
    city VARCHAR(50),
    state VARCHAR(10),
    zip_code VARCHAR(10),
    status_code VARCHAR(10),
    groups_with_access_code VARCHAR(200),
    access_days_time VARCHAR(200),
    cards_accepted VARCHAR(200),
    ev_level1_evse_num INT DEFAULT 0,
    ev_level2_evse_num INT DEFAULT 0,
    ev_dc_fast_count INT DEFAULT 0,
    ev_network VARCHAR(200),
    geocode_status VARCHAR(200),
    latitude DECIMAL(10, 6),
    longitude DECIMAL(10, 6),
    date_last_confirmed VARCHAR(20),
    updated_at VARCHAR(20),
    owner_type_code VARCHAR(50),
    federal_agency_id VARCHAR(50),
    federal_agency_name VARCHAR(200),
    open_date VARCHAR(20),
    ev_connector_types VARCHAR(50)
);
"""

# Connect to PostgreSQL and create the table
try:
    conn = psycopg2.connect(
        host=rds_endpoint,
        database=db_name,
        user=username,
        password=password,
        port=port
    )
    cursor = conn.cursor()
    cursor.execute(create_table_query)
    conn.commit()
    print("Table 'ev_charging_stations' created or updated successfully.")

    cursor.close()
    conn.close()
except Exception as e:
    print(f"Error creating table: {e}")
