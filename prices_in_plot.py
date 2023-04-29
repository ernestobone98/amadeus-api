import time
import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from api_calls import FlightSearch


class FlightPricePlotter:
    def __init__(self, origin, dest, start_date=None, end_date=None, period=None):
        self.origin = origin
        self.dest = dest
        self.api = FlightSearch()
        self.start_date = start_date
        self.end_date = end_date
        self.period = period
        self.x_vals = []
        self.y_vals = []
        
    def get_period_delta(self):
        if self.period == 'day':
            return datetime.timedelta(days=1)
        elif self.period == 'week':
            return datetime.timedelta(weeks=1)
        elif self.period == 'month':
            return datetime.timedelta(days=30)
        else:
            raise ValueError("Invalid period value: must be 'day', 'week', or 'month'")
    
    def get_price_over_time(self):
        '''
        Plots the cheapest flight prices from origin to destination over a specified time period.
        '''
        # Convert start and end date strings to datetime objects
        start_dt = datetime.datetime.strptime(self.start_date, '%Y-%m-%d')
        end_dt = datetime.datetime.strptime(self.end_date, '%Y-%m-%d')

        # Define the period of time to display data for
        period_delta = self.get_period_delta()

        # Iterate over the specified time period, making API calls and recording data
        curr_dt = start_dt
        while curr_dt <= end_dt:
            curr_date_str = curr_dt.strftime('%Y-%m-%d')
            cheapest_price = self.api.get_cheapest_price(self.origin, self.dest, curr_date_str)
            self.x_vals.append(curr_dt)
            self.y_vals.append(cheapest_price)
            curr_dt += period_delta

    def plot_price_over_time(self):
        self.get_price_over_time()
        # Create the plot
        plt.plot(self.x_vals, self.y_vals)
        plt.xlabel('Date')
        plt.ylabel('Price ($)')
        plt.title('Cheapest Flight Prices from {} to {} over the last {}'.format(self.origin, self.dest, self.period))

        # Show the plot
        plt.show()
        
    def plot_cheapest_price_over_time(self, date):
        '''
        Plots the cheapest price of a flight over (real) time
        '''
        # Create a generator to simulate time updates
        start_time = time.time()

        # Create a function to update the plot with new data
        def update(i):
            print("updating...")
            elapsed_time = time.time() - start_time
            self.x_vals.append(elapsed_time)
            self.y_vals.append(float(self.api.get_cheapest_price(self.origin, self.dest, date)))
            if len(self.x_vals) > 10:
                self.x_vals.pop(0)
                self.y_vals.pop(0)
            plt.cla()
            plt.plot(self.x_vals, self.y_vals)
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


if __name__ == "__main__":
    plotter = FlightPricePlotter('MAD', 'BCN', period='day')
    plotter.plot_cheapest_price_over_time('2023-10-01')