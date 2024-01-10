import csv
import subprocess
import numpy as np
import psycopg2
import sys
import re
import os

database = sys.argv[1]
size = sys.argv[2]
if(database=="influx"):
    data_dir = '/var/lib/influxdb/data/'
elif(database=="timescale"):
    data_dir = '/var/lib/postgresql/14/main/base/'
    #database connection details
    database_name = 'benchmark_' + size
    user = 'postgres'
    password = 'password'
    host = 'localhost'
    port = '5432'

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
    cur.execute("SELECT oid FROM pg_database WHERE datname = 'benchmark_"+size +"'")

    # Fetch all rows from the result set
    rows = cur.fetchall()

    # Close the cursor and connection
    cur.close()
    conn.close()
    oid = rows[0][0]
    
sudo_password = 'GsGLKgki5V'

def findBytesFromDatabaseFolderList(dir_path):
    global sudo_password
    command = 'du -h --apparent-size ' + dir_path
    output = subprocess.check_output('echo %s|sudo -S %s' % (sudo_password, command), shell=True).decode()
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

def write_data_to_file(category, value, file_path='data_file.txt'):

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
    full_data_dir = data_dir + 'benchmark_' + size
elif(database=="timescale"):
    full_data_dir = data_dir + str(oid)
data_bytes,unit  = extract_numeric_and_string_parts(findBytesFromDatabaseFolderList(full_data_dir))
write_data_to_file(database+"-"+size, str(data_bytes) + unit)
