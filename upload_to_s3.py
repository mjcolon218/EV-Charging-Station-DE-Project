import boto3

s3_client = boto3.client('s3')
s3_client.upload_file(
    'data\Electric_Vehicle_Charging_Stations_in_New_York_20241029.csv',
    'ev-charging-station-bucket',
    'ev_charging_data.csv'
)

print("Data uploaded to S3 successfully.")
