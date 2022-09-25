import unittest

from src.sorter import *


class TestSorter(unittest.TestCase):
    def setUp(self):
        super().setUp()

        self.sorter = MashStepsSorter()

    def test_Should_GetEmptyContent_When_GivenEmptyContent(self):
        self.assertEqual([], self.sorter.process([]))

    def test_Should_GetContent_When_GivenStandardNonemptyContent(self):
        raw_content = [{'NAME': "Mash Out"},
                       {'NAME': "Mash In"},
                       {'NAME': "Beta 2"},
                       {'NAME': "Beta 1"},
                       {'NAME': "Alpha"},
                       ]
        expected_content = [{'NAME': "Mash In"},
                            {'NAME': "Beta 1"},
                            {'NAME': "Beta 2"},
                            {'NAME': "Alpha"},
                            {'NAME': "Mash Out"},
                            ]
        self.assertEqual(expected_content, self.sorter.process(raw_content))

    def test_Should_GetContent_When_GivenNonemptyContentWithValueUnspecifiedInSortingOrder(self):
        raw_content = [{'NAME': "Unspecified"},
                       {'NAME': "Mash Out"},
                       ]
        expected_content = [{'NAME': "Mash Out"},
                            {'NAME': "Unspecified"},
                            ]
        self.assertEqual(expected_content, self.sorter.process(raw_content))

    def test_Should_GetContent_When_GivenNonemptyContentWithTwoPairsOfIdenticalValues(self):
        raw_content = [{'NAME': "Beta 1"},
                       {'NAME': "Mash Out"},
                       {'NAME': "Mash Out"},
                       {'NAME': "Beta 1"},
                       ]
        expected_content = [{'NAME': "Beta 1"},
                            {'NAME': "Beta 1"},
                            {'NAME': "Mash Out"},
                            {'NAME': "Mash Out"},
                            ]
        self.assertEqual(expected_content, self.sorter.process(raw_content))

    def test_Should_GetContent_When_GivenNonemptyContentWithNumericValues(self):
        raw_content = [{'NAME': "Mash Out 1"},
                       {'NAME': "1"},
                       {'NAME': "Mash Out"},
                       ]
        expected_content = [{'NAME': "Mash Out"},
                            {'NAME': "Mash Out 1"},
                            {'NAME': "1"},
                            ]
        self.assertEqual(expected_content, self.sorter.process(raw_content))

    def test_Should_GetContent_When_GivenNonemptyContentWithNonWordValues(self):
        raw_content = [{'NAME': "."},
                       {'NAME': "Mash Out."},
                       {'NAME': "Mash Out"},
                       ]
        expected_content = [{'NAME': "Mash Out"},
                            {'NAME': "Mash Out."},
                            {'NAME': "."},
                            ]
        self.assertEqual(expected_content, self.sorter.process(raw_content))


if __name__ == "__main__":
    unittest.main()
