# Pandas for data management
import pandas as pd

# os methods for manipulating paths
from os.path import dirname, join

from tabs.BarChart import UsageBarChart

# Bokeh basics
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs



class Dashboard:
    def __init__(self, filepath_minutes, filepath_data):
        # read in data
        self.data_minutes = pd.read_csv(filepath_minutes, index_col=0)
        self.data_data = pd.read_csv(filepath_data, index_col=0)
        # remove all unnamed columns
        self.data_minuts = self.data_minutes.loc[:, ~self.data_minutes.columns.str.contains('^Unnamed')]
        # create Bar Chart Object
        self.minutes_usage_bar_chart()
        self.data_usage_bar_chart()

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
        self.minutesbarchart = UsageBarChart(self.data_minutes, "Minutes Usage", x_labels, y_scale, y_data, self.minutes_usage_callback);

    @staticmethod
    def data_usage_callback(data: pd.DataFrame, user_idx: int):

        y_data = list(data.iloc(0)[user_idx][1:])

        return y_data


    def data_usage_bar_chart(self):
        # do some data preprocessing
        # get max value from dataframe to get the correct y scale of the chart
        max_value = 0
        # all columns exluding Mobile Number
        for col in self.data_data.columns[1:]:
            max_value = (max_value, self.data_data[col].max())[self.data_data[col].max() > max_value]

        y_scale = (0, max_value)

        # pull the first row of minute usage from the data frame as the
        y_data = list(self.data_data.iloc(0)[1][1:])

        # the x labels are the columns from the data frame
        x_labels = list(self.data_data.columns[1:])

        # pass the raw data, x axis labels, y scale tuple, and y data to bar chart object
        # it handles the construction of the figure and its ui componenets
        # the callback function is passed so that the object can replicate the
        # data preprocessing if any ui event is triggered
        self.databarchart = UsageBarChart(self.data_data, "Data Usage", x_labels, y_scale, y_data, self.data_usage_callback);

    def render(self):
        self.tabs = Tabs(tabs=[self.minutesbarchart.panel(), self.databarchart.panel()])
        curdoc().add_root(self.tabs)

