import logging

from ._simulator import TimeSeries
from qualitative_model_fitting._parser import Parser

LOG = logging.getLogger(__name__)


class ManualRunner:

    def __init__(self, ant_str, obs_str):
        self.ant_str = ant_str
        self.obs_str = obs_str

    def run(self):
        parser = Parser(self.ant_str, self.obs_str)
        for obs in parser.observation_block:
            print(obs)
        # result = []
        # for obs in self.obs:
        #     result.append(obs.reduce(data))
        # return result


