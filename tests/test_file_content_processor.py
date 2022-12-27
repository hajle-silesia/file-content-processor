import json
import pathlib
import unittest.mock

from src.category_filter import *
from src.file_content_processor import FileContentProcessor
from src.processor import Processor
from src.strategy import *
from src.strategy_context import StrategyContext
from src.usage_filter import *

with open(pathlib.Path(__file__).parent / "./files/file_content_processor.json",
          encoding="utf-8") as file_content_processor_json:
    recipe = json.load(file_content_processor_json)
with open(pathlib.Path(__file__).parent / "./files/file_content_processor_return_value.json",
          encoding="utf-8") as file_content_processor_return_value_json:
    expected_return_value = json.load(file_content_processor_return_value_json)


class MockProducer:
    def send(self, topic, value):
        pass


class TestFileContentProcessor(unittest.TestCase):
    producer = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.producer = MockProducer()

        hops_processor = Processor(recipe_filter=RecipesFilter(),
                                   category_filter=HopsFilter(),
                                   usage_filter=HopsUsageFilter(),
                                   strategy_context=StrategyContext(NameStrategy(),
                                                                    UseStrategy(),
                                                                    AmountHopsStrategy(),
                                                                    TimeStrategy()))
        miscs_processor = Processor(recipe_filter=RecipesFilter(),
                                    category_filter=MiscsFilter(),
                                    usage_filter=MiscsUsageFilter(),
                                    strategy_context=StrategyContext(NameStrategy(),
                                                                     UseStrategy(),
                                                                     AmountMiscsStrategy(),
                                                                     TimeStrategy()))
        fermentables_processor = Processor(recipe_filter=RecipesFilter(),
                                           category_filter=FermentablesFilter(),
                                           strategy_context=StrategyContext(NameStrategy(),
                                                                            AmountFermentablesStrategy()))
        mash_steps_processor = Processor(recipe_filter=RecipesFilter(),
                                         category_filter=MashStepsFilter(),
                                         strategy_context=StrategyContext(NameStrategy(),
                                                                          MashStepTimeStrategy(),
                                                                          MashStepTempStrategy()))
        parameters_processor = Processor(recipe_filter=RecipesFilter(),
                                         category_filter=ParametersFilter(),
                                         strategy_context=StrategyContext(ParametersStrategy()))

        cls.processors = {'hops': hops_processor,
                          'miscs': miscs_processor,
                          'fermentables': fermentables_processor,
                          'mash_steps': mash_steps_processor,
                          'parameters': parameters_processor,
                          }

    def setUp(self):
        super().setUp()

        self.file_content_processor = FileContentProcessor(producer=self.producer, processors=self.processors)

    def test_Should_GetEmptyContent_When_GivenNoneRawContent(self):
        self.file_content_processor.update(None)

        self.assertEqual({}, self.file_content_processor.content)

    def test_Should_GetEmptyContent_When_NoneRawContentBecomesEmptyRawContent(self):
        self.file_content_processor.update(None)
        self.file_content_processor.update({})

        self.assertEqual({}, self.file_content_processor.content)

    def test_Should_GetEmptyContent_When_GivenEmptyRawContent(self):
        self.file_content_processor.update({})

        self.assertEqual({}, self.file_content_processor.content)

    def test_Should_GetContent_When_EmptyRawContentBecomesNonemptyRawContent(self):
        self.file_content_processor.update({})
        self.file_content_processor.update(recipe)

        self.assertEqual(expected_return_value,
                         json.loads(json.dumps(self.file_content_processor.content, default=str)))

    def test_Should_GetContent_When_GivenNonemptyRawContent(self):
        self.file_content_processor.update(recipe)

        self.assertEqual(expected_return_value,
                         json.loads(json.dumps(self.file_content_processor.content, default=str)))

    def test_Should_GetContent_When_NoneRawContentBecomesNonemptyRawContent(self):
        self.file_content_processor.update(None)
        self.file_content_processor.update(recipe)

        self.assertEqual(expected_return_value,
                         json.loads(json.dumps(self.file_content_processor.content, default=str)))

    def test_Should_GetContent_When_NonemptyRawContentBecomesEmptyRawContent(self):
        self.file_content_processor.update(recipe)
        self.file_content_processor.update({})

        self.assertEqual(expected_return_value,
                         json.loads(json.dumps(self.file_content_processor.content, default=str)))

    def test_Should_GetEmptyContent_When_EmptyRawContentBecomesNoneRawContent(self):
        self.file_content_processor.update({})
        self.file_content_processor.update(None)

        self.assertEqual({}, self.file_content_processor.content)

    def test_Should_GetContent_When_NonemptyRawContentBecomesNoneRawContent(self):
        self.file_content_processor.update(recipe)
        self.file_content_processor.update(None)

        self.assertEqual(expected_return_value,
                         json.loads(json.dumps(self.file_content_processor.content, default=str)))
