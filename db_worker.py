import psycopg2
from config import db_connection, db_table

class DataBaseWorker():
    conn = psycopg2.connect(database=db_connection['database'],
                        host=db_connection['host'],
                        user=db_connection['user'],
                        password=db_connection['password'],
                        port=db_connection['port']
                        )
    cursor = conn.cursor()
    table_name = db_table

    def get_level_disasters(self, level):
        self.cursor.execute(f"SELECT * FROM {self.table_name} WHERE level = %s", level)
        return self.cursor.fetchall()

    def get_is_solved_disasters(self, is_solved):
        self.cursor.execute(f"SELECT * FROM {self.table_name} WHERE is_solved = {is_solved}")
        return self.cursor.fetchall()