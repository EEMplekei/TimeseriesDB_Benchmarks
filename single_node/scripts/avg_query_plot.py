import numpy as np
import parse_file
import os
import matplotlib.pyplot as plt

databases = ["influx", "timescale"]
nbr_queries = ["1", "10"]
dataset_size = ["small", "medium", "large"]
for nbr_query in nbr_queries:
    # Initialize lists to store means and database names for each query count
    means_list = []
    database_names = []

    for database in databases:
        means_per_database = []
        for size in dataset_size:
            file_path = os.path.join('..', 'performance', 'queries', f'{database}db' if database == "timescale" else database,
                                     f'{nbr_query}_queries', f'{database}_{nbr_query}_queries_{size}.out')
            try:
                means = parse_file.parse_file(file_path)
                # print("database -" + database+ " , size - " + size + ", nbr_query - " +nbr_query)
                means_per_database.append(np.mean(means))
            except FileNotFoundError:
                print(f"File not found: {file_path}")
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

        if means_per_database:
            means_list.append(means_per_database)
            database_names.append(database)

    # Create a bar plot for each number of queries
    x = np.arange(len(dataset_size))
    width = 0.2  # Width of the bars

    for i, (means, database_name) in enumerate(zip(means_list, database_names)):
        bar = plt.bar(x + i * width, list(map(lambda x : x / 1000, means)), width=width, label=database_name)
        plt.bar_label(bar, fmt = '{:,.2f} s')

    plt.xlabel('Dataset Size')
    plt.ylabel('Execution Time (s)')
    plt.title(
        f'Average execution time (for {nbr_query} Queries per query type)')
    plt.xticks(x + width * (len(databases) - 1) / 2, dataset_size)
    plt.legend()
    plt.show()
