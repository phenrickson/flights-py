# functions
import pandas as pd
import numpy as np
from src.prepare_data import prepare_flights
from src.plots import plot_delays_by_week
from src.modeling.split_data import create_train_val_test_split
from src.modeling.train_model import create_preprocessor, create_pipeline, train_model, extract_coefficients, score_data, assess_predictions

# import data from package
from nycflights13 import flights
from nycflights13 import airports

# prepare data
flights_prepared = prepare_flights(flights)

# print data
print(flights_prepared.head())

# # plot data
# flights_prepared.pipe(plot_delays_by_week)

# example chaining functions together
# (
#     flights
#     .pipe(prepare_flights)
#     .pipe(plot_delays_by_week)
# )

# create split
train_data, valid_data, test_data = flights_prepared.pipe(create_train_val_test_split, stratify_col = 'arr_delay')

# fit pipeline to training data
pipeline = train_model(
    train_data, 
    numeric_features=['distance', 'air_time'], 
    categorical_features=['carrier']  # Pass 'carrier' as a list
)

# extract coefficients
extract_coefficients(pipeline)

# results
assess_predictions(pipeline, valid_data)
