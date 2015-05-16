import sqlite3

class SqliteWriter:
    def __init__(self, *args, **kwargs):
        if 'database' in kwargs:
            self.db_sqlite3 = kwargs['database']
        else:
            print 'missing database argument, using tmp.sqlite'
            self.db_sqlite3 = 'tmp.sqlite'
        if 'table' in kwargs:
            self.db_table = kwargs['table']
        else:
            print 'missing table argument, using DataTable'
            self.db_table = 'DataTable'

    def save(self, list_of_dicts):
        all_keys = list(set().union(*(d.keys() for d in list_of_dicts)))
    
        db = sqlite3.connect(self.db_sqlite3)
        cursor = db.cursor()
        
        CREATE_TABLE = '''CREATE TABLE IF NOT EXISTS '''+self.db_table+'''(
                        '''+' TEXT,'.join([k for k in all_keys])+' TEXT'+'''
                        )'''
        
        cursor.execute(CREATE_TABLE)

        columns = ', '.join(all_keys)
        placeholders = ':'+', :'.join(all_keys)
        query = 'INSERT INTO '+self.db_table+' (%s) VALUES (%s)' % (columns, placeholders)
        cursor.executemany(query, ({k: d.get(k, None) for k in all_keys} for d in list_of_dicts))
        db.commit()
        cursor.close()
