---
icon: octicons/beaker-16
---

# :octicons-beaker-16: Testing

## Basic test
```
pipenv run python -m unittest discover -s test
```

## Test with coverage
```
pipenv run coverage run --omit=test_*.py -m unittest discover -s test
```

It would generate `.coverage` file (a binary file)

### Show coverage report
It would read from `.coverage`
```
pipenv run coverage report -m
```

### Generate `coverage.xml`
It would read from `.coverage`
```
pipenv run coverage xml
```

(`coverage.xml` can be used by some IDE's extension, eg: vscode extension "coverage gutter")
