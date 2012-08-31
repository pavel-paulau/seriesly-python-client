seriesly-python-client
======================

Python client for [seriesly](https://github.com/dustin/seriesly) database.


Prerequisites
=============

* Python 2.6
* pip

Dependencies
============

    pip install requests

API overview
============

    from seriesly import Seriesly

    seriesly = Seriesly(host='127.0.0.1', port=3133)

    seriesly.create_db('testdb')

    seriesly.list_dbs()

    seriesly.testdb.append({'key': 'value'})

    seriesly['testdb'].query(params={})

    seriesly.drop_db('testdb')
