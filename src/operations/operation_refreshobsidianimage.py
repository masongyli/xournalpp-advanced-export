import subprocess
import sys
from pathlib import Path
from typing import override

import jsonschema

from core import Context, Operation
from operations.registry import register_operation


@register_operation("refreshObsidianImage")
class RefreshObsidianImageOperation(Operation):
    def __init__(self, config: dict):
        super().__init__(config)

        self.filename: str = config.get("filename", "{{xoppStem}}")

    @override
    def validate(self, config: dict) -> None:
        CONFIG_SCHEMA = {
            "$schema": "http://json-schema.org/draft-04/schema#",
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "filename": { "type": "string" }
            }
        }

        jsonschema.validate(config, CONFIG_SCHEMA)

    @override
    def operate(self, context: Context) -> Context:
        """
        Refresh embedded images in the Obsidian note. (apply on the last used note in the last used vault)
        
        Caution: This operation relies on the "Advanced URI" plugin in Obsidian. Make sure to the plugin has been installed in Obsidian before using this operation.

        Args:
            context (Context): The context object containing the necessary information for the operation.
            
        Returns:
            Context: The updated context object.
        """
        if len(context.output_images) == 0:
            return context

        target_filename =  str(self._parse_filename(context.xopp_file_path)) + ".png"
        
        gibberish = '_tmp'

        if sys.platform.startswith("win"):
            command = ["cmd", "/c", "start", ""]
            ampersand = "^&"
        else:
            command = ["xdg-open"]
            ampersand = "&"

        subprocess.run(
            command + [f"obsidian://advanced-uri?search={target_filename}{ampersand}replace={target_filename}{gibberish}"],
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        
        subprocess.run(
            command + [f"obsidian://advanced-uri?search={target_filename}{gibberish}{ampersand}replace={target_filename}"],
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        
        return context
    
    def _parse_filename(self, xopp_file_path: Path) -> Path:
        xopp_filename_stem = xopp_file_path.stem

        return Path(self.filename.replace("{{xoppStem}}", xopp_filename_stem))
