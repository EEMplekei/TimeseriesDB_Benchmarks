#!/bin/bash

# Ensure generator is available
EXE_FILE_NAME=${EXE_FILE_NAME:-$(which tsbs_generate_data)}
if [[ -z "${EXE_FILE_NAME}" ]]; then
    echo "tsbs_generate_data not available. It is not specified explicitly and not found in \$PATH"
    exit 1
fi

# Data folder
BULK_DATA_DIR=${BULK_DATA_DIR:- "$(pwd)/iot_data"}

# Space-separated list of target DB formats to generate
FORMATS=${FORMATS:-"timescaledb influx"}

# Number of hosts to generate data about
SCALE=${SCALE:-"800"}

# Rand seed
SEED=${SEED:-"123"}

# Start and stop time for generated timeseries
TS_START=${TS_START:-"2023-01-01T00:00:00Z"}
TS_ENDS=${TS_ENDS:-"2023-01-01T10:00:00Z 2023-01-03T02:00:00Z 2023-01-07T06:00:00Z"}

# What set of data to generate: devops (multiple data), cpu-only (cpu-usage data)
USE_CASE=${USE_CASE:-"iot"}

# Step to generate data
LOG_INTERVAL=${LOG_INTERVAL:-"10s"}

# Max number of points to generate data. 0 means "use TS_START TS_END with LOG_INTERVAL"
MAX_DATA_POINTS=${MAX_DATA_POINTS:-"0"}

# Ensure DATA DIR available
mkdir -p ${BULK_DATA_DIR}
chmod a+rwx ${BULK_DATA_DIR}

pushd ${BULK_DATA_DIR}
set -eo pipefail

# Lo/home/ubuntu/TimeseriesDB_Benchmarks/data_generate/iot_dataop over all requested target formats and generate data
for FORMAT in ${FORMATS}; do

    for TS_END in ${TS_ENDS}; do

        if [ $TS_END == "2023-01-01T10:00:00Z" ]; then
            DATASET_SIZE="small"
        elif [ $TS_END == "2023-01-03T02:00:00Z" ]; then
            DATASET_SIZE="medium"
        elif [ $TS_END == "2023-01-07T06:00:00Z" ]; then
            DATASET_SIZE="large"
        fi

        DATA_FILE_NAME="data_${FORMAT}_${DATASET_SIZE}.dat.gz"
        if [ -f "${DATA_FILE_NAME}" ]; then
            echo "WARNING: file ${DATA_FILE_NAME} already exists, skip generating new data"
        else
            cleanup() {
                rm -f ${DATA_FILE_NAME}
                exit 1
            }
            trap cleanup EXIT

            echo "Generating ${DATA_FILE_NAME}:"
            ${EXE_FILE_NAME} \
                --format ${FORMAT} \
                --use-case ${USE_CASE} \
                --scale ${SCALE} \
                --timestamp-start ${TS_START} \
                --timestamp-end ${TS_END} \
                --seed ${SEED} \
                --log-interval ${LOG_INTERVAL} \
                --max-data-points ${MAX_DATA_POINTS} \
            | gzip > ${DATA_FILE_NAME}

            trap - EXIT
        fi
    done
done
