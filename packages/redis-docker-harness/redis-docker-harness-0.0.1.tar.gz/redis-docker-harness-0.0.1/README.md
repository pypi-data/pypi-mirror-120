# redis-docker-harness
Classes and methods for integrating code inside a docker image into a processing pipeline, using redis for exchanging data.

## Examples

* [basic](examples/basic.py)
* [custom options and logging](examples/custom_options_and_logging.py)

**Note:** For broadcasting data and listening to the generated output, you can use the 
[simple-redis-helper](https://github.com/fracpete/simple-redis-helper) library 
(executables `srh-broadcast` and `srh-listen`).
