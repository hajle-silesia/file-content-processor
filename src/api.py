import base64
import json
import threading

import fastapi
import kafka

from src.category_filter import *
from src.file_content_processor import FileContentProcessor
from src.processor import Processor
from src.sorter import *
from src.strategy import *
from src.strategy_context import StrategyContext
from src.usage_filter import *


def load_events():
    consumer = kafka.KafkaConsumer(bootstrap_servers="kafka-cluster-kafka-bootstrap.event-streaming:9092",
                                   value_deserializer=lambda message: base64.b64decode(message).decode(),
                                   )
    consumer.subscribe(topics=["file-content-converter-topic"])
    for event in consumer:
        file_content_processor.update(event.value)


app = fastapi.FastAPI()

producer = kafka.KafkaProducer(bootstrap_servers="kafka-cluster-kafka-bootstrap.event-streaming:9092",
                               value_serializer=lambda message: base64.b64encode(
                                   json.dumps(message, default=str).encode()),
                               )
miscs_processor = Processor(recipe_filter=RecipesFilter(),
                            category_filter=MiscsFilter(),
                            usage_filter=MiscsUsageFilter(),
                            strategy_context=StrategyContext(NameStrategy(),
                                                             UseStrategy(),
                                                             AmountMiscsStrategy(),
                                                             TimeStrategy()))
fermentables_processor = Processor(recipe_filter=RecipesFilter(),
                                   category_filter=FermentablesFilter(),
                                   strategy_context=StrategyContext(NameStrategy(),
                                                                    AmountFermentablesStrategy()))
mash_steps_processor = Processor(recipe_filter=RecipesFilter(),
                                 category_filter=MashStepsFilter(),
                                 strategy_context=StrategyContext(NameStrategy(),
                                                                  MashStepTimeStrategy(),
                                                                  MashStepTempStrategy()),
                                 sorter=MashStepsSorter())
hops_processor = Processor(recipe_filter=RecipesFilter(),
                           category_filter=HopsFilter(),
                           usage_filter=HopsUsageFilter(),
                           strategy_context=StrategyContext(NameStrategy(),
                                                            UseStrategy(),
                                                            AmountHopsStrategy(),
                                                            TimeStrategy()))
parameters_processor = Processor(recipe_filter=RecipesFilter(),
                                 category_filter=ParametersFilter(),
                                 strategy_context=StrategyContext(ParametersStrategy()))

processors = {'miscs': miscs_processor,
              'fermentables': fermentables_processor,
              'mash_steps': mash_steps_processor,
              'hops': hops_processor,
              'parameters': parameters_processor,
              }

file_content_processor = FileContentProcessor(producer=producer, processors=processors)

events_thread = threading.Thread(target=load_events)
events_thread.start()


@app.get("/healthz")
async def healthz():
    return {'status': "ok"}


@app.get("/content")
async def content():
    return {"content": file_content_processor.content,
            }
