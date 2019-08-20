import os
import yaml
import pandas as pd
import tellurium as te
from collections import OrderedDict


class TimeSeries:
    """
    Wrapper around tellurium's ODE integration feature.
    """

    def __init__(self, ant_str: str, inputs: (dict, str), start: int, stop: int, steps: int) -> None:
        """

        Args:
            ant_str: The model to integrate. Must be valid antimony model
            inputs: Nested dict. Contains details of how to configure model for integration (see docs)
            start: start time of integration
            stop:  end time of intergration
            steps: number of steps for integration
        """
        self.ant_str = ant_str
        self.inputs = inputs
        self.start = start
        self.stop = stop
        self.steps = steps

        if isinstance(self.inputs, dict):
            for k, v in self.inputs.items():
                if not isinstance(v, dict):
                    raise ValueError('If using dict type for inputs argument, it '
                                     ' should be a nested dictionary.')
        elif isinstance(self.inputs, str):
            if not os.path.isfile(self.inputs):
                raise ValueError('If using str type for inputs argument, must be a str pointing '
                                 'to a yaml file on disk')
            self.inputs = self._read_yaml()
        else:
            raise ValueError('inputs argument should be (dict, str). Got "{}"'.format(type(self.inputs)))

        self.model = self._load_model()

    def _read_yaml(self):
        with open(self.inputs, 'r') as f:
            inputs = yaml.load(f, Loader=yaml.FullLoader)
        return inputs

    def _load_model(self):
        return te.loada(self.ant_str)

    def _update_initial_conditions(self, condition_inputs):
        for k, v in condition_inputs.items():
            if not hasattr(self.model, k):
                raise AttributeError('Model does not have attribute "{}"'.format(k))
            setattr(self.model, k, v)
        return self.model

    def simulate(self) -> dict:
        dct = OrderedDict()
        for condition_name, condition in self.inputs.items():
            for i in ['inputs', 'obs']:
                if i not in condition:
                    raise ValueError(f'Every condition must have two keys: inputs and obs. {i} not found')
            cond_inputs = condition['inputs']
            cond_obs = condition['obs']
            # always reset the model before simulating in a loop
            self.model.reset()
            # set conditions
            self.model = self._update_initial_conditions(cond_inputs)
            globals = dict(zip(self.model.getGlobalParameterIds(), self.model.getGlobalParameterValues()))
            self.model.timeCourseSelections += list(globals.keys())
            results = self.model.simulate(self.start, self.stop, self.steps)
            colnames = [i.replace('[', '').replace(']', '') for i in results.colnames]
            results = pd.DataFrame(results, columns=colnames)
            results.set_index('time', inplace=True)
            dct[condition_name] = results

        return dct
