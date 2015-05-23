import mysql.connector

class MysqlWriter:
    def __init__(self, *args, **kwargs):
        if 'database' in kwargs:
            self.db_mysql = kwargs['database']
        else:
            print 'missing database argument, using data'
            self.db_mysql = 'data'
        if 'user' in kwargs:
            self.user_mysql = kwargs['user']
        else:
            print 'missing user argument, using root'
            self.user_mysql = 'root'
        if 'table' in kwargs:
            self.db_table = kwargs['table']
        else:
            print 'missing table argument, using DataTable'
            self.db_table = 'DataTable'

    def save(self, list_of_dicts, ignore_duplicate_row_from_key=''):
        all_keys = list(set().union(*(d.keys() for d in list_of_dicts)))
        all_vals = list(set().union(*(d.values() for d in list_of_dicts)))
        def key_order(val):
            return len(str(val))
        max_length = str(len(max(all_vals, key=key_order)))
        
        db = mysql.connector.connect(user=self.user_mysql)
        cursor = db.cursor()
        
        try:
            db.database = self.db_mysql
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
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
            "CREATE TABLE `"+self.db_table+"` ("
            "  `id` int(11) NOT NULL AUTO_INCREMENT,"
            "  `update_date` TIMESTAMP NOT NULL,"
            ""+('  varchar('+max_length+'),').join(['`'+str(k)+'`' for k in all_keys])+' varchar('+max_length+'),'+""
            "  PRIMARY KEY (`id`)"
            ") ENGINE=InnoDB"
        )
        
        try:
            print "Creating table "+self.db_table
            cursor.execute(TABLE_SQL)
            db.commit()
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_TABLE_EXISTS_ERROR:
                print("table already exists")
            else:
                print(err.msg)
        else:
            print("table already exists")
            
        if ignore_duplicate_row_from_key == '':
            cursor.executemany("INSERT INTO "+self.db_table+" (" + ",".join(all_keys) + ") " +
                               "VALUES(" + ",".join(["%s"] * len(all_keys)) + ")",
                               [tuple(d.get(k, "NULL") for k in all_keys) for d in list_of_dicts])
        else:
            existing_rows_from_key = ("select distinct(%s) from %s")
            cursor.execute(query, (ignore_duplicate_row_from_key,self.db_table))
            insert_vals  =  [tuple(d.get(k, "NULL") for k in all_keys)
                                for d in list_of_dicts if 
                                    ((ignore_duplicate_row_from_key in d and
                                    d[ignore_duplicate_row_from_key] not in cursor) or
                                    ignore_duplicate_row_from_key not in d)
                            ]
            cursor.executemany("INSERT INTO "+self.db_table+" (" + ",".join(all_keys) + ") " +
                               "VALUES(" + ",".join(["%s"] * len(all_keys)) + ")",
                               insert_vals)
        
        db.commit()

