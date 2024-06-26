from pathlib import Path
from typing import override

import jsonschema
from pathvalidate import validate_filename

from core import Context, Operation

from operations.registry import register_operation

@register_operation("save")
class SaveOperation(Operation):
    def __init__(self, config: dict):
        super().__init__(config)

        self.directory: str = config.get("directory", "{{xoppDir}}")
        self.filename: str = config.get("filename", "{{xoppStem}}")
    
    @override
    def validate(self, config: dict) -> None:
        CONFIG_SCHEMA = {
            "$schema": "http://json-schema.org/draft-04/schema#",
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "directory": {
                    "type": "string"
                },
                "filename": {
                    "type": "string"
                }
            }
        }

        jsonschema.validate(config, CONFIG_SCHEMA)

        # check if "directory" contains invalid characters
        if d := config.get("directory"):
            self._validate_directory(d)
        
        # check if "filename" contains invalid characters
        if f := config.get("filename"):
            f = f.replace("{{xoppStem}}", "xoppStem")
            validate_filename(f)
    
    def _validate_directory(self, path: str) -> None:
        if "{{xoppDir}}" in path:
            # we cannot validate this path until the operation starts
            return
        
        expanded_path = Path(path).expanduser()
        
        if not expanded_path.is_absolute():
            raise ValueError(f"Can't use relative path: '{path}'")
    
        if not expanded_path.exists():
            raise FileNotFoundError(f"Directory '{path}' does not exist.")
                        
        
    @override
    def operate(self, context: Context) -> Context:
        if len(context.output_images) == 0:
            return context

        directory_path: Path = self._parse_directory_path(context.xopp_file_path)
        filename = self._parse_filename(context.xopp_file_path)
        
        if len(context.output_images) == 1:
            context.output_images[0].save(directory_path / filename)
            return context

        for i in range(len(context.output_images)):
            file_path = f"{str(filename.stem)}-{i+1}.png"
            context.output_images[i].save(directory_path / file_path)
        return context
    
    def _parse_directory_path(self, xopp_file_path: Path) -> Path:
        xopp_dir_path = xopp_file_path.parent

        return Path(self.directory.replace("{{xoppDir}}", str(xopp_dir_path))).expanduser()
    
    def _parse_filename(self, xopp_file_path: Path) -> Path:
        xopp_filename_stem = xopp_file_path.stem

        return Path(self.filename.replace("{{xoppStem}}", xopp_filename_stem) + ".png")
