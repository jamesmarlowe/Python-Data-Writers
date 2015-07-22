Description
===========

This project is useful in any scenario where you need to write some data in a readable manner quickly and easily.

It can be used to write to:

* csv
* sqlite
* mysql
* redis
* mongo
* postgres
* aerospike

Look at https://pypi.python.org/pypi/data-readers/ to write to them. This library was written with the intention to be useful without `data-readers` but they work very well together.

Setup
=====
Install
-------
    pip install data-writers

Usage
=====
Import DataWriter

    from datawriters.datawriter import DataWriter

Create a list of dictionaries for your data:

    data = [{"column1":"row1-item1", "column2":"row1-item2"},
    {"column1":"row2-item1", "column2":"row2-item2"},
    {"column1":"row3-item1", "column2":"row3-item2"}]

csv
---
    DataWriter(writer='csv', database='data.csv').save(data)

sqlite
------
    DataWriter(writer='sqlite', database='data.sqlite', table='DataTable').save(data)

mysql
-----
    DataWriter(writer='mysql', database='data', user='root', table='DataTable').save(data)

redis
-----
    DataWriter(writer='redis', database='1').save(data)

mongo
-----
    DataWriter(writer='mongo', database='data', table='DataTable').save(data)

postgres
--------
    DataWriter(writer='postgres', database='data', table='DataTable').save(data)

aerospike
---------
    DataWriter(writer='aerospike', namespace='data', set='DataTable').save(data)
