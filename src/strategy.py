import datetime
from abc import ABC, abstractmethod


class Strategy(ABC):
    @abstractmethod
    def execute(self, content):
        return {}


class NameStrategy(Strategy):
    def execute(self, content):
        return {'NAME': content['NAME']} if content else super().execute(content)


class UseStrategy(Strategy):
    def execute(self, content):
        return {'USE': content['USE']} if content else super().execute(content)


class AmountHopsStrategy(Strategy):
    def execute(self, content):
        return {'AMOUNT': int(round(1e3 * float(content['AMOUNT']), 0))} if content else super().execute(content)


class AmountMiscsStrategy(Strategy):
    def execute(self, content):
        return {'AMOUNT': round(1e3 * float(content['AMOUNT']), 2)} if content else super().execute(content)


class AmountFermentablesStrategy(Strategy):
    def execute(self, content):
        return {'AMOUNT': round(float(content['AMOUNT']), 2)} if content else super().execute(content)


class TimeStrategy(Strategy):
    def execute(self, content):
        return {
            'TIME': datetime.timedelta(minutes=int(round(float(content['TIME']), 0)))} if content else super().execute(
            content)


class MashStepTimeStrategy(Strategy):
    def execute(self, content):
        return {'STEP_TIME': datetime.timedelta(
            minutes=int(round(float(content['STEP_TIME']), 0)))} if content else super().execute(content)


class MashStepTempStrategy(Strategy):
    def execute(self, content):
        return {'STEP_TEMP': int(round(float(content['STEP_TEMP']), 0))} if content else super().execute(content)
