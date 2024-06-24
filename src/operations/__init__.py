import pkgutil
import importlib

# Iterate through all modules in the current package
for loader, module_name, is_pkg in pkgutil.walk_packages(__path__, __name__ + '.'):
    importlib.import_module(module_name)


# We cannot use the following code because when we use pyinstaller to generate the executable, it won't preserve the directory structure of the source code.

# import os
# import importlib
# from pathlib import Path
# operations_path = Path(__file__).parent

# for file in operations_path.iterdir():
#     if file.stem.startswith('operation_') and file.suffix == '.py':
#         module_name = f"operations.{file.stem}"
#         importlib.import_module(module_name)