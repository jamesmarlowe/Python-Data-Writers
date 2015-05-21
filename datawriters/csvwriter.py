import csv

class CsvWriter:
    def __init__(self, *args, **kwargs):
        if 'database' in kwargs:
            self.db_csv = kwargs['database']
        else:
            print 'missing database argument, using data.csv'
            self.db_csv = 'data.csv'

    def save(self, list_of_dicts):
        all_keys = list(set().union(*(d.keys() for d in list_of_dicts)))

        f = open(self.db_csv, 'wb')
        writer = csv.writer(f, delimiter=',')
        writer.writerow(all_keys)
        
        for _dict in list_of_dicts:
            writer.writerow([_dict.get(key, '') for key in all_keys])
        
