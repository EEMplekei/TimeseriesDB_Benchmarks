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
index = range(len(query_types))
fig, ax = plt.subplots(3, 1)
fig.suptitle(
	f'Multi node deployment - Comparison of timescale and influx for each query type, 10 queries')
fig.subplots_adjust()

for db_size, i in zip(dataset_size, range(3)):

	bar1 = ax[i].bar(index, list(map(lambda x: x/1000, results[('influx', db_size, '10')])),
					 bar_width, label='influx', color=color_map['influx'])
	
	bar2 = ax[i].bar([i + bar_width for i in index],
					 list(map(lambda x: x/1000, results[('timescale', db_size, '10')])), bar_width, label='timescale', color=color_map['timescale'])
	
	#ax[i].set_yscale('log')
	ax[i].set_xlabel('Query type')
	ax[i].set_ylabel('Execution time (s)')
	ax[i].set_title(f'{db_size} dataset')
	ax[i].set_xticks([i + bar_width / 2 for i in index])
	ax[i].set_xticklabels(query_types, rotation=20)
	ax[i].legend(framealpha = 0)

	# Add labels above each bar
	for bar1, bar2, value_inf, value_time in zip(bar1, bar2, results[('influx', db_size, '10')], results[('timescale', db_size, '10')]):

		ax[i].text(bar1.get_x() + bar1.get_width() / 2, bar1.get_height() +
				   0.05 + (1 if value_inf > value_time else 0), f'{value_inf/1000:.1f}', ha='center', va='bottom')

		ax[i].text(bar2.get_x() + bar2.get_width() / 2, bar2.get_height() +
				   0.05+ (1 if value_time > value_inf else 0), f'{value_time/1000:.1f}', ha='center', va='bottom')

fig.autofmt_xdate()
plt.show()