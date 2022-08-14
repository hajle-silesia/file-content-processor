import unittest

from parameterized import parameterized_class

from src.category_filter import *
from tests.utils import customize_class_name

class_params = [('RECIPES', 'RECIPE', RecipesFilter(), "Recipes"),
                ('HOPS', 'HOP', HopsFilter(), "Hops"),
                ('MISCS', 'MISC', MiscsFilter(), 'Miscs'),
                ('FERMENTABLES', 'FERMENTABLE', FermentablesFilter(), "Fermentables"),
                ('MASH_STEPS', 'MASH_STEP', MashStepsFilter(), "MashSteps"),
                ]


@parameterized_class(('category', 'entry', 'category_filter', 'subname'), class_params,
                     class_name_func=customize_class_name)
class TestCategoryFilter(unittest.TestCase):
    def test_Should_GetEmptyContent_When_GivenEmptyContent(self):
        self.assertEqual({}, self.category_filter.process({}))

    def test_Should_GetContent_When_GivenNonemptyContent(self):
        raw_content = {self.category: {self.entry: [{'entry_1_k': "entry_1_v"}, {'entry_2_k': "entry_2_v"}]},
                       'dummy_key': "dummy_value",
                       }
        if self.subname == 'Recipes':
            expected_content = [{'entry_1_k': "entry_1_v"}, {'entry_2_k': "entry_2_v"}]
        else:
            expected_content = {self.category: [{'entry_1_k': "entry_1_v"}, {'entry_2_k': "entry_2_v"}]}
        self.assertEqual(expected_content, self.category_filter.process(raw_content))


if __name__ == "__main__":
    unittest.main()
