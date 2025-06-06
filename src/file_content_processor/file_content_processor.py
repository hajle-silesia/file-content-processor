import copy
import typing


class FileContentProcessor:
    _content_default: typing.ClassVar = {}

    def __init__(self, producer, processors):
        self.__producer = producer
        self.__processors = processors
        self.__raw_content = self._content_default
        self.__content = self._content_default

    @property
    def content(self):
        return self.__content

    def update(self, new_raw_content):
        self.__update_raw_content(new_raw_content)
        self.__process_raw_content()
        self.__notify()

    def __update_raw_content(self, new_raw_content):
        self.__raw_content = new_raw_content

    def __process_raw_content(self):
        if self.__raw_content:
            self.__content = copy.deepcopy(self._content_default)
            for processor_name, processor in self.__processors.items():
                if processor_name == "parameters":
                    self.__content.update({processor_name: processor.process(self.__raw_content)[0]})
                else:
                    self.__content.update({processor_name: processor.process(self.__raw_content)})

    def __notify(self):
        if self.content:
            self.__producer.send(
                topic="file-content-processor-topic",
                value=self.content,
            )
