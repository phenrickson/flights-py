# packages
import pandas as pd
import numpy as np
import datetime

# functions
def add_delay(data):
    data["arr_delay"] = np.where(data["arr_delay"] >= 30, "late", "on_time")
    data["arr_delay"] = pd.Categorical(
        data["arr_delay"], categories=["on_time", "late"]
    )
    return data


def add_date(data):
    # Ensure 'time_hour' is a datetime object
    data["time_hour"] = pd.to_datetime(data["time_hour"])

    # Add 'date' column from 'time_hour'
    data["date"] = data["time_hour"].dt.date

    # Add 'week' column
    data["week"] = data["time_hour"].dt.to_period("W").dt.start_time

    return data


def prepare_flights(data):

    data = data.copy()
    data = add_delay(data)
    data = add_date(data)

    # Select the specific columns
    selected_columns = [
        "date",
        "year",
        "month",
        "week",
        "day",
        "arr_delay",
        "sched_dep_time",
        "sched_arr_time",
        "dep_time",
        "arr_time",
        "carrier",
        "flight",
        "tailnum",
        "origin",
        "dest",
        "air_time",
        "distance",
        "time_hour",
    ]

    return data[selected_columns]
