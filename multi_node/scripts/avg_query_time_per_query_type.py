import numpy as np
import parse_file
import os
import matplotlib.pyplot as plt

databases = ["influx", "timescale"]
dataset_size = ["small", "medium", "large"]
query_sizes = ["10"]
query_types = ["avg-daily\ndriving-duration", "avg-daily\ndriving-session", "avg-load", "avg-vs-projected\nfuel-consumption",
			   "breakdown-frequency",  "daily-activity", "high-load", "last-loc", "long-driving-sessions", "low-fuel", "stationary-trucks"]
color_map = {'timescale': '#1f77b4', 'influx': '#ff7f0e'}
results = {}

for query_size in query_sizes:
	for database in databases:
		for size in dataset_size:
			file_path = os.path.join('..', 'performance', 'queries', f'{database}db' if database == "timescale" else database,
									 f'{query_size}_queries', f'{database}_{query_size}_queries_{size}.out')
			try:
				means = parse_file.parse_file(file_path)
			except FileNotFoundError:
				print(f"File not found: {file_path}")
			except Exception as e:
				print(f"Error processing file {file_path}: {e}")

			results[(database, size, query_size)] = means

bar_width = 0.35

for figure_num, index_range in enumerate([(0, 6), (6, len(query_types))], start=1):
    index = range(len(query_types))[index_range[0]:index_range[1]]

    fig, axs = plt.subplots(3, 1, figsize=(8, 10))
    fig.suptitle(f'Multi node deployment\nComparison of timescale and influx for each query type, 10 queries')
    fig.subplots_adjust()

    for db_size, i in zip(dataset_size, range(3)):
        bar1 = axs[i].bar(index, [x / 1000 for x in results[('influx', db_size, '10')][index_range[0]:index_range[1]]],
                          bar_width, label='influx', color=color_map['influx'])

        bar2 = axs[i].bar([x + bar_width for x in index],
                           [x / 1000 for x in results[('timescale', db_size, '10')][index_range[0]:index_range[1]]],
                           bar_width, label='timescale', color=color_map['timescale'])

        axs[i].set_xlabel('Query type')
        axs[i].set_ylabel('Execution time (s)')
        axs[i].set_title(f'{db_size} dataset')
        axs[i].set_xticks([x + bar_width / 2 for x in index])
        axs[i].set_xticklabels(query_types[index_range[0]:index_range[1]], rotation=20)
        axs[i].legend(framealpha=0)

        for bar_inf, bar_time, value_inf, value_time in zip(bar1, bar2,
                                                            results[('influx', db_size, '10')][index_range[0]:index_range[1]],
                                                            results[('timescale', db_size, '10')][index_range[0]:index_range[1]]):
            axs[i].text(bar_inf.get_x() + bar_inf.get_width() / 2, bar_inf.get_height() + 0.05 + (1 if value_inf > value_time else 0),
                         f'{value_inf/1000:.1f}', ha='center', va='bottom')

            axs[i].text(bar_time.get_x() + bar_time.get_width() / 2, bar_time.get_height() + 0.05 + (1 if value_time > value_inf else 0),
                         f'{value_time/1000:.1f}', ha='center', va='bottom')

    fig.autofmt_xdate()
    plt.show()