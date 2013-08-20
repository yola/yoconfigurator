Change Log
==========

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
