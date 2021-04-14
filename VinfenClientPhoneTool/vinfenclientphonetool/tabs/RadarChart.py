from collections.abc import Callable

import pandas as pd

import numpy as np

from bokeh.plotting import figure
from bokeh.layouts import column
from bokeh.models.widgets import Tabs, Panel
from bokeh.models import Dropdown, ColumnDataSource, LabelSet

def unit_poly_verts(theta, center):
    """Return vertices of polygon for subplot axes.
    This polygon is circumscribed by a unit circle centered at (0.5, 0.5)
    """
    x0, y0, r = [center] * 3
    verts = [(r * np.cos(t) + x0, r * np.sin(t) + y0) for t in theta]
    return verts


def radar_patch(r, theta, center):
    """ Returns the x and y coordinates corresponding to the magnitudes of
    each variable displayed in the radar plot
    """
    # offset from center of circle
    offset = 0.01
    yt = (r * center + offset) * np.sin(theta) + center
    xt = (r * center + offset) * np.cos(theta) + center
    return xt, yt

class RadarChart:
    def __init__(self, db_connection, title: str, data: np.array, y_labels: list,
                 dropdown_options: list, callback: Callable):
        self.db_connection = db_connection
        self.title = title
        self.data_callback = callback
        self.dropdown_options = dropdown_options
        self.num_vars = len(y_labels)

        self.center = 0.5

        self.theta = np.linspace(0, 2 * np.pi, self.num_vars, endpoint=False)
        # rotate theta such that the first axis is at the top
        self.theta += np.pi / 2

        self.verts = unit_poly_verts(self.theta, self.center)
        self.x = [v[0] + self.center for v in self.verts]
        self.y = [v[1] + self.center for v in self.verts]

        self.source = ColumnDataSource({'x': self.x + [self.center], 'y': self.y + [1],
                                        'text': y_labels})
        self.p = figure(title=title)
        self.p.line(x="x", y="y", source=self.source)

        self.labels = LabelSet(x="x", y="y", text="text", source=self.source)

        self.p.add_layout(self.labels)

        xt, yt = radar_patch(data, self.theta, self.center)
        self.child_idx = 0
        self.p.patch(x=xt, y=yt, fill_alpha=0.15, fill_color='blue', name=f"user{self.child_idx}")

    def select_callback(self, new):
        data = self.data_callback(self.db_connection, new.item)
        xt, yt = radar_patch(data, self.theta, self.center)
        user = self.p.select_one({'name': f"user{self.child_idx}"})
        user.visible = False
        self.child_idx += 1
        self.p.patch(x=xt, y=yt, fill_alpha=0.15, fill_color='blue', name=f"user{self.child_idx}")

    def panel(self) -> Panel:

        # getting user phone numbers and placing them into a list of tuples.
        # Each tuple is collection of the displayed value and its corresponding
        # index in the dataframe
        users = []
        for value in self.dropdown_options:
            users.append(str(value))

        self.data_select = Dropdown(name="Select User", menu=users)
        self.data_select.on_click(self.select_callback)

        col = column(self.data_select, self.p)

        tab = Panel(child=col, title=self.title)

        return tab
