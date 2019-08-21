import unittest

from collections import OrderedDict
from qualitative_model_fitting import manual_interface
from qualitative_model_fitting._simulator import TimeSeriesPlotter, TimeSeries

from tests import MODEL2


class ManualInterfaceTests(unittest.TestCase):

    def setUp(self) -> None:
        self.input = OrderedDict(
            WithSignal=OrderedDict(
                inputs=OrderedDict(
                    S=1
                ),
                obs=[
                    'A@t=20 > A@t=10',
                    'A@t=30 < A@t=20'
                ]
            ),
            WithSignalAndInhibitor=OrderedDict(
                inputs=OrderedDict(
                    S=1, I=1
                ),

                obs=[
                    'A@t=20 > A@t=10',
                    'A@t=30 < A@t=20'
                ]
            )
        )


    def test_correct_number_of_observations(self):
        results = manual_interface(MODEL2, self.input, 0, 50, 51)
        expected = 4
        actual = len(results)
        self.assertEqual(expected, actual)

    def test_obs1(self):
        results = manual_interface(MODEL2, self.input, 0, 50, 51)
        a = results.data['WithSignal']['A']
        t10 = a.loc[10]
        t20 = a.loc[20]
        t30 = a.loc[30]
        self.assertTrue(t20 > t10)

    def test_obs2(self):
        from qualitative_model_fitting import manual_interface
        results = manual_interface(MODEL2, self.input, 0, 50, 51)
        print(results.to_df())

        """
                                     observation  truth
        WithSignal             0  A@t=20 > A@t=10   True
                               1  A@t=30 < A@t=20   True
        WithSignalAndInhibitor 0  A@t=20 > A@t=10   True
                               1  A@t=30 < A@t=20  False 
        """




        a = results.data['WithSignal']['A']
        t20 = a.loc[20]
        t30 = a.loc[30]
        self.assertTrue(t30 < t20)

    def test_obs4(self):
        results = manual_interface(MODEL2, self.input, 0, 50, 51)
        print(results.to_df())
        # a = results.data['WithSignal']['A']
        # t20 = a.loc[20]
        # t30 = a.loc[30]
        # self.assertTrue(t30 < t20)

    def test_obs3(self):
        self.ts = TimeSeries(MODEL2, self.input, 0, 50, 51)
        plot_selection = dict(
            A=['A'],
            B=['B'],
            C=['C'],
            BI=['BI'],
        )
        conditions = ['WithSignal', 'WithSignalAndInhibitor']
        plotter = TimeSeriesPlotter(
            self.ts.simulate(),
            plot_selection,
            conditions,
            savefig=True,
            fname='test_plot.png',
            legend_loc='best',
            legend_fontsize=10,
            ncols=2
        )
        print(plotter.plot())

    # results = manual_interface(MODEL2, self.input, 0, 50, 51)
    # print(results.to_df())
    # a = results.data['WithSignal']['A']
    # t20 = a.loc[20]
    # t30 = a.loc[30]
    # self.assertTrue(t30 < t20)


if __name__ == '__main__':
    unittest.main()
