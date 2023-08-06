
## Build SDK

Run `./devtools/scripts/sdk/python/build.sh`.

This will produce SDK distributions in `sdk/python/dist`.

## Run tests

```
# Pre-requisite: build the SDK using the command above.

cd sdk/python/tests
poetry run pytest
```

## Update Version

Step 1: Prepare PR and land it

- grep for the existing version (see sdk/python/pyproject.toml) and update all files in axiom that use it
  - this will cover some sdk version tests, requirements.txt in examples/ projects
- build the SDK (see the Build SDK section above)

Step 2:
- run `./devtools/scripts/sdk/python/publish.sh`
