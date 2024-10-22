from plotnine import (
    ggplot,
    geom_point,
    geom_col,
    geom_line,
    aes,
    stat_smooth,
    facet_wrap,
)

# function to group flights by week and delay and display
def plot_delays_by_week(data):
    # plot the number of delays over the course of the year
    flights_weekly_count = data.groupby(['week', 'arr_delay'], observed=True).size().reset_index(name='n')

    plot = (
        ggplot(flights_weekly_count, aes(x='week', y='n', fill = 'arr_delay'))
        + geom_col()
    )

    return plot
