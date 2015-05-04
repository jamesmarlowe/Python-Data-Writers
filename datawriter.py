import mysqlwriter
import sqlitewriter
import csvwriter

class DataWriter:

    self.writers = {
        'mysql':mysqlwriter,
        'sqlite':sqlitewriter,
        'csv':csvwriter
    }

    def __init__(**kwargs):
        self.writer = self.writers[kwargs['writer']](kwargs)
        
    def save(list_of_dicts):
        self.writer.save(list_of_dicts)

