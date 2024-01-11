GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
RESET='\033[0m'
DATABASE_SIZES=("small" "medium" "large")
QUERY_COUNTS=("1" "10")

echo -e "${GREEN}Running all queries for influxdb. This will take a while...\n"

for SIZE in "${DATABASE_SIZES[@]}"; do
  for COUNT in "${QUERY_COUNTS[@]}"; do
    echo -e "${RED}Running ${COUNT} queries for ${SIZE} database...${RESET}\n"
    #run query for specified size and count
    bash execution_scripts/run_queries_influx.sh "${COUNT}_queries" "${SIZE}"
    echo -e "${BLUE}Finished running ${COUNT} queries for ${SIZE} database. Clearing caches...${RESET}\n"
    #cleer cache before running next query
    bash clear_caches/influx_clr_cache.sh
    echo
  done
done

