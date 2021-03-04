from collections.abc import Callable

import pandas as pd

from bokeh.io import show
from bokeh.plotting import figure
from bokeh.layouts import column
from bokeh.models.widgets import Tabs, Panel
from bokeh.models import Dropdown, ColumnDataSource
from bokeh.palettes import RdYlBu3

from Dashboard.utils import merge_lists

class UsageBarChart:
    def __init__(self, use_data: pd.DataFrame, title: str,
                 x_range: list, y_range: tuple,
                 y_data: list, callback: Callable[[pd.DataFrame], tuple]):
        self.user_data = use_data
        self.title = title
        self.data_callback = callback

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
        y_data = self.data_callback(self.user_data, int(new.item))
        self.hist_data_source.data['y'] = y_data


    def panel(self) -> Panel:

        # getting user phone numbers and placing them into a list of tuples.
        # Each tuple is collection of the displayed value and its corresponding
        # index in the dataframe
        users = []
        index = 0
        for value in self.user_data["Mobile Number"]:
            users.append((str(value), str(index)))
            index += 1

        self.data_select = Dropdown(name="Select User", menu=users)
        self.data_select.on_click(self.select_callback)

        col = column(self.data_select, self.fig)

        tab = Panel(child=col, title=self.title)

        return tab
