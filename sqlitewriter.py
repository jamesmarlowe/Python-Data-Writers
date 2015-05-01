class SqliteWriter:
    def __init__(self, sqlite_database):
        self.db_sqlite3 = sqlite_database

    def save(list_of_dicts):
        all_keys = set().union(*(d.keys() for d in list_of_dicts))
    
        db = sqlite3.connect(self.db_sqlite3)
        cursor = db.cursor()
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS InmobiData(
                    id INTEGER PRIMARY KEY,
                    manufacturer TEXT
                    )''')

        columns = ', '.join(list_of_dicts[0].keys())
        print columns
        placeholders = ':'+', :'.join(list_of_dicts[0].keys())
        print placeholders
        query = 'INSERT INTO InmobiData (%s) VALUES (%s)' % (columns, placeholders)
        print query
        cursor.executemany(query, ({k: d.get(k, defaults[k]) for k in defaults} for d in list_of_dicts))
        db.commit()
        cursor.close()
