import psycopg2


class Database:
    def __init__(self):
        self.con = psycopg2.connect(
            dbname="Slon",
            user="postgres",
            password="Sedoi27091964",
            host="localhost",
            port=5432
        )
        self.cur = self.con.cursor()
    def Select(self, id=None, country=None, rating=0):
        if id is not None:
            self.cur.execute(f'SELECT * FROM films WHERE id = {id}')
            data = self.prepare_data([self.cur.fetchone()])
            return data[0]

        if country is not None:
            self.cur.execute(f'SELECT * FROM films WHERE rating >= {rating} AND country = "{country}"')
        else:
            self.cur.execute(f'SELECT * FROM films WHERE rating >= {rating}')

        return self.prepare_data(self.cur.fetchall())


    def Insert(self, film):
        id, name, rating, country = film['id'], film['name'], film['rating'], film['country']
        self.cur.execute(f"INSERT INTO films VALUES({id}, '{name}', {rating}, '{country}')")
        self.con.commit()

    def prepare_data(self, data):
        films = []
        if len(data):
            column_names = [desc[0] for desc in self.cur.description]
            for row in data:
                films += [{c_name: row[key] for key, c_name in enumerate(column_names)}]

        return films