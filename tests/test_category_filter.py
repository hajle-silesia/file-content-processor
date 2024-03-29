import unittest

import common.utils
import parameterized

from src.category_filter import *

class_params = [('RECIPES', 'RECIPE', RecipesFilter(), {}, "Recipes"),
                ('HOPS', 'HOP', HopsFilter(), [], "Hops"),
                ('MISCS', 'MISC', MiscsFilter(), [], 'Miscs'),
                ('FERMENTABLES', 'FERMENTABLE', FermentablesFilter(), [], "Fermentables"),
                ('MASH_STEPS', 'MASH_STEP', MashStepsFilter(), [], "MashSteps"),
                ('CATEGORY', 'ENTRY', ParametersFilter(), [], "Parameters"),
                ]


@parameterized.parameterized_class(('category', 'entry', 'category_filter', 'expected_return_value', 'subname'),
                                   class_params, class_name_func=common.utils.customize_class_name)
class TestCategoryFilter(unittest.TestCase):
    def test_Should_GetEmptyContent_When_GivenEmptyContent(self):
        self.assertEqual(self.expected_return_value, self.category_filter.process({}))

    def test_Should_GetContent_When_GivenNonemptyContent(self):
        raw_content = {self.category: {self.entry: [{'entry_1_k': "entry_1_v"}, {'entry_2_k': "entry_2_v"}]},
                       'dummy_key': "dummy_value",
                       }
        if self.subname == "Parameters":
            expected_content = [raw_content]
        else:
            expected_content = [{'entry_1_k': "entry_1_v"}, {'entry_2_k': "entry_2_v"}]
        self.assertEqual(expected_content, self.category_filter.process(raw_content))


if __name__ == "__main__":
    unittest.main()
