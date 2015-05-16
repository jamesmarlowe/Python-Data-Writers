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

    def save(self, list_of_dicts):
        pipe = redis.StrictRedis(host=self.host, port=self.port, db=0).pipeline()
        pipe.flushdb()
        id = 0
        for _dict in list_of_dicts:
            id += 1
            pipe.hmset('data:'+str(id), _dict)
            [pipe.sadd(str(key)+':'+str(_dict[key]), str(id)) for key in _dict.keys()]
        pipe.execute()
