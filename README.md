# Python-Data-Writers
Write to multiple databases and formats easily from python


Install
=======
To use mysql:
```
sudo apt-get install libmysqlclient-dev mysql-server
sudo pip install --allow-external mysql-connector-python   mysql-connector-python
```
mysql -u root
> show databases;
> use Data;
> show tables;

my.cnf

#Replace xxx with your IP Address 
bind-address        = xxx.xxx.xxx.xxx
then

CREATE USER 'myuser'@'localhost' IDENTIFIED BY 'mypass';
CREATE USER 'myuser'@'%' IDENTIFIED BY 'mypass';
Then

GRANT ALL ON *.* TO 'myuser'@'localhost';
GRANT ALL ON *.* TO 'myuser'@'%';


