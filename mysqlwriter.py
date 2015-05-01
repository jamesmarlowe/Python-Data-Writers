class MysqlWriter:
    def __init__(self, mysql_database, mysql_user):
        self.db_mysql = mysql_database
        self.user_mysql = mysql_user

    def save(list_of_dicts):
        all_keys = set().union(*(d.keys() for d in list_of_dicts))
        
        db = mysql.connector.connect(user=self.user_mysql)
        cursor = db.cursor()
        try:
            db.database = self.db_mysql
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                try:
                    cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(self.db_mysql))
                    db.database = self.db_mysql
                except mysql.connector.Error as err:
                    print("Failed creating database: {}".format(err))
                    exit(1)
                    db.database = self.db_mysql
            else:
                print(err)
                exit(1)
        TABLE_SQL = (
        "CREATE TABLE `DataTable` ("
        "  `id` int(11) NOT NULL AUTO_INCREMENT,"
        "  `update_date` TIMESTAMP NOT NULL,"
        "  `manufacturer` varchar(40),"
        "  PRIMARY KEY (`id`)"
        ") ENGINE=InnoDB")
        try:
            print "Creating table DataTable Table"
            cursor.execute(TABLE_SQL)
            db.commit()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("table already exists")
            else:
                print(err.msg)
        else:
            print("table already exists")

        #print "INSERT INTO DataTable (" + ",".join(list_of_dicts[0].keys()) + ") VALUES(" + ",".join(["%s"] * len(list_of_dicts[0].keys())) + ")"

        #print [tuple(d.get(k, "NULL") for k in d.keys()) for d in list_of_dicts]
        cursor.executemany("INSERT INTO DataTable (" + ",".join(list_of_dicts[0].keys()) + ") " +
                        "VALUES(" + ",".join(["%s"] * len(list_of_dicts[0].keys())) + ")",
                        #[tuple(row[col] for col in cols) for row in data])
                        [tuple(d.get(k, "NULL") for k in list_of_dicts[0].keys()) for d in list_of_dicts])
        db.commit()

