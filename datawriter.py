from mysqlwriter     import MysqlWriter
from sqlitewriter    import SqliteWriter
from csvwriter       import CsvWriter
from rediswriter     import RedisWriter
from mongowriter     import MongoWriter
from postgreswriter  import PostgresWriter
from aerospikewriter import AerospikeWriter

class DataWriter:

    writers = {
        'mysql'    :MysqlWriter,
        'sqlite'   :SqliteWriter,
        'csv'      :CsvWriter,
        'redis'    :RedisWriter,
        'mongo'    :MongoWriter,
        'postgres' :PostgresWriter,
        'aerospike':AerospikeWriter
    }

    def __init__(self, *args, **kwargs):
        self.write_name = kwargs['writer']
        self.writer = self.writers[kwargs['writer']](*args, **kwargs)
        
    def reinit(self, *args, **kwargs):
        self.__init__(*args, **kwargs)
        
    def save(self, list_of_dicts):
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

