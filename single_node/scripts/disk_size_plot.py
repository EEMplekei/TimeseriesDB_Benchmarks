import matplotlib.pyplot as plt
color_map = {'timescale': '#1f77b4', 'influx': '#ff7f0e'}
file_path = '../performance/disk/size_on_disk.out'

try:
    # Read data from the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Parse the values from the lines
    data = {}
    for line in lines:
        key, value = line.strip().split(':')
        metric, size = key.split('-')
        data.setdefault(metric, {})[size] = float(float(value)/(1000 ** 3))  # converting to float

    # Check if all pairs exist
    categories = ['small', 'medium', 'large']
    missing_pairs = []

    for metric in ['timescale', 'influx']:
        for category in categories:
            if category not in data.get(metric, {}):
                missing_pairs.append(f"{metric}-benchmark_{category}")

    if missing_pairs:
        error_message = f"One or more databases are missing: {', '.join(missing_pairs)}. Please create them before running this script or check the input file."
        raise ValueError(error_message)
    else:
        # Plotting, we have everything
        timescale_values = [data['timescale'][category]
                            for category in categories]
        influx_values = [data['influx'][category] for category in categories]

        bar_width = 0.35
        index = range(len(categories))

        fig, ax = plt.subplots()
        bar1 = ax.bar(index, influx_values, bar_width, label='influx', color = color_map.get('influx'))
        bar2 = ax.bar([i + bar_width for i in index],
                      timescale_values, bar_width, label='timescale', color = color_map.get('timescale'))

        ax.set_xlabel('Category')
        ax.set_ylabel('Size (G)')
        ax.set_title('Comparison of timescale and influx database disk sizes')
        ax.set_xticks([i + bar_width / 2 for i in index])
        ax.set_xticklabels(categories)
        ax.legend()

        # Add labels above each bar
        for bar, value in zip(bar1, timescale_values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                    f'{value:.2f}G', ha='center', va='bottom')

        for bar, value in zip(bar2, influx_values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                    f'{value:.2f}G', ha='center', va='bottom')

        plt.show()

except FileNotFoundError:
    print(f"Error: File '{file_path}' not found. Please check the file path.")
except ValueError as e:
    print("Error:", e)
    # Terminate the script
