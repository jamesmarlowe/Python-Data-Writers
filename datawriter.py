import mysqlwriter
import sqlitewriter
import csvwriter

class DataWriter:

    writers = {
        'mysql' :mysqlwriter.MysqlWriter,
        'sqlite':sqlitewriter.SqliteWriter,
        'csv'   :csvwriter.CsvWriter
    }

    def __init__(self, *args, **kwargs):
        self.writer = self.writers[kwargs['writer']](*args, **kwargs)
        
    def reinit(self, *args, **kwargs):
        self.__init__(**kwargs)
        
    def save(self, list_of_dicts):
        self.writer.save(list_of_dicts)
        
    def test(self):
        self.writer.save([{"column1":"row1-item1", "column2":"row1-item2"},
                          {"column1":"row2-item1", "column2":"row2-item2"},
                          {"column1":"row3-item1", "column2":"row3-item2"}])

if __name__ == "__main__":
    DataWriter(writer='mysql').test()
    #for writer in DataWriter.writers.keys():
    #    #print "hi"
    #    DataWriter(writer=writer)#.test()

