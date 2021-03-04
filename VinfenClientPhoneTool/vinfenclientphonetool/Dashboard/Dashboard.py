# Pandas for data management
import pandas as pd

# os methods for manipulating paths
from os.path import dirname, join

from tabs.BarChart import DataUsageBarChart

# Bokeh basics
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs



class Dashboard:
    def __init__(self, filepath):
        # read in data
        self.data = pd.read_csv(filepath, index_col=0)
        # remove all unnamed columns
        self.data = self.data.loc[:, ~self.data.columns.str.contains('^Unnamed')]
        # create Bar Chart Object
        self.minutes_usage_bar_chart()

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
        for col in self.data.columns[1:]:
            max_value = (max_value, self.data[col].max())[self.data[col].max() > max_value]

        y_scale = (0, max_value)

        # pull the first row of minute usage from the data frame as the
        y_data = list(self.data.iloc(0)[1][1:])

        # the x labels are the columns from the data frame
        x_labels = list(self.data.columns[1:])

        # pass the raw data, x axis labels, y scale tuple, and y data to bar chart object
        # it handles the construction of the figure and its ui componenets
        # the callback function is passed so that the object can replicate the
        # data preprocessing if any ui event is triggered
        self.barchart = DataUsageBarChart(self.data, x_labels, y_scale, y_data, self.minutes_usage_callback);

    def render(self):
        self.tabs = Tabs(tabs=[self.barchart.panel()])
        curdoc().add_root(self.tabs)

