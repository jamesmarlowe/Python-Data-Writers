from pymongo import MongoClient

class MongoWriter:
    def __init__(self, *args, **kwargs):
        if 'host' in kwargs:
            self.host = kwargs['host']
        else:
            print 'missing host argument, using localhost'
            self.host = 'localhost'
        if 'port' in kwargs:
            self.port = kwargs['port']
        else:
            print 'missing port argument, using 27017'
            self.port = 27017
        if 'database' in kwargs:
            self.db_mongo = kwargs['database']
        else:
            print 'missing database argument, using data'
            self.db_mongo = 'data'
        if 'table' in kwargs:
            self.db_table = kwargs['table']
        else:
            print 'missing table argument, using DataTable'
            self.db_table = 'DataTable'

    def save(self, list_of_dicts):
        MongoClient(self.host, self.port)[self.db_mongo][self.db_table].insert_many(list_of_dicts)
            
