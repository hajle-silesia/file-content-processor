import unittest

import common.utils
import parameterized

from file_content_processor import usage_filter

class_params = [
    ("Boil", usage_filter.HopsUsageFilter(), "HopsBoil"),
    ("Aroma", usage_filter.HopsUsageFilter(), "HopsDryHop"),
    ("Mash", usage_filter.HopsUsageFilter(), "HopsMash"),
    ("First Wort", usage_filter.HopsUsageFilter(), "HopsFirstWort"),
    ("Boil", usage_filter.MiscsUsageFilter(), "MiscsBoil"),
    ("Mash", usage_filter.MiscsUsageFilter(), "MiscsMash"),
    ("Sparge", usage_filter.MiscsUsageFilter(), "MiscsSparge"),
]


@parameterized.parameterized_class(
    ("usage", "usage_filter", "subname"),
    class_params,
    class_name_func=common.utils.customize_class_name,
)
class TestUsageFilter(unittest.TestCase):
    def test_should_get_empty_content_when_given_empty_content(self):
        assert self.usage_filter.process([]) == []

    def test_should_get_content_when_given_nonempty_content(self):
        raw_content = [
            {"USE": self.usage, "entry_1_k": "entry_1_v"},
            {"USE": "dummy_value", "entry_2_k": "entry_2_v"},
        ]
        expected_content = [{"USE": self.usage, "entry_1_k": "entry_1_v"}]
        assert expected_content == self.usage_filter.process(raw_content)


class TestUsageFilterMiscsSpecial(unittest.TestCase):
    def test_should_get_content_when_given_content_without_use_key(self):
        raw_content = [
            {"USE": None, "entry_1_k": "entry_1_v"},
            {"USE": "dummy_value", "entry_2_k": "entry_2_v"},
        ]
        expected_content = [{"USE": "Sparge", "entry_1_k": "entry_1_v"}]
        assert expected_content == usage_filter.MiscsUsageFilter().process(raw_content)


if __name__ == "__main__":
    unittest.main()
