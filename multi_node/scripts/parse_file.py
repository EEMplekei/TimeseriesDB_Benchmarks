import re
import sys

def parse_file(file_path):
    mean_values = []

    # Regular expression pattern to match "mean: X.XXms" format
    pattern = re.compile(r'mean:\s+(\d+\.\d+)ms')

    with open(file_path, 'r') as file:
        for line in file:
            match = pattern.search(line)
            if match:
                # Extract the mean value and convert it to a float
                mean_value = float(match.group(1))
                mean_values.append(mean_value)
    
    # Keep only the even index in means list since we have 2 duplicates mean values per query
    length = len(mean_values)
    final_means = mean_values[0:length:2]
    
    return final_means
