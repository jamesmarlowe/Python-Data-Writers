import psycopg2

class PostgresWriter:
    def __init__(self, *args, **kwargs):
        if 'host' in kwargs:
            self.host = kwargs['host']
        else:
            print 'missing host argument, using localhost'
            self.host = 'localhost'
        if 'database' in kwargs:
            self.db_postgres = kwargs['database']
        else:
            print 'missing database argument, using data'
            self.db_postgres = 'data'
        if 'user' in kwargs:
            self.user_postgres = kwargs['user']
        else:
            print 'missing user argument, using postuser'
            self.user_postgres = 'postuser'
        if 'password' in kwargs:
            self.pass_postgres = kwargs['password']
        else:
            print 'missing password argument, using postpass'
            self.pass_postgres = 'postpass'
        if 'table' in kwargs:
            self.db_table = kwargs['table']
        else:
            print 'missing table argument, using DataTable'
            self.db_table = 'DataTable'

    def save(self, list_of_dicts):
        all_keys = list(set().union(*(d.keys() for d in list_of_dicts)))
        all_vals = list(set().union(*(d.values() for d in list_of_dicts)))
        max_length = str(len(max(all_vals, key=len)))
    
        db = psycopg2.connect("dbname='"+self.db_postgres+"' user='"+self.user_postgres+"' host='"+self.host+"' password='"+self.pass_postgres+"'")
        cursor = db.cursor()
        
        TABLE_SQL = (
            "CREATE TABLE "+self.db_table+" ("
            "  id SERIAL NOT NULL PRIMARY KEY,"
            "  update_date TIMESTAMP NOT NULL default current_timestamp,"
            ""+(' varchar('+max_length+'),').join([str(k) for k in all_keys])+' varchar('+max_length+')'
            ")"
        )
        
        try:
            cursor.execute(TABLE_SQL)
        except psycopg2.ProgrammingError:
            db.commit()

        cursor.executemany("INSERT INTO "+self.db_table+" (" + ",".join(all_keys) + ") " +
                           "VALUES(" + ",".join(["%s"] * len(all_keys)) + ")",
                           [tuple(d.get(k, "NULL") for k in all_keys) for d in list_of_dicts])
        db.commit()
        cursor.close()
