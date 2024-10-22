# functions
from src.prepare_data import prepare_flights
from src.plots import plot_delays_by_week

# import data from package
from nycflights13 import flights
from nycflights13 import airports

# prepare data
flights_prepared = prepare_flights(flights)

# print data
flights_prepared.head()

# plot data
flights_prepared.pipe(plot_delays_by_week)

# example chaining functions together
(
    flights
    .pipe(prepare_flights)
    .pipe(plot_delays_by_week)
)