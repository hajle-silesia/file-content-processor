import unittest

from parameterized import parameterized, parameterized_class

from src.usage_filter import *


def customize_class_name(cls, parameter_number, params_dict):
    class_name = cls.__name__
    class_subname = parameterized.to_safe_name(params_dict['subname'])

    return f"{class_name}{class_subname}"


class_params = [("Boil", HopsUsageFilter(), "HopsBoil"),
                ("Aroma", HopsUsageFilter(), "HopsDryHop"),
                ("Mash", HopsUsageFilter(), "HopsMash"),
                ("First Wort", HopsUsageFilter(), "HopsFirstWort"),
                ("Boil", MiscsUsageFilter(), "MiscsBoil"),
                ("Mash", MiscsUsageFilter(), "MiscsMash"),
                ("Sparge", MiscsUsageFilter(), "MiscsSparge"),
                ]


@parameterized_class(('usage', 'usage_filter', 'subname'), class_params,
                     class_name_func=customize_class_name)
class TestUsageFilter(unittest.TestCase):
    def test_Should_GetEmptyContent_When_GivenEmptyContent(self):
        self.assertEqual([], self.usage_filter.process({}))

    def test_Should_GetContent_When_GivenNonemptyContent(self):
        raw_content = [{'USE': self.usage, 'entry_1_k': "entry_1_v"},
                       {'USE': "dummy_value", 'entry_2_k': "entry_2_v"},
                       ]
        expected_content = [{'USE': self.usage, 'entry_1_k': "entry_1_v"}]
        self.assertEqual(expected_content, self.usage_filter.process(raw_content))


class TestUsageFilterMiscsSpecial(unittest.TestCase):
    def test_Should_GetContent_When_GivenContentWithoutUSEKey(self):
        raw_content = [{'entry_1_k': "entry_1_v"},
                       {'USE': "dummy_value", 'entry_2_k': "entry_2_v"},
                       ]
        expected_content = [{'USE': "Sparge", 'entry_1_k': "entry_1_v"}]
        self.assertEqual(expected_content, MiscsUsageFilter().process(raw_content))


if __name__ == "__main__":
    unittest.main()
