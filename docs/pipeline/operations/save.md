---
icon: material/content-save
---

# :material-content-save: Save

## Overview

The Save Operation would save the images in the pipeline to the disk.

## Configuration

Use "save" as the type of the operation.

Keys in "config":

| Key       | Type   | Default value    | Description                                                                                                                                           |
| --------- | ------ | ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| directory | string | `"{{xoppDir}}"`  | The directory to save the output images.<br>You can use `{{xoppDir}}` to represent the directory where the Xournal++ note is.<br>                     |
| filename  | string | `"{{xoppStem}}"` | The filename of the output images. (excluding the file extension)<br>You can use `{{xoppStem}}` to represent the stem name of the Xournal++ note.<br> |


## Examples
Take [this xopp file](xopps/three_pages.xopp) as an example.

Assume the xopp file's path is `/a/path/to/xopp/file/three_pages.xopp`

### One export image

```json title="config.json" hl_lines="14"
{
    "pipeline": [
        {
            "type": "load",
            "config": {
                "paper_background_preserved": true,
                "trim": true
            }
        },
        {
            "type": "combine"
        },
        {
            "type": "save"
        }
    ]
}
```

- The directory for save would be `/a/path/to/xopp/file/`
- The filename would be `three_pages.png`

### Multiple export images

```json title="config.json" hl_lines="11"
{
    "pipeline": [
        {
            "type": "load",
            "config": {
                "paper_background_preserved": true,
                "trim": true
            }
        },
        {
            "type": "save"
        }
    ]
}
```

- The directory for save would be `/a/path/to/xopp/file/`
- Because there are multiple images to save, the filenames would be `three_pages-1.png`, `three_pages-2.png`, `three_pages-3.png`

### Customize export filename

```json title="config.json" hl_lines="13 14"
{
    "pipeline": [
        {
            "type": "load",
            "config": {
                "paper_background_preserved": true,
                "trim": true
            }
        },
        {
            "type": "save",
            "config": {
                "directory": "{{xoppDir}}",
                "filename": "{{xoppStem}}_exported"
            }
        }
    ]
}
```

- The directory for save would be `/a/path/to/xopp/file/`
- The filenames would be `three_pages_exported-1.png`, `three_pages_exported-2.png`, `three_pages_exported-3.png`



### Customize export directory and filename

```json title="config.json" hl_lines="13 14"
{
    "pipeline": [
        {
            "type": "load",
            "config": {
                "paper_background_preserved": true,
                "trim": true
            }
        },
        {
            "type": "save",
            "config": {
                "directory": "~/Pictures",
                "filename": "exported"
            }
        }
    ]
}
```

- The directory for save would be `~/Pictures`
- The filenames would be `exported.png`

!!! note
    The character `~` would be expanded to the home directory of the user.
    
    For example,  
    In Linux, `~` would possibly be expanded to `/home/<username>`.  
    In Windows, `~` would possibly be expanded to `C:\Users\<username>`.


### Customize export directory and filename 2

```json title="config.json" hl_lines="13 14"
{
    "pipeline": [
        {
            "type": "load",
            "config": {
                "paper_background_preserved": true,
                "trim": true
            }
        },
        {
            "type": "save",
            "config": {
                "directory": "{{xoppDir}}/../abc",
                "filename": "another_{{xoppStem}}"
            }
        }
    ]
}
```

- The directory for save would be `/a/path/to/xopp/abc`
- The filenames would be `another_three_pages.png`
