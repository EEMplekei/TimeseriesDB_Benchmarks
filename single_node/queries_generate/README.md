

# Query generation scripts

This folders contains the scripts for generating timeseries queries using `tsbs_generate_queries` and a helper script to automate the generation with different query counts. It generates 1, 10, 100, 1000 queries to test the scaling of the database against multiple queries execution of the same kind.

## Prerequisites

- [tsbs_generate_queries](https://github.com/timescale/tsbs) must be installed and available in your system. It comes with TSBS package, whose installation is in the [single_node README](https://github.com/EEMplekei/TimeseriesDB_Benchmarks/tree/main/single_node)

## Usage

### 1. Generate Queries

The script `generate_queries.sh` generates timeseries queries using `tsbs_generate_queries`. It takes the number of queries as a command-line argument.

```bash
bash generate_queries.sh <number_of_queries>
```
Replace _<number_of_queries>_ with disirable number of queries.

*This should no be used on it's own and the helper `generate_all_queries.sh` script should be used*

### 2. Helper Script

The helper script `helper_script.sh` automates the generation of queries for multiple query counts. It calls `generate_queries.sh` with predefined values.

```bash
bash helper_script.sh
```
## Directory Structure
A folder named _queries_ is generated containing all the queries for the two databases, InfluxDB and TimescaleDB.

- `queries`: Main folder for generated queries with subfolders for different query counts..
  - `queries/{number_of_queries}_queries/`: Subfolder containing the specified amount of queries for each query type for both databases.
    - `queries_timescaledb/`: Subfolder containing queries in TimescaleDB format.
      - `small/`: Subfolder for small-sized dataset.
      - `medium/`: Subfolder for medium-sized dataset.
      - `large/`: Subfolder for large-sized dataset.
    - `queries_influx/`: Subfolder containing queries in InfluxDB format.
      - `small/`: Subfolder for small-sized dataset.
      - `medium/`: Subfolder for medium-sized dataset.
      - `large/`: Subfolder for large-sized dataset.


