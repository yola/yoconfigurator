Change Log
==========

0.5.2
-----

* Fix `seeded_auth_token` to accept arguments of `str` type

0.5.1
-----

* Fix `DotDict.setdefault()` to return value (previously it always
  returned None)

0.5.0
-----

* Update to work with Python 2.7, 3.2, 3.3, 3.4, 3.5
* Drop support for Python <= 2.6

0.4.6
-----

* Add new lib for configuration filtering
* Add support and docs for generating public configuration.
* Add DotDict support for getting & setting values using dotted keys

0.4.5
-----

* Generated configuration.json no longer has trailing whitespace.

0.4.4
-----

* Fix a bug in the DotDict __getattr__ method so it fails with an
  AttributeError if the attr is not found. This arose because, during a
  deepcopy, the getattr was mapped to dict.getitem and dict does not have
  a __deepcopy__ attribute

0.4.3
-----

* Allow replacing `None` with other types.

0.4.2
-----

* Add --build option to produce build-time configurations for tests.

0.4.1
-----

* Fixes bug where generating configuration without --local resulted in missing
  configuration values

0.4.0
-----

* Inject the app name as `yoconfigurator.app`.
* Overridden configuration gets sourced too.

0.3.0
-----

* Renamed to yoconfigurator.
* `MissingValues` can be replaced with dicts.
* `MissingValues` get a name provided automatically.
* Add `DeletedValue`.
* Use a `hostname-local` source when run with `--local`.

0.2.1-0.2.2
-----------

* Change the default search paths for `configurator.py`

0.2.0
-----

* Add an initial `hostname` source.

0.1
---

* Initial release.
