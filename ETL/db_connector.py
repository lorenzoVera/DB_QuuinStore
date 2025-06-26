import psycopg2
from psycopg2 import Error

def connect_db(db_config):
    try:
        conn = psycopg2.connect(**db_config)
        conn.autocommit = False  # Usaremos transacciones explícitas para mayor control
        print(f"Conectado a la base de datos: {db_config['database']}")
        return conn
    except Error as e:
        print(f"Error al conectar a la base de datos {db_config['database']}: {e}")
        return None

def close_db(conn):
    if conn:
        conn.close()
        print("Conexión a la base de datos cerrada.")
