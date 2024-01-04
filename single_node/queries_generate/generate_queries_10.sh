#/bin/bash

# Ensure generator is available
EXE_FILE_NAME=${EXE_FILE_NAME:-$(which tsbs_generate_queries)}
if [[ -z "${EXE_FILE_NAME}" ]]; then
	echo "tsbs_generate_queries not available. It is not specified explicitly and not found in \$PATH"
	exit 1
fi

# Queries folder
BULK_DATA_DIR=${BULK_DATA_DIR:-"/home/ubuntu/TimeseriesDB_Benchmarks/single_node/queries_generate/queries/10_queries"}
TIMESCALE_DATA_DIR="${BULK_DATA_DIR}/queries_timescaledb"
INFLUX_DATA_DIR="${BULK_DATA_DIR}/queries_influx"

# Form of data to generate
USE_JSON=${USE_JSON:-false}
USE_TAGS=${USE_TAGS:-true}
USE_TIME_BUCKET=${USE_TIME_BUCKET:-true}

# Space-separated list of target DB formats to generate
FORMATS=${FORMATS:-"timescaledb influx"}

# All available for generation query types (sorted alphabetically)
QUERY_TYPES_ALL="\
	last-loc \
	low-fuel \
	high-load \
	stationary-trucks \
	long-driving-sessions \
	avg-vs-projected-fuel-consumption \
	avg-daily-driving-duration \
	avg-daily-driving-session \
	avg-load \
	daily-activity \
	breakdown-frequency"

# What query types to generate
QUERY_TYPES=${QUERY_TYPES:-$QUERY_TYPES_ALL}
SCALE=${SCALE:-"800"}
QUERIES=${QUERIES:-"10"}
SEED=${SEED:-"123"}

# Start and stop time for generated timeseries
TS_START=${TS_START:-"2023-01-01T00:00:00Z"}
TS_ENDS=${TS_ENDS:-"2023-01-01T10:00:00Z 2023-01-03T02:00:00Z 2023-01-07T06:00:00Z"}

# What set of data to generate: devops (multiple data), cpu-only (cpu-usage data)
USE_CASE=${USE_CASE:-"iot"}

# Ensure DATA DIR available
mkdir -p ${BULK_DATA_DIR}
chmod a+rw ${BULK_DATA_DIR}

mkdir -p "${TIMESCALE_DATA_DIR}"
mkdir -p "${INFLUX_DATA_DIR}"

chmod a+rw "${TIMESCALE_DATA_DIR}"
chmod a+rw "${INFLUX_DATA_DIR}"

pushd ${BULK_DATA_DIR}
set -eo pipefail

# Loop over all requested queries types and generate data
for FORMAT in ${FORMATS}; do
	echo "Generating queries for format: ${FORMAT}"
	if [ "${FORMAT}" == "timescaledb" ]; then
		pushd "${TIMESCALE_DATA_DIR}"
	elif [ "${FORMAT}" == "influx" ]; then
		pushd "${INFLUX_DATA_DIR}"
	fi

	for QUERY_TYPE in ${QUERY_TYPES}; do
		echo "	Generating queries for type: ${QUERY_TYPE}"
		for TS_END in ${TS_ENDS}; do

			case "$TS_END" in
				"2023-01-01T10:00:00Z")
					DATASET_SIZE="small"
					mkdir -p "small"
					pushd "small"
					;;
				"2023-01-03T02:00:00Z")
					DATASET_SIZE="medium"
					mkdir -p "medium"
					pushd "medium"
					;;
				"2023-01-07T06:00:00Z")
					DATASET_SIZE="large"
					mkdir -p "large"
					pushd "large"
					;;
				*)
					echo "Unknown dataset size"
					exit 1
					;;
			esac
			echo "		Generating queries for dataset size: ${DATASET_SIZE}"
			DATA_FILE_NAME="query_${FORMAT}_${DATASET_SIZE}_${QUERY_TYPE}.dat.gz"

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
					--queries ${QUERIES} \
					--query-type ${QUERY_TYPE} \
					--scale ${SCALE} \
					--seed ${SEED} \
					--timestamp-start ${TS_START} \
					--timestamp-end ${TS_END} \
					--use-case ${USE_CASE} \
					--timescale-use-json=${USE_JSON} \
					--timescale-use-tags=${USE_TAGS} \
					--timescale-use-time-bucket=${USE_TIME_BUCKET} \
					--clickhouse-use-tags=${USE_TAGS} \
					| gzip  > ${DATA_FILE_NAME}

				trap - EXIT

		# Make files accessible by everyone
		chmod a+r "${DATA_FILE_NAME}"
			fi
			popd
		done
	done
	popd
done

