import unittest

from parameterized import parameterized_class

from src.category_filter import *
from tests.utils import customize_class_name

class_params = [('HOPS', 'HOP', HopsFilter(), "Hops"),
                ('MISCS', 'MISC', MiscsFilter(), 'Miscs'),
                ('FERMENTABLES', 'FERMENTABLE', FermentablesFilter(), "Fermentables"),
                ('MASH_STEPS', 'MASH_STEP', MashStepsFilter(), "MashSteps"),
                ]


@parameterized_class(('category', 'entry', 'category_filter', 'subname'), class_params,
                     class_name_func=customize_class_name)
class TestCategoryFilter(unittest.TestCase):
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
        self.assertEqual({}, self.category_filter.process(None))

    def test_Should_GetEmptyContent_When_GivenEmptyContent(self):
        self.assertEqual({}, self.category_filter.process({}))

    def test_Should_GetContent_When_GivenNonemptyContent(self):
        raw_content = {self.category: {self.entry: [{'entry_1_k': "entry_1_v"}, {'entry_2_k': "entry_2_v"}]},
                       'dummy_key': "dummy_value",
                       }
        expected_content = {self.category: [{'entry_1_k': "entry_1_v"}, {'entry_2_k': "entry_2_v"}]}
        self.assertEqual(expected_content, self.category_filter.process(raw_content))


if __name__ == "__main__":
    unittest.main()
