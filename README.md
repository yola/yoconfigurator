# yoconfigurator

[![Build Status](https://api.travis-ci.org/yola/yoconfigurator.svg)](https://travis-ci.org/yola/yoconfigurator)


Combine configuration from multiple sources into a single JSON file.
This allows cluster and environment configuration to override defaults
from the application.


## Running Tests:

1. Activate virtual environment:

  ```
  source virtualenv/bin/activate
  ```

2. Run tests:

  ```
  python -m unittest discover
  ```


## Configuring with local overrides

Local overrides are done in a persistant way that does not put a project repo in a dirty state.

1. Create a configuration source for local overrides, example `projectfoo/deploy/configuration/local/`.

1. Tell version control to ignore the contents of this directory.

1. Create a new local override configuration file, example `projectfoo/deploy/configuration/local/projectfoo-local.py`.

As long as `projectfoo-local.py` is in place, all newly generated `configuration.json` files will have the local overrides.

To restore default behavior, delete the local override configuration files and regenerate `configuration.json`.
