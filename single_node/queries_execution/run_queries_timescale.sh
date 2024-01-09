#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Ensure runner is available
EXE_FILE_NAME=${EXE_FILE_NAME:-$(which tsbs_run_queries_timescaledb)}
if [[ -z "$EXE_FILE_NAME" ]]; then
    echo "tsbs_run_queries_timescaledb not available. It is not specified explicitly and not found in \$PATH"
    exit 1
fi

QUERY_TEST=${1};
DATASET_SIZE=${2};

DATABASE_NAME="benchmark_${2}"
DATABASE_PORT=5432;
DATABASE_PASSWORD="password";

# Queries folder
BULK_DATA_DIR=${BULK_DATA_DIR:-"/home/ubuntu/TimeseriesDB_Benchmarks/single_node/queries_generate/queries/${QUERY_TEST}"};

# How many queries would be run
MAX_QUERIES=${MAX_QUERIES:-"0"}

# How many concurrent worker would run queries - match num of cores, or default to 4
NUM_WORKERS=${NUM_WORKERS:-$(grep -c ^processor /proc/cpuinfo 2> /dev/null || echo 4)}

mkdir -p /home/ubuntu/TimeseriesDB_Benchmarks/single_node/performance/queries
mkdir -p /home/ubuntu/TimeseriesDB_Benchmarks/single_node/performance/queries/timescaledb
mkdir -p /home/ubuntu/TimeseriesDB_Benchmarks/single_node/performance/queries/timescaledb/${QUERY_TEST}
rm -f /home/ubuntu/TimeseriesDB_Benchmarks/single_node/performance/queries/timescaledb/${QUERY_TEST}/timescale_${QUERY_TEST}_${DATASET_SIZE}.out

for FULL_DATA_FILE_NAME in ${BULK_DATA_DIR}/queries_timescaledb/${DATASET_SIZE}/*; do

    DATA_FILE_NAME=$(basename -- "${FULL_DATA_FILE_NAME}")
    DIR=$(dirname "${FULL_DATA_FILE_NAME}")
    EXTENSION="${DATA_FILE_NAME##*.}"
    NO_EXT_DATA_FILE_NAME="${DATA_FILE_NAME%.*}"
    


    OUT_FULL_FILE_NAME=${OUT_FULL_FILE_NAME:-"/home/ubuntu/TimeseriesDB_Benchmarks/single_node/performance/queries/timescaledb/${QUERY_TEST}/timescale_${QUERY_TEST}_${DATASET_SIZE}.out"};
    
    if [ "${EXTENSION}" == "gz" ]; then
        GUNZIP="gunzip"
    else
        GUNZIP="cat"
    fi

    echo "Running ${DATA_FILE_NAME}"
    cat $FULL_DATA_FILE_NAME \
        | $GUNZIP \
        | $EXE_FILE_NAME \
            --max-queries $MAX_QUERIES \
            --workers $NUM_WORKERS \
	        --db-name $DATABASE_NAME \
	        --port $DATABASE_PORT \
            --pass $DATABASE_PASSWORD >> $OUT_FULL_FILE_NAME;
    done