from typing import override

import jsonschema
from PIL import Image

from core import Context, Operation

from operations.registry import register_operation

@register_operation("combine")
class CombineOperation(Operation):
    def __init__(self, config: dict):
        super().__init__(config)

        self.direction: str = config.get("direction", "ttb")
        self.horizontal_align: str = config.get("horizontal_align", "center")
        self.vertical_align: str = config.get("vertical_align", "center")

    @override
    def validate(self, config: dict) -> None:
        CONFIG_SCHEMA = {
            "$schema": "http://json-schema.org/draft-04/schema#",
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "direction": {
                    "type": "string",
                    "enum": ["ttb", "btt", "ltr", "rtl"],
                },
                "horizontal_align": {
                    "type": "string",
                    "enum": ["left", "center", "right"]
                },
                "vertical_align": {
                    "type": "string",
                    "enum": ["top", "center", "bottom"]
                }
            }
        }

        jsonschema.validate(config, CONFIG_SCHEMA)

    @override
    def operate(self, context: Context) -> Context:
        if len(context.output_images) == 0:
            return context
        
        if len(context.output_images) == 1:
            return context

        match self.direction:
            case "ttb": combined_im = self._ttb_combine(context.output_images)
            case "ltr": combined_im = self._ltr_combine(context.output_images)
            case "btt": combined_im = self._btt_combine(context.output_images)
            case "rtl": combined_im = self._rtl_combine(context.output_images)
            case _: raise AssertionError("Invalid direction")  # pragma: no cover
        
        context.output_images = [combined_im]
        
        return context
    
    def _ttb_combine(self, images: list[Image.Image]) -> Image.Image:
        """ Combines a list of images vertically from top to bottom.

        Args:
            images (list[Image.Image]): A list of PIL Image objects to be combined.

        Returns:
            Image.Image: The combined image.

        Raises:
            ValueError: If the vertical alignment is invalid.
        """
        width = max([im.width for im in images])

        total_height = 0
        for im in images:
            total_height += im.height
        
        combined_im = Image.new('RGBA', (width, total_height), (0, 0, 0, 0))

        match self.horizontal_align:
            case "left":
                offsets  = [0] * len(images)
            case "center":
                offsets = [(width - im.width) // 2 for im in images]
            case "right":
                offsets = [(width - im.width) for im in images]
            case _:  # pragma: no cover
                raise AssertionError("Invalid horizontal alignment")  

        current_height = 0
        for img, offset in zip(images, offsets):
            combined_im.paste(img, (offset, current_height))
            current_height += img.height
        
        return combined_im
    
    def _ltr_combine(self, images: list[Image.Image]) -> Image.Image:
        """ Combines a list of images horizontally from left to right.

        Args:
            images (list[Image.Image]): A list of PIL Image objects to be combined.

        Returns:
            Image.Image: The combined image.

        Raises:
            ValueError: If the vertical alignment is invalid.
        """
        match self.vertical_align:
            case "top":
                self.horizontal_align = "right"
            case "center":
                self.horizontal_align = "center"
            case "bottom":
                self.horizontal_align = "left"
            case _:  # pragma: no cover
                raise AssertionError("Invalid vertical alignment")

        images = [im.transpose(Image.Transpose.ROTATE_270) for im in images]
        combined_im = self._ttb_combine(images)
        combined_im = combined_im.transpose(Image.Transpose.ROTATE_90)

        return combined_im

    def _btt_combine(self, images: list[Image.Image]) -> Image.Image:
        """ Combines a list of images vertically from bottom to top.

        Args:
            images (list[Image.Image]): A list of PIL Image objects to be combined.

        Returns:
            Image.Image: The combined image.

        Raises:
            ValueError: If the vertical alignment is invalid.
        """
        images.reverse()
        return self._ttb_combine(images)
    
    def _rtl_combine(self, images: list[Image.Image]) -> Image.Image:
        """ Combines a list of images horizontally from right to left.

        Args:
            images (list[Image.Image]): A list of PIL Image objects to be combined.

        Returns:
            Image.Image: The combined image.

        Raises:
            ValueError: If the vertical alignment is invalid.
        """
        images.reverse()
        return self._ltr_combine(images)
