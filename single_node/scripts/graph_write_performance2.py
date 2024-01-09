import plotext as plt

database_names = ["influx"]
dataset_sizes = ["small"]

for ds_size in dataset_sizes:
    rows_per_sec = []
    metrics_per_sec = []
    
    for db_name in database_names:
        with open(f"/home/ubuntu/TimeseriesDB_Benchmarks/single_node/performance/write/{db_name}_{ds_size}.out") as f:
            lines = f.readlines()
            for l in lines:
                if l.startswith('loaded'):
                    line = l.split()
                    if "metrics/sec)" in l:
                        metrics_per_sec.append(float(line[-2]))
                    if "rows/sec)" in l:
                        rows_per_sec.append(float(line[-2]))

    plt.bar(database_names, metrics_per_sec, color=['orange', 'purple'])
    plt.title(f"{ds_size.capitalize()} dataset insert performance comparison")
    plt.xlabel("Database")
    plt.ylabel("Metrics / second")
    plt.ylim(bottom=0)  # Set the y-axis lower limit to 0
    plt.xticks(ticks=range(len(database_names)), labels=database_names)
    plt.show()

    plt.bar(database_names, rows_per_sec, color=['orange', 'purple'])
    plt.title(f"{ds_size.capitalize()} dataset insert performance comparison")
    plt.xlabel("Database")
    plt.ylabel("Rows / second")
    plt.ylim(bottom=0)  # Set the y-axis lower limit to 0
    plt.xticks(ticks=range(len(database_names)), labels=database_names)
    plt.show()

