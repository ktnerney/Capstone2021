# Pandas for data management
import pandas as pd
import numpy as np

# os methods for manipulating paths
from os.path import dirname, join

from tabs.BarChart import UsageBarChart
from tabs.RadarChart import RadarChart

# Bokeh basics
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs

from Database.Queries import Q_DATA_USAGE_FMT, Q_DATA_USAGE_MEAN,\
    Q_MINUTES_FMT, Q_MESSAGES_FMT, Q_PHONE_NUMBERS, Q_TOTAL_COMMUNICATION_FMT, Q_STANDARD_DEV_COMMUNICATION, \
    Q_MEAN_COMMUNICATION

class Dashboard:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    @staticmethod
    def execute_query(db_connection, query: str, parse_dates: list = []) -> pd.DataFrame:
        if len(parse_dates):
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
    def minutes_usage_callback(db_connection, phone_num: str):
        # Query the database for all the usage entries relating to the first phone number
        minutes_usage = Dashboard.execute_query(db_connection, Q_MINUTES_FMT.format(phone_num),
                                                parse_dates=["report_date"])

        y_data = minutes_usage["total_minutes"].tolist()
        x_labels = minutes_usage["report_date"].dt.month_name().tolist()

        return x_labels, y_data

    def minutes_usage_bar_chart(self):
        phone_numbers = self.execute_query(self.db_connection, Q_PHONE_NUMBERS)

        # get first phone number from dataframe
        first_num = phone_numbers["phone_number"][0]

        # Query the database for all the minutes entries relating to the first phone number
        minutes = self.execute_query(self.db_connection, Q_MINUTES_FMT.format(first_num), ["report_date"])

        # do some data preprocessing
        # get max value from dataframe to get the correct y scale of the chart
        max_value = minutes["total_minutes"].max()

        y_scale = (0, max_value)

        # pull the first row of minute usage from the data frame as the y data
        y_data = minutes["total_minutes"].tolist()

        # the x labels are the columns from the data frame
        x_labels = minutes["report_date"].dt.month_name().tolist()

        dropdown_options = phone_numbers["phone_number"].tolist()

        # pass the raw data, x axis labels, y scale tuple, and y data to bar chart object
        # it handles the construction of the figure and its ui components
        # the callback function is passed so that the object can replicate the
        # data preprocessing if any ui event is triggered
        return UsageBarChart(self.db_connection, "Minutes Usage", x_labels, y_scale,
                             y_data, dropdown_options, self.data_usage_callback)

    @staticmethod
    def data_usage_callback(db_connection, phone_num: str):
        # Query the database for all the usage entries relating to the first phone number
        if phone_num == "Mean":
            query = Q_DATA_USAGE_MEAN
        elif phone_num == "Median":
            query = Q_DATA_USAGE_MEDIAN
        else:
            query = Q_DATA_USAGE_FMT.format(phone_num)

        data_usage = Dashboard.execute_query(db_connection, query,
                                             parse_dates=["report_date"])
        print(data_usage)
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

        dropdown_options = ["Mean", "Median"]

        dropdown_options += phone_numbers["phone_number"].tolist()

        # pass the raw data, x axis labels, y scale tuple, and y data to bar chart object
        # it handles the construction of the figure and its ui componenets
        # the callback function is passed so that the object can replicate the
        # data preprocessing if any ui event is triggered
        return UsageBarChart(self.db_connection, "Data Usage", x_labels, y_scale, y_data,
                             dropdown_options, self.data_usage_callback)

    @staticmethod
    def messages_callback(db_connection, phone_num: str):
        # Query the database for all the usage entries relating to the first phone number
        messages = Dashboard.execute_query(db_connection, Q_MESSAGES_FMT.format(phone_num),
                                           parse_dates=["report_date"])

        y_data = messages["total_messages"].tolist()
        x_labels = messages["report_date"].dt.month_name().tolist()

        return x_labels, y_data

    def messages_bar_chart(self):

        phone_numbers = self.execute_query(self.db_connection, Q_PHONE_NUMBERS)

        # get first phone number from dataframe
        first_num = phone_numbers["phone_number"][0]

        # Query the database for all the usage entries relating to the first phone number
        messages = self.execute_query(self.db_connection, Q_MESSAGES_FMT.format(first_num), ["report_date"])

        # do some data preprocessing
        # get max value from dataframe to get the correct y scale of the chart
        max_value = messages["total_messages"].max()

        y_scale = (0, max_value)

        # pull the first row of minute usage from the data frame as the
        y_data = messages["total_messages"].tolist()

        # the x labels are the columns from the data frame
        x_labels = messages["report_date"].dt.month_name().tolist()

        dropdown_options = phone_numbers["phone_number"].tolist()

        # pass the raw data, x axis labels, y scale tuple, and y data to bar chart object
        # it handles the construction of the figure and its ui componenets
        # the callback function is passed so that the object can replicate the
        # data preprocessing if any ui event is triggered
        return UsageBarChart(self.db_connection, "Messages", x_labels, y_scale, y_data,
                             dropdown_options, self.messages_callback)

    # Rescales the values from (0,1) in a normal distribution
    @staticmethod
    def rescale(stddev, mean, value):
        z = (value - mean) / stddev
        z = (z / 2) + 0.5
        return z

    @staticmethod
    def communication_radar_callback(db_connection, phone_num: str):
        total_communication = Dashboard.execute_query(db_connection, Q_TOTAL_COMMUNICATION_FMT.format(phone_num),
                                                 ["report_date"])
        total_communication_data = total_communication["avg(total_data)"].tolist()[0]
        total_communication_minutes = total_communication["avg(total_minutes)"].tolist()[0]
        total_communication_messages = total_communication["avg(total_messages)"].tolist()[0]

        std_dev_communication = Dashboard.execute_query(db_connection, Q_STANDARD_DEV_COMMUNICATION.format(phone_num))
        std_dev_data = std_dev_communication["std(total_data)"].tolist()[0]
        std_dev_minutes = std_dev_communication["std(total_minutes)"].tolist()[0]
        std_dev_messages = std_dev_communication["std(total_messages)"].tolist()[0]

        mean_communication = Dashboard.execute_query(db_connection, Q_MEAN_COMMUNICATION.format(phone_num))
        mean_data = mean_communication["avg(total_data)"].tolist()[0]
        mean_minutes = mean_communication["avg(total_minutes)"].tolist()[0]
        mean_messages = mean_communication["avg(total_messages)"].tolist()[0]

        rescale_data = Dashboard.rescale(std_dev_data, mean_data, total_communication_data)
        rescale_minutes = Dashboard.rescale(std_dev_minutes, mean_minutes, total_communication_minutes)
        rescale_messages = Dashboard.rescale(std_dev_messages, mean_messages, total_communication_messages)

        return np.array([rescale_data, rescale_minutes, rescale_messages])

    def communication_radar_chart(self):
        phone_numbers = self.execute_query(self.db_connection, Q_PHONE_NUMBERS)

        # get first phone number from dataframe
        first_num = phone_numbers["phone_number"][0]

        # Query the database for all the communication entries relating to the first phone number
        total_communication = self.execute_query(self.db_connection, Q_TOTAL_COMMUNICATION_FMT.format(first_num), ["report_date"])
        total_communication_data = total_communication["avg(total_data)"].tolist()[0]
        total_communication_minutes = total_communication["avg(total_minutes)"].tolist()[0]
        total_communication_messages = total_communication["avg(total_messages)"].tolist()[0]

        std_dev_communication = self.execute_query(self.db_connection, Q_STANDARD_DEV_COMMUNICATION.format(first_num))
        std_dev_data = std_dev_communication["std(total_data)"].tolist()[0]
        std_dev_minutes = std_dev_communication["std(total_minutes)"].tolist()[0]
        std_dev_messages = std_dev_communication["std(total_messages)"].tolist()[0]

        mean_communication = self.execute_query(self.db_connection, Q_MEAN_COMMUNICATION.format(first_num))
        mean_data = mean_communication["avg(total_data)"].tolist()[0]
        mean_minutes = mean_communication["avg(total_minutes)"].tolist()[0]
        mean_messages = mean_communication["avg(total_messages)"].tolist()[0]

        rescale_data = self.rescale(std_dev_data, mean_data, total_communication_data)
        rescale_minutes = self.rescale(std_dev_minutes, mean_minutes, total_communication_minutes)
        rescale_messages = self.rescale(std_dev_messages, mean_messages, total_communication_messages)

        data = np.array([rescale_data, rescale_minutes, rescale_messages])

        title = "Communication Radar Graph"

        dropdown_options = phone_numbers["phone_number"].tolist()

        labels = ["Data", "Minutes", "Messages"]

        return RadarChart(self.db_connection, title, data, labels, dropdown_options, self.communication_radar_callback)


    def render(self):
        self.databarchart = self.data_usage_bar_chart()
        self.minutesbarchart = self.minutes_usage_bar_chart()
        self.messagesbarchart = self.messages_bar_chart()
        self.communicationradar = self.communication_radar_chart()
        self.tabs = Tabs(tabs=[self.databarchart.panel(),
                               self.minutesbarchart.panel(),
                               self.messagesbarchart.panel(),
                               self.communicationradar.panel()])
        curdoc().add_root(self.tabs)
