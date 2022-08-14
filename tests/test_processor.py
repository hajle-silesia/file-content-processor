import json
import unittest
from pathlib import Path

from parameterized import parameterized_class

from src.category_filter import *
from src.processor import Processor
from src.strategy import *
from src.strategy_context import StrategyContext
from src.usage_filter import *
from tests.utils import customize_class_name

with open(Path(__file__).parent / "./files/processor.json", encoding="utf-8") as processor_json:
    recipe = json.load(processor_json)

class_params = [(Processor(recipe_filter=RecipesFilter(),
                           category_filter=FermentablesFilter()),
                 [{"NAME": "Viking Malt Słód pale ale 5,5 EBC", "AMOUNT": "3.2723358"},
                  {"NAME": "Weyermann Słód pilzneński 4,5 EBC", "AMOUNT": "3.2723358"},
                  {"NAME": "Malteurop Słód pszeniczny jasny Mep@Wheat", "AMOUNT": "0.5799076"},
                  {"NAME": "Oats, Flaked", "AMOUNT": "0.5799076"},
                  {"NAME": "Wheat, Flaked", "AMOUNT": "0.5799076"}],
                 "None"),
                (Processor(recipe_filter=RecipesFilter(),
                           category_filter=HopsFilter(),
                           usage_filter=HopsUsageFilter(),
                           strategy_context=StrategyContext(NameStrategy(),
                                                            UseStrategy(),
                                                            AmountHopsStrategy(),
                                                            TimeStrategy(),
                                                            )),
                 [{"NAME": "TB Citra 2020", "USE": "Mash", "AMOUNT": 5, "TIME": datetime.timedelta(seconds=3600)},
                  {"NAME": "TB El Dorado 2020", "USE": "First Wort", "AMOUNT": 5,
                   "TIME": datetime.timedelta(seconds=3600)},
                  {"NAME": "TB Nectaron 2020", "USE": "Boil", "AMOUNT": 5,
                   "TIME": datetime.timedelta(seconds=3600)},
                  {"NAME": "TB Citra 2020", "USE": "Aroma", "AMOUNT": 7, "TIME": datetime.timedelta(seconds=2400)},
                  ],
                 "Hops"),
                (Processor(recipe_filter=RecipesFilter(),
                           category_filter=MiscsFilter(),
                           usage_filter=MiscsUsageFilter(),
                           strategy_context=StrategyContext(NameStrategy(),
                                                            UseStrategy(),
                                                            AmountMiscsStrategy(),
                                                            TimeStrategy(),
                                                            )),
                 [{"NAME": "Baker's Dry Yeast", "USE": "Mash", "AMOUNT": 12.77,
                   "TIME": datetime.timedelta(seconds=0)},
                  {"NAME": "Phosphoric Acid 75%", "USE": "Sparge", "AMOUNT": 6.0,
                   "TIME": datetime.timedelta(seconds=0)},
                  {"NAME": "Calcium Chloride", "USE": "Boil", "AMOUNT": 4.39,
                   "TIME": datetime.timedelta(seconds=0)},
                  ],
                 'Miscs'),
                (Processor(recipe_filter=RecipesFilter(),
                           category_filter=FermentablesFilter(),
                           strategy_context=StrategyContext(NameStrategy(),
                                                            AmountFermentablesStrategy(),
                                                            )),
                 [{"NAME": "Viking Malt Słód pale ale 5,5 EBC", "AMOUNT": 3.272},
                  {"NAME": "Weyermann Słód pilzneński 4,5 EBC", "AMOUNT": 3.272},
                  {"NAME": "Malteurop Słód pszeniczny jasny Mep@Wheat", "AMOUNT": 0.580},
                  {"NAME": "Oats, Flaked", "AMOUNT": 0.580},
                  {"NAME": "Wheat, Flaked", "AMOUNT": 0.580},
                  ],
                 'Fermentables'),
                (Processor(recipe_filter=RecipesFilter(),
                           category_filter=MashStepsFilter(),
                           strategy_context=StrategyContext(NameStrategy(),
                                                            MashStepTimeStrategy(),
                                                            MashStepTempStrategy(),
                                                            )),
                 [{"NAME": "Mash In", "STEP_TIME": datetime.timedelta(seconds=0), "STEP_TEMP": 55},
                  {"NAME": "Beta 2", "STEP_TIME": datetime.timedelta(seconds=5700), "STEP_TEMP": 61},
                  {"NAME": "Beta 1", "STEP_TIME": datetime.timedelta(seconds=300), "STEP_TEMP": 65},
                  {"NAME": "Alpha", "STEP_TIME": datetime.timedelta(seconds=1800), "STEP_TEMP": 72},
                  {"NAME": "Mash Out", "STEP_TIME": datetime.timedelta(seconds=600), "STEP_TEMP": 78},
                  ],
                 "MashSteps"),
                ]


@parameterized_class(('processor', 'expected_return_value', 'subname'), class_params,
                     class_name_func=customize_class_name)
class TestProcessor(unittest.TestCase):
    def test_Should_ReturnEmptyValue_When_GivenEmptyContent(self):
        self.assertEqual([], self.processor.process({}))

    def test_Should_ReturnNonemptyValue_When_GivenNonemptyContent(self):
        self.assertEqual(self.expected_return_value, self.processor.process(recipe))


if __name__ == "__main__":
    unittest.main()
