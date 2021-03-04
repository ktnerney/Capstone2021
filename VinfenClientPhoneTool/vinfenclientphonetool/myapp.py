# Pandas for data management
import pandas as pd

# os methods for manipulating paths
from os.path import dirname, join

# Bokeh basics
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs

from Dashboard.Dashboard import Dashboard

dash = Dashboard("./test_minutes.csv", "./test_data.csv")

dash.render()
