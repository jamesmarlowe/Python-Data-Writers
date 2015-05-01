class CsvWriter:
    def __init__(self, csv_database):
        self.db_csv = csv_database

    def save(list_of_dicts):
        all_keys = set().union(*(d.keys() for d in list_of_dicts))

        writer = csv.writer(f, delimiter=',')
        writer.writerow(all_keys)
        
        for _dict in list_of_dicts:
            row = [_dict.get()]
            writer.writerow(list())
        
