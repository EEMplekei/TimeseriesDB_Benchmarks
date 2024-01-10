#!/bin/bash

# Path to the script to generate queries
GENERATE_SCRIPT="./generate_queries.sh"

# Values for the number of queries
QUERY_VALUES=(1 10 100)

# Loop through the values and call the generate_queries.sh script
for value in "${QUERY_VALUES[@]}"; do
    # Call the generate_queries.sh script with the current value
    bash "${GENERATE_SCRIPT}" "${value}"

    # Output success message
    echo "Called ${GENERATE_SCRIPT} with value ${value}"
done

