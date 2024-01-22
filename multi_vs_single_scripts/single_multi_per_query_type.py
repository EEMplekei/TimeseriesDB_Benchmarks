import os
import sys
import matplotlib.pyplot as plt
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


databases = ["influx", "timescale"]
dataset_size = ["large"]
query_types = ["avg-daily\ndriving-duration", "avg-daily\ndriving-session", "avg-load", "avg-vs-projected\nfuel-consumption",
			   "breakdown-frequency",  "daily-activity", "high-load", "last-loc", "long-driving-sessions", "low-fuel", "stationary-trucks"]
color_map = {  # color map to be persistent across all graphs, could be exported somewhere globally
	'influx_single': '#ff7f0e',
	'timescale_single': '#1f77b4',
	'influx_multi': '#993404',
	'timescale_multi': '#084594'
}
results_single = {}
results_multi = {}

for database in databases:
	for size in dataset_size:
		means_single = get_mean_from_file('single_node', database, '10', size)
		means_multi = get_mean_from_file('multi_node', database, '10', size)
		results_single[(database, size)] = means_single
		results_multi[(database, size)] = means_multi

bar_width = 0.2
for figure_num, index_range in enumerate([(0, 6), (6, len(query_types))], start=1):
	index = range(len(query_types))[index_range[0]:index_range[1]]

	fig, ax = plt.subplots(1, 1, figsize=(8, 10))
	fig.suptitle(f'Multi node vs single node deployment\nComparison of timescale and influx for each query type, 10 queries')
	fig.subplots_adjust()
	
	for db_size in dataset_size:

		bar1 = ax.bar(index, list(map(lambda x: x/1000, results_single[('influx', db_size)][index_range[0]:index_range[1]])),
						bar_width, label='influx single node', color=color_map['influx_single'])

		bar2 = ax.bar([i + bar_width for i in index],
						list(map(lambda x: x/1000, results_multi[('influx', db_size)][index_range[0]:index_range[1]])), bar_width, label='influx multi node', color=color_map['influx_multi'])

		bar3 = ax.bar([i + 2 * bar_width for i in index],
						list(map(lambda x: x/1000, results_single[('timescale', db_size)][index_range[0]:index_range[1]])), bar_width, label='timescale single node', color=color_map['timescale_single'])

		bar4 = ax.bar([i + 3 * bar_width for i in index],
						list(map(lambda x: x/1000, results_multi[('timescale', db_size)][index_range[0]:index_range[1]])), bar_width, label='timescale multi node', color=color_map['timescale_multi'])

		# ax.set_yscale('log')

		ax.set_xlabel('Query type')
		ax.set_ylabel('Execution time (s)')
		ax.set_title(f'{db_size} dataset')
		ax.set_xticks([i + 3*bar_width / 2 for i in index])
		ax.set_xticklabels(query_types[index_range[0]:index_range[1]], rotation=20)
		ax.legend(framealpha=0)

		# Add labels above each bar
		for bar1, bar2, bar3, bar4, value_inf_s, value_inf_m, value_time_s, value_time_m in zip(bar1, bar2, bar3, bar4, 
									results_single[('influx', db_size)][index_range[0]:index_range[1]], 
									results_multi[('influx', db_size)][index_range[0]:index_range[1]],
									results_single[('timescale', db_size)][index_range[0]:index_range[1]], 
									results_multi[('timescale', db_size)][index_range[0]:index_range[1]]):

			ax.text(bar1.get_x() + bar1.get_width() / 2, bar1.get_height(), f'{value_inf_s/1000:.1f}', ha='center', va='bottom').set_size(6)

			ax.text(bar2.get_x() + bar2.get_width() / 2, bar2.get_height(), f'{value_inf_m/1000:.1f}', ha='center', va='bottom').set_size(6)
			
			ax.text(bar3.get_x() + bar3.get_width() / 2, bar3.get_height(), f'{value_time_s/1000:.1f}', ha='center', va='bottom').set_size(6)
			
			ax.text(bar4.get_x() + bar4.get_width() / 2, bar4.get_height(), f'{value_time_m/1000:.1f}', ha='center', va='bottom').set_size(6)

	fig.autofmt_xdate()
	plt.show()
