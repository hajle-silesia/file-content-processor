import unittest

from parameterized import parameterized, parameterized_class

from src.strategy import *


def customize_class_name(cls, parameter_number, params_dict):
    class_name = cls.__name__
    class_subname = parameterized.to_safe_name(params_dict['subname'])

    return f"{class_name}{class_subname}"


@parameterized_class(('raw_content', 'strategy', 'expected_content', 'subname'),
                     [({'NAME': "test"}, NameStrategy(), {'NAME': "test"}, "Name"),
                      ({'USE': "test"}, UseStrategy(), {'USE': "test"}, "Use"),
                      ({'AMOUNT': "0.23499"}, AmountHopsStrategy(), {'AMOUNT': 235}, "AmountHops"),
                      ({'AMOUNT': "0.23499"}, AmountMiscsStrategy(), {'AMOUNT': 234.99}, "AmountMiscs"),
                      ({'AMOUNT': "0.23499"}, AmountFermentablesStrategy(), {'AMOUNT': 0.23}, "AmountFermentables"),
                      ({'TIME': "10"}, TimeStrategy(), {'TIME': datetime.timedelta(seconds=600)}, "Time"),
                      ({'STEP_TIME': "10"}, MashStepTimeStrategy(), {'STEP_TIME': datetime.timedelta(seconds=600)},
                       "MashStepTime"),
                      ({'STEP_TEMP': "64.99"}, MashStepTempStrategy(), {'STEP_TEMP': 65}, "MastStepTemp"),
                      ],
                     class_name_func=customize_class_name)
class TestStrategy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.set_test_arguments()
        cls.set_tested_objects()
        cls.set_test_expected_results()

    @classmethod
    def set_test_arguments(cls):
        pass

    @classmethod
    def set_tested_objects(cls):
        pass

    @classmethod
    def set_test_expected_results(cls):
        pass

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_Should_GetEmptyContent_When_GivenNoneContent(self):
        self.assertEqual({}, self.strategy.execute(None))

    def test_Should_GetEmptyContent_When_GivenEmptyContent(self):
        self.assertEqual({}, self.strategy.execute({}))

    def test_Should_GetContent_When_GivenNonemptyContent(self):
        self.assertEqual(self.expected_content, self.strategy.execute(self.raw_content))


if __name__ == "__main__":
    unittest.main()
