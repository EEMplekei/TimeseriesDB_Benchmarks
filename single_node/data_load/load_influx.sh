#!/bin/bash

# Ensure loader is available
EXE_FILE_NAME=${EXE_FILE_NAME:-$(which tsbs_load_influx)}
if [[ -z "$EXE_FILE_NAME" ]]; then
    echo "tsbs_load_influx not available. It is not specified explicitly and not found in \$PATH"
    exit 1
fi

DATASET_SIZE=${1};
DB_NAME="benchmark_${DATASET_SIZE}";

# Load parameters - common
DATA_FILE_NAME=${DATA_FILE_NAME:-data_influx_${DATASET_SIZE}.dat.gz}
DATABASE_PORT=${DATABASE_PORT:-8086}

if [-f ${DATA_FILE_NAME}]; then
    echo "Data file ${DATA_FILE_NAME} not found"
    exit -1
fi


EXE_DIR=${EXE_DIR:-$(dirname $0)}
source ${EXE_DIR}/load_common.sh

until curl http://${DATABASE_HOST}:${DATABASE_PORT}/ping 2>/dev/null; do
    echo "Waiting for InfluxDB"
    sleep 1
done

# Remove previous database
curl -X POST http://${DATABASE_HOST}:${DATABASE_PORT}/query?q=drop%20database%20${DB_NAME}
# Load new data
cat ${DATA_FILE} | gunzip | $EXE_FILE_NAME \
                                --db-name=${DB_NAME} \
                                --backoff=${BACKOFF_SECS} \
                                --workers=${NUM_WORKERS} \
                                --batch-size=${BATCH_SIZE} \
                                --reporting-period=${REPORTING_PERIOD} \
                                --urls=http://${DATABASE_HOST}:${DATABASE_PORT}
