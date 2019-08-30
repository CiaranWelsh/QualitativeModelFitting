import logging

from ._simulator import TimeSeries
from ._interpreter import _Clause, _Observation

LOG = logging.getLogger(__name__)


class ManualRunner:

    def __init__(self, model, ts_definition, obs):
        self.ant_str = model
        self.ts_definition = ts_definition
        self.obs = obs

    def run(self):
        data = self._run_timeseries()
        result = {}
        for obs in self.obs:
            result[str(obs.name)] = obs.reduce(data)
        return result

    def _run_timeseries(self):
        dct = {}
        for ts in self.ts_definition:
            conditions = ts['conditions']
            start = ts['integration_settings']['start']
            stop = ts['integration_settings']['stop']
            step = ts['integration_settings']['step']
            data = TimeSeries(self.ant_str, conditions, int(start), int(stop), int(step)).simulate()
            dct[ts['name']] = data
        return dct

    def _statement(self, statement):
        if not isinstance(statement, _Observation):
            raise TypeError
        name = statement.name
        clause1_value = self._clause(statement.clause1)
        clause2_value = self._clause(statement.clause2)
        op_func = statement.operator.operator
        return {'truth': op_func(clause1_value, clause2_value)}

    def _clause(self, clause):
        if not isinstance(clause, _Clause):
            raise TypeError
        condition = clause.model_entity.condition
        if condition not in self.data.keys():
            raise ValueError(f'Condition {condition} has been referenced'
                             f' but it does not exist. These are your defined '
                             f'condition names: {self.data.keys()}')

        name = clause.model_entity.component_name
        if name not in self.data[condition].columns:
            raise ValueError(f'model entity {name} not found. '
                             f'These are valid model entities: {list(self.data[condition].columns)}')

        time = clause.model_entity.time
        time = eval(time)

        clause_value = self.data[condition][name]
        if isinstance(time, tuple):
            clause_value = clause_value.loc[time[0]: time[1]]
        else:
            clause_value = clause_value.loc[time]

        if clause.modifier:
            clause_value = clause.modifier(clause_value)

        return clause_value
