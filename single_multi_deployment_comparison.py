import os
import sys
import matplotlib.pyplot as plt
import numpy as np
sys.path.insert(1, './single_node/scripts')
import parse_file

def get_mean_from_file(node_count, database, query_size, size):
    file_path = os.path.join(node_count, 'performance', 'queries', f'{database}db' if database == "timescale" else database,
                             f'{query_size}_queries', f'{database}_{query_size}_queries_{size}.out')
    try:
        means = parse_file.parse_file(file_path)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        exit(-1)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        exit(-1)
    return means


color_map = {
    'timescale single node': '#1f77b4',
    'influx single node': '#ff7f0e',
    'influx multi node': '#993404',
    'timescale multi node': '#084594'
}

nbr_query = "10"
node_counts = ["single_node", "multi_node"]
databases = ["influx", "timescale"]
dataset_size = ["small", "medium", "large"]

results = {}

for node_count in node_counts:
    for database in databases:
        for size in dataset_size:
            means = get_mean_from_file(node_count, database, nbr_query, size)
            results[(node_count, database, size)] = np.mean(means)

x = np.arange(len(dataset_size))
width = 0.2  # Width of the bars
categories = ["influx single node", "influx multi node",
              "timescale single node", "timescale multi node"]
influx_single_values = [results[('single_node', 'influx', 'small')], results[(
    'single_node', 'influx', 'medium')], results[('single_node', 'influx', 'large')]]
influx_multi_values = [results[('multi_node', 'influx', 'small')], results[(
    'multi_node', 'influx', 'medium')], results[('multi_node', 'influx', 'large')]]
timescale_single_values = [results[('single_node', 'timescale', 'small')], results[(
    'single_node', 'timescale', 'medium')], results[('single_node', 'timescale', 'large')]]
timescale_multi_values = [results[('multi_node', 'timescale', 'small')], results[(
    'multi_node', 'timescale', 'medium')], results[('multi_node', 'timescale', 'large')]]

for i, (means, database_name) in enumerate(zip([influx_single_values, influx_multi_values, timescale_single_values, timescale_multi_values], categories)):
    bar = plt.bar(x + i * width, list(map(lambda x: x / 1000, means)),
                  width=width, label=database_name, color=color_map.get(database_name))
    plt.bar_label(bar, fmt='{:,.2f}s', size=6)

plt.xlabel('Dataset Size')
plt.ylabel('Execution Time (s)')
plt.title(
    f'Multi node vs single node deployment\nAverage execution time (for {nbr_query} queries per query type)')
plt.xticks(x + width * (len(categories) - 1) / 2, dataset_size)
plt.legend()
plt.show()
