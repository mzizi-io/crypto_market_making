import os
from stable_baselines3 import A2C, PPO
from stable_baselines3.common.vec_env import DummyVecEnv

from crypto_market_making.strategies.reinforcement_learning.raw_data_market_maker.bot_environment import (
    MarketMakingEnvironment,
)

env = DummyVecEnv([lambda: MarketMakingEnvironment()])

# Set log directory
data_directory = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "models", "A2C_Model_Raw_1m")
)
log_path = os.path.abspath(os.path.join(data_directory, "logs"))

# Learn strategies
models = A2C("MlpPolicy", env, verbose=10000, tensorboard_log=log_path)
models.learn(total_timesteps=1000000)

# Save strategies
models.save(data_directory)

model = A2C.load(data_directory)
