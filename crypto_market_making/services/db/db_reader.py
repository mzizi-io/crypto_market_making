import psycopg
from datetime import datetime, timedelta
from typing import List
import numpy as np
import itertools
import pandas as pd


class PsycopgSQLReader:
    """
    This reader provides data on a daily basis as a dask dataframe.

    The streamer provides a rolling window of 3600 observations (about 1h) to the strategies.

    At the end of the day, the environment is reset and a new dataframe is obtained.
    """

    def __init__(self, start_date: datetime, end_date: datetime):
        self.conn = psycopg.connect(
            "dbname=market_making_db user=caleb password=Iwillbegr8"
        )
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()
        self.start_date = start_date
        self.end_date = end_date

        # Read data for given day
        self.read_data_by_dates()

        #

    def read_data_by_dates(self):
        # Dates to string
        start_date_str = self.start_date.strftime("%Y-%m-%d %H:%M:%S")
        end_date_str = self.end_date.strftime("%Y-%m-%d %H:%M:%S")

        self.cursor.execute(
            "SELECT * FROM readers where date >= '%s' and date <= '%s' ORDER BY date ASC;"
            % (start_date_str, end_date_str)
        )

    def stream(self) -> List:
        return self.cursor.fetchmany(3600)


if __name__ == "__main__":
    start_date = datetime(2021, 1, 1)
    end_date = datetime(2021, 1, 2)
    reader = PsycopgSQLReader(start_date, end_date)
    print(reader.stream()[0][1])
    print(reader.stream()[0][1])
    print(reader.stream()[0][1])
    print(reader.stream()[0][1])
    print(reader.stream()[0][1])
    print(reader.stream()[0][1])
    print(reader.stream()[0][1])
    print(reader.stream()[0][1])
    print(reader.stream()[0][1])
