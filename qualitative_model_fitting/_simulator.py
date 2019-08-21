import os
import yaml
import pandas as pd
import tellurium as te

from collections import OrderedDict
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib
matplotlib.use('Qt5Agg')
import seaborn as sns
sns.set_context(context='talk')

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

        print(self.inputs)

        # if isinstance(self.inputs, (dict, OrderedDict)):
        #     for k, v in self.inputs.items():
        #         if not isinstance(v, dict):
        #             raise ValueError('If using dict type for inputs argument, it '
        #                              ' should be a nested dictionary. Got {} of type {}'.format(
        #                 v, type(v)
        #             )
        #             )
        # if isinstance(self.inputs, str):
        #     if not os.path.isfile(self.inputs):
        #         raise ValueError('If using str type for inputs argument, must be a str pointing '
        #                          'to a yaml file on disk')
        #     self.inputs = self._read_yaml()
        # else:
        #     raise ValueError('inputs argument should be (dict, str). Got "{}"'.format(type(self.inputs)))

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


class _PlotterBase:

    def __init__(self, data, plot_selection, conditions, subplot_titles={}, savefig=False,
                 plot_dir=os.path.abspath(''), fname=None, ncols=3, wspace=0.25, hspace=0.3,
                 figsize=(12, 7), legend_fontsize=12,
                 legend_loc='best', subplots_adjust={}, **kwargs):
        self.data = data
        self.plot_selection = plot_selection
        self.conditions = conditions
        self.subplot_titles = subplot_titles
        self.fname = fname
        self.savefig = savefig
        self.plot_dir = plot_dir
        self.legend_fontsize = legend_fontsize
        self.legend_loc = legend_loc
        self.ncols = ncols
        self.wspace = wspace
        self.hspace = hspace
        self.figsize = figsize
        self.subplots_adjust = subplots_adjust
        self.kwargs = kwargs

        if not self.savefig:
            self.animation = False

        self._nplots = len(self.plot_selection)
        if self._nplots == 1:
            self.ncols = 1
        self._num_rows = int(self._nplots / ncols)
        self._remainder = self._nplots % ncols
        if self._remainder > 0:
            self._num_rows += 1

    def _recursive_fname(self, zipped_inputs) -> str:
        """
        Make an appropriate filename from strings of inputs and values
        :return (str):
        """
        from functools import reduce
        if isinstance(zipped_inputs[0], (list, tuple)):  # if zipped is nested list
            new_zipped = [reduce(lambda x, y: f'{x}_{y}', i) for i in zipped_inputs]
            reduced = self._recursive_fname(new_zipped)
            return reduced
        else:
            reduced = reduce(lambda x, y: f'{x}_{y}', zipped_inputs)
            assert reduced is not None
            return reduced

    def _savefig(self, fname, dire=None):
        if not os.path.isdir(self.plot_dir):
            os.makedirs(self.plot_dir)

        fname = os.path.join(self.plot_dir, f'{fname}-{str(self.count).zfill(self.num_zeros_needed)}.png')
        plt.savefig(fname, dpi=300, bbox_inches='tight')
        print('saved to {}'.format(fname))
        return fname

    def animate(self, fname, ext='mp4', ovewrite=False, fps=8):
        if not hasattr(self, 'files_'):
            raise ValueError('must simulate files first')
        # files_str = "' '".join(self.files_)
        fname = f'{fname}.{ext}'

        if ovewrite:
            if os.path.isfile(fname):
                os.remove(fname)
        s = ''
        for f in self.files_:
            s += "file '{}'\n".format(f)
            tmp = os.path.join(self.plot_dir, 'tmp.txt')
        with open(tmp, 'w') as f:
            f.write(s)

        s = f"ffmpeg -f concat -safe 0 -r {fps} -i {tmp} {fname}"
        print('final command', s)
        os.system(s)
        os.remove(tmp)


class TimeSeriesPlotter(_PlotterBase):

    def plot(self):
        # take care of title
        fig = plt.figure(figsize=self.figsize)
        gs = GridSpec(self._num_rows, self.ncols, wspace=self.wspace, hspace=self.hspace)
        count = 0
        print(self.data)
        for k, v in self.plot_selection.items():
            ax = fig.add_subplot(gs[count])
            for cond in self.conditions:
                data = self.data[cond]
                for i in v:
                    plt.plot(data.index, data[i], label=f'{cond}_{i}')
            plt.legend(loc=self.legend_loc, fontsize=self.legend_fontsize)
            plt.title(k)
            sns.despine(fig, top=True, right=True)
            count += 1

        # plt.show()
        # plt.suptitle(plot_suptitle)
        plt.subplots_adjust(**self.subplots_adjust)
        if self.savefig:
            if not os.path.isdir(self.plot_dir):
                os.makedirs(self.plot_dir)
            fname = os.path.join(self.plot_dir, self.fname)
            plt.savefig(fname, dpi=300, bbox_inches='tight')
            print('saved to {}'.format(fname))

        else:
            plt.show()
        # return fname
