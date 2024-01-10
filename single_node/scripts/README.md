# Scripts Explanation:
This folder contains python scripts mainly for ploting the benchmarks about the two compared databases. In this file we will provide a brief explanation for each script and its utility.

## measure_db_size_parametrizable:
* To run this script, execute the following command:

```
python3 measure_db_size_parametrizable {database} {dataset_size}
```
This script retrieves the disk size of a database ,specified by the parameters. For this purpose we use the command "du -h --apparent-size" in the appropriate directories based on database type (influx or timescale)

## graph_write_performance:
* To run this script, execute the following command:

```
python3 graph_write_performance
```
This script retrieves the performance of dataset insertion on databases. Specifically it keeps track of the number of metrics and rows per second that each database can achieve. Finally these benchmarks will be ploted in a graph (one for metrics/sec and one for rows/sec)

## parse_file:

## avg_query_plot:
* To run this script, execute the following command:

```
python3 avg_query_plot
```

