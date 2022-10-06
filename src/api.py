import base64
import json
import os
from pathlib import Path

import requests
from fastapi import FastAPI, Request

from src.category_filter import *
from src.file_content_processor import FileContentProcessor
from src.notifier import Notifier
from src.processor import Processor
from src.sorter import *
from src.storage import Storage
from src.strategy import *
from src.strategy_context import StrategyContext
from src.usage_filter import *

config_path = Path(__file__).parent / "../file_content_processor/config.json"

app = FastAPI()

storage = Storage()
storage.path = config_path
notifier = Notifier(storage)

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

file_content_processor = FileContentProcessor(notifier=notifier, processors=processors)

notifier_host = os.getenv('FILE_CONTENT_CONVERTER_SERVICE_HOST')
notifier_port = os.getenv('FILE_CONTENT_CONVERTER_SERVICE_PORT')
notifier_url = f"http://{notifier_host}:{notifier_port}/observers/register"

host = os.getenv('FILE_CONTENT_PROCESSOR_SERVICE_HOST')
port = os.getenv('FILE_CONTENT_PROCESSOR_SERVICE_PORT')
url = f"http://{host}:{port}/update"

requests.post(notifier_url, base64.b64encode(json.dumps({'file-content-processor': url}).encode()))


@app.get("/healthz")
async def healthz():
    return {'status': "ok"}


@app.get("/api")
async def api():
    return {"/content",
            "/update",
            }


@app.get("/content")
async def content():
    return {"content": file_content_processor.content,
            }


@app.get("/observers")
async def observers():
    return notifier.observers


@app.post("/observers/register")
async def observers_register(request: Request):
    request_body_json = base64.b64decode(await request.body()).decode()
    request_body = json.loads(request_body_json)
    notifier.register_observer(request_body)


@app.post("/observers/remove")
async def observers_remove(request: Request):
    request_body_json = base64.b64decode(await request.body()).decode()
    request_body = json.loads(request_body_json)
    notifier.remove_observer(request_body)


@app.post("/update")
async def update(request: Request):
    request_body_json = base64.b64decode(await request.body()).decode()
    request_body = json.loads(request_body_json)
    file_content_processor.update(request_body)
