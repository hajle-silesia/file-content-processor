import abc


class UsageFilter(abc.ABC):
    _usage = []

    def process(self, raw_content):
        content = []
        for entry in raw_content:
            if entry['USE'] in self._usage:
                content.append(entry)
        return content


class HopsUsageFilter(UsageFilter):
    _usage = ['Mash', 'First Wort', 'Boil', 'Aroma']


class MiscsUsageFilter(UsageFilter):
    _usage = ['Mash', 'Sparge', 'Boil']

    def process(self, raw_content):
        self.__add_missing_usage_key(raw_content)
        return super().process(raw_content)

    def __add_missing_usage_key(self, raw_content):
        for entry in raw_content:
            if entry['USE'] is None:
                entry['USE'] = "Sparge"
