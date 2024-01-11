import matplotlib.pyplot as plt

# Define a function to assign numerical values to sizes
def size_order(size):
    size_order_dict = {"small": 1, "medium": 2, "large": 3}
    return size_order_dict.get(size, 0)

database_names = ["timescale", "influx"]
dataset_sizes = ["small", "medium", "large"]

pairs_all = [(db, size) for db in database_names for size in dataset_sizes]
# Sort the pairs based on the custom size_order function
pairs_all = sorted(pairs_all, key=lambda pair: size_order(pair[1]))
# Define colors for each database
color_map = {"timescale": "#1f77b4", "influx": "#fe7f10"}

# Create a single figure with subplots
fig, axes = plt.subplots(2, 1, figsize=(10, 8))

for pair in pairs_all:
    rows_per_sec = []
    metrics_per_sec = []
    try:
        with open(f"../performance/write/{pair[0]}_{pair[1]}.out") as f:
            lines = f.readlines()
            for l in lines:
                if l.startswith('loaded'):
                    line = l.split(' ')
                    if "metrics/sec)" in l:
                        metrics_per_sec.append(float(line[-2]))
                    if "rows/sec)" in l:
                        rows_per_sec.append(float(line[-2]))

    except FileNotFoundError:
        print(f"File not found: ../performance/write/{pair[0]}_{pair[1]}.out")
    except Exception as e:
        print(f"File not found: ../performance/write/{pair[0]}_{pair[1]}.out :{e}")
    # Use the index to access the appropriate subplot
    ax1, ax2 = axes

    # Assign colors based on the database name
    color = color_map.get(pair[0], "gray")

    ax1.bar(str(pair[0]) + " - " + str(pair[1]), metrics_per_sec, color=color, width=0.4)
    ax2.bar(str(pair[0]) + " - " + str(pair[1]), rows_per_sec, color=color, width=0.4)

    ax1.set_ylabel("Metrics / second")
    ax2.set_xlabel("Database, Dataset Size")
    ax2.set_ylabel("Rows / second")

# Set common xlabel for the last subplot
ax2.set_xlabel("Database - Dataset Size")

# Set title for the entire figure
fig.suptitle("Dataset insert performance comparison")

# Rotate x-axis tick labels
for ax in axes:
    ax.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()
