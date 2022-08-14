from abc import ABC


class CategoryFilter(ABC):
    _category = ''
    _entry = ''
    _content_default = []

    def process(self, raw_content):
        return raw_content[self._category][self._entry] if raw_content else self._content_default


class RecipesFilter(CategoryFilter):
    _category = 'RECIPES'
    _entry = 'RECIPE'
    _content_default = {}


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
