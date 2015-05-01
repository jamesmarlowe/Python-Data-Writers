import mysqlwriter
import sqlitewriter

class DataWriter:

    self.writers = {
        'mysql':mysqlwriter,
        'sqlite':sqlitewriter
    }

    def __init__(**kwargs):
        self.writer = self.writers[kwargs['writer']](kwargs)
        
    def save(list_of_dicts):
        self.writer.save(list_of_dicts)
