import configparser, os
from pyspark.sql import SparkSession
from datetime import datetime, timedelta

# Spark login configurations
config = configparser.ConfigParser()
CONFIG_FILE = os.path.abspath(
    os.path.join(
        __file__,
        os.pardir,
        os.pardir,
        os.pardir,
        "config",
        "postgres.ini",
    )
)
config.read(CONFIG_FILE)


class SparkOrderbookReader:
    def __init__(self):
        # database parameters
        driver = "org.postgresql.Driver"
        table = "orderbook"

        # Build session
        self.spark = (
            SparkSession.builder.appName("spark_reader")
            .config("spark.jars", "/home/caleb/Downloads/postgresql-42.5.0.jar")
            .config("spark.driver.memory", "50g")
            .getOrCreate()
        )

        # Get table from db
        self.table = (
            self.spark.read.format("jdbc")
            .option("url", config["POSTGRES"]["spark_url"])
            .option("driver", driver)
            .option("dbtable", table)
            .option("user", config["POSTGRES"]["user"])
            .option("password", config["POSTGRES"]["password"])
            .load()
        )

    def get_data_chunk_for_date(self, date: datetime):
        """
        Get all data for a specific date.

        Inputs
        --------
        date: datetime - date from which to obtain data

        returns: numpy array of orderbook data
        """
        self.counter = 0
        data = self.table.filter(
            (self.table.date < date + timedelta(days=1)) & (self.table.date >= date)
        )
        self.numpy_data = (
            data.toPandas().set_index("date").drop(["id", "symbol"], axis=1).to_numpy()
        )

    def stream_next_observation(self):
        """
        Stream data line by line
        """
        while self.counter < len(self.numpy_data):
            data = self.numpy_data[self.counter]
            self.counter += 1
            yield data


if __name__ == "__main__":
    reader = SparkOrderbookReader()
    reader.get_data_chunk_for_date(datetime(2021, 1, 1))

    for i in range(1000):
        print(next(reader.stream_next_observation()))
