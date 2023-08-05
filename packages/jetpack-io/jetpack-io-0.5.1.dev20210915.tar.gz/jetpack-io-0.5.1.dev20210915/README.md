
## Build SDK

Run `./devtools/scripts/sdk/python/build.sh`.

This will produce SDK distributions in `sdk/python/dist`.

## Run tests

```
# Pre-requisite: build the SDK using the command above.

cd sdk/python/tests
poetry run pytest
```
