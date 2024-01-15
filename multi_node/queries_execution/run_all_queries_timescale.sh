GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
RESET='\033[0m'
DATABASE_SIZES=("small" "medium" "large")
QUERY_COUNTS=("1" "10")

echo -e "${GREEN}Running all queries for timescaledb. This will take a while...\n"

for SIZE in "${DATABASE_SIZES[@]}"; do
	for COUNT in "${QUERY_COUNTS[@]}"; do
		echo -e "${RED}Running ${COUNT} queries for ${SIZE} database...${RESET}\n"
		bash execution_scripts/run_queries_timescale.sh "${COUNT}_queries" "${SIZE}"
		echo -e "${BLUE}Finished running ${COUNT} queries for ${SIZE} database. Clearing local and remote caches...${RESET}\n"
		bash clear_caches/timescale_clr_cache.sh
		ssh ubuntu@10.0.0.2 "bash timescale_clr_cache.sh"
		ssh ubuntu@10.0.0.3 "bash timescale_clr_cache.sh"
		echo -e
	done
done
