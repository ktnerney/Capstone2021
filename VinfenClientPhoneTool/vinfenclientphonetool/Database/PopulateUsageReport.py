from datetime import datetime
import sys

import mysql.connector
import pandas as pd
import yaml

from constants import DB_NAME
from Database.utils import generate_insert

def populate_db_from_usage_report(filename: str):

    with open(r'../vinfen_config.yaml') as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        config = yaml.load(file, Loader=yaml.FullLoader)

    # Connect to server
    cnx = mysql.connector.connect(
        host=config['host'],
        port=config['port'],
        user=config['user'],
        password=config['password'])

    # Get a cursor
    cursor = cnx.cursor()

    # Select database
    cursor.execute(f"USE {DB_NAME};")

    # Read in file
    month = pd.read_csv(filename)

    # Drop last row
    month.drop(month.tail(1).index,inplace=True)

    # Create Phone data frame
    Phone = pd.DataFrame()

    Phone['phone_number'] = month['Mobile Number']

    # Cast values to expected type
    phone_types = {
        'phone_number' : 'int64'
        }
    
    Phone.astype(phone_types).dtypes

    # Insert values into Phone
    cursor.execute(generate_insert(Phone, "phone", True))

    # Create UsageReport data frame
    UsageReport = pd.DataFrame()

    UsageReport['phone_number'] = month['Mobile Number']
    UsageReport['report_date'] = month['Report Date']
    UsageReport['total_messages'] = month['Total Messages']
    UsageReport['total_minutes'] = month['Total Minutes']
    UsageReport['total_data'] = month['Total (Domestic) Data Usage (KB)']

    # Cast values to expected type
    usage_types = {
        
        'phone_number' : 'int64',
        'report_date' : 'str',
        'total_messages' : 'int32',
        'total_minutes' : 'int32',
        'total_data' : 'float'
        }

    UsageReport.astype(usage_types).dtypes

    UsageReport["report_date"] = pd.to_datetime(UsageReport.report_date)
    UsageReport["report_date"] = UsageReport.report_date.dt.strftime('%Y-%m-%d')

    # Insert values into UsageReport
    cursor.execute(generate_insert(UsageReport, "usage_report"))

    # Create Client data frame
    Client = pd.DataFrame()

    Client['phone_number'] = month['Mobile Number']

    client_types = {
        'phone_number' : 'int64'
        }

    # Insert values in Client
    cursor.execute(generate_insert(Client, "client", True))
    
    # Close cursor 
    cursor.close()

    # Commit Changes
    cnx.commit()

    # Close connection
    cnx.close()

def main():
    if (len(sys.argv) > 2):
        print("Too many arguments: expected 1 file path.")
    elif(len(sys.argv) < 2):
        print("Too few arguments: expected 1 file path")
    else:
        populate_db_from_usage_report(sys.argv[1])

if __name__ == "__main__":
    main()
