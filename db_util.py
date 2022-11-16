import psycopg2


class Database:
    def __init__(self):
        self.con = psycopg2.connect(
            dbname="sem_work",
            user="user1",
            password="1212",
            host='localhost',
            port=5432
        )
        self.cur = self.con.cursor()

    def insert(self, query):
        self.cur.execute(query)
        self.con.commit()

    def select(self, query):
        self.cur.execute(query)
        data = self.prepare_data(self.cur.fetchall())
        if len(data) == 1:
            data = data[0]

        return data

    def execute(self, query):
        #self.insert(query)
        self.cur.execute(query)
        data = self.prepare_data(self.cur.fetchall())
        if len(data) == 1:
            data = data[0]

        return data

    def prepare_data(self, data):
        films = []
        if len(data):
            column_names = [desc[0] for desc in self.cur.description]
            for row in data:
                films += [{c_name: row[key] for key, c_name in enumerate(column_names)}]

        return films