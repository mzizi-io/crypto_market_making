from gym.spaces import Box
from datetime import datetime
from crypto_market_making.db_service.airflow.db_handler import SQLReader


class ObservationGenerator:
    def __init__(self, sql_reader: SQLReader):
        # Define variable space
        self.space = Box(low=-1, high=1, shape=(196,))
        self.sql_reader = sql_reader
        self.count = 0
        self.generator = self.data_generator()

    def data_generator(self):
        streamer = self.sql_reader.read_data_by_dates()

        for row in streamer:
            yield list(row[3:])

    def sample(self):
        return next(self.generator)


if __name__ == "__main__":
    start_date = datetime(2021, 1, 1)
    end_date = datetime(2021, 1, 20)
    reader = SQLReader(start_date, end_date)
    space = ObservationGenerator(reader)
    print(space.sample())
    print(space.sample())
    print(space.sample())
    print(space.sample())
    print(space.sample())
    print(space.sample())
    print(space.sample())
    print(space.sample())
