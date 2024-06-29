# Pipeline

Xournalpp Advanced Export use the `config.json` file to configure the pipeline.

![alt text](../images/pipeline.drawio.svg)


This is an example of `config.json`

```json title="config.json"
{
    "pipeline": [
        {
            "type": "load",
            "config": {
                "paper_background_preserved": true,
                "transparent_pdf_background": false,
                "crop_empty_margins": true,
                "direction_enabled": [false, true, false, true],
                "paddings": [0, 50, 0, 50]
            }
        },
        {
            "type": "combine",
            "config": {
                "direction": "ttb",
                "horizontal_align": "center",
                "vertical_align": "center"
            }
        },
        {
            "type": "save",
            "config": {
                "directory": "{{xoppDir}}",
                "filename": "{{xoppStem}}"
            }
        }
    ]
}
```

!!! note
    To edit `config.json`, you can press the key ++i++ in Xournal++ to open the config file by your default text editor.  
    Or at the top menu of Xournal++ click `Plugin` > `Edit config.json`

"operations" is an array of objects, each object represents an operation. 
The order of the operations is important, as the output of the previous operation will be the input of the next operation.

- "type" is the type of the operation, it can be "load", "combine", "save", "refreshObsidianImage" for now. 
- "config" is the configuration of the operation, the content of the configuration depends on the type of the operation. If you doesn't specify the "config" field, the default configuration will be used. See the documentation of each operation for more details.

!!! note
    You can have multiple operations of same "type" in the "operations" array to achieve the effect you want. For example, you can have multiple "save" operations to save the images to different directories or with different filenames.

The minimum useful configuration would be:
```json title="config.json"
{
    "pipeline": [
        {
            "type": "load"
        },
        {
            "type": "save"
        }
    ]
}
```

It would load the xopp file as images, and save the images as png files in the same directory as the xopp file.
