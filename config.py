from secret import pg_user, pg_password
db_connection = { 'database': 'disaster_db',
                    'host': 'localhost',
                    'user': pg_user,
                    'password': pg_password,
                    'port': '5432'}

db_table = "disasters"

need_db = False

disaster_levels = ['A', 'B', 'C']

zabbix_server_api = 'zabbix.local'
