import psycopg2
import config


# Database connection details
rds_endpoint = config.RDS_ENDPOINT
db_name = config.DB_NAME
username = config.DB_USER
password = config.DB_PASSWORD
port = config.DB_PORT

# Verify the table
try:
    conn = psycopg2.connect(
        host=rds_endpoint,
        database=db_name,
        user=username,
        password=password,
        port=port
    )
    cursor = conn.cursor()
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    tables = cursor.fetchall()
    print("Tables in the database:")
    for table in tables:
        print(f"- {table[0]}")

    cursor.close()
    conn.close()
except Exception as e:
    print(f"Error verifying table: {e}")
