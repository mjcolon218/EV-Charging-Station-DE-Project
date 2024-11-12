import pandas as pd
import psycopg2
import config

# Database connection details
rds_endpoint = config.RDS_ENDPOINT
db_name = config.DB_NAME
username = config.DB_USER
password = config.DB_PASSWORD
port = config.DB_PORT

# Load the cleaned data
file_path = 'data/cleaned_ev_charging_data.csv'
df = pd.read_csv(file_path)

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

    # Define the SQL query
    insert_query = """
    INSERT INTO ev_charging_stations (
        id, fuel_type_code, station_name, street_address, city, state, zip_code,
        status_code, groups_with_access_code, access_days_time, cards_accepted,
        ev_level1_evse_num, ev_level2_evse_num, ev_dc_fast_count, ev_network,
        geocode_status, latitude, longitude, date_last_confirmed,
        updated_at, owner_type_code, federal_agency_id, federal_agency_name,
        open_date, ev_connector_types
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (id) DO NOTHING;
    """

    # Initialize counters
    row_count = 0
    skipped_count = 0

    # Iterate through the DataFrame rows and insert the data
    for _, row in df.iterrows():
        # Convert columns to strings and handle NaN values
        text_columns = [
            'Station Name', 'Street Address', 'Federal Agency Name', 'Cards Accepted',
            'EV Network', 'Geocode Status', 'Owner Type Code'
        ]
        for col in text_columns:
            row[col] = str(row[col]) if pd.notnull(row[col]) else ''

        # Debugging: Check the length of text columns
        if (
            len(row['Station Name']) > 200 or
            len(row['Street Address']) > 200 or
            len(row['Federal Agency Name']) > 200 or
            len(row['Cards Accepted']) > 200 or
            len(row['EV Network']) > 200 or
            len(row['Geocode Status']) > 200 or
            len(row['Owner Type Code']) > 50
        ):
            print(f"Skipping row {row['ID']} due to value length exceeding the limit.")
            skipped_count += 1
            continue

        # Prepare the data tuple
        data_tuple = (
            row['ID'], row['Fuel Type Code'], row['Station Name'], row['Street Address'], row['City'], row['State'], row['ZIP'],
            row['Status Code'], row['Groups With Access Code'], row['Access Days Time'], row['Cards Accepted'],
            row['EV Level1 EVSE Num'], row['EV Level2 EVSE Num'], row['EV DC Fast Count'], row['EV Network'],
            row['Geocode Status'], row['Latitude'], row['Longitude'],
            row['Date Last Confirmed'], row['Updated At'], row['Owner Type Code'], row['Federal Agency ID'],
            row['Federal Agency Name'], row['Open Date'], row['EV Connector Types']
        )

        try:
            cursor.execute(insert_query, data_tuple)
            row_count += 1
        except Exception as row_error:
            print(f"Error inserting row {row['ID']}: {row_error}")

    # Commit the transaction and close the connection
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Data loaded successfully. Total rows inserted: {row_count}")
    print(f"Total rows skipped due to length issues: {skipped_count}")

except Exception as e:
    print(f"Error loading data into PostgreSQL: {e}")
