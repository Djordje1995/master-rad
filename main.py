import constant
import csv_handler
import linear_regression
import time
import k_nearest_neighbors


start_time = time.process_time()
linear_regression.train(csv_handler.read_csv(constant.LEARNING_DATA))
# 1.640625 seconds
# k_nearest_neighbors.train()
print(time.process_time() - start_time, "seconds")
