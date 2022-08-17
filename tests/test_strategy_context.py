import json
import unittest
from pathlib import Path

from parameterized import parameterized_class

from src.strategy import *
from src.strategy_context import StrategyContext
from tests.utils import customize_class_name

class_params = [('HOPS', StrategyContext(NameStrategy(),
                                         UseStrategy(),
                                         AmountHopsStrategy(),
                                         TimeStrategy(),
                                         ),
                 [{"NAME": "TB Citra 2020", "USE": "Mash", "AMOUNT": 5, "TIME": datetime.timedelta(seconds=3600)},
                  {"NAME": "TB El Dorado 2020", "USE": "First Wort", "AMOUNT": 5,
                   "TIME": datetime.timedelta(seconds=3600)},
                  {"NAME": "TB Nectaron 2020", "USE": "Boil", "AMOUNT": 5,
                   "TIME": datetime.timedelta(seconds=3600)},
                  {"NAME": "TB Citra 2020", "USE": "Aroma", "AMOUNT": 7, "TIME": datetime.timedelta(seconds=2400)},
                  ],
                 "Hops"),
                ('MISCS', StrategyContext(NameStrategy(),
                                          UseStrategy(),
                                          AmountMiscsStrategy(),
                                          TimeStrategy(),
                                          ),
                 [{"NAME": "Baker's Dry Yeast", "USE": "Mash", "AMOUNT": 12.77, "TIME": datetime.timedelta(seconds=0)},
                  {"NAME": "Phosphoric Acid 75%", "USE": "Sparge", "AMOUNT": 6.0,
                   "TIME": datetime.timedelta(seconds=0)},
                  {"NAME": "Calcium Chloride", "USE": "Boil", "AMOUNT": 4.39, "TIME": datetime.timedelta(seconds=0)},
                  ],
                 'Miscs'),
                ('FERMENTABLES', StrategyContext(NameStrategy(),
                                                 AmountFermentablesStrategy(),
                                                 ),
                 [{"NAME": "Viking Malt Słód pale ale 5,5 EBC", "AMOUNT": 3.272},
                  {"NAME": "Weyermann Słód pilzneński 4,5 EBC", "AMOUNT": 3.272},
                  {"NAME": "Malteurop Słód pszeniczny jasny Mep@Wheat", "AMOUNT": 0.580},
                  {"NAME": "Oats, Flaked", "AMOUNT": 0.580}, {"NAME": "Wheat, Flaked", "AMOUNT": 0.580},
                  ],
                 'Fermentables'),
                ('MASH_STEPS', StrategyContext(NameStrategy(),
                                               MashStepTimeStrategy(),
                                               MashStepTempStrategy(),
                                               ),
                 [{"NAME": "Mash In", "STEP_TIME": datetime.timedelta(seconds=0), "STEP_TEMP": 55},
                  {"NAME": "Beta 2", "STEP_TIME": datetime.timedelta(seconds=5700), "STEP_TEMP": 61},
                  {"NAME": "Beta 1", "STEP_TIME": datetime.timedelta(seconds=300), "STEP_TEMP": 65},
                  {"NAME": "Alpha", "STEP_TIME": datetime.timedelta(seconds=1800), "STEP_TEMP": 72},
                  {"NAME": "Mash Out", "STEP_TIME": datetime.timedelta(seconds=600), "STEP_TEMP": 78},
                  ],
                 "MashSteps"),
                ]


@parameterized_class(('category', 'strategy_context', 'expected_return_value', 'subname'), class_params,
                     class_name_func=customize_class_name)
class TestStrategyContext(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        with open(Path(__file__).parent / "./files/strategy_context.json", encoding="utf-8") as strategy_context_json:
            cls.recipe = json.load(strategy_context_json)

    def test_Should_ReturnEmptyValue_When_GivenEmptyContent(self):
        self.assertEqual([], self.strategy_context.process({}))

    def test_Should_ReturnNonemptyValue_When_GivenNonemptyContent(self):
        self.assertEqual(self.expected_return_value, self.strategy_context.process(self.recipe[self.category]))


class TestStrategyContextParameters(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.strategy_context = StrategyContext(ParametersStrategy(),
                                               )

    def test_Should_ReturnEmptyValue_When_GivenEmptyContent(self):
        self.assertEqual([], self.strategy_context.process({}))

    def test_Should_ReturnNonemptyValue_When_GivenNonemptyContent(self):
        with open(Path(__file__).parent / "./files/strategy_context_parameters.json",
                  encoding="utf-8") as strategy_context_parameters_json:
            recipe = json.load(strategy_context_parameters_json)

        self.assertEqual([{'BATCH_NAME': 'NEIPA (Juicy Bits)',
                           'BATCH_NUMBER': 93,
                           'BATCH_VOLUME': 21.0,
                           'BOIL_TIME': datetime.timedelta(seconds=3600),
                           'BOIL_VOLUME': 27.58,
                           'COOLING_SHRINKAGE_PERCENTAGE': 4.0,
                           'EVAPORATION_PERCENTAGE': 1.81,
                           'FERMENTATION_TEMP': 19.0,
                           'GRAIN_TEMP': 22.2,
                           'IBU': 34.3,
                           'INFUSE_TEMP': 60.2,
                           'INFUSE_VOLUME': 24.2,
                           'KNOCKOUT_VOLUME': 26.0,
                           'MLT_DEADSPACE_VOLUME': 15.9,
                           'OG': 1.066,
                           'POST_BOIL_VOLUME': 27.08,
                           'PRE_BOIL_OG': 1.062,
                           'SPARGE_VOLUME': 27.58,
                           'TRUB_CHILLER_VOLUME': 5.0,
                           'WATER_GRAIN_RATIO': 2.6},
                          ], self.strategy_context.process(recipe))


if __name__ == "__main__":
    unittest.main()
