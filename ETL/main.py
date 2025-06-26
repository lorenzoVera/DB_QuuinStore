import argparse
import sys
import os
from dotenv import load_dotenv

# Añadir el directorio actual al PATH para que Python encuentre los módulos locales
sys.path.append(os.path.dirname(__file__))

from db_connector import connect_db, close_db
from etl_process import run_etl_process

load_dotenv()
SOURCE_DB_CONFIG = {
    "host": os.getenv("SOURCE_DB_HOST"),
    "database": os.getenv("SOURCE_DB_NAME"),
    "user": os.getenv("SOURCE_DB_USER"),
    "password": os.getenv("SOURCE_DB_PASSWORD")
}

TARGET_DB_CONFIG = {
    "host": os.getenv("TARGET_DB_HOST"),
    "database": os.getenv("TARGET_DB_NAME"),
    "user": os.getenv("TARGET_DB_USER"),
    "password": os.getenv("TARGET_DB_PASSWORD")
}

def main():
    
    parser = argparse.ArgumentParser(
        description="Programa ETL para extraer datos de ventas de PostgreSQL a un almacén de datos.",
        formatter_class=argparse.RawTextHelpFormatter # Para que el texto de ayuda se muestre tal cual
    )
    parser.add_argument("--limit", type=int, default=None,
                        help="Número máximo de pedidos de venta a procesar desde la base de datos de origen.\n"
                             "Si no se especifica (o es 0/negativo), procesará todos los pedidos de venta extraídos.\n"
                             "Ejemplo: python main.py --limit 100")
    args = parser.parse_args()

    conn_src = None
    conn_tgt = None
    try:
        # Conectar a la base de datos de origen
        conn_src = connect_db(SOURCE_DB_CONFIG)
        if not conn_src:
            print("Error: No se pudo conectar a la base de datos de origen. Terminando.")
            return

        # Conectar a la base de datos de destino
        conn_tgt = connect_db(TARGET_DB_CONFIG)
        if not conn_tgt:
            print("Error: No se pudo conectar a la base de datos de destino. Terminando.")
            return

        # Ejecutar el proceso ETL
        run_etl_process(conn_src, conn_tgt, args.limit)

    except Exception as e:
        print(f"Un error inesperado ocurrió durante el proceso ETL: {e}")
    finally:
        # Cerrar las conexiones
        close_db(conn_src)
        close_db(conn_tgt)

if __name__ == "__main__":
    main()
