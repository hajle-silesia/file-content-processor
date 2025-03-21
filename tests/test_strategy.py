import datetime
import json
import pathlib
import unittest

import common.utils
import parameterized

from file_content_processor import strategy

class_params = [
    ({"NAME": "test"}, strategy.NameStrategy(), {"NAME": "test"}, "Name"),
    ({"USE": "test"}, strategy.UseStrategy(), {"USE": "test"}, "Use"),
    ({"AMOUNT": "0.23499"}, strategy.AmountHopsStrategy(), {"AMOUNT": 235}, "AmountHops"),
    ({"AMOUNT": "0.23499"}, strategy.AmountMiscsStrategy(), {"AMOUNT": 234.99}, "AmountMiscs"),
    ({"AMOUNT": "0.23499"}, strategy.AmountFermentablesStrategy(), {"AMOUNT": 0.235}, "AmountFermentables"),
    ({"TIME": "10"}, strategy.TimeStrategy(), {"TIME": datetime.timedelta(seconds=600)}, "Time"),
    (
        {"STEP_TIME": "10"},
        strategy.MashStepTimeStrategy(),
        {"STEP_TIME": datetime.timedelta(seconds=600)},
        "MashStepTime",
    ),
    ({"STEP_TEMP": "64.99"}, strategy.MashStepTempStrategy(), {"STEP_TEMP": 65}, "MastStepTemp"),
]

with (pathlib.Path(__file__).parent / "./files/strategy.json").open(encoding="utf-8") as parameters_raw_content_json:
    parameters_raw_content = json.load(parameters_raw_content_json)
parameters_expected_content = {
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
}
class_params.append((parameters_raw_content, strategy.ParametersStrategy(), parameters_expected_content, "Parameters"))

dummy_raw_content = {"dummy_key": "dummy_value"}
for param in class_params:
    param[0].update(dummy_raw_content)


@parameterized.parameterized_class(
    ("raw_content", "strategy", "expected_content", "subname"),
    class_params,
    class_name_func=common.utils.customize_class_name,
)
class TestStrategy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.set_test_arguments()
        cls.set_tested_objects()
        cls.set_test_expected_results()

    @classmethod
    def set_test_arguments(cls):
        pass

    @classmethod
    def set_tested_objects(cls):
        pass

    @classmethod
    def set_test_expected_results(cls):
        pass

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_should_get_empty_content_when_given_none_content(self):
        assert self.strategy.process(None) == {}

    def test_should_get_empty_content_when_given_empty_content(self):
        assert self.strategy.process({}) == {}

    def test_should_get_content_when_given_nonempty_content(self):
        assert self.expected_content == self.strategy.process(self.raw_content)


if __name__ == "__main__":
    unittest.main()
