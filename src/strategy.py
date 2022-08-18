import datetime
from abc import ABC, abstractmethod


class Strategy(ABC):
    @abstractmethod
    def process(self, raw_content):
        return {}


class NameStrategy(Strategy):
    def process(self, raw_content):
        return {'NAME': raw_content['NAME']} if raw_content else super().process(raw_content)


class UseStrategy(Strategy):
    def process(self, raw_content):
        return {'USE': raw_content['USE']} if raw_content else super().process(raw_content)


class AmountHopsStrategy(Strategy):
    def process(self, raw_content):
        return {'AMOUNT': int(round(1e3 * float(raw_content['AMOUNT']), 0))} if raw_content else super().process(
            raw_content)


class AmountMiscsStrategy(Strategy):
    def process(self, raw_content):
        return {'AMOUNT': round(1e3 * float(raw_content['AMOUNT']), 2)} if raw_content else super().process(raw_content)


class AmountFermentablesStrategy(Strategy):
    def process(self, raw_content):
        return {'AMOUNT': round(float(raw_content['AMOUNT']), 3)} if raw_content else super().process(raw_content)


class TimeStrategy(Strategy):
    def process(self, raw_content):
        return {
            'TIME': datetime.timedelta(
                minutes=int(round(float(raw_content['TIME']), 0)))} if raw_content else super().process(raw_content)


class MashStepTimeStrategy(Strategy):
    def process(self, raw_content):
        return {'STEP_TIME': datetime.timedelta(
            minutes=int(round(float(raw_content['STEP_TIME']), 0)))} if raw_content else super().process(raw_content)


class MashStepTempStrategy(Strategy):
    def process(self, raw_content):
        return {'STEP_TEMP': int(round(float(raw_content['STEP_TEMP']), 0))} if raw_content else super().process(
            raw_content)


class ParametersStrategy(Strategy):
    def process(self, raw_content):
        if raw_content:
            content = {}
            content['GRAIN_TEMP'] = round(float(raw_content['GRAIN_TEMP']), 2)
            content['WATER_GRAIN_RATIO'] = round(
                float(raw_content['MASH_STEPS']['MASH_STEP'][0]['WATER_GRAIN_RATIO'].split()[0].replace(',', '.')), 1)
            content['INFUSE_VOLUME'] = round(
                float(raw_content['MASH_STEPS']['MASH_STEP'][0]['DISPLAY_INFUSE_AMT'].split()[0]), 2)
            content['INFUSE_TEMP'] = round(float(raw_content['MASH_STEPS']['MASH_STEP'][0]['INFUSE_TEMP'].split()[0]),
                                           1)
            content['MLT_DEADSPACE_VOLUME'] = round(float(raw_content['MLT_DEADSPACE_VOLUME']), 2)
            content['SPARGE_VOLUME'] = round(float(raw_content['SPARGE_VOLUME'].split()[0]), 2)
            content['BOIL_VOLUME'] = round(float(raw_content['BOIL_VOLUME']), 2)
            content['PRE_BOIL_OG'] = round(float(raw_content['PRE_BOIL_OG'].split()[0]), 3)
            content['BOIL_TIME'] = datetime.timedelta(minutes=int(round(float(raw_content['BOIL_TIME']), 0)))
            content['TRUB_CHILLER_VOLUME'] = round(float(raw_content['TRUB_CHILLER_VOLUME']), 2)
            content['COOLING_SHRINKAGE_PERCENTAGE'] = round(float(raw_content['COOLING_SHRINKAGE_PERCENTAGE']), 2)
            content['EVAPORATION_PERCENTAGE'] = round(float(raw_content['EVAPORATION_PERCENTAGE']), 2)
            content['POST_BOIL_VOLUME'] = round(content['BOIL_VOLUME'] - (
                    content['EVAPORATION_PERCENTAGE'] / 100 * content['BOIL_VOLUME'] * int(
                round(float(raw_content['BOIL_TIME']), 0)) / 60.0), 2)
            content['KNOCKOUT_VOLUME'] = round(
                content['POST_BOIL_VOLUME'] * (1 - content['COOLING_SHRINKAGE_PERCENTAGE'] / 100), 2)
            content['BATCH_VOLUME'] = round(float(raw_content['BATCH_VOLUME']), 2)
            content['FERMENTATION_TEMP'] = round(float(raw_content['FERMENTATION_TEMP']), 1)
            content['OG'] = round(float(raw_content['OG'].split()[0]), 3)
            content['IBU'] = round(float(raw_content['IBU'].split()[0]), 1)
            content['BATCH_NUMBER'] = int(raw_content['NAME'].split()[0][1:])
            content['BATCH_NAME'] = raw_content['NAME'].strip(raw_content['NAME'].split()[0] + ' ')
            return content
        else:
            return super().process(raw_content)
