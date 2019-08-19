import unittest


from tests import MODEL1, TEST_INPUT1
from qualitative_model_fitting._test_factory import TestFactory


class TestMakerTests(unittest.TestCase):


    def test_dynamic_class_creation(self):
        statement = 'IRS1a@t=10 > Akt@t=10'
        t = TestFactory(MODEL1, TEST_INPUT1, 0, 100, 101)
        cls_list = t.create_test_cases()
        self.assertEqual('InsulinOnly', cls_list[0].__name__)

    def test_metaclass_usage(self):
        t = TestFactory(MODEL1, TEST_INPUT1, 0, 100, 101)
        cls = t.create_test_cases()
        expected = 'TestCaseMeta'
        actual = cls[0].__metaclass__.__name__
        self.assertEqual(expected, actual)

    def test_registered_by_metaclass(self):
        t = TestFactory(MODEL1, TEST_INPUT1, 0, 100, 101)
        cls = t.create_test_cases()
        print(cls[0].__metaclass__)

    def test_dynamic_class_creation3(self):
        t = TestFactory(MODEL1, TEST_INPUT1, 0, 100, 101)
        cls = t.create_test_cases()[0]
        print('sasdfasdf')
        print(cls)
        print(type(cls))

    def test_dynamic_class_creation2(self):
        statement = 'IRS1a@t=10 > Akt@t=10'
        t = TestFactory(MODEL1, TEST_INPUT1, 0, 100, 101)
        cls = t.create_test_cases()[0]
        cls().make_test()

if __name__ == '__main__':
    unittest.main()
