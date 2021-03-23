# Pandas for data management
import pandas as pd

# os methods for manipulating paths
from os.path import dirname, join

from tabs.BarChart import UsageBarChart

# Bokeh basics
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs

from Database.Queries import Q_DATA_USAGE_FMT, Q_PHONE_NUMBERS

class Dashboard:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    @staticmethod
    def execute_query(db_connection, query: str, parse_dates: list = []) -> pd.DataFrame:
        if (len(parse_dates)):
            return pd.read_sql(query, con=db_connection, parse_dates=parse_dates)
        else:
            return pd.read_sql(query, con=db_connection)

    # this staticmethod decorator signifies that this function is associated
    # with the class, however, it is general to all instances of the class.
    # This means that it can be called anywhere not just from a Dashboard
    # object. This is a callback that will manipulate the data when a ui event
    # is triggered. It will then pass back all the required information to
    # re-render the figure for the new user specified by the Selection button.
    @staticmethod
    def minutes_usage_callback(data: pd.DataFrame, user_idx: int):

        y_data = list(data.iloc(0)[user_idx][1:])

        return y_data

    def minutes_usage_bar_chart(self):
        # do some data preprocessing
        # get max value from dataframe to get the correct y scale of the chart
        max_value = 0
        # all columns exluding Mobile Number
        for col in self.data_minutes.columns[1:]:
            max_value = (max_value, self.data_minutes[col].max())[self.data_minutes[col].max() > max_value]

        y_scale = (0, max_value)

        # pull the first row of minute usage from the data frame as the
        y_data = list(self.data_minutes.iloc(0)[1][1:])

        # the x labels are the columns from the data frame
        x_labels = list(self.data_minutes.columns[1:])

        # pass the raw data, x axis labels, y scale tuple, and y data to bar chart object
        # it handles the construction of the figure and its ui componenets
        # the callback function is passed so that the object can replicate the
        # data preprocessing if any ui event is triggered
        self.minutesbarchart = UsageBarChart(self.data_minutes, "Minutes Usage", x_labels, y_scale, y_data,
                                             self.minutes_usage_callback);

    @staticmethod
    def data_usage_callback(db_connection, phone_num: str):
        # Query the database for all the usage entries relating to the first phone number
        data_usage = Dashboard.execute_query(db_connection, Q_DATA_USAGE_FMT.format(phone_num), parse_dates=["report_date"])

        y_data = data_usage["total_data"].tolist()
        x_labels = data_usage["report_date"].dt.month_name().tolist()

        return x_labels, y_data

    def data_usage_bar_chart(self):

        phone_numbers = self.execute_query(self.db_connection, Q_PHONE_NUMBERS)

        # get first phone number from dataframe
        first_num = phone_numbers["phone_number"][0]

        # Query the database for all the usage entries relating to the first phone number
        data_usage = self.execute_query(self.db_connection, Q_DATA_USAGE_FMT.format(first_num), ["report_date"])

        # do some data preprocessing
        # get max value from dataframe to get the correct y scale of the chart
        max_value = data_usage["total_data"].max()

        y_scale = (0, max_value)

        # pull the first row of minute usage from the data frame as the
        y_data = data_usage["total_data"].tolist()

        # the x labels are the columns from the data frame
        x_labels = data_usage["report_date"].dt.month_name().tolist()

        dropdown_options = phone_numbers["phone_number"].tolist()

        # pass the raw data, x axis labels, y scale tuple, and y data to bar chart object
        # it handles the construction of the figure and its ui componenets
        # the callback function is passed so that the object can replicate the
        # data preprocessing if any ui event is triggered
        self.databarchart = UsageBarChart(self.db_connection, "Data Usage", x_labels, y_scale, y_data,
                                          dropdown_options, self.data_usage_callback);

    def render(self):
        self.data_usage_bar_chart()
        self.tabs = Tabs(tabs=[self.databarchart.panel()])
        curdoc().add_root(self.tabs)

