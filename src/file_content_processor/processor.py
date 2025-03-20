class Processor:
    def __init__(self, recipe_filter, category_filter, usage_filter=None, strategy_context=None, sorter=None):
        self._recipe_filter = recipe_filter
        self._category_filter = category_filter
        self._usage_filter = usage_filter
        self._strategy_context = strategy_context
        self._sorter = sorter

    def process(self, raw_content):
        recipe_filtered_content = self._filter_recipe(raw_content)
        category_filtered_content = self._filter_category(recipe_filtered_content)
        usage_filtered_content = self._filter_usage(category_filtered_content)
        strategy_context_processed_content = self._process_context_strategy(usage_filtered_content)
        return self._sort(strategy_context_processed_content)

    def _filter_recipe(self, raw_content):
        return self._recipe_filter.process(raw_content)

    def _filter_category(self, raw_content):
        return self._category_filter.process(raw_content)

    def _filter_usage(self, raw_content):
        return self._usage_filter.process(raw_content) if self._usage_filter else raw_content

    def _process_context_strategy(self, raw_content):
        return self._strategy_context.process(raw_content) if self._strategy_context else raw_content

    def _sort(self, raw_content):
        return self._sorter.process(raw_content) if self._sorter else raw_content
