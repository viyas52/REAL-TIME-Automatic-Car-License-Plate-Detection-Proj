import mysql.connector
import pandas as pd
import numpy as np
from datetime import datetime

# List of authorized license plates
authorized_plates = ['ABC1234', 'XYZ5678', 'DEF9012']  # Add authorized license plates here

# Function to insert data into the database
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
    
    
# Function to process results and save to the database
def process_results(conn, results):
    for car_id in np.unique(results['car_id']):
        if (results['car_id'] == car_id).sum() >= 0:  # Check if car_id appears at least 50 times
            max_score = np.amax(results[results['car_id'] == car_id]['license_number_score'])
            license_plate_number = results[(results['car_id'] == car_id) &
                                           (results['license_number_score'] == max_score)]['license_number'].iloc[0]
            
            permission = "Allowed" if license_plate_number in authorized_plates else "Not Allowed"
            insert_data(conn, license_plate_number, max_score, permission)

# Set up the database
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
    print("table connection created")

# Main function
def main():
    conn = mysql.connector.connect(host='localhost', user='root', password='mysql#98841@', database='license_plate_db')
    
    create_table(conn)
    
    results = pd.read_csv('./test.csv', encoding='ISO-8859-1')
    process_results(conn, results)
    
    conn.close()

if __name__ == "__main__":
    main()
