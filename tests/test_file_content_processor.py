import json
import pathlib
import unittest.mock

import common.notifier
import common.storage
import common.utils

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

url = {'observer': "http://observer/update"}


def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] in url.values():
        return MockResponse(None, 204)
    else:
        return MockResponse(None, 404)


@unittest.mock.patch("common.notifier.requests.post", side_effect=mocked_requests_post)
class TestFileContentProcessor(unittest.TestCase):
    storage = None
    storage_path = None
    notifier = None

    @classmethod
    def setUpClass(cls):
        cls.storage = common.storage.Storage()
        cls.storage_path = pathlib.Path(__file__).parent / "./data.json"
        cls.storage.path = cls.storage_path
        cls.notifier = common.notifier.Notifier(cls.storage)
        cls.notifier.register_observer(url)

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

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

        common.utils.remove_file(cls.storage_path)

    def setUp(self):
        super().setUp()

        self.file_content_processor = FileContentProcessor(notifier=self.notifier, processors=self.processors)

    def test_Should_GetEmptyContent_When_GivenNoneRawContent(self, mock_get):
        self.file_content_processor.update(None)

        self.assertEqual({}, self.file_content_processor.content)

    def test_Should_GetEmptyContent_When_NoneRawContentBecomesEmptyRawContent(self, mock_get):
        self.file_content_processor.update(None)
        self.file_content_processor.update({})

        self.assertEqual({}, self.file_content_processor.content)

    def test_Should_GetEmptyContent_When_GivenEmptyRawContent(self, mock_get):
        self.file_content_processor.update({})

        self.assertEqual({}, self.file_content_processor.content)

    def test_Should_GetContent_When_EmptyRawContentBecomesNonemptyRawContent(self, mock_get):
        self.file_content_processor.update({})
        self.file_content_processor.update(recipe)

        self.assertEqual(expected_return_value,
                         json.loads(json.dumps(self.file_content_processor.content, default=str)))
        self.assertEqual(204, self.notifier.responses[0].status_code)
        self.assertEqual(None, self.notifier.responses[0].json())

    def test_Should_GetContent_When_GivenNonemptyRawContent(self, mock_get):
        self.file_content_processor.update(recipe)

        self.assertEqual(expected_return_value,
                         json.loads(json.dumps(self.file_content_processor.content, default=str)))
        self.assertEqual(204, self.notifier.responses[0].status_code)
        self.assertEqual(None, self.notifier.responses[0].json())

    def test_Should_GetContent_When_NoneRawContentBecomesNonemptyRawContent(self, mock_get):
        self.file_content_processor.update(None)
        self.file_content_processor.update(recipe)

        self.assertEqual(expected_return_value,
                         json.loads(json.dumps(self.file_content_processor.content, default=str)))
        self.assertEqual(204, self.notifier.responses[0].status_code)
        self.assertEqual(None, self.notifier.responses[0].json())

    def test_Should_GetContent_When_NonemptyRawContentBecomesEmptyRawContent(self, mock_get):
        self.file_content_processor.update(recipe)
        self.file_content_processor.update({})

        self.assertEqual(expected_return_value,
                         json.loads(json.dumps(self.file_content_processor.content, default=str)))

    def test_Should_GetEmptyContent_When_EmptyRawContentBecomesNoneRawContent(self, mock_get):
        self.file_content_processor.update({})
        self.file_content_processor.update(None)

        self.assertEqual({}, self.file_content_processor.content)

    def test_Should_GetContent_When_NonemptyRawContentBecomesNoneRawContent(self, mock_get):
        self.file_content_processor.update(recipe)
        self.file_content_processor.update(None)

        self.assertEqual(expected_return_value,
                         json.loads(json.dumps(self.file_content_processor.content, default=str)))
