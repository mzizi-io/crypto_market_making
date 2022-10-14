from gym import Env, spaces
import numpy as np
import random
from itertools import product
from datetime import datetime, timedelta
from typing import List
from crypto_market_making.services.db.spark_orderbook_reader import (
    SparkOrderbookReader,
)


class MarketMakingEnvironment(Env):
    MAX_ACCOUNT_BALANCE = 1000000
    INITIAL_ACCOUNT_BALANCE = 10000
    START_TEST_DATE = datetime(2021, 1, 1)
    END_TEST_DATE = datetime(2021, 3, 31)
    TEST_INTERVAL_DAYS = (END_TEST_DATE - START_TEST_DATE).days
    MAX_NUM_SHARES = 1000
    MAX_SHARE_PRICE = 100000
    MAX_STEPS = 20000
    BLOTTER = {"OPEN_LIMIT_BIDS": [], "OPEN_LIMIT_ASKS": [], "POSITIONS": 0}
    BID_ASK_VOLUME = 0.001
    MARGIN_PENALTY = 100 / INITIAL_ACCOUNT_BALANCE

    def __init__(self):
        """
        Market making environment:

        Action Space
        -------------
        1 - bid
        2 - ask
        3 - do nothing

        spreads = {25, 50, 100}

        Observation space
        ------------------
        * normalized_order_book rows for the most recent hour
        """
        super(MarketMakingEnvironment, self).__init__()

        # Create all options. (BID/ASK, SPREAD)
        trade_options = list(product([1, 2], [2, 5, 10]))

        # Option to do nothing. 100 is a dummy variable
        trade_options.append((3, 1))

        # Define action space
        self.action_space = spaces.Box(
            low=np.array([0, 0]), high=np.array([3, 10]), shape=(2,), dtype=np.float16
        )
        self.observation_space = spaces.Box(
            low=0, high=np.inf, shape=(1, 120), dtype=np.float16
        )
        self.reward_range = (0, self.MAX_ACCOUNT_BALANCE)
        self.observation_generator = SparkOrderbookReader()
        random.seed(1)

    def step(self, action: List):
        obs = self._next_observation()
        self._take_action(action, obs)

        if self.current_step > self.END_TEST_DATE:
            self.current_step = self.START_TEST_DATE

        reward = self.balance
        done = self.net_worth <= 0 or self.balance < 0
        return obs, reward, done, {}

    def render(self, *args, **kwargs):
        profit = self.net_worth - self.INITIAL_ACCOUNT_BALANCE

        print(f"Step: {self.current_step}")
        print(f"Balance: {self.balance}")
        print(f"Shares held: {self.BLOTTER['POSITIONS']}")
        print(f"Net worth: {self.net_worth}")
        print(f"Profit: {profit}")
        print("\n")

    def reset(self):
        self.BLOTTER = {"OPEN_LIMIT_BIDS": [], "OPEN_LIMIT_ASKS": [], "POSITIONS": 0}
        self.balance = self.INITIAL_ACCOUNT_BALANCE
        self.net_worth = self.INITIAL_ACCOUNT_BALANCE
        self.max_net_worth = self.INITIAL_ACCOUNT_BALANCE
        self.shares_held = 0
        self.cost_basis = 0
        self.total_shares_sold = 0
        self.total_sales_value = 0

        # Set current step to random point within the df
        self.current_step = self.START_TEST_DATE + timedelta(
            days=random.randint(0, self.TEST_INTERVAL_DAYS)
        )
        self.observation_generator.get_data_chunk_for_date(self.current_step)
        return self._next_observation()

    def _next_observation(self):
        try:
            sample = next(self.observation_generator.stream_next_observation())
        except StopIteration:
            self.observation_generator.get_data_chunk_for_date(self.current_step)
            sample = next(self.observation_generator.stream_next_observation())

        return sample

    def _take_action(self, action: List, observation: np.array):
        action_type = action[0]
        spread = self.get_spread(action[1])

        # Get list of asks and volumes
        self.current_ask_list = [
            (observation[i], observation[i + 1])
            for i in range(60, len(observation[:-1]), 2)
        ]

        # Get list of bids and volumes
        self.current_bid_list = [
            (observation[i], observation[i + 1])
            for i in range(0, len(observation[:60]), 2)
        ]

        # Bid for asset
        if action_type < 1:
            # Add bid position to blotter
            new_bid_price = observation[1] * (1 - spread / 1000000)
            self.BLOTTER["OPEN_LIMIT_BIDS"].append((self.BID_ASK_VOLUME, new_bid_price))

            # Sort list in descending order
            self.BLOTTER["OPEN_LIMIT_BIDS"].sort(reverse=True)

        # Ask for asset
        elif action_type < 2:
            new_ask_price = observation[61] * (1 + spread / 1000000)
            self.BLOTTER["OPEN_LIMIT_ASKS"].append((self.BID_ASK_VOLUME, new_ask_price))

            # Sort list in descending order
            self.BLOTTER["OPEN_LIMIT_ASKS"].sort()

            # Fill ask orders using current readers
            self.fill_ask_orders()

        # Fill bid orders using current readers
        self.fill_bid_orders()
        self.fill_ask_orders()
        self.calculate_net_worth()

    def fill_bid_orders(self):
        for position in self.BLOTTER["OPEN_LIMIT_BIDS"]:
            for ask in self.current_ask_list:
                if ask[1] < position[1]:
                    self.BLOTTER["POSITIONS"] += position[0]
                    self.balance -= position[0] * position[1]
                else:
                    break

    def fill_ask_orders(self):
        for position in self.BLOTTER["OPEN_LIMIT_ASKS"]:
            for bid in self.current_bid_list:
                if bid[1] > position[1]:
                    self.BLOTTER["POSITIONS"] -= position[0]
                    self.balance += position[0] * position[1]
                    # Penalty for holding short positions on margin
                    if self.BLOTTER["POSITIONS"] < 0:
                        self.balance = self.balance * (1 - self.MARGIN_PENALTY)
                else:
                    break

    def calculate_net_worth(self):
        if self.BLOTTER["POSITIONS"] > 0:
            self.net_worth = (
                self.balance + self.BLOTTER["POSITIONS"] * self.current_bid_list[0][1]
            )
        else:
            self.net_worth = (
                self.balance + self.BLOTTER["POSITIONS"] * self.current_ask_list[0][1]
            )

    def get_spread(self, action_spread):
        if action_spread < 2:
            return 2
        elif action_spread < 5.0:
            return 5
        else:
            return 10


if __name__ == "__main__":
    market_making_env = MarketMakingEnvironment()
    market_making_env.reset()
    bids = [0.5] * 100
    bids.extend([1.5] * 100)
    for elem in list(product(bids, [1.5, 4.5, 10])):
        market_making_env.step(list(elem))
        market_making_env.render()
