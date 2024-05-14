import re
from datetime import datetime
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np
import ipaddress
import joblib

# Sample log data (replace this with the actual log data)
log_data = """
2024-05-13 22:26:41,359 - INFO - Successfully connected to the Ethereum node.
2024-05-13 22:26:42,869 - INFO - Successfully connected to the Ethereum node.
2024-05-13 22:26:44,826 - DEBUG - {"source_ip": "127.0.0.1", "destination_ip": "127.0.0.1:5000", "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36", "endpoint": "index", "method": "GET", "user": "Anonymous"}
2024-05-13 22:26:44,885 - DEBUG - {"source_ip": "127.0.0.1", "destination_ip": "127.0.0.1:5000", "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36", "endpoint": "static", "method": "GET", "user": "Anonymous"}
2024-05-13 22:26:46,831 - DEBUG - {"source_ip": "127.0.0.1", "destination_ip": "127.0.0.1:5000", "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36", "endpoint": "login", "method": "GET", "user": "Anonymous"}
2024-05-13 22:26:46,842 - DEBUG - {"source_ip": "127.0.0.1", "destination_ip": "127.0.0.1:5000", "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36", "endpoint": "static", "method": "GET", "user": "Anonymous"}
2024-05-13 22:26:46,843 - DEBUG - {"source_ip": "127.0.0.1", "destination_ip": "127.0.0.1:5000", "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36", "endpoint": "static", "method": "GET", "user": "Anonymous"}
2024-05-13 22:26:50,195 - DEBUG - {"data": {"address": "0x454aa5a1c2342c903fbdb885423fb3c7ff73d8a8", "signature": "0xa6c1b58b21989a3b4d53f15fd6809d93c6aba24724c549507d1fbfad2f3511a63413186d5683821035a3c982ebc3443a210cc575cef3c301d30b6389ac5edf871c", "message": "Please sign this message to confirm your identity."}, "source_ip": "127.0.0.1", "destination_ip": "127.0.0.1:5000", "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36", "endpoint": "login", "method": "POST", "user": "Anonymous"}
2024-05-13 22:26:50,217 - INFO - User 0x454aa5a1c2342c903fbdb885423fb3c7ff73d8a8 logged in successfully.
2024-05-13 22:26:50,223 - DEBUG - {"source_ip": "127.0.0.1", "destination_ip": "127.0.0.1:5000", "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36", "endpoint": "dashboard", "method": "GET", "user": "0x454aa5a1c2342c903fbdb885423fb3c7ff73d8a8"}
2024-05-13 22:26:50,237 - DEBUG - {"source_ip": "127.0.0.1", "destination_ip": "127.0.0.1:5000", "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36", "endpoint": "static", "method": "GET", "user": "0x454aa5a1c2342c903fbdb885423fb3c7ff73d8a8"}
2024-05-13 22:26:52,034 - DEBUG - {"source_ip": "127.0.0.1", "destination_ip": "127.0.0.1:5000", "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36", "endpoint": "logout", "method": "GET", "user": "0x454aa5a1c2342c903fbdb885423fb3c7ff73d8a8"}
2024-05-13 22:26:52,034 - INFO - User 0x454aa5a1c2342c903fbdb885423fb3c7ff73d8a8 logged out successfully.
"""

# Define a function to parse the log file
def parse_log(log_data):
    pattern = re.compile(r'(?P<timestamp>[\d-]+ [\d:,]+) - (?P<level>\w+) - (?P<message>.+)')
    log_entries = []

    for line in log_data.strip().split('\n'):
        match = pattern.match(line)
        if match:
            entry = match.groupdict()
            log_entries.append(entry)
    
    return pd.DataFrame(log_entries)

# Parse the sample log data
log_df = parse_log(log_data)

# Feature engineering: extract additional features from timestamp
log_df['timestamp'] = pd.to_datetime(log_df['timestamp'])
log_df['hour'] = log_df['timestamp'].dt.hour
log_df['minute'] = log_df['timestamp'].dt.minute
log_df['day_of_week'] = log_df['timestamp'].dt.dayofweek
log_df['is_business_hours'] = log_df['hour'].apply(lambda x: 1 if 9 <= x <= 17 else 0)

# Extract features from JSON log messages
def extract_json_features(message):
    try:
        log_json = eval(message)
        if isinstance(log_json, dict):
            return pd.Series({
                'source_ip': log_json.get('source_ip', 'Unknown'),
                'destination_ip': log_json.get('destination_ip', 'Unknown'),
                'user_agent': log_json.get('user_agent', 'Unknown'),
                'endpoint': log_json.get('endpoint', 'Unknown'),
                'method': log_json.get('method', 'Unknown'),
                'user': log_json.get('user', 'Unknown')
            })
    except:
        return pd.Series({
            'source_ip': 'Unknown',
            'destination_ip': 'Unknown',
            'user_agent': 'Unknown',
            'endpoint': 'Unknown',
            'method': 'Unknown',
            'user': 'Unknown'
        })

json_features = log_df[log_df['level'] == 'DEBUG']['message'].apply(extract_json_features)
log_df = log_df.join(json_features)

# Fill missing values with 'Unknown'
log_df = log_df.fillna('Unknown')

# Convert IP addresses to numerical features
def ip_to_int(ip):
    try:
        return int(ipaddress.ip_address(ip.split(':')[0]))
    except ValueError:
        return 0

log_df['source_ip'] = log_df['source_ip'].apply(ip_to_int)
log_df['destination_ip'] = log_df['destination_ip'].apply(ip_to_int)

# Encode categorical features using LabelEncoder
label_encoders = {}
for column in ['level', 'user_agent', 'endpoint', 'method', 'user']:
    le = LabelEncoder()
    log_df[column] = le.fit_transform(log_df[column])
    label_encoders[column] = le

# Select relevant features for the model
features = ['hour', 'minute', 'day_of_week', 'is_business_hours', 'source_ip', 'destination_ip', 'user_agent', 'endpoint', 'method', 'user']
X_log = log_df[features]

# For simplicity, we'll use 'level' as the target variable for the log file, though you can replace this with your actual target
y_log = log_df['level']

# Load the CSV dataset
file_path = 'cybersecurity_attacks.csv'
csv_data = pd.read_csv(file_path)

# Drop columns that are not needed or contain too much irrelevant information
columns_to_drop = ['Timestamp', 'Payload Data', 'User Information', 'Device Information', 
                   'Geo-location Data', 'Firewall Logs', 'IDS/IPS Alerts']
csv_data_cleaned = csv_data.drop(columns=columns_to_drop)

# Fill missing values with a placeholder
csv_data_cleaned = csv_data_cleaned.fillna('Unknown')

# Encode categorical features using LabelEncoder
for column in csv_data_cleaned.select_dtypes(include=['object']).columns:
    le = LabelEncoder()
    csv_data_cleaned[column] = le.fit_transform(csv_data_cleaned[column])
    label_encoders[column] = le

# Feature engineering: extract additional features from Timestamp in CSV
csv_data['Timestamp'] = pd.to_datetime(csv_data['Timestamp'])
csv_data['Hour'] = csv_data['Timestamp'].dt.hour
csv_data['Minute'] = csv_data['Timestamp'].dt.minute
csv_data['DayOfWeek'] = csv_data['Timestamp'].dt.dayofweek
csv_data['IsBusinessHours'] = csv_data['Hour'].apply(lambda x: 1 if 9 <= x <= 17 else 0)

# Include the new time-based features in the cleaned dataset
csv_data_cleaned['Hour'] = csv_data['Hour']
csv_data_cleaned['Minute'] = csv_data['Minute']
csv_data_cleaned['DayOfWeek'] = csv_data['DayOfWeek']
csv_data_cleaned['IsBusinessHours'] = csv_data['IsBusinessHours']

# Convert IP addresses to numerical features
csv_data_cleaned['Source IP Address'] = csv_data['Source IP Address'].apply(ip_to_int)
csv_data_cleaned['Destination IP Address'] = csv_data['Destination IP Address'].apply(ip_to_int)

# Encode port ranges
def port_range(port):
    if port < 1024:
        return 'Well-known'
    elif port < 49152:
        return 'Registered'
    else:
        return 'Dynamic'

csv_data_cleaned['Source Port Range'] = csv_data['Source Port'].apply(port_range)
csv_data_cleaned['Destination Port Range'] = csv_data['Destination Port'].apply(port_range)

# Encode the new port range features
for column in ['Source Port Range', 'Destination Port Range']:
    le = LabelEncoder()
    csv_data_cleaned[column] = le.fit_transform(csv_data_cleaned[column])
    label_encoders[column] = le

# Feature: Payload data length
csv_data_cleaned['Payload Length'] = csv_data['Payload Data'].str.len()

# Select relevant features for the model
features_csv = ['Hour', 'Minute', 'DayOfWeek', 'IsBusinessHours', 'Source IP Address', 'Destination IP Address', 
                'Source Port Range', 'Destination Port Range', 'Payload Length']
X_csv = csv_data_cleaned[features_csv]

# Use 'Action Taken' as the target variable
y_csv = csv_data_cleaned['Action Taken']

# Combine log data and CSV data (if relevant, ensure features match)
X_combined = pd.concat([X_log, X_csv], axis=0)
y_combined = pd.concat([y_log, y_csv], axis=0)

# Split the combined dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_combined, y_combined, test_size=0.2, random_state=42)

# Train the Random Forest model
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

model_path = 'pre-trained_model.lib'
joblib.dump(rf_model, model_path)

label_encoders_path = 'label_encoders.pkl'
joblib.dump(label_encoders, label_encoders_path)

# Evaluate the model
y_pred = rf_model.predict(X_test)
classification_report_output = classification_report(y_test, y_pred)
confusion_matrix_output = confusion_matrix(y_test, y_pred)

print("Classification Report:\n", classification_report_output)
print("Confusion Matrix:\n", confusion_matrix_output)
