import logging
import pandas as pd
from ._simulator import TimeSeries
from qualitative_model_fitting._parser import Parser

LOG = logging.getLogger(__name__)


class ManualRunner:

    def __init__(self, ant_str, obs_str):
        self.ant_str = ant_str
        self.obs_str = obs_str

    def run(self):
        results = []
        parser = Parser(self.ant_str, self.obs_str)
        for obs in parser.observation_block:
            obs_result = dict(
                name=obs.name,
                observation=str(obs),
                evaluation=obs.reduce()
            )
            df = pd.DataFrame(obs_result, index=[0])
            results.append(df)
        df = pd.concat(results).reset_index()
        return df


