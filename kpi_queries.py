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

    # KPI 1: Total Number of Charging Stations
    query_1 = "SELECT COUNT(*) AS total_stations FROM ev_charging_stations;"
    cursor.execute(query_1)
    total_stations = cursor.fetchone()[0]
    print(f"Total Number of Charging Stations: {total_stations}")

    # KPI 2: Total Number of Chargers (Level 1, Level 2, DC Fast)
    query_2 = """
    SELECT 
        SUM(ev_level1_evse_num) AS total_level1_chargers,
        SUM(ev_level2_evse_num) AS total_level2_chargers,
        SUM(ev_dc_fast_count) AS total_dc_fast_chargers
    FROM ev_charging_stations;
    """
    cursor.execute(query_2)
    chargers = cursor.fetchone()
    print(f"Total Level 1 Chargers: {chargers[0]}")
    print(f"Total Level 2 Chargers: {chargers[1]}")
    print(f"Total DC Fast Chargers: {chargers[2]}")

    # KPI 3: Average Number of Chargers per Station
    query_3 = """
    SELECT 
        AVG(ev_level1_evse_num) AS avg_level1_chargers,
        AVG(ev_level2_evse_num) AS avg_level2_chargers,
        AVG(ev_dc_fast_count) AS avg_dc_fast_chargers
    FROM ev_charging_stations;
    """
    cursor.execute(query_3)
    averages = cursor.fetchone()
    print(f"Average Level 1 Chargers per Station: {averages[0]:.2f}")
    print(f"Average Level 2 Chargers per Station: {averages[1]:.2f}")
    print(f"Average DC Fast Chargers per Station: {averages[2]:.2f}")

    # KPI 4: Top 5 Cities by Number of Charging Stations
    query_4 = """
    SELECT city, COUNT(*) AS station_count
    FROM ev_charging_stations
    GROUP BY city
    ORDER BY station_count DESC
    LIMIT 5;
    """
    cursor.execute(query_4)
    top_cities = cursor.fetchall()
    print("Top 5 Cities by Number of Charging Stations:")
    for city, count in top_cities:
        print(f"{city}: {count} stations")

    # KPI 5: State with the Highest Number of Stations
    query_5 = """
    SELECT state, COUNT(*) AS station_count
    FROM ev_charging_stations
    GROUP BY state
    ORDER BY station_count DESC
    LIMIT 1;
    """
    cursor.execute(query_5)
    top_state = cursor.fetchone()
    print(f"State with the Highest Number of Stations: {top_state[0]} ({top_state[1]} stations)")

    # KPI 6: Charger Type Distribution (Level 1, Level 2, DC Fast Count)
    query_6 = """
    SELECT
        SUM(ev_level1_evse_num) AS total_level1,
        SUM(ev_level2_evse_num) AS total_level2,
        SUM(ev_dc_fast_count) AS total_dc_fast
    FROM ev_charging_stations;
    """
    cursor.execute(query_6)
    distribution = cursor.fetchone()
    total_chargers = sum(distribution)
    level1_percentage = (distribution[0] / total_chargers) * 100 if total_chargers > 0 else 0
    level2_percentage = (distribution[1] / total_chargers) * 100 if total_chargers > 0 else 0
    dc_fast_percentage = (distribution[2] / total_chargers) * 100 if total_chargers > 0 else 0

    print(f"Charger Type Distribution:")
    print(f"Level 1: {level1_percentage:.2f}%")
    print(f"Level 2: {level2_percentage:.2f}%")
    print(f"DC Fast: {dc_fast_percentage:.2f}%")

    # Close the connection
    cursor.close()
    conn.close()
    print("Disconnected from PostgreSQL.")

except Exception as e:
    print(f"Error executing queries: {e}")
