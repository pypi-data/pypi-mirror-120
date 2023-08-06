Monkey IOC
==========

Monkey IoC is a simple framework for inversion of control by dependency injection.

It works with a registry of named elements whose definitions have been loaded from a JSON file.

Supported types:
    * string
    * boolean
    * integer, float and complex
    * date, time and datetime
    * object
    * list, set, tuple and range
    * dictionary
    * JSON map
    * reference to :
        * another definition
        * an environment variable
        * a Python class
        * a Python module


Installation guide
------------------

::

    pip install monkey.ioc

User guide
----------

::

    from monkey.ioc.core import Registry

    registry = Registry()
    registry.load('config.json')
    my_object = registry.get('myObjectID')

Logging
,,,,,,,

Logger name for Registry instances is :code:`monkey.ioc.core.Registry`.

