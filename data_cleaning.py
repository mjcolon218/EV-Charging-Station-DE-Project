import pandas as pd

# Load the raw data
file_path = 'data/ev_charging_data.csv'
df = pd.read_csv(file_path)

# Display basic information about the data
print("Initial Data Overview:")
print(df.info())

# **Data Cleaning Steps**

# Drop unnecessary columns, including 'Expected Date'
columns_to_drop = ['Plus4', 'Station Phone', 'Intersection Directions', 'EV Other Info', 'EV Network Web', 'Expected Date']
df.drop(columns=[col for col in columns_to_drop if col in df.columns], inplace=True)

# Handle missing values for numerical columns
df['EV Level1 EVSE Num'] = pd.to_numeric(df['EV Level1 EVSE Num'], errors='coerce').fillna(0).astype(int)
df['EV Level2 EVSE Num'] = pd.to_numeric(df['EV Level2 EVSE Num'], errors='coerce').fillna(0).astype(int)
df['EV DC Fast Count'] = pd.to_numeric(df['EV DC Fast Count'], errors='coerce').fillna(0).astype(int)

# Replace NaN values in text columns with an empty string
text_columns = [
    'Fuel Type Code', 'Station Name', 'Street Address', 'City', 'State', 'ZIP', 'Status Code',
    'Groups With Access Code', 'Access Days Time', 'Cards Accepted', 'EV Network',
    'Geocode Status', 'Owner Type Code', 'Federal Agency ID', 'Federal Agency Name', 'EV Connector Types'
]
df[text_columns] = df[text_columns].fillna('')

# Convert date columns to string format (to handle missing values)
date_columns = ['Date Last Confirmed', 'Updated At', 'Open Date']
for col in date_columns:
    df[col] = pd.to_datetime(df[col], errors='coerce')
    # Convert date columns to string and replace NaT with empty string
    df[col] = df[col].dt.strftime('%Y-%m-%d').fillna('')

# Standardize data types for ZIP, Latitude, and Longitude
df['ZIP'] = df['ZIP'].astype(str)
df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce').fillna(0)
df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce').fillna(0)

# Ensure ID column is an integer type
df['ID'] = pd.to_numeric(df['ID'], errors='coerce').fillna(0).astype(int)

# Display cleaned data information
print("Cleaned Data Overview:")
print(df.info())

# Save the cleaned data to a new CSV file
cleaned_file_path = 'data/cleaned_ev_charging_data.csv'
df.to_csv(cleaned_file_path, index=False)
print(f"Cleaned data saved to {cleaned_file_path}.")
