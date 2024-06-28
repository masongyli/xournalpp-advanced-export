---
icon: octicons/package-16
---

# :octicons-package-16: Packaging

Cd to project's root directory and run:
```
pipenv run pyinstaller main.spec --clean --distpath .
```

It would bundle all python source code in `src` directory into 1 executable.

It would be `main` for Linux, and `main.exe` for Windows.
