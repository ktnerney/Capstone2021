import mysql.connector
import pandas as pd
from datetime import datetime
import sys

# Name Database
DB_NAME = 'VINFEN_CLIENT_DB'

def generate_insert(table, table_name):
    df_list = table.values.tolist()

    insert_str = f"INSERT INTO {table_name} ("
    for label in table.columns:
        if label != table.columns[-1]:
            insert_str += f"{label},"
        else:
            insert_str += f"{label})"

    insert_str += " VALUES "
    
    for ii in range(len(df_list)):
        row = df_list[ii]
        insert_str += "("
        for jj in range(len(row)):
            value = row[jj]
            if isinstance(value, str):
                for char in ["'", '"']:
                    value = value.replace(char, "")
                insert_str += f"'{value}'"
            else:
                insert_str += f"{value}"
            if ii == len(df_list) - 1 and jj == len(row) - 1:
                insert_str += ");"
            elif jj == len(row) - 1:
                insert_str += "),"
            else:
                insert_str += ","
    return insert_str

def populate_db():
    # Connect to server
    cnx = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="Goldrocks65!")

    # Get a cursor
    cursor = cnx.cursor()

    # Select database
    cursor.execute(f"USE {DB_NAME};")

    # Read in file
    june = pd.read_csv('C:/Users/Chris Nerney/Documents/Python/Capstone2021/VinfenClientPhoneTool/vinfenclientphonetool/CSVs/Usage_Report_June2020.csv')
    staff = pd.read_csv('C:/Users/Chris Nerney/Documents/Python/Capstone2021/VinfenClientPhoneTool/vinfenclientphonetool/CSVs/StaffDirectory_ACCSTeams.csv')

    # Drop last row
    june.drop(june.tail(1).index,inplace=True)

    # Create Phone data frame
    Phone = pd.DataFrame()

    Phone['phone_number'] = june['Mobile Number']

    # Cast values to expected type
    phone_types = {
        'phone_number' : 'int64'
        }
    
    Phone.astype(phone_types).dtypes

    # Insert values into Phone
    cursor.execute(generate_insert(Phone, "phone"))

    # Create UsageReport data frame
    UsageReport = pd.DataFrame()

    UsageReport['phone_number'] = june['Mobile Number']
    UsageReport['report_date'] = june['Report Date']
    UsageReport['total_messages'] = june['Total Messages']
    UsageReport['total_minutes'] = june['Total Minutes']
    UsageReport['total_data'] = june['Total (Domestic) Data Usage (KB)']

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

    Client['phone_number'] = june['Mobile Number']

    client_types = {
        'phone_number' : 'int64'
        }


    # Insert values in Client
    cursor.execute(generate_insert(Client, "client"))

    # Create VinfenStaff data frame
    VinfenStaff = pd.DataFrame()

    VinfenStaff['name'] = staff['Name']
    VinfenStaff['position'] = staff['Position']
    VinfenStaff['team'] = staff['workordername']

    # Cast values to expected type
    staff_types = {
        'name' : 'str',
        'position' : 'str',
        'team' : 'str'
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
    populate_db()

if __name__ == "__main__":
    main()
