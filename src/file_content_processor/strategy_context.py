class StrategyContext:
    def __init__(self, *strategies):
        self._strategies = strategies

    def process(self, raw_content):
        content = []
        for entry in raw_content:
            processed_entry = {}
            for strategy in self._strategies:
                processed_entry.update(strategy.process(entry))
            content.append(processed_entry)
        return content
