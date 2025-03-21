import json
import pathlib
import unittest.mock

from file_content_processor import (
    category_filter,
    file_content_processor,
    processor,
    strategy,
    strategy_context,
    usage_filter,
)

with (pathlib.Path(__file__).parent / "./files/file_content_processor.json").open(
    encoding="utf-8",
) as file_content_processor_json:
    recipe = json.load(file_content_processor_json)
with (pathlib.Path(__file__).parent / "./files/file_content_processor_return_value.json").open(
    encoding="utf-8",
) as file_content_processor_return_value_json:
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

        hops_processor = processor.Processor(
            recipe_filter=category_filter.RecipesFilter(),
            category_filter=category_filter.HopsFilter(),
            usage_filter=usage_filter.HopsUsageFilter(),
            strategy_context=strategy_context.StrategyContext(
                strategy.NameStrategy(),
                strategy.UseStrategy(),
                strategy.AmountHopsStrategy(),
                strategy.TimeStrategy(),
            ),
        )
        miscs_processor = processor.Processor(
            recipe_filter=category_filter.RecipesFilter(),
            category_filter=category_filter.MiscsFilter(),
            usage_filter=usage_filter.MiscsUsageFilter(),
            strategy_context=strategy_context.StrategyContext(
                strategy.NameStrategy(),
                strategy.UseStrategy(),
                strategy.AmountMiscsStrategy(),
                strategy.TimeStrategy(),
            ),
        )
        fermentables_processor = processor.Processor(
            recipe_filter=category_filter.RecipesFilter(),
            category_filter=category_filter.FermentablesFilter(),
            strategy_context=strategy_context.StrategyContext(
                strategy.NameStrategy(),
                strategy.AmountFermentablesStrategy(),
            ),
        )
        mash_steps_processor = processor.Processor(
            recipe_filter=category_filter.RecipesFilter(),
            category_filter=category_filter.MashStepsFilter(),
            strategy_context=strategy_context.StrategyContext(
                strategy.NameStrategy(),
                strategy.MashStepTimeStrategy(),
                strategy.MashStepTempStrategy(),
            ),
        )
        parameters_processor = processor.Processor(
            recipe_filter=category_filter.RecipesFilter(),
            category_filter=category_filter.ParametersFilter(),
            strategy_context=strategy_context.StrategyContext(strategy.ParametersStrategy()),
        )

        cls.processors = {
            "hops": hops_processor,
            "miscs": miscs_processor,
            "fermentables": fermentables_processor,
            "mash_steps": mash_steps_processor,
            "parameters": parameters_processor,
        }

    def setUp(self):
        super().setUp()

        self.file_content_processor = file_content_processor.FileContentProcessor(
            producer=self.producer,
            processors=self.processors,
        )

    def test_should_get_empty_content_when_given_none_raw_content(self):
        self.file_content_processor.update(None)

        assert self.file_content_processor.content == {}

    def test_should_get_empty_content_when_none_raw_content_becomes_empty_raw_content(self):
        self.file_content_processor.update(None)
        self.file_content_processor.update({})

        assert self.file_content_processor.content == {}

    def test_should_get_empty_content_when_given_empty_raw_content(self):
        self.file_content_processor.update({})

        assert self.file_content_processor.content == {}

    def test_should_get_content_when_empty_raw_content_becomes_nonempty_raw_content(self):
        self.file_content_processor.update({})
        self.file_content_processor.update(recipe)

        assert expected_return_value == json.loads(json.dumps(self.file_content_processor.content, default=str))

    def test_should_get_content_when_given_nonempty_raw_content(self):
        self.file_content_processor.update(recipe)

        assert expected_return_value == json.loads(json.dumps(self.file_content_processor.content, default=str))

    def test_should_get_content_when_none_raw_content_becomes_nonempty_raw_content(self):
        self.file_content_processor.update(None)
        self.file_content_processor.update(recipe)

        assert expected_return_value == json.loads(json.dumps(self.file_content_processor.content, default=str))

    def test_should_get_content_when_nonempty_raw_content_becomes_empty_raw_content(self):
        self.file_content_processor.update(recipe)
        self.file_content_processor.update({})

        assert expected_return_value == json.loads(json.dumps(self.file_content_processor.content, default=str))

    def test_should_get_empty_content_when_empty_raw_content_becomes_none_raw_content(self):
        self.file_content_processor.update({})
        self.file_content_processor.update(None)

        assert self.file_content_processor.content == {}

    def test_should_get_content_when_nonempty_raw_content_becomes_none_raw_content(self):
        self.file_content_processor.update(recipe)
        self.file_content_processor.update(None)

        assert expected_return_value == json.loads(json.dumps(self.file_content_processor.content, default=str))
