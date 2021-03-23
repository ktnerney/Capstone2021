from datetime import datetime
import sys

import mysql.connector
import pandas as pd
import yaml

from constants import DB_NAME
from Database.utils import generate_insert

def populate_db_from_staff_report(filename: str):

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
    staff = pd.read_csv(filename)

    # Create VinfenStaff data frame
    VinfenStaff = pd.DataFrame()

    VinfenStaff['name'] = staff['Name']
    VinfenStaff['position'] = staff['Position']
    VinfenStaff['team'] = staff['workordername']

    # Cast values to expected type
    staff_types = {
        'name': 'str',
        'position': 'str',
        'team': 'str'
    }

    VinfenStaff.astype(staff_types).dtypes

    # Insert values into VinfenStaff
    cursor.execute(generate_insert(VinfenStaff, "vinfen_staff"))

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
        populate_db_from_staff_report(sys.argv[1])


if __name__ == "__main__":
    main()
