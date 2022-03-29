import constant
import csv_handler
import file_reformator
import percentage_value_maps
import linear_regression
import time
import k_nearest_neighbors


file_reformator.recreate_file(constant.LEARNING)

# file_reformator.recreate_file(constant.LEARNING)
# print("Transmission")
# percentage_value_maps.print_avgs(
#     percentage_value_maps.calculate_differences_in_percentage(
#         percentage_value_maps.avg_price_per_category(
#             csv_handler.read_csv(constant.LEARNING_DATA), constant.TRANSMISSION)))
# print("Fuel type")
# percentage_value_maps.print_avgs(
#     percentage_value_maps.calculate_differences_in_percentage(
#         percentage_value_maps.avg_price_per_category(
#             csv_handler.read_csv(constant.LEARNING_DATA), constant.FUEL_TYPE)))
# print("Engine size")
# percentage_value_maps.print_avgs(
#     percentage_value_maps.sort_category_by_value(
#         percentage_value_maps.calculate_differences_in_percentage(
#             percentage_value_maps.avg_price_per_category(
#                 csv_handler.read_csv(constant.LEARNING_DATA), constant.ENGINE_SIZE))))
# print("miles per gallon")
# percentage_value_maps.print_avgs(
#     percentage_value_maps.sort_category_by_value(
#         percentage_value_maps.calculate_differences_in_percentage(
#             percentage_value_maps.avg_price_per_category(
#                 csv_handler.read_csv(constant.LEARNING_DATA), constant.MPG))))
# tart_time = time.process_time()
# linear_regression.train(csv_handler.read_csv(constant.LEARNING_DATA))
# 1.640625 seconds
# k_nearest_neighbors.train()
# print(time.process_time() - start_time, "seconds")
