# db_sequence_sync.py
import psycopg2
from psycopg2 import sql
import tkinter.messagebox

def synchronize_sequence(db_config, table_name, id_column):
    
    conn = None
    try:
        conn = psycopg2.connect(**db_config)
        with conn.cursor() as cur:
            
            table_name_db = table_name.lower()
            id_column_db = id_column.lower()

            get_sequence_name_sql = sql.SQL("SELECT pg_get_serial_sequence({table_literal}, {column_literal});").format(
                table_literal=sql.Literal(table_name_db),
                column_literal=sql.Literal(id_column_db)
            )
            cur.execute(get_sequence_name_sql)
            sequence_name_result = cur.fetchone()
            
            if not sequence_name_result or not sequence_name_result[0]:
                print(f"Advertencia: No se encontró la secuencia para la tabla '{table_name_db}', columna '{id_column_db}'.")
                return True, "No se encontró secuencia para sincronizar."
            
            full_sequence_name = sequence_name_result[0] 
            
            set_sequence_sql = sql.SQL("""
                SELECT setval({sequence_name_literal}, COALESCE((SELECT MAX({column_name_identifier}) FROM {table_name_identifier}), 0) + 1, false);
            """).format(
                sequence_name_literal=sql.Literal(full_sequence_name),
                column_name_identifier=sql.Identifier(id_column_db), 
                table_name_identifier=sql.Identifier(table_name_db)   
            )
            
            cur.execute(set_sequence_sql)
            conn.commit()
            print(f"Secuencia '{full_sequence_name}' sincronizada exitosamente.")
            return True, f"Secuencia {table_name_db}.{id_column_db} sincronizada."

    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        print(f"Error al sincronizar la secuencia para {table_name_db}.{id_column_db}: {e}")
        tkinter.messagebox.showerror("Error de Sincronización de DB", f"Error al sincronizar la secuencia de IDs de {table_name_db}: {e}")
        return False, f"Error al sincronizar la secuencia: {e}"
    finally:
        if conn:
            conn.close()

# Ejemplo de uso (solo para pruebas, no se ejecuta si se importa)
if __name__ == "__main__":
    # Asegúrate de reemplazar con tus propios datos de configuración de la base de datos
    db_config_example = {
        'host': 'localhost',
        'database': 'ventas_db',
        'user': 'tu_usuario',
        'password': 'tu_password',
        'port': '5432'
    }
    
    print("Intentando sincronizar la secuencia de Pedidos_Venta...")
    # Pasa los nombres de la tabla y columna en minúsculas
    success, msg = synchronize_sequence(db_config_example, "pedidos_venta", "id_pedido_venta") 
    print(f"Resultado de la sincronización: {msg} (Éxito: {success})")