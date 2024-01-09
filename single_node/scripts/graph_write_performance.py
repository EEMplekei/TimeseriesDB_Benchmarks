import matplotlib.pyplot as plt

database_names = ["influx"]
dataset_sizes = ["small", "medium", "large"]

pairs_all = [(db, size) for db in database_names for size in dataset_sizes]

# Create a single figure with subplots
fig, axes = plt.subplots(2, 1, figsize=(8, 6))

for pair in pairs_all:
    rows_per_sec = []
    metrics_per_sec = []
    with open(f"../performance/write/{pair[0]}_{pair[1]}.out") as f:
        lines = f.readlines()
        for l in lines:
            if l.startswith('loaded'):
                line = l.split(' ')
                if "metrics/sec)" in l:
                    metrics_per_sec.append(float(line[-2]))
                if "rows/sec)" in l:
                    rows_per_sec.append(float(line[-2]))

    # Use the index to access the appropriate subplot
    ax1, ax2 = axes

    ax1.bar(str(pair), metrics_per_sec, color=['orange', 'purple'], width=0.2)
    ax2.bar(str(pair), rows_per_sec, color=['orange', 'purple'], width=0.2)

    ax1.set_ylabel("Metrics / second")
    ax2.set_xlabel("Database, Dataset Size")
    ax2.set_ylabel("Rows / second")

# Set common xlabel for the last subplot
ax2.set_xlabel("Database, Dataset Size")

# Set title for the entire figure
fig.suptitle("Dataset insert performance comparison")

plt.show()
