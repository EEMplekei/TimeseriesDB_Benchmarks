import csv
import subprocess
import psycopg2
import sys
import re
import os
from psycopg2 import OperationalError
sudo_password_B = 'HaPI7BusVR'
sudo_password_C = 'mArHF77Hly'

if(len(sys.argv)!=3):
    print("Error: Please enter the correct number of arguments.")
    sys.exit(1)

database = sys.argv[1]
size = sys.argv[2]

if(size not in ["small", "medium", "large"]):
    print("Error: Please enter a valid size.")
    sys.exit(1)
if(database not in ["influx", "timescale"]):
    print("Error: Please enter a valid database name.")
    sys.exit(1)

#timescale
    #nodeb size
    #nodec size
    #ssh username@host "command"
#inlux
    #nodebsize
    #nodec size

if(database=="influx"):
    data_dir = '/var/lib/influxdb/data/'
elif(database=="timescale"):
    data_dir = '/var/lib/postgresql/14/main/base/'
    #database connection details
    database_name = 'benchmark_' + size
    user = 'postgres'
    password = 'password'
    host = '10.0.0.2'
    port = '5432'
    
    #CONNECT TO NODE_B
    # Initialize cur and conn outside the try block
    cur = None
    conn = None
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
                dbname=database_name,
                user=user,
                password=password,
                host=host,
                port=port
                )

        # Create a cursor object to execute queries
        cur = conn.cursor()

        # Execute the query to fetch database names and OIDs for databases starting with 'benchmark'
        cur.execute("SELECT oid FROM pg_database WHERE datname = %s", (database_name,))

        # Fetch all rows from the result set
        rows = cur.fetchall()

        # Continue with your code for processing the results
        oid_B = rows[0][0]
    except OperationalError as e:
        # Catch the exception if the database connection fails
        # You can check the specific error message to determine if it's due to the database not existing
        error_message = str(e)
        if "does not exist" in error_message:
            print(f"Error: The database '{database_name}' does not exist. Please create it before running this script.")
        else:
            # Handle other operational errors if needed
            print(f"Error: {error_message}")
        sys.exit(1)  # Terminate the script with a non-zero exit code
    finally:
        # Close the cursor and connection in the finally block to ensure they are always closed
        if cur:
            cur.close()
        if conn:
            conn.close()
    
    #CONNECT TO NODE_C
    host = '10.0.0.3'
    # Initialize cur and conn outside the try block
    cur = None
    conn = None
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
                dbname=database_name,
                user=user,
                password=password,
                host=host,
                port=port
                )

        # Create a cursor object to execute queries
        cur = conn.cursor()

        # Execute the query to fetch database names and OIDs for databases starting with 'benchmark'
        cur.execute("SELECT oid FROM pg_database WHERE datname = %s", (database_name,))

        # Fetch all rows from the result set
        rows = cur.fetchall()

        # Continue with your code for processing the results
        oid_C = rows[0][0]
    except OperationalError as e:
        # Catch the exception if the database connection fails
        # You can check the specific error message to determine if it's due to the database not existing
        error_message = str(e)
        if "does not exist" in error_message:
            print(f"Error: The database '{database_name}' does not exist. Please create it before running this script.")
        else:
            # Handle other operational errors if needed
            print(f"Error: {error_message}")
        sys.exit(1)  # Terminate the script with a non-zero exit code
    finally:
        # Close the cursor and connection in the finally block to ensure they are always closed
        if cur:
            cur.close()
        if conn:
            conn.close()


def findBytesFromDatabaseFolderList(dir_path,sudo_password):
    command = 'du --bytes ' + dir_path
    output = subprocess.check_output('echo %s|sudo -S %s' % (sudo_password, command), shell=True).decode()
    data_bytes_str = output.split('\n')[-2].split('\t')[0]
    return data_bytes_str

def execute_ssh_command(username, host ,dir_path,sudo_password):
    command = 'du --bytes ' + dir_path
    full_command = 'ssh {}@{} "{}"'.format(username, host, 'echo %s|sudo -S %s' % (sudo_password, command))
    output = subprocess.check_output(full_command, shell=True).decode()
    data_bytes_str = output.split('\n')[-2].split('\t')[0]
    return data_bytes_str

def extract_numeric_and_string_parts(input_string):
    # Use a regular expression to separate numeric and string parts
    match = re.match(r'([0-9.]+)([a-zA-Z]+)', input_string)

    if match:
        numeric_part = match.group(1)
        string_part = match.group(2)
        return numeric_part, string_part
    else:
        # No match, return None for both parts
        return None, None

def write_data_to_file(category, value, file_path='../performance/disk/size_on_disk.out'):

    # Check if the file already exists
    file_exists = os.path.isfile(file_path)

    if not file_exists:
        # Create the file if it doesn't exist
        open(file_path, 'a').close()

    # Open the file in read mode to check if the category already exists
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Check if the category already exists in the lines
    category_found = False
    for i, line in enumerate(lines):
        if category in line:
            lines[i] = f"{category}:{value}\n"
            category_found = True
            break

    # If the category is not found, add a new entry
    if not category_found:
        lines.append(f"{category}:{value}\n")

    # Open the file in write mode to overwrite the content
    with open(file_path, 'w') as file:
        file.writelines(lines)

if(database=="influx"):
    try:
        full_data_dir = data_dir + 'benchmark_' + size
        # Check if the full_data_dir exists
        #if not os.path.exists(full_data_dir):
        #    raise FileNotFoundError("Error: The database benchmark_" + size + " does not exist. Please create it before running this script.")

        # Proceed with your existing code
        data_bytes_B= execute_ssh_command("ubuntu", "10.0.0.2", full_data_dir, sudo_password_B)
        data_bytes_C= execute_ssh_command("ubuntu", "10.0.0.3", full_data_dir, sudo_password_C)
        data_bytes_B = int(data_bytes_B)
        data_bytes_C = int(data_bytes_C)
        write_data_to_file(database + "-" + size, "B_size="+str(data_bytes_B)+", "+ "C_size="+str(data_bytes_C))

    except ValueError:
        raise ValueError(f"Something goes worng")
    sys.exit(1)  # Terminate the script with a non-zero exit code
elif(database=="timescale"):
    full_data_dir_B = data_dir + str(oid_B)
    full_data_dir_C = data_dir + str(oid_C)
    data_bytes_B= execute_ssh_command("ubuntu", "10.0.0.2", full_data_dir_B, sudo_password_B)
    data_bytes_C= execute_ssh_command("ubuntu", "10.0.0.3", full_data_dir_C, sudo_password_C)
    data_bytes_B = int(data_bytes_B)
    data_bytes_C = int(data_bytes_C)
    write_data_to_file(database + "-" + size, "B_size="+str(data_bytes_B)+", "+ "C_size="+str(data_bytes_C))
