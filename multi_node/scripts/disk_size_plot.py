import matplotlib.pyplot as plt
import numpy as np

color_map = {'timescale': {'B_size': '#1f77b4', 'C_size': '#aec7e8'},
             'influx': {'B_size': '#ff7f0e', 'C_size': '#ffbb78'}}
file_path = '../performance/disk/size_on_disk.out'

try:
    # Read data from the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Parse the values from the lines
    data = {'influx': {'B_size': [], 'C_size': []}, 'timescale': {'B_size': [], 'C_size': []}}
    categories = ['small', 'medium', 'large']

    for line in lines:
        key, value = line.strip().split(':')
        metric, size = key.split('-')
        b_pair, c_pair = value.split(',')
        b, b_size = b_pair.split('=')
        c, c_size = c_pair.split('=')

        data[metric]['B_size'].append(float(b_size) / (1000 ** 3))  # Convert to GB
        data[metric]['C_size'].append(float(c_size) / (1000 ** 3))  # Convert to GB

    # Plotting, we have everything
    timescale_values_B = data['timescale']['B_size']
    influx_values_B = data['influx']['B_size']
    timescale_values_C = data['timescale']['C_size']
    influx_values_C = data['influx']['C_size']

    bar_width = 0.2
    index = range(len(categories))
   
    fig, ax = plt.subplots()
    bar1 = ax.bar(index, influx_values_B, bar_width, label='Influx data node B', color = color_map.get('influx', {}).get('B_size', None))
    bar2 = ax.bar([i + bar_width for i in index],
                    influx_values_C, bar_width, label='Influx data node C', color = color_map.get('influx', {}).get('C_size', None))
    bar3 = ax.bar([i + 2*bar_width for i in index], timescale_values_B, bar_width, label='Timescale data node B', color = color_map.get('timescale', {}).get('B_size', None))
    bar4 = ax.bar([i + 3*bar_width for i in index],
                    timescale_values_C, bar_width, label='Timescale data node C', color = color_map.get('timescale', {}).get('C_size', None))

    ax.set_xlabel('Category')
    ax.set_ylabel('Size (Gb)')
    ax.set_title('Multi node deployment\nComparison of timescale and influx database disk sizes\non each data node', fontsize = 12)
    # Modify the x-ticks to be at the center of each group of bars
    ax.set_xticks([i + bar_width*(len(categories)) / 2 for i in index])
    ax.set_xticklabels(categories)
    ax.legend()

    #Add labels above each bar
    for bar, value in zip(bar1, influx_values_B):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                f'{value:.2f}Gb', ha='center', va='bottom').set_size(6)

    for bar, value in zip(bar2, influx_values_C):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                f'{value:.2f}Gb', ha='center', va='bottom').set_size(6)

    for bar, value in zip(bar3, timescale_values_B):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                f'{value:.2f}Gb', ha='center', va='bottom').set_size(6)

    for bar, value in zip(bar4, timescale_values_C):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                f'{value:.2f}Gb', ha='center', va='bottom').set_size(6)


    plt.show()

except FileNotFoundError:
    print(f"Error: File '{file_path}' not found. Please check the file path.")
except ValueError as e:
    print("Error:", e)
    # Terminate the script
