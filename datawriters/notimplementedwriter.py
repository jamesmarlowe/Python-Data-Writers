class FailedWriter:
    def __init__(self, *args, **kwargs):
        self.write_name = kwargs['writer']
        error = self.write_name + " failed, did you install its requirements?"
        print self.write_name + " failed, did you install its requirements?"
        raise ImportError(error)

    def save(self, list_of_dicts):
        print 'Could not save using ' + self.write_name + ", import failed"
