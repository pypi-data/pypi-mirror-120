Definition syntax
,,,,,,,,,,,,,,,,,

String
......

::

    "city": {
        "type": "str",
        "value": "Tombstone"
    }

Boolean
.......

::

    "truth": {
        "type": "bool",
        "value": true
    }

Integer
.......

::

    "year": {
        "type": "int",
        "value": 1873
    }

Float
.....

::

    "height": {
        "type": "float",
        "value": 1.83
      }

Complex
.....

::

    "c": {
        "type": "complex",
        "value": "4.12+7j"
      }
or

::

    "c": {
        "type": "complex",
        "value": {
            "real": 4.12,
            "imag":8
        }
      }

Date
....

::

    "gunfight_at_the_ok_corral": {
        "type": "date",
        "format": "%d/%m/%Y",
        "value": "26/10/1881"
    }

Default pattern: :code:`%d-%m-%Y`

Time
....

::

    "ten_past_ten_pm": {
        "type": "time",
        "value": "22h10'00\"",
        "format": "%Hh%M'%S\""
    }

Default pattern: :code:`%H:%M:%S`

Datetime
........

::

    "first_moon_walk": {
        "type": "datetime",
        "value": "21/07/1969 02:56",
        "format": "%d/%m/%Y %H:%M"
    }

Default pattern: :code:`%Y-%m-%dT%H:%M:%S`


Object
......

::

    "wyatt_earp": {
        "module": "monkey_samples.gunslingers",
        "class": "Person",
        "parameters": [
            {
                "name": "first_name",
                "type": "str",
                "value": "Wyatt"
            },
            {
                "name": "last_name",
                "type": "str",
                "value": "EARP"
            }
        ]
    }

List
....

::

    "bazaar": {
        "type": "list",
        "value": [
            {
                "type": "int",
                "value": "42"
            },
            {
                "type": "str",
                "value": "elephant"
            },
            {
                "type": "ref",
                "value": "wyatt_earp"
            }
        ]
    }

Set
...

::

    "tombstone_police": {
        "type": "set",
        "value": [
            {
                "type": "ref",
                "value": "wyatt_earp"
            },
            {
                "type": "ref",
                "value": "morgan_earp"
            }
        ]
    }

Tuple
.....

::

    "four_first_fibonacci_numbers": {
        "type": "tuple",
        "value": [
            {
                "type": "int",
                "value": "0"
            },
            {
                "type": "int",
                "value": "1"
            },
            {
                "type": "int",
                "value": "1"
            },
            {
                "type": "int",
                "value": "2"
            }
        ]
    }

Range
.....

::

    "five_step_range": {
        "type": "tuple",
        "value": {
            "start": 0,
            "stop": 100,
            "step": 5
        }

Dictionary
..........

::

    "bazaar": {
        "type": "dict",
        "value": {
            "forty_two": {
                "type": "int",
                "value": 42
            },
            "wyatt": {
                "type": "ref",
                "value": "wyatt_earp"
            },
            "colt_saa_1873": {
                "module": "samples.data",
                "class": "Handgun",
                "parameters": [
                    {
                        "name": "name",
                        "type": "str",
                        "value": "Colt 1873 Single Action Army"
                    },
                    {
                        "name": "model",
                        "type": "str",
                        "value": "1873 Army"
                    },
                    {
                        "name": "year",
                        "type": "int",
                        "value": 1873
                    }
                ]
            }
        }
    }

JSON map
........

::

    "native_json_map": {
        "type": "map",
        "value": {
            "key1": "some text",
            "key2": 567.98,
            "key3": {
                "key4": "foo"
                "key5": "bar"
            }
        }
    }

Reference
.........

::

    "wyatt_earp_ref": {
        "type": "ref",
        "value": "wyatt_earp"
    }

Environment variable
....................

::

    "username": {
        "type": "envvar",
        "value": "USERNAME"
    }


Class
.....

::

    "person_class": {
        "type": "cls",
        "value": {
            "module": "samples.data",
            "class": "Person"
        }
    }

Module
......

::

    "data_module": {
        "type": "module",
        "value": "samples.data"
    }

Inclusion
.........
It is possible to compose the registry configuration by including multiple JSON files.

File paths are absolute or relative to working directory and support wildcards.

::

    "include": [
        "**/*guns.json",
        "data/guns/rif*"
    ]
