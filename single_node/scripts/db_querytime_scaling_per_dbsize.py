import parse_file
import os
import numpy as np
import matplotlib.pyplot as plt

databases = ["influx", "timescale"]
nbr_queries = ["1", "10"]
dataset_size = ["small", "medium", "large"]
color_map = {'timescale': '#1f77b4', 'influx': '#ff7f0e'}
results_dictionary = {}

# for each number of queries
for query_count in nbr_queries:
    results_dictionary[f"{query_count}_queries"] = {}

    # for each database, influx or timescale
    for database in databases:
        results_dictionary[f"{query_count}_queries"][database] = []
        # for each dataset size, small, medium, large
        for size in dataset_size:
            file_path = os.path.join('..', 'performance', 'queries', f'{database}db' if database == "timescale" else database,
                                     f'{query_count}_queries', f'{database}_{query_count}_queries_{size}.out')

            try:
                means = parse_file.parse_file(file_path)
                results_dictionary[f"{query_count}_queries"][database].append(
                    np.mean(means))
            except FileNotFoundError:
                print(f"File not found: {file_path}")
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

# Creating subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6))

# Plotting lines for 1_queries
for db, values in results_dictionary['1_queries'].items():
    ax1.plot(list(map(lambda x: x / 1000, values)),
             label=db, color=color_map.get(db))

# Add labels directly on the data points
for db, values in results_dictionary['1_queries'].items():
    for x, y in enumerate(values):
        ax1.text(x, y/1000, f"{y/1000:.2f} s", ha='center', va='bottom')

ax1.set_title('Mean execution time (1 Query per query type)')
ax1.set_xlabel('Dataset Size')
ax1.set_ylabel('Execution Time (s)')
ax1.set_xticks(range(3))
ax1.set_xticklabels(dataset_size)
ax1.legend()

# Plotting lines for 10_queries
for db, values in results_dictionary['10_queries'].items():
    ax2.plot(list(map(lambda x: x/1000, values)),
             label=db, color=color_map.get(db))

for db, values in results_dictionary['10_queries'].items():
    for x, y in enumerate(values):
        ax2.text(x, y/1000, f"{y/1000:.2f} s", ha='center', va='bottom')

ax2.set_title('Mean execution time (10 Query per query type)')
ax2.set_xlabel('Dataset Size')
ax2.set_ylabel('Execution Time (s)')
ax2.set_xticks(range(3), dataset_size)
ax2.legend()

plt.tight_layout()
plt.show()
