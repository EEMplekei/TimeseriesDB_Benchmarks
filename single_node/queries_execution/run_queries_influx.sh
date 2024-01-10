#!/bin/bash

# Ensure runner is available
EXE_FILE_NAME=${EXE_FILE_NAME:-$(which tsbs_run_queries_influx)}
if [[ -z "$EXE_FILE_NAME" ]]; then
    echo "tsbs_run_queries_influx not available. It is not specified explicitly and not found in \$PATH"
    exit 1
fi

QUERY_TEST=${1};
DATASET_SIZE=${2};
DB_NAME="benchmark_${DATASET_SIZE}";

# Default queries folder
BULK_DATA_DIR=${BULK_DATA_DIR:-"/home/ubuntu/TimeseriesDB_Benchmarks/single_node/queries_generate/queries/${QUERY_TEST}"}
MAX_QUERIES=${MAX_QUERIES:-"0"}
# How many concurrent worker would run queries - match num of cores, or default to 4
NUM_WORKERS=${NUM_WORKERS:-$(grep -c ^processor /proc/cpuinfo 2> /dev/null || echo 4)}


mkdir -p /home/ubuntu/TimeseriesDB_Benchmarks/single_node/performance/queries/influx/${QUERY_TEST}
rm -f /home/ubuntu/TimeseriesDB_Benchmarks/single_node/performance/queries/influx/${QUERY_TEST}/influx_${QUERY_TEST}_${DATASET_SIZE}.out

function run_file()
{

    FULL_DATA_FILE_NAME=$1
    DATA_FILE_NAME=$(basename -- "${FULL_DATA_FILE_NAME}")
    DIR=$(dirname "${FULL_DATA_FILE_NAME}")
    EXTENSION="${DATA_FILE_NAME##*.}"
    NO_EXT_DATA_FILE_NAME="${DATA_FILE_NAME%.*}"

    OUT_FULL_FILE_NAME=${OUT_FULL_FILE_NAME:-"/home/ubuntu/TimeseriesDB_Benchmarks/single_node/performance/queries/influx/${QUERY_TEST}/influx_${QUERY_TEST}_${DATASET_SIZE}.out"};

    if [ "${EXTENSION}" == "gz" ]; then
        GUNZIP="gunzip"
    else
        GUNZIP="cat"
    fi

    echo "Running ${DATA_FILE_NAME}"
    cat $FULL_DATA_FILE_NAME \
        | $GUNZIP \
        | $EXE_FILE_NAME \
            --db-name $DB_NAME \
            --max-queries $MAX_QUERIES \
            --workers $NUM_WORKERS >> $OUT_FULL_FILE_NAME
}

if [ "$#" -gt 0 ]; then
    for FULL_DATA_FILE_NAME in ${BULK_DATA_DIR}/queries_influx/${DATASET_SIZE}/*; do
        run_file $FULL_DATA_FILE_NAME
    done
else
    echo "Do not have any queries to run. Your parameters are not right."
fi
