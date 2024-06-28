---
icon: material/power-standby
---


# :material-power-standby: Setup 

## 1. Fork the repository and clone it to your local machine.

## 2. Install "pyenv" to manage multiple python versions on your machine

This step may not seem necessary, but it is recommended to use "pyenv" to manage multiple python versions. Especially Xournal Advanced Export use Python 3.12, which is quite new.

=== ":simple-linux: :simple-apple: Linux & macOS"
    Install `pyenv`  
    Follow the [instruction](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation) to install `pyenv` on your machine.

=== ":simple-windows: Windows"
    Install `pyenv-win`  
    Follow the [instruction](https://github.com/pyenv-win/pyenv-win?tab=readme-ov-file#installation)  to install `pyenv-win` on your machine.

## 3. Install `pipenv`
```
pip install --user pipenv
```

## 4. Install packages in virtual environment

=== ":simple-linux: :simple-apple: Linux & macOS"

    ```
    cd ~/.config/xournalpp/plugins/AdvanedExport
    mkdir .venv
    pipenv install --dev
    ```

=== ":simple-windows: Windows"

    ```
    cd %homedrive%%homepath%\AppData\Local\xournalpp\plugins\AdvancedExport
    mkdir .venv
    pipenv install --dev
    ```

    !!! note
        Also make sure you have installed poppler and added it to your PATH.  
        And add the path to Xournal++ (C:\Program Files\Xournal++\bin) to your Path.

!!! note
    When running `pipenv install` to install dependency in virtual environment, because pipenv detects the existence of `.venv` directory in current directory, it would install all dependencies in the `.venv` directory we have created. This make sure those dependencies won't scatter around your file system.

!!! note
    `pyenv` is a good friend of `pipenv`. When running `pipenv install`, if the python version specified in the `Pipfile` has not been installed, `pyenv` will install it for you.


