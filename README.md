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


## Public configuration

If it is necessary to share configuration with non-privledged sources
(example: publishing API urls), a publicly consumable configuration is required.

Yoconfigurator will produce `configuration_public.json` if an app has the deploy
config `public-data.py`. The public data config contains a list of keys that is
a subset of the private config, instructing yoconfigurator which values are to
be written to `configuration_public.json`. Note that if a key's value is a large
configuration dictionary, the entire dict will be included in the resulting json.

For an example of use, review the
[sample app](https://github.com/yola/yoconfigurator/tree/master/yoconfigurator/tests/samples)
found in the tests.


## Configuring with local overrides

Local overrides are done in a persistant way that does not put a project repo in a dirty state.

1. Create a configuration source for local overrides, example `projectfoo/deploy/configuration/local/`.

1. Tell version control to ignore the contents of this directory.

1. Create a new local override configuration file, example `projectfoo/deploy/configuration/local/projectfoo-local.py`.

As long as `projectfoo-local.py` is in place, all newly generated `configuration.json` files will have the local overrides.

To restore default behavior, delete the local override configuration files and regenerate `configuration.json`.
