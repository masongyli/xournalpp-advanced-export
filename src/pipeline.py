from abc import ABC, abstractmethod
import json
import warnings
from typing import override

import jsonschema
from tqdm import TqdmExperimentalWarning
from tqdm.tk import tqdm_tk

from core import Context, Operation
from operations.registry import operation_registry


class Pipeline(ABC):
    @abstractmethod
    def __init__(self, config_filepath: str):
        ...  # pragma: no cover
    
    @abstractmethod
    def validate(self, config: dict) -> None:
        ...  # pragma: no cover
    
    @abstractmethod
    def run(self, context: Context) -> Context:
        ...  # pragma: no cover

class LinearPipeline(Pipeline):
    @override
    def __init__(self, config_filepath: str):
        with open(config_filepath, encoding='utf-8') as f:
            config = json.load(f)

        self.validate(config)

        self.operations = []
        for operation in config['pipeline']:
            if operation['type'] not in operation_registry:
                raise ValueError(f"Invalid operation type: {operation['type']}")
            
            op_class: type[Operation] = operation_registry[operation['type']]
            op = op_class(operation.get('config', dict()))
            
            self.operations.append(op)

    @override
    def validate(self, config: dict) -> None:
        CONFIG_SCHEMA = {
            "$schema": "http://json-schema.org/draft-04/schema#",
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "pipeline": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "type": {
                                "type": "string",
                            },
                            "config": {
                                "type": "object",
                            }
                        }
                    }
                }
            }
        }

        jsonschema.validate(config, CONFIG_SCHEMA)
    
    @override
    def run(self, context: Context) -> Context:
        warnings.filterwarnings("ignore", category=TqdmExperimentalWarning)

        t = tqdm_tk(total=len(self.operations)+1)
        t.update(1)

        for operation in self.operations:
            context = operation.operate(context)
            t.update(1)
        
        t.close()
        
        return context
