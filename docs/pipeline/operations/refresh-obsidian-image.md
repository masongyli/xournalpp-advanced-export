---
icon: simple/obsidian
---

# :simple-obsidian: Reload Obsidian Image (experimental)

only works for Linux now

## Overview

If your export image is embedded in an Obsidian note, this operation would make Obsidian to reload the embedded images.

This is useful when you change the images embedded in a Obsidian note because by default Obisidian would not detect the change of the embedded images in the note automatically.

!!! note
    Obsidian URI is a custom URI protocol supported by Obsidian that lets you trigger various action. Please follow the [Obsidian URI](https://help.obsidian.md/Extending+Obsidian/Obsidian+URI) to to register the Obsidian URI protocol on your computer. 

!!! note
    This operation relies on the [Obsidian Advanced URI plugin](https://vinzent03.github.io/obsidian-advanced-uri/installing). Make sure the plugin has been installed in Obsidian before using this operation.

!!! warning
    Currently, this operation works by changing the target text in the obsidian note into some gibberish, and change it back to force obsidian to reload the images. Although the possibility is nearly zero, be aware that this gibberish still has chance to collide with some meaningful text in your obsidian note. (if your note do have some text look like the gibberish, you may need to change the gibberish in the source code to avoid collision.)

## Configuration

| Key      | Type   |          | Default value  | Description                                                                                                                                           |
| -------- | ------ | -------- | -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| filename | string | optional | "{{xoppStem}}" | The filename of the output images. (excluding the file extension)<br>You can use `{{xoppStem}}` to represent the stem name of the Xournal++ note.<br> |

In general, you would assign "filename" with the value same as that in "save" operation's "filename".

## Demo

