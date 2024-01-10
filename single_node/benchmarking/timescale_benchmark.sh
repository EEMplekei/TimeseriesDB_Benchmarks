#Prerequisites: timescaledb installed and running, data and queries generated
#!/bin/bash

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color
db_sizes=("small" "medium")
cd ..

##Small, medium datasets
echo -e "${YELLOW}### Loading data into databases${NC}"

# Load into database small, medium datasets
for db in "${db_sizes[@]}"; do
    echo -e "${GREEN}Loading data into InfluxDB for $db dataset${NC}"
    bash data_load/load_timescale.sh "$db"
done

#Run queries for small, medium datasets
echo -e "${YELLOW}### Running scripts to load data into TimescaleDB for small, medium datasets${NC}"
bash queries_execution/run_smallmedium_queries_timescale.sh

echo -e "${YELLOW}### Dropping databases${NC}"

# Drop databases
sudo -i -u postgres
psql
for db in "${db_sizes[@]}"; do
    echo -e "${RED}Dropping database benchmark_$db${NC}"
	drop database benchmark_$db;
done
\q
exit

##Large dataset
# Load into database small, medium datasets
echo -e "${GREEN}Loading data into InfluxDB for large dataset${NC}"
bash data_load/load_timescale.sh large

#Run queries for small, medium datasets
echo -e "${YELLOW}### Running scripts to load data into TimescaleDB for lage dataset${NC}"
bash queries_execution/run_large_queries_timescale.sh

echo -e "${YELLOW}### Dropping databaset${NC}"

# Drop database
sudo -i -u postgres
psql
echo -e "${RED}Dropping database benchmark_$db${NC}"
drop database benchmark_large;
\q
exit

echo -e "${YELLOW}### Clearing TimescaleDB cache${NC}"
# Clear Timescale cache just in case
bash queries_execution/clear_caches/timescale_clr_cache.sh