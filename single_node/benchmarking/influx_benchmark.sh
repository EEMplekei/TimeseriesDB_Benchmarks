#Prerequisites: influxdb installed and running, data and queries generated
#!/bin/bash

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color
db_sizes=("small" "medium" "large")
cd ..

echo -e "${YELLOW}### Loading data into databases${NC}"

# Load into database small, medium, large datasets
for db in "${db_sizes[@]}"; do
    echo -e "${GREEN}Loading data into InfluxDB for $db dataset${NC}"
    bash data_load/load_influx.sh "$db"
done

#Run queries for small, medium, large datasets
echo -e "${YELLOW}### Running scripts to load data into InfluxDB for small, medium, large datasets${NC}"
bash queries_execution/run_all_queries_influx.sh

echo -e "${YELLOW}### Dropping databases${NC}"

# Drop databases
for db in "${db_sizes[@]}"; do
    echo -e "${RED}Dropping database benchmark_$db${NC}"
    influx -execute "drop database benchmark_$db"
done

echo -e "${YELLOW}### Clearing InfluxDB cache${NC}"
# Clear InfluxDB cache just in case
bash queries_execution/clear_caches/influx_clr_cache.sh