require("config")

function initUi()
  app.registerUi({["menu"] = "Edit config.lua ", ["callback"] = "editConfigLua", ["accelerator"] = edit_config_lua_shortcut});

  for i, settings in ipairs(settings_all) do
    local activate_shortcut = settings[1]
    local user_config = settings[2]
    local func_name = string.format("exportPng_%s", tostring(i))
    local func_code = string.format("exportPng('%s')", user_config)
    _G[func_name] = load(func_code)
    app.registerUi({["menu"] = "Export images using " .. user_config, ["callback"] = func_name, ["accelerator"] = activate_shortcut});

    local edit_config_shortcut = settings[3]
    local func_name = string.format("editConfigFile_%s", tostring(i))
    local func_code = string.format("editConfigFile('%s')", user_config)
    _G[func_name] = load(func_code)
    app.registerUi({["menu"] = "Edit " .. user_config, ["callback"] = func_name, ["accelerator"] = edit_config_shortcut});
  end
end

function editConfigLua()
  local plugin_path = script_path()
  local config_path = plugin_path .. "config.lua"
  os.execute("xdg-open " .. config_path)
  app.msgbox("After changing config.lua, you need to repoen the xournal++ note for it to take efftect.", {[1] = "Ok"})
end

function editConfigFile(config_file)
  local file_separator = package.config:sub(1,1)
  local plugin_path = script_path()
  local config_path = plugin_path .. "config" .. file_separator .. config_file

  if not file_exists(config_path) then
    os.execute("touch " .. config_path)
  end

  os.execute("xdg-open " .. config_path)
end

function exportPng(config)
  local xoppName = app.getDocumentStructure()["xoppFilename"]
  if (xoppName == "" or xoppName == nil) then 
    app.msgbox("You haven't saved the note. Save the file and try again.", {[1] = "Ok"})
    app.uiAction({["action"] = "ACTION_SAVE"})
    return
  end

  app.uiAction({["action"] = "ACTION_SAVE"})

  local plugin_path = script_path()

  -- Use file_separator to determine the OS
  file_separator = package.config:sub(1,1)

  local python_path = ""

  -- Linux
  if file_separator == "/" then
    if file_exists(plugin_path .. "main") then
      local executable_path = plugin_path .. "main"
      command = string.format("%s ", executable_path)
    else
      local python_path = plugin_path .. ".venv"  .. file_separator .. "bin" .. file_separator .. "python3"
      local script_path = plugin_path .. "src" .. file_separator .. "main.py"
      command = string.format("%s %s ", python_path, script_path)
    end

  -- Windows
  elseif file_separator == "\\" then 
    if file_exists(plugin_path .. "main.exe") then
      local executable_path = plugin_path .. "main.exe"
      command = string.format("%s ", executable_path)
    else
      local python_path = plugin_path .. ".venv"  .. file_separator .. "Scripts" .. file_separator .. "python.exe"
      local script_path = plugin_path .. "src" .. file_separator .. "main.py"
      command = string.format("%s %s ", python_path, script_path)
    end

  else
    app.msgbox("Unknown system", {[1] = "Ok"})
    return
  end


  -- When the project is bundled by pyinstaller, the user config file would not be included
  -- because the content of config file is not determined before the plugin is executed.
  -- When the executable is executed, it would be unzip to a temp folder and run.
  -- In that situation, it need to know the location of the user config file
  -- so we need to pass this information to the executable
  local config_path = plugin_path .. "config" .. file_separator .. config

  local filename = xoppName:match("(.+)%..+$") .. ".xopp"

  local docStructure = app.getDocumentStructure()
  local numPages = #docStructure["pages"]

  command = string.format("%s -x %s -c %s -n %s ", command, filename, config_path, numPages)

  if docStructure["pdfBackgroundFilename"] ~= "" then
    command = command .. " -p " .. docStructure["pdfBackgroundFilename"]
  end

  -- Linux
  if file_separator == "/" then   
    command = command .. " 2>&1 1>/dev/null"

  -- Windows
  else 
    command = command .. " 2>&1 >nul"
  end

  local handle = io.popen(command)
  local result = handle:read("*a")
  handle:close()

  if result ~= "" then
    app.msgbox(result, {[1] = "Ok"})
  end

end

function script_path()
  local str = debug.getinfo(2, "S").source:sub(2)
  return str:match("(.*[/\\])") or "./"
end

function file_exists(name)
  local f = io.open(name, "r")
  return f ~= nil and io.close(f)
end