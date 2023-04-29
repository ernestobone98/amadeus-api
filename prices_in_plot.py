import time
import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from api_calls import get_cheapest_price

def plot_cheapest_price_over_time(origin, dest, date):
    '''
    Plots the cheapest price of a flight over (real) time
    '''
    # Create a generator to simulate time updates
    x_vals = []
    y_vals = []
    start_time = time.time()

    # Create a function to update the plot with new data
    def update(i):
        print("updating...")
        nonlocal x_vals, y_vals
        elapsed_time = time.time() - start_time
        x_vals.append(elapsed_time)
        y_vals.append(float(get_cheapest_price(origin, dest, date)))
        if len(x_vals) > 10:
            x_vals.pop(0)
            y_vals.pop(0)
        plt.cla()
        plt.plot(x_vals, y_vals)
        plt.xlabel('Time (s)')
        plt.ylabel('Price ($)')
        plt.title('Flight Cheapest Price over Time')

    # Create the initial plot
    plt.style.use('fivethirtyeight')
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    # Create an animation that updates the plot every 8 seconds
    ani = FuncAnimation(fig, update, interval=8000)
    print("showing...")

    # Show the plot
    plt.tight_layout()
    plt.show()


def plot_price_over_time(origin, dest, start_date, end_date, period):
    '''
    Plots the cheapest flight prices from origin to destination over a specified time period.
    '''
    # Convert start and end date strings to datetime objects
    start_dt = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_dt = datetime.datetime.strptime(end_date, '%Y-%m-%d')

    # Define the period of time to display data for
    if period == 'day':
        period_delta = datetime.timedelta(days=1)
    elif period == 'week':
        period_delta = datetime.timedelta(weeks=1)
    elif period == 'month':
        period_delta = datetime.timedelta(days=30)
    else:
        raise ValueError("Invalid period value: must be 'day', 'week', or 'month'")

    # Initialize empty lists to hold x and y data
    x_vals = []
    y_vals = []

    # Iterate over the specified time period, making API calls and recording data
    curr_dt = start_dt
    while curr_dt <= end_dt:
        curr_date_str = curr_dt.strftime('%Y-%m-%d')
        cheapest_price = get_cheapest_price(origin, dest, curr_date_str)
        x_vals.append(curr_dt)
        y_vals.append(cheapest_price)
        curr_dt += period_delta

    # Create the plot
    plt.plot(x_vals, y_vals)
    plt.xlabel('Date')
    plt.ylabel('Price ($)')
    plt.title('Cheapest Flight Prices from {} to {} over the last {}'.format(origin, dest, period))

    # Show the plot
    plt.show()


# plot_cheapest_price_over_time('MAD', 'BCN', '2023-11-11')
plot_price_over_time('MAD', 'BCN', '2023-10-11', '2023-11-11', 'day')
