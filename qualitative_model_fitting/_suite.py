import os, glob

from collections.abc import Container, Iterator


class Suite:

    def __init__(self, tests: list):
        self.tests = tests
        self._tests = []
        self._iter_idx = 0  # index for iteration

        if not isinstance(self.tests, list):
            raise TypeError('Expecting a list for tests argument but got "{}"'.format(self.tests))

    def add_test_case(self, test):
        self._tests.append(test)

    def remove_test_case(self, idx):
        self._tests.pop(idx)

    @property
    def tests(self):
        return self._tests

    @tests.setter
    def tests(self, tests):
        self._tests = tests

    def __iter__(self):
        return self

    def __next__(self):
        yield self.tests[self._iter_idx]
        self._iter_idx += 1


GLOBAL_TEST_SUITE = Suite([])
