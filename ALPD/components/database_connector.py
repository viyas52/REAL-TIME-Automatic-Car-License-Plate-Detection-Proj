import numpy as np
from datetime import datetime
import mysql.connector
from ALPD.constants import mysql_password 
# Replace with your RDS details
rds_endpoint = 'alpd.cvquoeky09pg.ap-south-1.rds.amazonaws.com'
username = 'admin'
password = mysql_password 
database_name = 'ALPD_Machine'  # Specify your new database name

# Connect to the MySQL RDS instance
conn = mysql.connector.connect(
    host=rds_endpoint,
    user=username,
    password=password
)

# Create a new database
def create_database(conn, database_name):
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name};")
    conn.commit()
    cursor.close()
    print(f"Database '{database_name}' created or already exists.")

# Create the database
create_database(conn, database_name)

# Now reconnect to the specific database
conn.close()  # Close the previous connection

# Re-establish the connection to the new database
conn = mysql.connector.connect(
    host=rds_endpoint,
    user=username,
    password=password,
    database=database_name  # Connect to the newly created database
)

# Authorized license plates
authorized_plates = ['TN01BT3837']

def insert_data(conn, license_plate, confidence_score, permission):
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%H:%M:%S')
    cursor.execute('''
        INSERT INTO license_plates (license_plate, confidence_score, timestamp, permission)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE confidence_score = VALUES(confidence_score), timestamp = VALUES(timestamp), permission = VALUES(permission);
    ''', (license_plate, confidence_score, timestamp, permission))
    conn.commit()
    cursor.close()
    print(f"Data inserted: license_plate={license_plate}, confidence_score={confidence_score}, permission={permission}, timestamp={timestamp}")

def process_results(conn, results):
    for car_id in np.unique(results['car_id']):
        if (results['car_id'] == car_id).sum() >= 0:
            max_score = np.amax(results[results['car_id'] == car_id]['license_number_score'])
            license_plate_number = results[(results['car_id'] == car_id) &
                                           (results['license_number_score'] == max_score)]['license_number'].iloc[0]
            
            permission = "Allowed" if license_plate_number in authorized_plates else "Not Allowed"
            insert_data(conn, license_plate_number, max_score, permission)
            
            
def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS license_plates (
            license_plate VARCHAR(255) PRIMARY KEY,
            confidence_score FLOAT,
            timestamp VARCHAR(255),
            permission VARCHAR(255)
        );
    ''')
    conn.commit()
    cursor.close()
    print("Table created or already exists.")

# Create the table
create_table(conn)

# Example data for testing the process_results function
results = {
    'car_id': np.array(['car1', 'car1', 'car2']),
    'license_number_score': np.array([0.8, 0.9, 0.7]),
    'license_number': np.array(['TN01BT3837', 'TN01AB1234', 'TN01BT3837'])
}

# Process the results
process_results(conn, results)

# Close the connection
conn.close()
