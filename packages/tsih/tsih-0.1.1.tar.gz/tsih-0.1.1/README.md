# TSIH - A dict with a HISTory

`tsih.Dict` is a type of `UserDict` that allows versioning, backed up by a `sqlite3` database.

* Transparent operation
* Only changes (deltas) are stored.
* Forward-filling of values. A value is reused in future versions, unless it changes.

## Use cases

Tsih was originally part of the [Soil](https://github.com/gsi-upm/soil) Agent-Based Social Simulation framework, where both the environment and the agents need to keep track of state (i.e., attribute) changes.
