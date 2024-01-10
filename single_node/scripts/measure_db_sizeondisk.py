import matplotlib.pyplot as plt
import subprocess
import numpy as np
import psycopg2

# Replace these with your actual database connection details
user = 'postgres'
password = 'password'
host = 'localhost'
port = '5432'

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    user=user,
    password=password,
    host=host,
    port=port
)

# Create a cursor object to execute queries
cur = conn.cursor()

# Execute the query to fetch database names and OIDs for databases starting with 'benchmark'
cur.execute("SELECT datname, oid FROM pg_database WHERE datname LIKE 'benchmark%'")

# Fetch all rows from the result set
rows = cur.fetchall()

# Create the dictionary
timescaledb_database_dictionary = {}

# Map size identifiers to specific OIDs
size_mapping = {'small', 'medium', 'large'}

for name, oid in rows:
    for size in size_mapping:
        if f'benchmark_{size}' in name:
            timescaledb_database_dictionary[size] = str(oid)
            break

# Close the cursor and connection
cur.close()
conn.close()

# Print the resulting dictionary
#print(timescaledb_database_dictionary)

sudo_password = 'GsGLKgki5V'

def findBytesFromDatabaseFolderList(dir_path):
    global sudo_password
    command = 'du --apparent-size ' + dir_path
    output = subprocess.check_output('echo %s|sudo -S %s' % (sudo_password, command), shell=True).decode()
    data_bytes = output.split('\n')[-2].split('\t')[0]
    return data_bytes

database_names = ["influx", "timescaledb"]
dataset_sizes = ["small", "medium", "large"]
timescaledb_data_dir = '/var/lib/postgresql/14/main/base/'
influx_data_dir = '/var/lib/influxdb/data/'
influx_database_dictionary = { 'small' : 'benchmark_small', 'medium' : 'benchmark_medium', 'large' : 'benchmark_large' }
database_dictionary = {
    'timescaledb' : timescaledb_database_dictionary,
    'timescaledb_data_dir' : timescaledb_data_dir ,
    'influx': influx_database_dictionary , 
    'influx_data_dir': influx_data_dir, 
}
results_per_db = []
for db_name in database_names:
    bytes_per_size = []
    for ds_size in dataset_sizes:
        data_dir = db_name + "_data_dir"
        full_data_dir = database_dictionary[data_dir] + database_dictionary[db_name][ds_size]
        data_bytes =  float(findBytesFromDatabaseFolderList(full_data_dir))/1000
        bytes_per_size.append(data_bytes)
    
    results_per_db.append(bytes_per_size)    

x ,width = np.arange(2), 0.2
plt.bar(x, results_per_db[1], width, color='orange') 
plt.bar(x-width, results_per_db[0], width, color='purple')
plt.xticks(x, ['Small 1 GB', 'Medium 5GB', 'Large 15GB'])
plt.xlabel("Original dataset size")
plt.ylabel("KBytes in disk")
plt.legend(["TimescaleDB", "InfluxDB"])
plt.show()