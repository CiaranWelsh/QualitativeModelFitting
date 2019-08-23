import logging
from typing import Optional

from qualitative_model_fitting import _suite, _results

LOG = logging.getLogger(__name__)

class _RunnerBase:
    """
    Base class for Runner types
    """

    def __init__(self, suite: Optional[_suite.Suite]):
        """

        Args:
            suite: A Suite of tests to run.
        """
        self.suite = suite


class ManualRunner(_RunnerBase):
    """
    Runner for the manual interface. No optimization required.
    """

    def run_tests(self) -> _results.DictResults:
        """
        Run the results in test suite and store the results in a
        DictResults object.

        Returns:

        """

        if self.suite.isempty():
            raise ValueError('Test suite is empty')

        results = _results.DictResults()
        for test_case in self.suite:
            test_case = test_case()
            # results.obs[test_case] = test_case.obs
            obs = test_case.obs
            tests = test_case.make_tests()
            results[test_case.__class__.__name__] = {}
            for i, (test_name, test_method) in enumerate(tests.items()):
                # LOG.debug(f'name', test_case.__class__.__name__)
                # LOG.debug(f'obs i', obs[i])
                # LOG.debug(f'method out', test_method())
                results[test_case.__class__.__name__][obs[i]] = test_method()
                results.data[test_case.__class__.__name__] = test_case.data
        print('results', results)
        return results


class AutomaticRunner(_RunnerBase):
    """
    Runner for automatic interface. Not yet implemented
    but eventually will modify parameters to satisfy conditions
    """

    def __init__(self):
        raise NotImplementedError
