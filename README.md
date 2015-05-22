Python-Data-Writers
===================
Write to multiple databases and formats easily from python. This project is useful in any scenario where you need to write some data in a readable manner quickly and easily.

It can be used to write to:
* csv
* sqlite
* mysql
* redis
* mongo
* postgres
* aerospike


Setup
=====
Install
-------
pypi: https://pypi.python.org/pypi/data-writers/
```
pip install data-writers
```
or manually install with:
```
python setup.py install
```
To use mysql:
-------------
```
sudo apt-get install libmysqlclient-dev mysql-server
sudo pip install --allow-external mysql-connector-python mysql-connector-python
mysql -u root
> CREATE USER 'myuser'@'localhost' IDENTIFIED BY 'mypass';
> CREATE USER 'myuser'@'%' IDENTIFIED BY 'mypass';
> GRANT ALL ON *.* TO 'myuser'@'localhost';
> GRANT ALL ON *.* TO 'myuser'@'%';
> show databases;
> use Data;
> show tables;
```

In my.cnf replace xxx with your IP Address 
bind-address        = xxx.xxx.xxx.xxx

To use redis:
----------------
```
sudo pip install redis
sudo apt-get install redis-server
sudo service redis-server restart
```

To use mongo:
----------------
```
sudo pip install pymongo
sudo apt-get install mongodb-server
sudo service mongodb restart
```

To use postgres:
----------------
```
sudo pip install psycopg2
sudo apt-get install postgresql-9.3
sudo -u postgres psql
> create user postuser password 'postpass';
> GRANT ALL PRIVILEGES ON DATABASE data TO postuser;
```

To use aerospike:
----------------
Install instructions: http://www.aerospike.com/docs/operations/install/linux/ubuntu/
```
sudo pip install aerospike
sudo nano /etc/aerospike/aerospike.conf
> namespace data {storage-engine memory}
sudo /etc/init.d/aerospike start
```

Usage
=====
Import DataWriter
```
from datawriters.datawriter import DataWriter
```
Create a list of dictionaries for your data:
```
data = [{"column1":"row1-item1", "column2":"row1-item2"},
        {"column1":"row2-item1", "column2":"row2-item2"},
        {"column1":"row3-item1", "column2":"row3-item2"}]
```
csv
---
```
DataWriter(writer='csv', database='data.csv').save(data)
```
```
cat data.csv
```
sqlite
------
```
DataWriter(writer='sqlite', database='data.sqlite', table='DataTable').save(data)
```
```
sqlite3
> .open data.sqlite
> select * from DataTable;
```
mysql
-----
```
DataWriter(writer='mysql', database='data', user='root', table='DataTable').save(data)
```
```
mysql -u root
> use data;
> select * from DataTable;
```
redis
-----
```
DataWriter(writer='redis', database='1').save(data)
```
```
redis-cli keys *
redis-cli hgetall data:1
redis-cli SINTER "column1":"row2-item1" "column2":"row2-item2"
redis-cli SUNION "column1":"row2-item1" "column1":"row3-item1"
```
mongo
-----
```
DataWriter(writer='mongo', database='data', table='DataTable').save(data)
```
```
mongo
> use data;
> db.DataTable.find();
```
postgres
--------
```
DataWriter(writer='postgres', database='data', table='DataTable').save(data)
```
```
sudo -u postgres psql
> \connect data;
> select * from DataTable;
```
aerospike
---------
```
DataWriter(writer='aerospike', namespace='data', set='DataTable').save(data)
```
```
asinfo -v "namespace/data"
asinfo -v "bins/data"
cli -o get -n data -s DataTable -k 1
```

