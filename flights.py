# functions
from src.prepare_data import prepare_flights
from src.plots import plot_delays_by_week
from src.split_data import create_train_val_test_split

# import data from package
from nycflights13 import flights
from nycflights13 import airports

# prepare data
flights_prepared = prepare_flights(flights)

# plot data
flights_prepared.pipe(plot_delays_by_week)

# example chaining functions together
(
    flights
    .pipe(prepare_flights)
    .pipe(plot_delays_by_week)
)

# creating a split
train, valid, test = create_train_val_test_split(
    flights_prepared, stratify_col="arr_delay"
)
