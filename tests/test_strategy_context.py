import datetime
import json
import pathlib
import unittest

import common.utils
import parameterized

from file_content_processor import strategy, strategy_context

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
    ("category", "strategy_context", "expected_return_value", "subname"),
    class_params,
    class_name_func=common.utils.customize_class_name,
)
class TestStrategyContext(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        with (pathlib.Path(__file__).parent / "./files/strategy_context.json").open(
            encoding="utf-8",
        ) as strategy_context_json:
            cls.recipe = json.load(strategy_context_json)

    def test_should_return_empty_value_when_given_empty_content(self):
        assert self.strategy_context.process([]) == []

    def test_should_return_nonempty_value_when_given_nonempty_content(self):
        assert self.expected_return_value == self.strategy_context.process(self.recipe[self.category])


class TestStrategyContextParameters(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.strategy_context = strategy_context.StrategyContext(
            strategy.ParametersStrategy(),
        )

    def test_should_return_empty_value_when_given_empty_content(self):
        assert self.strategy_context.process([]) == []

    def test_should_return_nonempty_value_when_given_nonempty_content(self):
        with (pathlib.Path(__file__).parent / "./files/strategy_context_parameters.json").open(
            encoding="utf-8",
        ) as strategy_context_parameters_json:
            recipe = json.load(strategy_context_parameters_json)

        assert [
            {
                "BATCH_NAME": "NEIPA (Juicy Bits)",
                "BATCH_NUMBER": 93,
                "BATCH_VOLUME": 21.0,
                "BOIL_TIME": datetime.timedelta(seconds=3600),
                "BOIL_VOLUME": 27.58,
                "COOLING_SHRINKAGE_PERCENTAGE": 4.0,
                "EVAPORATION_PERCENTAGE": 1.81,
                "FERMENTATION_TEMP": 19.0,
                "GRAIN_TEMP": 22.2,
                "IBU": 34.3,
                "INFUSE_TEMP": 60.2,
                "INFUSE_VOLUME": 24.2,
                "KNOCKOUT_VOLUME": 26.0,
                "MLT_DEADSPACE_VOLUME": 15.9,
                "OG": 1.066,
                "POST_BOIL_VOLUME": 27.08,
                "PRE_BOIL_OG": 1.062,
                "SPARGE_VOLUME": 27.58,
                "TRUB_CHILLER_VOLUME": 5.0,
                "WATER_GRAIN_RATIO": 2.6,
            },
        ] == self.strategy_context.process(recipe)


if __name__ == "__main__":
    unittest.main()
