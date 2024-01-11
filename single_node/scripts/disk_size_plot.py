import matplotlib.pyplot as plt

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
        data.setdefault(metric, {})[size] = float(value[:-1])  # Removing 'G' and converting to float

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
        # Plotting
        timescale_values = [data['timescale'][category] for category in categories]
        influx_values = [data['influx'][category] for category in categories]

        bar_width = 0.35
        index = range(len(categories))

        fig, ax = plt.subplots()
        bar1 = ax.bar(index, timescale_values, bar_width, label='timescale')
        bar2 = ax.bar([i + bar_width for i in index], influx_values, bar_width, label='influx')

        ax.set_xlabel('Category')
        ax.set_ylabel('Size (G)')
        ax.set_title('Comparison of timescale and influx database disk sizes')
        ax.set_xticks([i + bar_width / 2 for i in index])
        ax.set_xticklabels(categories)
        ax.legend()

        plt.show()

except FileNotFoundError:
    print(f"Error: File '{file_path}' not found. Please check the file path.")
except ValueError as e:
    print("Error:", e)
    # Terminate the script or perform additional error handling here
