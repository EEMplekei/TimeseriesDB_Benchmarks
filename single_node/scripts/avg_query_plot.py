import numpy as np
import parse_file

databases = ["influx"]
nbr_queries = ["10","100"]
dataset_size = ["small", "medium", "large"]
for database in databases:
    for nbr_query in nbr_queries:
        for dataset_size in dataset_size:
            file_path = '../performance/queries/' + database + '/' + nbr_query + '_queries/' + database + '_' + nbr_query + '_queries_' + dataset_size + '.out'
            means = parse_file.parse_file(file_path)
            print("Database: " + database + " - Nbr queries: " + nbr_query + " - Dataset size: " + dataset_size)
            print("Mean: " + str(np.mean(means)))
            #print("Standard deviation: " + str(np.std(means)))
            #print("Median: " + str(np.median(means)))
            #print("Min: " + str(np.min(means)))
            #print("Max: " + str(np.max(means)))
            print("")