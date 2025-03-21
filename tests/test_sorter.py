import unittest

from file_content_processor import sorter


class TestSorter(unittest.TestCase):
    def setUp(self):
        super().setUp()

        self.sorter = sorter.MashStepsSorter()

    def test_should_get_empty_content_when_given_empty_content(self):
        assert self.sorter.process([]) == []

    def test_should_get_content_when_given_standard_nonempty_content(self):
        raw_content = [
            {"NAME": "Mash Out"},
            {"NAME": "Mash In"},
            {"NAME": "Beta 2"},
            {"NAME": "Beta 1"},
            {"NAME": "Alpha"},
        ]
        expected_content = [
            {"NAME": "Mash In"},
            {"NAME": "Beta 1"},
            {"NAME": "Beta 2"},
            {"NAME": "Alpha"},
            {"NAME": "Mash Out"},
        ]
        assert expected_content == self.sorter.process(raw_content)

    def test_should_get_content_when_given_nonempty_content_with_value_unspecified_in_sorting_order(self):
        raw_content = [
            {"NAME": "Unspecified"},
            {"NAME": "Mash Out"},
        ]
        expected_content = [
            {"NAME": "Mash Out"},
            {"NAME": "Unspecified"},
        ]
        assert expected_content == self.sorter.process(raw_content)

    def test_should_get_content_when_given_nonempty_content_with_two_pairs_of_identical_values(self):
        raw_content = [
            {"NAME": "Beta 1"},
            {"NAME": "Mash Out"},
            {"NAME": "Mash Out"},
            {"NAME": "Beta 1"},
        ]
        expected_content = [
            {"NAME": "Beta 1"},
            {"NAME": "Beta 1"},
            {"NAME": "Mash Out"},
            {"NAME": "Mash Out"},
        ]
        assert expected_content == self.sorter.process(raw_content)

    def test_should_get_content_when_given_nonempty_content_with_numeric_values(self):
        raw_content = [
            {"NAME": "Mash Out 1"},
            {"NAME": "1"},
            {"NAME": "Mash Out"},
        ]
        expected_content = [
            {"NAME": "Mash Out"},
            {"NAME": "Mash Out 1"},
            {"NAME": "1"},
        ]
        assert expected_content == self.sorter.process(raw_content)

    def test_should_get_content_when_given_nonempty_content_with_non_word_values(self):
        raw_content = [
            {"NAME": "."},
            {"NAME": "Mash Out."},
            {"NAME": "Mash Out"},
        ]
        expected_content = [
            {"NAME": "Mash Out"},
            {"NAME": "Mash Out."},
            {"NAME": "."},
        ]
        assert expected_content == self.sorter.process(raw_content)


if __name__ == "__main__":
    unittest.main()
