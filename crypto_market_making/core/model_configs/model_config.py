from crypto_market_making.core.model_configs.action_space_config import (
    ActionSpaceConfig
)
from crypto_market_making.core.model_configs.observation_space_config import (
    ObservationSpaceConfig
)


class ModelConfig(ActionSpaceConfig, ObservationSpaceConfig):
    """Defining all the configurations for training this model can be complex

    It makes sense to put everything in a single manageable class for
    transparency
    """
    def __init__():
        pass

    @property
    def action_space_configs(self) -> ActionSpaceConfig:
        return self._get_action_space_configs()

    @property
    def observation_space_configs(self) -> ObservationSpaceConfig:
        return self._get_action_space_configs()
