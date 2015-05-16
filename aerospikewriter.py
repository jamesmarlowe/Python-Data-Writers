import aerospike

class AerospikeWriter:
    def __init__(self, *args, **kwargs):
        if 'host' in kwargs:
            self.host = kwargs['host']
        else:
            print 'missing host argument, using 127.0.0.1'
            self.host = '127.0.0.1'
        if 'port' in kwargs:
            self.port = kwargs['port']
        else:
            print 'missing port argument, using 3000'
            self.port = 3000
        if 'namespace' in kwargs:
            self.namespace = kwargs['namespace']
        else:
            print 'missing namespace argument, using data'
            self.namespace = 'data'
        if 'set' in kwargs:
            self.set = kwargs['set']
        else:
            print 'missing set argument, using DataTable'
            self.set = 'DataTable'

    def save(self, list_of_dicts):
        all_keys = list(set().union(*(d.keys() for d in list_of_dicts)))

        config = {'hosts': [ (self.host, self.port) ]}
        client = aerospike.client(config).connect()
        
        id = 0
        for _dict in list_of_dicts:
            id += 1
            key = (self.namespace, self.set, str(id))
            client.put(key, _dict)
        client.close()

