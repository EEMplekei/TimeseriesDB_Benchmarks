# Query execution

This folder contains scripts and tools for benchmarking two popular timeseries databases, InfluxDB and TimescaleDB. The benchmarking process includes running predefined queries on databases of different sizes and analyzing the performance.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Running Benchmark](#running-benchmark)
- [Results](#results)
- [Additional Notes](#additional-notes)

## Prerequisites

Queries should be generated beforehand using the scripts in [queries_generate](https://github.com/EEMplekei/TimeseriesDB_Benchmarks/tree/main/single_node/queries_generate) folder. If now the execution scripts will fail.

## Running Benchmark

* To run the benchmark, execute the following commands:

```bash
bash execution_scripts/run_queries_{timeseries_database}.sh {query_size} {db_size}
```
- {timeseries_database} : 
- {query_size}: size of the generated query count. The script in [queries_generate](https://github.com/EEMplekei/TimeseriesDB_Benchmarks/tree/main/single_node/queries_generate) generate default values of 1, 10, 100 and 100 and thus these values can be *1_queries*, *10_queries* or *100_queries*.
- {db_size} The size of the database dataset. Should be *small*, *medium* or *large*

To run all influx queries all you have  to do is execute the `run_all_queries_influx.sh` bash script which takes care of all the calls of the `execution_scripts/run_queries_influx.sh` with the correct parameters. It also clears the cache between each call so that prior queries do not affect the performance of subsequent calls
```bash
bash run_all_queries_influx.sh
```

The same applies for scripts `run_smallmedium_queries_timescale.sh` and `run_smallmedium_large_timescale.sh`.
---

## Additional Notes

- **Executable Paths:** Ensure that the required executables (`tsbs_run_queries_influx` and `tsbs_run_queries_timescaledb`) are in your system's PATH or specify their paths explicitly in the scripts.

- **Database Configurations:** Customize the database configurations, such as names, ports, and passwords, in the respective scripts based on your setup.

- **Script Parameters:** Adjust the script parameters, such as the number of workers and maximum queries, according to your system's capabilities.

- **Multiple timescale query execution scripts:** The benchmarking system was developed/tested/deployed on a machine with limited disk size that timescale could not have all of the databases loaded simultaneously, so that 2 scripts have to be run. The script `run_smallmedium_queries_timescale.sh` runs the *small* and *medium* database sizes and the `run_large_queries_timescale.sh` runs for the *large* database.