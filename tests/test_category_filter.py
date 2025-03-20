import unittest

import common.utils
import parameterized

from file_content_processor import category_filter

class_params = [
    ("RECIPES", "RECIPE", category_filter.RecipesFilter(), {}, "Recipes"),
    ("HOPS", "HOP", category_filter.HopsFilter(), [], "Hops"),
    ("MISCS", "MISC", category_filter.MiscsFilter(), [], "Miscs"),
    ("FERMENTABLES", "FERMENTABLE", category_filter.FermentablesFilter(), [], "Fermentables"),
    ("MASH_STEPS", "MASH_STEP", category_filter.MashStepsFilter(), [], "MashSteps"),
    ("CATEGORY", "ENTRY", category_filter.ParametersFilter(), [], "Parameters"),
]


@parameterized.parameterized_class(
    ("category", "entry", "category_filter", "expected_return_value", "subname"),
    class_params,
    class_name_func=common.utils.customize_class_name,
)
class TestCategoryFilter(unittest.TestCase):
    def test_should_getemptycontent_when_given_empty_content(self):
        assert self.expected_return_value == self.category_filter.process({})

    def test_should_get_content_when_given_nonempty_content(self):
        raw_content = {
            self.category: {self.entry: [{"entry_1_k": "entry_1_v"}, {"entry_2_k": "entry_2_v"}]},
            "dummy_key": "dummy_value",
        }
        if self.subname == "Parameters":
            expected_content = [raw_content]
        else:
            expected_content = [{"entry_1_k": "entry_1_v"}, {"entry_2_k": "entry_2_v"}]
        assert expected_content == self.category_filter.process(raw_content)


if __name__ == "__main__":
    unittest.main()
