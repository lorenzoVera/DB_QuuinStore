import psycopg2

# Reemplaza esto con tu cadena de conexión de Render
#DATABASE_URL = "postgres://usuario:contraseña@host:puerto/nombre_db"

# Ruta a tu archivo .sql
sql_file_path = "create.sql"
conn = None  # 🔸 Asegura que esté definida antes del try

try:
    # Conexión a la base de datos
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True  # Necesario para ejecutar múltiples sentencias

    with conn.cursor() as cursor:
        # Leer el archivo SQL
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql = f.read()
        
        # Ejecutar el contenido del archivo
        cursor.execute(sql)

    print("✅ Importación completada exitosamente.")

except Exception as e:
    print("❌ Ocurrió un error al importar:", e)

finally:
    if conn:
        conn.close()
