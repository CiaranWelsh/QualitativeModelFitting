import os, glob

from collections.abc import Container, Iterator

#todo think about an alternative interface whereby
#  a interface/protocol is supplied and the user can define
#  their own test cases to a suite.


class Suite:

    def __init__(self, tests=[], name=None):
        self.tests = tests
        self.name = name
        self._tests = []

        self._iter_idx = 0  # index for iteration

        if not isinstance(self.tests, list):
            raise TypeError('Expecting a list for tests argument but got "{}"'.format(self.tests))

    def isempty(self):
        if not self.tests:
            return True
        return False

    def append(self, test):
        if test in self:
            raise ValueError(f'Test suite already '
                             f'has a test named "{test}". {self.tests}')
        self._tests.append(test)

    def pop(self, idx):
        self._tests.pop(idx)

    def clear(self):
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
