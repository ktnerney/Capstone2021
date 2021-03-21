import mysql.connector
from mysql.connector import errorcode

# Name Database
DB_NAME = 'VINFEN_CLIENT_DB'

# Create Database
## creating a databse called 'datacamp'
## 'execute()' method is used to compile a 'SQL' statement
## below statement is used to create tha 'datacamp' database
def create_database(cursor):
    try:
        cursor.execute(
        "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

def create_db():
    # Connect to server
    cnx = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="Goldrocks65!")

    # Get a cursor
    cursor = cnx.cursor()

    try:
        cursor.execute("USE {}".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            print("Database {} created successfully.".format(DB_NAME))
            cnx.database = DB_NAME
        else:
            print(err)
            exit(1)

    # Create Tables

    TABLES = {}
    TABLES['phone'] = (
        "CREATE TABLE `phone`  ("
        "   phone_number BIGINT UNSIGNED PRIMARY KEY"
        ");")
       
    TABLES['client'] = (
        "CREATE TABLE `client`  ("
        "   client_id INT PRIMARY KEY AUTO_INCREMENT,"
        "   phone_number BIGINT UNSIGNED,"
        
        "   FOREIGN key (phone_number) references phone(phone_number)"
        ");")

    TABLES['usage_report'] = (
        "CREATE TABLE `usage_report`  ("
        "   usage_report_id INT PRIMARY KEY AUTO_INCREMENT,"
        "   phone_number BIGINT UNSIGNED,"
        "   report_date DATE NOT NULL,"
        "   total_messages INT NOT NULL,"
        "   total_minutes INT NOT NULL,"
        "   total_data FLOAT NOT NULL,"
        
        "   FOREIGN key (phone_number) references phone(phone_number)"
        ");")


    TABLES['vinfen_staff'] = (
        "CREATE TABLE `vinfen_staff`  ("
        "   staff_id INT AUTO_INCREMENT PRIMARY KEY,"
        "   name VARCHAR(100) NOT NULL,"
        "   position VARCHAR(100) NOT NULL,"
        "   team VARCHAR(100) NOT NULL"
        ");")

    TABLES['staff_has_client'] = (
        "CREATE TABLE `staff_has_client` ("
        "   staff_id INT,"
        "   client_id INT,"
        
        "   FOREIGN key (staff_id) references vinfen_staff(staff_id),"
        "   FOREIGN key (client_id) references client(client_id)"
        ");")

    TABLES['staff_to_phone'] = (
        "CREATE TABLE `staff_to_phone` ("
        "   staff_id INT,"
        "   phone_number BIGINT UNSIGNED,"
        
        "   FOREIGN key (staff_id) references vinfen_staff(staff_id),"
        "   FOREIGN key (phone_number) references phone(phone_number)"
        ");")


    for table_name in reversed(TABLES):
        try:
            print("Dropping table if exists {} ".format(table_name), end='\n')
            cursor.execute(f"drop table if exists {table_name};")
            
        except mysql.connector.Error as err:
            print(err.msg)
        else:
            print("OK") 
                                                 

    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:    
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            print(err.msg)
        else:
            print("OK")
            
    # Close cursor 
    cursor.close()

    # Close connection
    cnx.close()

def main():
    create_db()

if __name__ == "__main__":
    main()
