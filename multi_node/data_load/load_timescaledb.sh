#!/bin/bash

# Ensure loader is available
EXE_FILE_NAME=${EXE_FILE_NAME:-$(which tsbs_load_timescaledb)}
if [[ -z "$EXE_FILE_NAME" ]]; then
    echo "tsbs_load_timescaledb not available. It is not specified explicitly and not found in \$PATH"
    exit 1
fi

DATASET_SIZE=${1};
# Load parameters - common
DATA_FILE_NAME=${DATA_FILE_NAME:-data_timescaledb_${DATASET_SIZE}.dat.gz}

if [ -f ${DATA_FILE_NAME} ]; then
    echo "Data file ${DATA_FILE_NAME} not found"
    exit -1
fi

DATABASE_USER=${DATABASE_USER:-postgres}
DATABASE_NAME=${DATABASE_NAME:-benchmark_${DATASET_SIZE}}
DATABASE_HOST=${DATABASE_HOST:-localhost}
DATABASE_PORT=${DATABASE_PORT:-5432}
DATABASE_PWD=${DATABASE_PWD:-password}
# Load parameters - personal
CHUNK_TIME=${CHUNK_TIME:-8h}
PARTITIONS=${PARTITIONS:-0}
HASH_WORKERS=${HASH_WORKERS:-false}
TIME_PARTITION_INDEX=${TIME_PARTITION_INDEX:-false}
PERF_OUTPUT=${PERF_OUTPUT:-}
JSON_TAGS=${JSON_TAGS:-false}
IN_TABLE_PARTITION_TAG=${IN_TABLE_PARTITION_TAG:-true}
USE_HYPERTABLE=${USE_HYPERTABLE:-true}
DO_CREATE_DB=${DO_CREATE_DB:-false}
FORCE_TEXT_FORMAT=${FORCE_TEXT_FORMAT:-false}
USE_COPY=${USE_COPY:-true}
REPLICATION_FACTOR=${REPLICATION_FACTOR:-1}
CREATE_METRICS_TABLE=${CREATE_METRICS_TABLE:-true}
PARTITION_ON_HOSTNAME=${PARTITION_ON_HOSTNAME:-false}

EXE_DIR=${EXE_DIR:-$(dirname $0)}
source ${EXE_DIR}/load_common.sh

while ! pg_isready -h ${DATABASE_HOST} -p ${DATABASE_PORT}; do
    echo "Waiting for timescaledb"
    sleep 1
done

mkdir -p ../performance/write

cat ${DATA_FILE} | gunzip | $EXE_FILE_NAME \
                                --postgres="sslmode=disable" \
                                --db-name=${DATABASE_NAME} \
                                --host=${DATABASE_HOST} \
                                --port=${DATABASE_PORT} \
                                --pass=${DATABASE_PWD} \
                                --user=${DATABASE_USER} \
                                --workers=${NUM_WORKERS} \
                                --batch-size=${BATCH_SIZE} \
                                --reporting-period=${REPORTING_PERIOD} \
                                --use-hypertable=${USE_HYPERTABLE} \
                                --use-jsonb-tags=${JSON_TAGS} \
                                --in-table-partition-tag=${IN_TABLE_PARTITION_TAG} \
                                --hash-workers=${HASH_WORKERS} \
                                --time-partition-index=${TIME_PARTITION_INDEX} \
                                --partitions=${PARTITIONS} \
                                --chunk-time=${CHUNK_TIME} \
                                --write-profile=${PERF_OUTPUT} \
                                --field-index-count=1 \
                                --do-create-db=${DO_CREATE_DB} \
                                --force-text-format=${FORCE_TEXT_FORMAT} \
                                --replication-factor=${REPLICATION_FACTOR} \
                                --create-metrics-table=${CREATE_METRICS_TABLE} | tee ~/TimeseriesDB_Benchmarks/multi_node/performance/write/timescale_${DATASET_SIZE}.out
