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
    fig.suptitle(f'Single node deployment\nComparison of timescale and influx for each query type, 10 queries')
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

# These results show us that the two timeseries database systems execute queries differently. We can see query types that have very large differences in execution speed.
# Beneath is a brief explanation of each query type label and the corresponding SQL query. This will assist us in understanding why some queries are faster than others on each database system.

# average driver driving duration per day - avg-daily-driving-duration
# Calculate average daily driving duration per driver
# `SELECT count("mv")/6 as "hours driven" 
# 		FROM (SELECT mean("velocity") as "mv" 
# 		 FROM "readings" 
# 		 WHERE time > '%s' AND time < '%s' 
# 		 GROUP BY time(10m),"fleet", "name", "driver") 
# 		WHERE time > '%s' AND time < '%s' 
# 		GROUP BY time(1d),"fleet", "name", "driver"`

# average driver driving session without stopping per day - avg-daily-driving-session
# Get trucks which haven't rested for at least 20 mins in the last 4 hours
# WITH driver_status
# 		AS (
# 			SELECT tags_id, time_bucket('10 mins', TIME) AS ten_minutes, avg(velocity) > 5 AS driving
# 			FROM readings
# 			GROUP BY tags_id, ten_minutes
# 			ORDER BY tags_id, ten_minutes
# 			), driver_status_change
# 		AS (
# 			SELECT tags_id, ten_minutes AS start, lead(ten_minutes) OVER (PARTITION BY tags_id ORDER BY ten_minutes) AS stop, driving
# 			FROM (
# 				SELECT tags_id, ten_minutes, driving, lag(driving) OVER (PARTITION BY tags_id ORDER BY ten_minutes) AS prev_driving
# 				FROM driver_status
# 				) x
# 			WHERE x.driving <> x.prev_driving
# 			)
# 		SELECT t.%s, time_bucket('24 hours', start) AS day, avg(age(stop, start)) AS duration
# 		FROM tags t
# 		INNER JOIN driver_status_change d ON t.id = d.tags_id
# 		WHERE t.%s IS NOT NULL
# 		AND d.driving = true
# 		GROUP BY name, day
# 		ORDER BY name, day`

# average load per truck model per fleet - avg-load
# Calculate average load per truck model per fleet
# `SELECT mean("ml") AS mean_load_percentage 
# 		FROM (SELECT "current_load"/"load_capacity" AS "ml" 
# 		 FROM "diagnostics" 
# 		 GROUP BY "name", "fleet", "model") 
# 		GROUP BY "fleet", "model"`

# average vs projected fuel consumption per fleet - avg-vs-projected-fuel-consumption
# Calculate average vs. projected fuel consumption per fleet
# `SELECT mean("fuel_consumption") AS "mean_fuel_consumption", mean("nominal_fuel_consumption") AS "nominal_fuel_consumption" 
# 		FROM "readings" 
# 		WHERE "velocity" > 1 
# 		GROUP BY "fleet"`

# truck breakdown frequency per model - breakdown-frequency
# Calculate breakdown frequency by truck model
# FROM (SELECT difference("broken_down") AS "state_changed" 
# 		 FROM (SELECT floor(2*(sum("nzs")/count("nzs")))/floor(2*(sum("nzs")/count("nzs"))) AS "broken_down" 
# 		  FROM (SELECT "model", "status"/"status" AS nzs 
# 		   FROM "diagnostics" 
# 		   WHERE time >= '%s' AND time < '%s') 
# 		  WHERE time >= '%s' AND time < '%s' 
# 		  GROUP BY time(10m),"model") 
# 		 GROUP BY "model") 
# 		WHERE "state_changed" = 1 
# 		GROUP BY "model"`,

# daily truck activity per fleet per model - daily-activity
# Get the number of hours truck has been active (vs. out-of-commission) per day per fleet
# `SELECT count("ms")/144 
# 		FROM (SELECT mean("status") AS ms 
# 		 FROM "diagnostics" 
# 		 WHERE time >= '%s' AND time < '%s' 
# 		 GROUP BY time(10m), "model", "fleet") 
# 		WHERE time >= '%s' AND time < '%s' AND "ms"<1 
# 		GROUP BY time(1d), "model", "fleet"


# trucks with high load
# Fetch trucks with high current load (over 90% load capacity)
# `SELECT "name", "driver", "current_load", "load_capacity" 
# 		FROM (SELECT  "current_load", "load_capacity" 
# 		 FROM "diagnostics" WHERE fleet = '%s' 
# 		 GROUP BY "name","driver" 
# 		 ORDER BY "time" DESC 
# 		 LIMIT 1) 
# 		WHERE "current_load" >= 0.9 * "load_capacity" 
# 		GROUP BY "name" 
# 		ORDER BY "time" DESC`

# last location per truck - last-loc
# Fetch real-time (i.e. last) location of each truck
# `SELECT "latitude", "longitude" 
# 		FROM "readings" 
# 		WHERE "fleet"='%s' 
# 		GROUP BY "name","driver" 
# 		ORDER BY "time" 
# 		LIMIT 1`

# trucks with longer driving sessions - long-daily-sessions
# Get trucks which haven't rested for at least 20 mins in the last 4 hours
# `SELECT "name","driver" 
# 		FROM(SELECT count(*) AS ten_min 
# 		 FROM(SELECT mean("velocity") AS mean_velocity 
# 		  FROM readings 
# 		  WHERE "fleet" = '%s' AND time > '%s' AND time <= '%s' 
# 		  GROUP BY time(10m),"name","driver") 
# 		 WHERE "mean_velocity" > 1 
# 		 GROUP BY "name","driver") 
# 		WHERE ten_min_mean_velocity > %d`

# trucks with low fuel - low-fuel
# Fetch all trucks with low fuel (less than 10%)
# `SELECT "name", "driver", "fuel_state" 
# 		FROM "diagnostics" 
# 		WHERE "fuel_state" <= 0.1 AND "fleet" = '%s' 
# 		GROUP BY "name" 
# 		ORDER BY "time" DESC 
# 		LIMIT 1`

# stationary trucks - stationary-trucks
# Fetch all trucks that are stationary (low avg velocity in last 10 mins)
# `SELECT "name", "driver" 
# 		FROM(SELECT mean("velocity") as mean_velocity 
# 		 FROM "readings" 
# 		 WHERE time > '%s' AND time <= '%s' 
# 		 GROUP BY time(10m),"name","driver","fleet"  
# 		 LIMIT 1) 
# 		WHERE "fleet" = '%s' AND "mean_velocity" < 1 
# 		GROUP BY "name"`
