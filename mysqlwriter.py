import mysql.connector

class MysqlWriter:
    def __init__(self, *args, **kwargs):
        if 'database' in kwargs:
            self.db_mysql = kwargs['database']
        else:
            print 'missing database argument, using tmp'
            self.db_mysql = 'tmp.sqlite'
        if 'user' in kwargs:
            self.db_mysql = kwargs['user']
        else:
            print 'missing user argument, using root'
            self.user_mysql = 'root'

    def save(self, list_of_dicts):
        all_keys = list(set().union(*(d.keys() for d in list_of_dicts)))
        all_vals = list(set().union(*(d.values() for d in list_of_dicts)))
        max_length = max(all_vals, key=len)
        
        db = mysql.connector.connect(user=self.user_mysql)
        cursor = db.cursor()
        
        try:
            db.database = self.db_mysql
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                try:
                    cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(self.db_mysql))
                    db.database = self.db_mysql
                except mysql.connector.Error as err:
                    print("Failed creating database: {}".format(err))
                    exit(1)
                    db.database = self.db_mysql
            else:
                print(err)
                exit(1)
                
        TABLE_SQL = (
            "CREATE TABLE `DataTable` ("
            "  `id` int(11) NOT NULL AUTO_INCREMENT,"
            "  `update_date` TIMESTAMP NOT NULL,"
            ""+'  varchar('+max_length+'),'.join([k for k in all_keys])+' varchar('+max_length+')'+""
            "  PRIMARY KEY (`id`)"
            ") ENGINE=InnoDB"
        )
        
        print TABLE_SQL
        
        try:
            print "Creating table DataTable Table"
            cursor.execute(TABLE_SQL)
            db.commit()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("table already exists")
            else:
                print(err.msg)
        else:
            print("table already exists")

        cursor.executemany("INSERT INTO DataTable (" + ",".join(all_keys) + ") " +
                           "VALUES(" + ",".join(["%s"] * len(all_keys)) + ")",
                           [tuple(d.get(k, "NULL") for k in all_keys) for d in list_of_dicts])
        db.commit()

