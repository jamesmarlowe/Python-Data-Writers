writers = {}

from notimplementedwriter import FailedWriter

try:
    from mysqlwriter import MysqlWriter
    writers['mysql'] = MysqlWriter
except ImportError:
    writers['mysql'] = FailedWriter
try:
    from sqlitewriter import SqliteWriter
    writers['sqlite'] = SqliteWriter
except ImportError:
    writers['sqlite'] = FailedWriter
try:
    from csvwriter import CsvWriter
    writers['csv'] = CsvWriter
except ImportError:
    writers['csv'] = FailedWriter
try:
    from rediswriter import RedisWriter
    writers['redis'] = RedisWriter
except ImportError:
    writers['redis'] = FailedWriter
try:
    from mongowriter import MongoWriter
    writers['mongo'] = MongoWriter
except ImportError:
    writers['mongo'] = FailedWriter
try:
    from postgreswriter import PostgresWriter
    writers['postgres'] = PostgresWriter
except ImportError:
    writers['postgres'] = FailedWriter
try:
    from aerospikewriter import AerospikeWriter
    writers['aerospike'] = AerospikeWriter
except ImportError:
    writers['aerospike'] = FailedWriter
try:
    from datareaders.datareader import DataReader
except ImportError:
    pass
    
class DataWriter:

    writers = writers

    def __init__(self, *args, **kwargs):
        self.write_name = kwargs['writer']
        self.writer = self.writers[kwargs['writer']](*args, **kwargs)
        try:
            self.reader = DataReader(reader=self.write_name, *args, **kwargs)
        except:
            pass
        
    def reinit(self, *args, **kwargs):
        self.__init__(*args, **kwargs)
        
    def save(self, list_of_dicts, *args, **kwargs):
        self.writer.save(list_of_dicts, *args, **kwargs)
        print 'Data writen to '+self.write_name
        
    def read(self, *args, **kwargs):
        try:
            list_of_dicts = self.reader.read(*args, **kwargs)
            if isinstance(list_of_dicts, list):
                print 'Data read from '+self.reader_name
            return list_of_dicts
        except:
            print "Can't read without DataReader"
        
    def test(self):
        try:
            data = [{"column1":"row1-item1", "column2":"row1-item2"},
                    {"column1":"row2-item1", "column2":"row2-item2"},
                    {"column1":"row3-item1", "column2":"row3-item2"}]
            self.writer.save(data)
            print "Read: ", self.reader.read()
        except:
            print "Can't test without DataReader"

if __name__ == "__main__":
    DataWriter(writer='mongo').test()

