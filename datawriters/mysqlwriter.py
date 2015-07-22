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
        if 'pass' in kwargs:
            self.pass_mysql = kwargs['pass']
        else:
            print 'missing pass argument, skipping'
            self.pass_mysql = ''
        if 'table' in kwargs:
            self.db_table = kwargs['table']
        else:
            print 'missing table argument, using DataTable'
            self.db_table = 'DataTable'

    def save(self, list_of_dicts, *args, **kwargs):
        all_keys = list(set().union(*(d.keys() for d in list_of_dicts)))
        all_vals = list(set().union(*(d.values() for d in list_of_dicts)))
        def key_order(val):
            return len(str(val))
        max_length = str(len(max(all_vals, key=key_order)))
        
        config = {user=self.user_mysql}
        if self.pass_mysql != '':
            config['password'] = self.pass_mysql
        
        db = mysql.connector.connect(**config)
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
            
        if 'expire_minutes' in kwargs:
            expire_entries = ("CREATE EVENT IF NOT EXISTS Expire"+self.db_mysql+self.db_table+" "
                              "ON SCHEDULE EVERY 5 MINUTE "
                              "DO DELETE FROM "+self.db_table+" "
                              "WHERE TIMESTAMPDIFF(MINUTE,"+self.db_table+".update_date, NOW())>"
                              ""+str(kwargs['expire_minutes']))
            cursor.execute(expire_entries)
            
        if 'override_previous_from_key' in kwargs:
            existing_rows_from_key = ("select distinct("+kwargs['override_previous_from_key']+") from "+self.db_table)
            cursor.execute(existing_rows_from_key)
            existing_rows = set([item for (item,) in cursor])
            #print "existing_rows", existing_rows
            new_rows = set([d.get(kwargs['override_previous_from_key'], "NULL") for k in all_keys for d in list_of_dicts])
            #print "new_rows", new_rows
            overlap = list(set.intersection(existing_rows, new_rows))
            #print "overlap", overlap
            delete_entries = ("DELETE FROM "+self.db_table+" "
                              "WHERE "+kwargs['override_previous_from_key']+" = %s")
            #print delete_entries
            #print [[o] for o in overlap]
            cursor.executemany(delete_entries, [[o] for o in overlap])
            cursor.executemany("INSERT INTO "+self.db_table+" (" + ",".join(all_keys) + ") " +
                               "VALUES(" + ",".join(["%s"] * len(all_keys)) + ")",
                               [tuple(d.get(k, "NULL") for k in all_keys) for d in list_of_dicts])
        elif 'ignore_duplicate_row_from_key' in kwargs:
            existing_rows_from_key = ("select distinct("+kwargs['ignore_duplicate_row_from_key']+") from "+self.db_table)
            cursor.execute(existing_rows_from_key)
            existing_rows = [item for (item,) in cursor]
            insert_vals  =  [tuple(d.get(k, "NULL") for k in all_keys)
                                for d in list_of_dicts if 
                                    ((kwargs['ignore_duplicate_row_from_key'] in d and
                                    d[kwargs['ignore_duplicate_row_from_key']] not in existing_rows) or
                                    kwargs['ignore_duplicate_row_from_key'] not in d)
                            ]
            cursor.executemany("INSERT INTO "+self.db_table+" (" + ",".join(all_keys) + ") " +
                               "VALUES(" + ",".join(["%s"] * len(all_keys)) + ")",
                               insert_vals)
            print "saving", len(insert_vals), "rows of",len(list_of_dicts) 
        else:
            cursor.executemany("INSERT INTO "+self.db_table+" (" + ",".join(all_keys) + ") " +
                               "VALUES(" + ",".join(["%s"] * len(all_keys)) + ")",
                               [tuple(d.get(k, "NULL") for k in all_keys) for d in list_of_dicts])
        db.commit()

