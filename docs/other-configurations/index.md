# Other configurations

## Manage multiple config files

For some cases, you may want to have multiple config files for different purposes. 

You can do this by editting `config.lua` file.

In Xournal++, from the top menu, click `Plugins` > `Edit config.lua`.

For example, edit `config.lua` to:

```lua title="config.lua"
settings_all = {
  -- {shortcut to start exporting, config file name, shortcut to edit this config file}
  {"g", "config.json", "i"},
  {"", "config-2.json", ""},
}

edit_config_lua_shortcut = ""
```



Then you would have two config files, `config.json` and `config-2.json`.

After editting `config.lua`, you need to restart xournal++ to make the changes take effect.

Then, In xournal++, from the top menu, click `Plugins` -> `Advanced Export` -> `Edit config-2.json` to edit `config-2.json`

## Shortcuts

The shortcut for executing plugin and editing config file can also be set in `config.lua`.


```lua title="config.lua"
settings_all = {
  -- {shortcut to start exporting, config file name, shortcut to edit this config file}
  {"g", "config.json", "i"},
  {"h", "config-2.json", ""},
}

edit_config_lua_shortcut = ""
```

In this example,  
the shortcut for exporting using `config.json` is ++g++, and the shortcut for editing the `config.json` is ++i++.
the shortcut for exporting using `config-2.json` is ++h++, and the shortcut for editing the `config-2.json` is "empty", meaning you doesn't set a shortcut for editing `config-2.json`.

Use `<Ctrl>` to represent the ++ctrl++ key, `<Alt>` to represent the ++alt++ key, `<Shift>` to represent the ++shift++ key, and `<Super>` to represent the ++super++ key.  
Eg: `<Alt><Shift>j` represents ++alt+shift+j++


!!! note
    If your shortcut conflict with default Xournal++ shortcuts, default shortcuts would have higher priority. For exapmle, ++ctrl+s++ is the default shortcut for saving the file, so you could not set ++ctrl+s++ as a shortcut for this plugin. 
