import os
import re
import matplotlib.pyplot as plt

directory_path = "../performance/write"

# Create a dictionary to store mean rates
mean_rates_dict = {}

# Iterate through each file in the directory
for filename in os.listdir(directory_path):
	file_path = os.path.join(directory_path, filename)
	# Check if the path is a file
	if os.path.isfile(file_path):
		with open(file_path, 'r') as file:
			# Read the last two lines of the file
			lines = file.readlines()[-2:]

			# Extract mean rates using regular expressions
			metrics_mean_rate_match = re.search(
				r'mean rate (\d+\.\d+) metrics/sec', lines[0])
			rows_mean_rate_match = re.search(
				r'mean rate (\d+\.\d+) rows/sec', lines[1])

			# If both matches are successful, append mean rates to dictionary
			if metrics_mean_rate_match and rows_mean_rate_match:
				metrics_mean_rate = float(metrics_mean_rate_match.group(1))
				rows_mean_rate = float(rows_mean_rate_match.group(1))

				mean_rates_dict[filename] = {
					'metrics_mean_rate': metrics_mean_rate,
					'rows_mean_rate': rows_mean_rate
				}

# Iterate through the dictionary and separate the values for each database
timescale_dict = {}
influx_dict = {}
for key, value in mean_rates_dict.items():
	database, size = key.split('_')
	size = size.split('.')[0]
	if database == 'timescale':
		timescale_dict[size] = value
	else:
		influx_dict[size] = value

#Define and parse into lists
influx_rowspersec = {"small": 0, "medium": 0, "large": 0}
influx_metricspersec = {"small": 0, "medium": 0, "large": 0}
timescale_rowspersec = {"small": 0, "medium": 0, "large": 0}
timescale_metricspersec = {'small': 0, 'medium': 0, 'large': 0}

for key, value in influx_dict.items():
	influx_rowspersec[key] = value['rows_mean_rate']
	influx_metricspersec[key] = value['metrics_mean_rate']

for key, value in timescale_dict.items():
	timescale_rowspersec[key] = value['rows_mean_rate']
	timescale_metricspersec[key] = value['metrics_mean_rate']

influx_rowspersec = list(influx_rowspersec.values())
influx_metricspersec = list(influx_metricspersec.values())
timescale_rowspersec = list(timescale_rowspersec.values())
timescale_metricspersec = list(timescale_metricspersec.values())

# Plotting
rows_per_sec = [influx_rowspersec, timescale_rowspersec]
metrics_mean_rate = [influx_metricspersec, timescale_metricspersec]
categories = ['small', 'medium', 'large']
axes = [None, None]
bar_width = 0.35
index = range(len(categories))
fig, (axes[0], axes[1]) = plt.subplots(nrows=2, ncols=1, figsize=(10, 8))

bar1 = axes[0].bar(index, influx_rowspersec, bar_width, label='influx', color='#fe7f10')
bar2 = axes[0].bar([i + bar_width for i in index], timescale_rowspersec, bar_width, label='timescale', color='#1f77b4')

axes[0].set_ylabel('Rows / second')
axes[0].set_title('Comparison of TimescaleDB and Influx dataset insertion speed')
axes[0].set_xticks([i + bar_width / 2 for i in index])
axes[0].set_xticklabels(categories)

bar3 = axes[1].bar(index, influx_metricspersec, bar_width, label='influx', color='#fe7f10')
bar4 = axes[1].bar([i + bar_width for i in index], timescale_metricspersec, bar_width, label='timescale', color='#1f77b4')

axes[1].set_xlabel('Dataset Size')
axes[1].set_ylabel('Metrics / second')
axes[1].set_xticks([i + bar_width / 2 for i in index])
axes[1].set_xticklabels(categories)
bars = [ [bar1, bar2], [bar3, bar4] ]

# Add labels above each bar
for item in zip(axes, [rows_per_sec, metrics_mean_rate], bars):
	item[0].legend(loc='upper right', fancybox=True, framealpha=0.5)
	for bar, value in zip(item[2][0], item[1][0]):
		item[0].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
				f'{value/1000:.2f}k ', ha='center', va='bottom')

	for bar, value in zip(item[2][1], item[1][1]):
		item[0].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
				f'{value/1000:.2f}k', ha='center', va='bottom')

plt.show()