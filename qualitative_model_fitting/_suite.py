from typing import Optional

from qualitative_model_fitting._case import TestCase

#todo think about an alternative interface whereby
#  a interface/protocol is supplied and the user can define
#  their own test cases to a suite.


class Suite:
    """
    Stores collections of TestCase derivatives.
    """

    def __init__(self, tests=[], name=None):
        """

        Args:
            tests: list of TestCase derivatives
            name: optional name
        """
        self.tests = tests
        self.name = name
        self._tests = []

        self._iter_idx = 0  # index for iteration

        if not isinstance(self.tests, list):
            raise TypeError('Expecting a list for tests argument but got "{}"'.format(self.tests))

    def isempty(self):
        """
        Evaluate to True when Suite is void of tests
        Returns:

        """
        if not self.tests:
            return True
        return False

    def append(self, test: TestCase) -> None:
        """
        akin to the list.append method. Only accepts TestCase objects.
        Cannot already have an element `test` in the suite

        Args:
            test:

        Returns:

        """
        if test in self:
            raise ValueError(f'Test suite already '
                             f'has a test named "{test}". {self.tests}')
        if not isinstance(test, TestCase):
            raise TypeError('Can only store instances of TestCase in '
                            'a Suite. Got r"{}"'.format(type(test)))
        self._tests.append(test)

    def pop(self, idx: int):
        """
        Akin to list.pop method. Removes index idx from tests
        in the test suite.

        Args:
            idx: Index to remove

        Returns:

        """
        self._tests.pop(idx)

    def clear(self):
        """
        Clear suite of all tests
        Returns:

        """
        self._tests = []

    @property
    def tests(self):
        return self._tests

    @tests.setter
    def tests(self, tests):
        self._tests = tests

    def __iter__(self):
        return self

    def __next__(self):
        try:
            test = self.tests[self._iter_idx]
            self._iter_idx += 1
            return test
        except IndexError:
            self._iter_idx = 0
            raise StopIteration

    def __contains__(self, item):
        if item in self.tests:
            return True
        return False

    def __getitem__(self, item):
        if not isinstance(item, int):
            raise TypeError('Expecting an int index but got "{}"'.format(type(item)))
        return self.tests[item]



GLOBAL_TEST_SUITE = Suite([], name='global_test_suite')
