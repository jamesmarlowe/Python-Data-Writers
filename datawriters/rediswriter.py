import redis

class RedisWriter:
    def __init__(self, *args, **kwargs):
        if 'host' in kwargs:
            self.host = kwargs['host']
        else:
            print 'missing host argument, using 127.0.0.1'
            self.host = '127.0.0.1'
        if 'port' in kwargs:
            self.port = kwargs['port']
        else:
            print 'missing port argument, using 6379'
            self.port = '6379'
        if 'database' in kwargs:
            self.database = kwargs['database']
        else:
            print 'missing database argument, using 0'
            self.database = '0'

    def save(self, list_of_dicts):
        pipe = redis.StrictRedis(host=self.host, port=self.port, db=self.database).pipeline()
        pipe.flushdb()
        id = 0
        for _dict in list_of_dicts:
            if len(_dict.keys()) > 1:
                id += 1
                pipe.hmset('data:'+str(id), _dict)
                [pipe.sadd(str(key)+':'+str(_dict[key]), str(id)) for key in _dict.keys()]
            elif len(_dict.keys()) == 1:
                pipe.mset(_dict)
        pipe.execute()
