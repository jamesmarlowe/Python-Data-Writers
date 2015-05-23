writers = {}

from notimplementedwriter import FailedWriter

try:
    from mysqlwriter import MysqlWriter
    writers['mysql'] = MysqlWriter if (MysqlWriter is not None) else FailedWriter
except ImportError:
    pass
try:
    from sqlitewriter import SqliteWriter
    writers['sqlite'] = SqliteWriter
except ImportError:
    pass
try:
    from csvwriter import CsvWriter
    writers['csv'] = CsvWriter
except ImportError:
    pass
try:
    from rediswriter import RedisWriter
    writers['redis'] = RedisWriter if (RedisWriter is not None) else FailedWriter
except ImportError:
    pass
try:
    from mongowriter import MongoWriter
    writers['mongo'] = MongoWriter if (MongoWriter is not None) else FailedWriter
except ImportError:
    pass
try:
    from postgreswriter import PostgresWriter
    writers['postgres'] = PostgresWriter if (PostgresWriter is not None) else FailedWriter
except ImportError:
    pass
try:
    from aerospikewriter import AerospikeWriter
    writers['aerospike'] = AerospikeWriter if (AerospikeWriter is not None) else FailedWriter
except ImportError:
    pass

class DataWriter:

    writers = writers

    def __init__(self, *args, **kwargs):
        self.write_name = kwargs['writer']
        self.writer = self.writers[kwargs['writer']](*args, **kwargs)
        
    def reinit(self, *args, **kwargs):
        self.__init__(*args, **kwargs)
        
    def save(self, list_of_dicts, *args, **kwargs):
        self.writer.save(list_of_dicts)
        print 'data writen to '+self.write_name
        
    def test(self):
        self.writer.save([{"column1":"row1-item1", "column2":"row1-item2"},
                          {"column1":"row2-item1", "column2":"row2-item2"},
                          {"column1":"row3-item1", "column2":"row3-item2"}])

if __name__ == "__main__":
    DataWriter(writer='mongo').test()
    #for writer in DataWriter.writers.keys():
    #    DataWriter(writer=writer).test()

