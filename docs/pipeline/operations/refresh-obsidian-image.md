---
icon: simple/obsidian
---

# :simple-obsidian: Refresh Obsidian Image (experimental)

## Overview
By default, when you change the images embedded in a [Obsidian](https://obsidian.md/) note, Obsidian would not detect the change of the embedded images in the note automatically. This operation is designed to force Obsidian to reload the embedded images in a note.

!!! note
    Obsidian URI is a custom URI protocol supported by Obsidian that lets you trigger various action. Please follow the [Obsidian URI](https://help.obsidian.md/Extending+Obsidian/Obsidian+URI) to to register the Obsidian URI protocol on your computer. 
    For Linux user, there is a [good article](https://amir.rachum.com/obsidian-uri-linux/) about how to set it.

!!! note
    This operation relies on the [Obsidian Advanced URI plugin](https://vinzent03.github.io/obsidian-advanced-uri/installing). Make sure to **install** and **enable** it in Obsidian before using this operation.

## Configuration

| Key      | Type   |          | Default value  | Description                                                                                                                                           |
| -------- | ------ | -------- | -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| filename | string | optional | `"{{xoppStem}}"` | The filename of the output images. (excluding the file extension)<br> :octicons-dot-fill-16: You can use `{{xoppStem}}` to represent the stem name of the Xournal++ note. |

In general, you would assign "filename" with the value same as that in "save" operation's "filename".

## Example

```json title="config.json" hl_lines="26-31"
{
    "pipeline": [
        {
            "type": "load",
            "config": {
                "paper_background_preserved": true,
                "trim": true,
                "trim_directions": [false, true, false, true],
                "trim_paddings": [0, 50, 0, 50]
            }
        },
        {
            "type": "combine",
            "config": {
                "direction": "ttb",
                "horizontal_align": "center"
            }
        },
        {
            "type": "save",
            "config": {
                "directory": "{{xoppDir}}",
                "filename": "{{xoppStem}}"
            }
        },
        {
            "type": "refreshObsidianImage",
            "config": {
                "filename": "{{xoppStem}}"
            }
        }
    ]
}
```

## Demo
<iframe width="560" height="315" src="https://www.youtube.com/embed/HBGRsj9YhuA?si=B_D-5t0zsf3gW1f4" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>