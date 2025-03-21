import datetime
import json
import pathlib
import unittest

import common.utils
import parameterized

from file_content_processor import strategy, strategy_context

with (pathlib.Path(__file__).parent / "./files/category_processor.json").open(
    encoding="utf-8",
) as category_processor_json:
    recipe = json.load(category_processor_json)

class_params = [
    (
        "HOPS",
        strategy_context.StrategyContext(
            strategy.NameStrategy(),
            strategy.UseStrategy(),
            strategy.AmountHopsStrategy(),
            strategy.TimeStrategy(),
        ),
        [
            {"NAME": "TB Citra 2020", "USE": "Mash", "AMOUNT": 5, "TIME": datetime.timedelta(seconds=3600)},
            {"NAME": "TB El Dorado 2020", "USE": "First Wort", "AMOUNT": 5, "TIME": datetime.timedelta(seconds=3600)},
            {"NAME": "TB Nectaron 2020", "USE": "Boil", "AMOUNT": 5, "TIME": datetime.timedelta(seconds=3600)},
            {"NAME": "TB Citra 2020", "USE": "Aroma", "AMOUNT": 7, "TIME": datetime.timedelta(seconds=2400)},
        ],
        "Hops",
    ),
    (
        "MISCS",
        strategy_context.StrategyContext(
            strategy.NameStrategy(),
            strategy.UseStrategy(),
            strategy.AmountMiscsStrategy(),
            strategy.TimeStrategy(),
        ),
        [
            {"NAME": "Baker's Dry Yeast", "USE": "Mash", "AMOUNT": 12.77, "TIME": datetime.timedelta(seconds=0)},
            {"NAME": "Phosphoric Acid 75%", "USE": "Sparge", "AMOUNT": 6.0, "TIME": datetime.timedelta(seconds=0)},
            {"NAME": "Calcium Chloride", "USE": "Boil", "AMOUNT": 4.39, "TIME": datetime.timedelta(seconds=0)},
        ],
        "Miscs",
    ),
    (
        "FERMENTABLES",
        strategy_context.StrategyContext(
            strategy.NameStrategy(),
            strategy.AmountFermentablesStrategy(),
        ),
        [
            {"NAME": "Viking Malt Słód pale ale 5,5 EBC", "AMOUNT": 3.272},
            {"NAME": "Weyermann Słód pilzneński 4,5 EBC", "AMOUNT": 3.272},
            {"NAME": "Malteurop Słód pszeniczny jasny Mep@Wheat", "AMOUNT": 0.580},
            {"NAME": "Oats, Flaked", "AMOUNT": 0.580},
            {"NAME": "Wheat, Flaked", "AMOUNT": 0.580},
        ],
        "Fermentables",
    ),
    (
        "MASH_STEPS",
        strategy_context.StrategyContext(
            strategy.NameStrategy(),
            strategy.MashStepTimeStrategy(),
            strategy.MashStepTempStrategy(),
        ),
        [
            {"NAME": "Mash In", "STEP_TIME": datetime.timedelta(seconds=0), "STEP_TEMP": 55},
            {"NAME": "Beta 2", "STEP_TIME": datetime.timedelta(seconds=5700), "STEP_TEMP": 61},
            {"NAME": "Beta 1", "STEP_TIME": datetime.timedelta(seconds=300), "STEP_TEMP": 65},
            {"NAME": "Alpha", "STEP_TIME": datetime.timedelta(seconds=1800), "STEP_TEMP": 72},
            {"NAME": "Mash Out", "STEP_TIME": datetime.timedelta(seconds=600), "STEP_TEMP": 78},
        ],
        "MashSteps",
    ),
]


@parameterized.parameterized_class(
    ("category", "category_processor", "expected_return_value", "subname"),
    class_params,
    class_name_func=common.utils.customize_class_name,
)
class TestCategoryProcessor(unittest.TestCase):
    def test_should_return_empty_value_when_given_empty_content(self):
        assert self.category_processor.process({}) == []

    def test_should_return_nonempty_value_when_given_nonempty_content(self):
        assert self.expected_return_value == self.category_processor.process(recipe[self.category])


if __name__ == "__main__":
    unittest.main()
