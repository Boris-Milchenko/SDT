import psycopg2

error = 'No database connected! Connect to one to work with("connect" command)'
class Db_Working:
    def __init__(self):
        self.connection = None

    def Connect(self, host, username, password, db):
        try:
            self.connection = psycopg2.connect(
                    host = host,
                    user = username,
                    password = password,
                    database = db
                    )
        except Exception as _e:
            print(_e)

    def Get_Tables(self, source = None):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                        """SELECT table_name FROM information_schema.tables
                            WHERE table_schema NOT IN ('information_schema','pg_catalog');"""
                        )
                return [x[0] for x in cursor.fetchall()]
        except AttributeError:
            raise AttributeError(error)

    def Write(self, table, data):
        try:
            with self.connection.cursor() as cursor:
                if table not in self.Get_Tables():
                    self.__add_table(table)

                cursor.execute(
                    'DELETE FROM {0}'.format(table)
                )

                for row in data:
                    cursor.execute(
                            """INSERT INTO {0}
                                VALUES ('{1}', '{2}', '{3}', '{4}', '{5}', '{6}');""".format(table, *row)
                            )
            self.connection.commit()
        except AttributeError:
            raise AttributeError(error)

    def Read(self, table):
        try:
            with self.connection.cursor() as cursor:
                if table not in self.Get_Tables():
                    self.__add_table(table)
                    return []

                cursor.execute(
                        """SELECT * FROM {0};""".format(table)
                        )
                return cursor.fetchall()
        except AttributeError:
            raise AttributeError(error)

    def Del(self, table):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                        "DROP TABLE {0};".format(table)
                        )
            self.connection.commit()
        except AttributeError:
            raise AttributeError(error)

    def __add_table(self, name):
        with self.connection.cursor() as cursor:
            cursor.execute(
                    """CREATE TABLE %s(
                        num int NOT NULL,
                        name character varying(30) NOT NULL,
                        sex varchar(1) NOT NULL,
                        age smallint NOT NULL,
                        domicile character varying(50) NOT NULL,
                        diagnosis text
                    );""" %name
                    )

#db = Db_Working()
#db.Connect('localhost', 'boris', '12345', 'boarding_house')
#print(db.Read('test'))
