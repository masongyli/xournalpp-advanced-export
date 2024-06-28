# Get started

## Installation
=== ":simple-linux: Linux"

    1. Download zip file from [the release page](https://github.com/masongyli/xournalpp-advanced-export/releases/latest)
    2. Unzip it as a directory into `~/.config/xournalpp/plugins`.  
    After that, `main.lua` should be in located at `~/.config/xournalpp/plugins/AdvancedExport/main.lua`
    3. Then you are good to go.

=== ":simple-windows: Windows"
    1. Download zip file from [the release page](https://github.com/masongyli/xournalpp-advanced-export/releases/latest)
    2. Unzip it as a directory into `C:\Users\<user>\AppData\Local\xournalpp\plugins` (replace `<user>` with your username).  
    After that, `main.lua` should be located at  `C:\Users\<user>\AppData\Local\xournalpp\plugins\AdvancedExport\main.lua`
    3. Install poppler and configure it in the system path. (Because the python package pdf2Image depends on it)

    >  1. Download the latest poppler package from [@oschwartz10612 version](https://github.com>oschwartz10612/poppler-windows/releases/) which is the most up-to-date.
    >  2.  Move the extracted directory to the desired place on your system
    >  3. Add the `bin/` directory to your PATH
    >  4. Test that all went well by opening cmd and making sure that you can call `pdftoppm -h`
    >> This block is extracted from [pdf2image's documentation](https://pdf2image.readthedocs.io/en/latest/installation.html)

    4. Add the path to xournal++ (`C:\Program Files\Xournal++\bin`) to the system environment Path.
    5. Then you are good to go.

=== ":simple-apple: macOS"
    Currently, Xournapp Advanced Export doesn't have a bundle for macOS.  
    So macOS users need to setup the plugin manually from source.
    See [Development](development/setup.md) for more information.

    !!! warning
        The plugin is only tested under Linux (.deb installer) and Windows (.exe installer), so I am not sure it works on macOS.

## Usage
After installation, you can start using the plugin.

Open a xopp file with Xournal++.

Press the key ++g++ to start executing the plugin.

After executation, you should see the image being generated in the same directory as the xopp file.

## Config pipeline
To change the pipeline of the plugin, go to [pipeline](pipeline/index.md) for more information.

## Other Configurations
To change shortcuts and manage multiple config files, go to [Other Configuration](other-configurations/index.md) for more information.

## Development
To develop the plugin, go to [Development](development/setup.md) for more information.