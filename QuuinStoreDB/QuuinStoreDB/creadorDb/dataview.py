import psycopg2

# Reemplaza esto con tu cadena de conexión de Render
#DATABASE_URL = "postgres://usuario:contraseña@host:puerto/nombre_db"

try:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
    """)

    tables = cursor.fetchall()

    print("📦 Tablas en la base de datos:")
    for table in tables:
        print(" -", table[0])

except Exception as e:
    print("❌ Error:", e)

finally:
    if conn:
        conn.close()
