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
        
    def reinit(**kwargs):
        self.__init__(**kwargs)
        
    def save(list_of_dicts):
        self.writer.save(list_of_dicts)
        
    def test():
        self.writer.save([{"column1":"row1-item1", "column2":"row1-item2"},
                          {"column1":"row2-item1", "column2":"row2-item2"},
                          {"column1":"row3-item1", "column2":"row3-item2"}])

if __name__ == "__main__":
    for writer in DataWriter.writers:
        DataWriter({'writer':writer}).test()

