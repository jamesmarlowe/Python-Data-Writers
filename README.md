Python-Data-Writers
===================
Write to multiple databases and formats easily from python


Install
=======
To use mysql:
-------------
```
sudo apt-get install libmysqlclient-dev mysql-server
sudo pip install --allow-external mysql-connector-python   mysql-connector-python
```
mysql -u root
> CREATE USER 'myuser'@'localhost' IDENTIFIED BY 'mypass';
> CREATE USER 'myuser'@'%' IDENTIFIED BY 'mypass';
> GRANT ALL ON *.* TO 'myuser'@'localhost';
> GRANT ALL ON *.* TO 'myuser'@'%';
> show databases;
> use Data;
> show tables;

In my.cnf replace xxx with your IP Address 
bind-address        = xxx.xxx.xxx.xxx




