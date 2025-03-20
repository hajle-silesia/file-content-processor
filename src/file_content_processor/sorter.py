import abc
import re
import typing


class Sorter(abc.ABC):
    _order: typing.ClassVar = {}

    @abc.abstractmethod
    def process(self, raw_content):
        pass

    def _get_max_order_value(self):
        return max(self._order.values())


class MashStepsSorter(Sorter):
    _order: typing.ClassVar = {"MashIn": 0, "Beta": 1, "Alpha": 2, "MashOut": 3}

    def process(self, raw_content):
        return sorted(
            raw_content,
            key=lambda k: (
                self._order.get(self.__filter_non_alphabetic_characters(k["NAME"]), self._get_max_order_value() + 1),
                self.__filter_non_numeric_characters(k["NAME"]),
                self.__filter_word_characters(k["NAME"]),
            ),
        )

    def __filter_non_alphabetic_characters(self, value):
        return re.sub("[^a-zA-Z]", "", value)

    def __filter_non_numeric_characters(self, value):
        return re.sub("[^0-9]", "", value)

    def __filter_word_characters(self, value):
        return re.sub("[a-zA-Z0-9]", "", value)
