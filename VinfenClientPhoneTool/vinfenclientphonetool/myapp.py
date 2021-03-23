# Bokeh basics
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs

# MySQL Connection
from sqlalchemy import create_engine
import mysql.connector

# Pandas for data management
import pandas as pd

import yaml

from Dashboard.Dashboard import Dashboard
from constants import DB_NAME

with open(r'../vinfen_config.yaml') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    config = yaml.load(file, Loader=yaml.FullLoader)

db_connection_str = f'mysql+mysqlconnector://{config["user"]}:{config["password"]}@{config["host"]}:{config["port"]}/{DB_NAME}'
db_connection = create_engine(db_connection_str)

dash = Dashboard(db_connection)

dash.render()
