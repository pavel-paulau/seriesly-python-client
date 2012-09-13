seriesly-python-client
======================

Python client for [seriesly](https://github.com/dustin/seriesly) database.

Prerequisites
=============

* Python 2.6
* pip

Installation
============

    pip install seriesly

API overview
============

    from seriesly import Seriesly

    seriesly = Seriesly(host='127.0.0.1', port=3133)

    seriesly.create_db('testdb')

    seriesly.list_dbs()

    seriesly.testdb.append({'key': 'value'})

    seriesly['testdb'].query(params={})

    seriesly.testdb.get_one(timestamp='2005-07-10T02:38:46Z')

    seriesly['testdb'].get_all()

    seriesly.drop_db('testdb')

See [API reference](http://seriesly.readthedocs.org/en/latest/api.html) for details.

Testing
=======

    pip install lettuce

    pip install nose

    lettuce
