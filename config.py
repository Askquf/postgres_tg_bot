from secret import password #чтобы гитхаб не ругался на пароль в открытом доступе

db_connection = { 'database': 'disaster_db',
                    'host': 'localhost',
                    'user': 'postgres',
                    'password': password,
                    'port': '5432'}

db_table = "disasters"

need_db = False

disaster_levels = ['A', 'B', 'C']