#!/bin/bash

current_script="$(basename "$0")"

# Loop through all .sh files in the current directory
for script in *.sh; do
    # Skip the current script
    if [ "$script" != "$current_script" ]; then
        # Execute the script
        echo "Executing $script..."
        bash "$script"
        echo "Done executing $script."
    fi
done

