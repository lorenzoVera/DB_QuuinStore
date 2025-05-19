import psycopg2
from consultas_sql import *
from funciones_graficos import *

def conectar_db():
    """Solicita al usuario los detalles de conexión y retorna un objeto de conexión a la base de datos."""
    dbname = input("Ingrese el nombre de la base de datos: ")
    user = input("Ingrese el nombre de usuario: ")
    password = input("Ingrese la contraseña: ")
    host = input("Ingrese el host (por defecto: localhost): ") or "localhost"
    port = input("Ingrese el puerto (por defecto: 5432): ") or "5432"

    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        print("Conexión a la base de datos exitosa.")
        return conn
    except psycopg2.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def obtener_datos(conn, consulta):
    """Ejecuta una consulta SQL y devuelve los resultados."""
    cur = conn.cursor()
    cur.execute(consulta)
    resultados = cur.fetchall()
    return resultados

if __name__ == "__main__":
    conexion = conectar_db()
    if conexion:
        while True:
            try:
                anio_input = input("Ingrese el año para generar los gráficos (o 'salir' para terminar): ")
                if anio_input.lower() == 'salir':
                    break
                anio_a_filtrar = int(anio_input)

                # Generar gráfico de tendencia de ventas
                consulta_tendencia = consulta_tendencia_ventas(anio_a_filtrar)
                datos_tendencia = obtener_datos(conexion, consulta_tendencia)
                generar_grafico_tendencia_ventas(datos_tendencia, anio_a_filtrar)

                # Generar gráfico de ventas por canal
                consulta_canal = consulta_ventas_por_canal(anio_a_filtrar)
                datos_canal = obtener_datos(conexion, consulta_canal)
                generar_grafico_ventas_por_canal(datos_canal, anio_a_filtrar)

                # Generar gráfico de top N productos
                n = 5
                consulta_top_productos = consulta_top_n_productos(anio_a_filtrar, n)
                datos_top_productos = obtener_datos(conexion, consulta_top_productos)
                generar_grafico_top_n_productos(datos_top_productos, anio_a_filtrar, n)

                # Generar gráfico de ventas por categoría
                consulta_categoria = consulta_ventas_por_categoria(anio_a_filtrar)
                datos_categoria = obtener_datos(conexion, consulta_categoria)
                generar_grafico_ventas_por_categoria(datos_categoria, anio_a_filtrar)

                # Generar gráfico de distribución de métodos de pago
                consulta_metodo_pago = consulta_distribucion_metodos_pago(anio_a_filtrar)
                datos_metodo_pago = obtener_datos(conexion, consulta_metodo_pago)
                generar_grafico_distribucion_metodos_pago(datos_metodo_pago, anio_a_filtrar)

                # Generar gráfico de ventas por región
                consulta_region = consulta_ventas_por_region(anio_a_filtrar)
                datos_region = obtener_datos(conexion, consulta_region)
                generar_grafico_ventas_por_region(datos_region, anio_a_filtrar)
                print("GRAFICOS GENERADOS en la carpeta graficosImagenes")
            except ValueError:
                print("Error: Por favor, ingrese un año válido o 'salir'.")
            except Exception as e:
                print(f"Ocurrió un error: {e}")
            finally:
                pass # La conexión se mantiene abierta hasta que el usuario decide salir

        conexion.close()
        print("Conexión a la base de datos cerrada.")