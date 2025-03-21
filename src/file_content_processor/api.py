import base64
import json
import threading

import category_filter
import fastapi
import kafka
import processor
import sorter
import strategy
import strategy_context
import usage_filter

import file_content_processor


def load_events():
    consumer = kafka.KafkaConsumer(
        bootstrap_servers="kafka-cluster-kafka-bootstrap.event-streaming:9092",
        value_deserializer=lambda message: json.loads(base64.b64decode(message).decode()),
    )
    consumer.subscribe(topics=["file-content-converter-topic"])
    for event in consumer:
        file_content_processor.update(event.value)


app = fastapi.FastAPI()

producer = kafka.KafkaProducer(
    bootstrap_servers="kafka-cluster-kafka-bootstrap.event-streaming:9092",
    value_serializer=lambda message: base64.b64encode(json.dumps(message, default=str).encode()),
)
miscs_processor = processor.Processor(
    recipe_filter=category_filter.RecipesFilter(),
    category_filter=category_filter.MiscsFilter(),
    usage_filter=usage_filter.MiscsUsageFilter(),
    strategy_context=strategy_context.StrategyContext(
        strategy.NameStrategy(),
        strategy.UseStrategy(),
        strategy.AmountMiscsStrategy(),
        strategy.TimeStrategy(),
    ),
)
fermentables_processor = processor.Processor(
    recipe_filter=category_filter.RecipesFilter(),
    category_filter=category_filter.FermentablesFilter(),
    strategy_context=strategy_context.StrategyContext(strategy.NameStrategy(), strategy.AmountFermentablesStrategy()),
)
mash_steps_processor = processor.Processor(
    recipe_filter=category_filter.RecipesFilter(),
    category_filter=category_filter.MashStepsFilter(),
    strategy_context=strategy_context.StrategyContext(
        strategy.NameStrategy(),
        strategy.MashStepTimeStrategy(),
        strategy.MashStepTempStrategy(),
    ),
    sorter=sorter.MashStepsSorter(),
)
hops_processor = processor.Processor(
    recipe_filter=category_filter.RecipesFilter(),
    category_filter=category_filter.HopsFilter(),
    usage_filter=usage_filter.HopsUsageFilter(),
    strategy_context=strategy_context.StrategyContext(
        strategy.NameStrategy(),
        strategy.UseStrategy(),
        strategy.AmountHopsStrategy(),
        strategy.TimeStrategy(),
    ),
)
parameters_processor = processor.Processor(
    recipe_filter=category_filter.RecipesFilter(),
    category_filter=category_filter.ParametersFilter(),
    strategy_context=strategy_context.StrategyContext(strategy.ParametersStrategy()),
)

processors = {
    "miscs": miscs_processor,
    "fermentables": fermentables_processor,
    "mash_steps": mash_steps_processor,
    "hops": hops_processor,
    "parameters": parameters_processor,
}

file_content_processor = file_content_processor.FileContentProcessor(producer=producer, processors=processors)

events_thread = threading.Thread(target=load_events)
events_thread.start()


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


@app.get("/content")
async def content():
    return {
        "content": file_content_processor.content,
    }
