import threading


class FileContentProcessor(threading.Thread):
    _content_default = {}

    def __init__(self, notifier):
        threading.Thread.__init__(self, daemon=True)

        self.__notifier = notifier
        self.__raw_content = self._content_default
        self.__content = self._content_default

    @property
    def content(self):
        return self.__content

    def update(self, new_raw_content):
        if new_raw_content:
            self.__update_raw_content(new_raw_content)
            self.__process_raw_content()
            self.__notify()

    def __update_raw_content(self, new_raw_content):
        self.__raw_content = new_raw_content

    def __process_raw_content(self):
        if self.__raw_content:
            self.__content = self.__raw_content
            # converter = self.__create_converter(file_type_header)
            #
            # if converter:
            #     converter.process(self.__raw_content)
            #     self.__content = converter.content
            # else:
            #     self.__content = self.__raw_content

    def __notify(self):
        if self.content:
            self.__notifier.notify_observers(self.content)
