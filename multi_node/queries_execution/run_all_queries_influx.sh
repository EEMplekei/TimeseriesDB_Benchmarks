GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
RESET='\033[0m'
DATABASE_SIZES=("small" "medium" "large")
QUERY_COUNTS=("1" "10")

echo -e "${GREEN}Starting proccess for running all queries for influx. First starting with clearing caches.${RESET}\n"

#bash clear_caches/influx_clr_cache.sh
#echo -e "Local cache cleared"
ssh ubuntu@10.0.0.2 "bash influx_clr_cache.sh" &
wait
echo -e "NodeB cache cleared"
ssh ubuntu@10.0.0.3 "bash influx_clr_cache.sh" &
wait
echo -e "NodeC cache cleared"

echo -e "${GREEN}Running all queries for influxdb. This will take a while...\n"

for SIZE in "${DATABASE_SIZES[@]}"; do
	for COUNT in "${QUERY_COUNTS[@]}"; do
		echo -e "${RED}Running ${COUNT} queries for ${SIZE} database...${RESET}\n"
		#run query for specified size and count
		bash ./execution_scripts/run_queries_influx.sh "${COUNT}_queries" "${SIZE}"
		echo -e "${BLUE}Finished running ${COUNT} queries for ${SIZE} database. Clearing caches...${RESET}\n"
		#clear cache before running next query
		ssh ubuntu@10.0.0.2 "bash influx_clr_cache.sh" &
		wait
		ssh ubuntu@10.0.0.3 "bash influx_clr_cache.sh" &   
		wait    
		#bash ./clear_caches/influx_clr_cache.sh
		echo
	done
done

