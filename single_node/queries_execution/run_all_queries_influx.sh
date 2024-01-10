GREEN='\033[0;32m'
RED='\033[0;31m'
RESET='\033[0m'
DATABASE_SIZES=("small" "medium" "large")
QUERY_COUNTS=("1" "10" "100" "1000")

echo -e "${GREEN}Running all queries for influxdb. This will take a while...\n"

for SIZE in "${DATABASE_SIZES[@]}"; do
  for COUNT in "${QUERY_COUNTS[@]}"; do
    echo -e "${RED}Running ${COUNT} queries for ${SIZE} database...${RESET}\n"
    bash run_queries_influx.sh "${COUNT}_queries" "${SIZE}"
    echo
  done
done

