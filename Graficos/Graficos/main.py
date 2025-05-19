import psycopg2
from consultas_sql import *
from funciones_graficos import *

# --- Configuración de la conexión a PostgreSQL ---
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "qsdb2"
DB_USER = "python_user"
DB_PASSWORD = "1234"

def conectar_db():
    """Establece una conexión a la base de datos PostgreSQL."""
    conn = None
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD, port=DB_PORT)
    except psycopg2.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
    return conn

def obtener_datos(conn, consulta):
    """Ejecuta una consulta SQL y devuelve los resultados."""
    cur = conn.cursor()
    cur.execute(consulta)
    resultados = cur.fetchall()
    return resultados

if __name__ == "__main__":
    conexion = conectar_db()
    if conexion:
        try:
            anio_a_filtrar = int(input("Ingrese el año para generar los gráficos: "))

            # Generar gráfico de tendencia de ventas
            consulta_tendencia = consulta_tendencia_ventas(anio_a_filtrar)
            datos_tendencia = obtener_datos(conexion, consulta_tendencia)
            generar_grafico_tendencia_ventas(datos_tendencia)

            # Generar gráfico de ventas por canal
            consulta_canal = consulta_ventas_por_canal(anio_a_filtrar)
            datos_canal = obtener_datos(conexion, consulta_canal)
            generar_grafico_ventas_por_canal(datos_canal)

            # Generar gráfico de top N productos
            consulta_top_productos = consulta_top_n_productos(anio_a_filtrar, n=10)
            datos_top_productos = obtener_datos(conexion, consulta_top_productos)
            generar_grafico_top_n_productos(datos_top_productos)

            # Generar gráfico de ventas por categoría
            consulta_categoria = consulta_ventas_por_categoria(anio_a_filtrar)
            datos_categoria = obtener_datos(conexion, consulta_categoria)
            generar_grafico_ventas_por_categoria(datos_categoria)

            # Generar gráfico de distribución de métodos de pago
            consulta_metodo_pago = consulta_distribucion_metodos_pago(anio_a_filtrar)
            datos_metodo_pago = obtener_datos(conexion, consulta_metodo_pago)
            generar_grafico_distribucion_metodos_pago(datos_metodo_pago)

            # Generar gráfico de ventas por región
            consulta_region = consulta_ventas_por_region(anio_a_filtrar)
            datos_region = obtener_datos(conexion, consulta_region)
            generar_grafico_ventas_por_region(datos_region)

        except ValueError:
            print("Error: Por favor, ingrese un año válido.")
        finally:
            conexion.close()