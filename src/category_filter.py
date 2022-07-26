from abc import ABC


class CategoryFilter(ABC):
    _category = ''
    _entry = ''

    def __init__(self):
        self._raw_content = None

    def process(self, raw_content):
        return {self._category: raw_content[self._category][self._entry]} if raw_content else {}


class HopsFilter(CategoryFilter):
    _category = 'HOPS'
    _entry = 'HOP'


class MiscsFilter(CategoryFilter):
    _category = 'MISCS'
    _entry = 'MISC'


class FermentablesFilter(CategoryFilter):
    _category = 'FERMENTABLES'
    _entry = 'FERMENTABLE'


class MashStepsFilter(CategoryFilter):
    _category = 'MASH_STEPS'
    _entry = 'MASH_STEP'
