from collections.abc import Callable

import pandas as pd

from bokeh.plotting import figure
from bokeh.layouts import column
from bokeh.models.widgets import Tabs, Panel
from bokeh.models import Dropdown, ColumnDataSource

class UsageBarChart:
    def __init__(self, db_connection, title: str,
                 x_range: list, y_range: tuple,
                 y_data: list, dropdown_options: list, callback: Callable):
        self.db_connection = db_connection
        self.title = title
        self.data_callback = callback
        self.dropdown_options = dropdown_options
        self.hist_data_source = ColumnDataSource(data={'x':x_range, 'y':y_data})

        self.fig = figure(title=title, x_range=x_range, y_range=y_range, plot_height=500)
        self.fig.vbar(
            x='x',
            top='y',
            width=0.9,
            source=self.hist_data_source
        )
        self.fig.xgrid.grid_line_color = None
        self.fig.y_range.start = 0

    def select_callback(self, new):
        x_data, y_data = self.data_callback(self.db_connection, new.item)
        self.hist_data_source.data['y'] = y_data
        self.hist_data_source.data['x'] = x_data

    def panel(self) -> Panel:

        # getting user phone numbers and placing them into a list of tuples.
        # Each tuple is collection of the displayed value and its corresponding
        # index in the dataframe
        users = []
        for value in self.dropdown_options:
            users.append(str(value))

        self.data_select = Dropdown(name="Select User", menu=users)
        self.data_select.on_click(self.select_callback)

        col = column(self.data_select, self.fig)

        tab = Panel(child=col, title=self.title)

        return tab
