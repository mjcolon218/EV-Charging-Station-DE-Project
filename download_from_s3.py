import boto3

# Initialize the S3 client
s3_client = boto3.client('s3', region_name='us-east-1')

# Define your bucket and file names
bucket_name = 'ev-charging-station-bucket'
file_name = 'ev_charging_data.csv'
local_file_path = 'data/'+file_name

# Download the file from S3
try:
    s3_client.download_file(bucket_name, file_name, local_file_path)
    print(f"Downloaded {file_name} from S3 bucket {bucket_name}.")
except Exception as e:
    print(f"Error downloading file from S3: {e}")
