import psycopg2
from psycopg2.extras import execute_values
import random
from datetime import datetime


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

    
    
count_time = 1

from datetime import datetime, timedelta
import random

def generar_tiempo(cursor):
        #conn = conectar_db()
        global count_time
        id_tiempo = count_time
        
        # Genera una fecha aleatoria
        start_date = datetime(2018, 1, 1)
        end_date = datetime.now()
        delta = end_date - start_date
        random_days = random.randint(0, delta.days)
        fecha = start_date + timedelta(days=random_days)

        # Estructura del tiempo
        tiempo = {
            "id_tiempo": id_tiempo,
            "fecha": fecha.strftime("%Y-%m-%d"),
            "año": fecha.year,
            "mes": fecha.month,
            "dia": fecha.day,
        }

        # Guardar en la base de datos
        cursor.execute("""
            INSERT INTO tiempo (id_tiempo, fecha, año, mes, dia)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (id_tiempo) DO NOTHING;
        """, (tiempo["id_tiempo"], tiempo["fecha"], tiempo["año"], tiempo["mes"], tiempo["dia"]))

        count_time += 1
        return tiempo
    
def insertar_canales(conn):
    canales = [
        (1, 'facebook'),
        (2, 'whatsapp'),
        (3, 'instagram'),
        (4, 'tiktok'),
    ]
    with conn.cursor() as cur:
        # Opcional: limpiar tabla primero para evitar duplicados
        cur.execute("DELETE FROM canal_ventas;")
        
        # Insertar canales
        sql = "INSERT INTO canal_ventas (id_canal, nombre_canal) VALUES (%s, %s);"
        cur.executemany(sql, canales)
    conn.commit()
    print("[INFO] Canales insertados correctamente.")
    
def insertar_metodos_pago(conn):
    metodos = [
        (1, "Efectivo"),
        (2, "Tarjeta de crédito"),
        (3, "Tarjeta de débito"),
        (4, "Transferencia bancaria"),
        (5, "MercadoPago")
    ]
    with conn.cursor() as cur:
        cur.execute("DELETE FROM metodo_pagos;")
        sql = "INSERT INTO metodo_pagos (id_metodo, nombre_metodo) VALUES (%s, %s);"
        cur.executemany(sql, metodos)
    conn.commit()
    print("[INFO] Métodos de pago insertados correctamente.")
    
def insertar_proveedores(conn, proveedores):
    print(f"\n[INSERTANDO {len(proveedores)} PROVEEDORES]")
    with conn.cursor() as cur:
        sql = """
        INSERT INTO proveedores (id_proveedor, nombre, telefono, correo)
        VALUES %s
        ON CONFLICT DO NOTHING
        RETURNING id_proveedor;
        """
        values = [(p["id_proveedor"], p["nombre"], p["telefono"], p["correo"]) for p in proveedores]
        execute_values(cur, sql, values)
    conn.commit()
    print("[INFO] Proveedores insertados correctamente.")
    

def insertar_promociones(conn):
    promociones = [
        (1, "Descuento 10%"),
        (2, "Promoción verano"),
        (3, "Oferta 2x1"),
        (4, "Envío gratis"),
        (5, "Black Friday")
    ]
    with conn.cursor() as cur:
        cur.execute("DELETE FROM promociones;")
        sql = "INSERT INTO promociones (id_promo, nombre_promo) VALUES (%s, %s);"
        cur.executemany(sql, promociones)
    conn.commit()
    print("[INFO] Promociones insertadas correctamente.")



def insertar_clientes(conn, clientes):
    print(f"\n[INSERTANDO {len(clientes)} CLIENTES]")
    for c in clientes:
        print("Cliente:", c)
    with conn.cursor() as cur:
        sql = """
        INSERT INTO clientes (id_cliente, nombre, apellido, comuna, region, telefono)
        VALUES %s ON CONFLICT (id_cliente) DO NOTHING;
        """
        values = [(c['id_cliente'], c['nombre'], c['apellido'], c['comuna'], c['region'], c['telefono']) for c in clientes]
        execute_values(cur, sql, values)
    conn.commit()


def insertar_productos(conn, productos):
    print(f"\n[INSERTANDO {len(productos)} PRODUCTOS]")
    for p in productos:
        print("Producto:", p)
    with conn.cursor() as cur:
        sql = """
        INSERT INTO productos (id_producto, nombre, categoría, precio_unitario)
        VALUES %s ON CONFLICT (id_producto) DO NOTHING;
        """
        values = [(p['id_producto'], p['nombre'], p['categoría'], p['precio_unitario']) for p in productos]
        execute_values(cur, sql, values)
    conn.commit()


def insertar_detalle_productos(conn, detalles):
    print(f"\n[INSERTANDO {len(detalles)} DETALLES DE PRODUCTO]")
    for d in detalles:
        print("Detalle:", d)
    with conn.cursor() as cur:
        sql = """
        INSERT INTO detalle_productos (id_detalle_producto, talla, color, genero, temporada, material, marca, estilo)
        VALUES %s ON CONFLICT (id_detalle_producto) DO NOTHING;
        """
        values = [
            (
                d['id_detalle_producto'], d['talla'], d['color'], d['genero'],
                d['temporada'], d['material'], d['marca'], d['estilo'],
            ) for d in detalles
        ]
        execute_values(cur, sql, values)
    conn.commit()


def obtener_id_tiempo(conn, fecha_venta_str):
    fecha_obj = datetime.strptime(fecha_venta_str, "%Y-%m-%d").date()
    with conn.cursor() as cur:
        cur.execute("SELECT id_tiempo FROM tiempo WHERE fecha = %s", (fecha_obj,))
        resultado = cur.fetchone()
        if resultado:
            return resultado[0]
        else:
            mes = fecha_obj.month
            año = fecha_obj.year
            cur.execute("SELECT COALESCE(MAX(id_tiempo), 0) + 1 FROM tiempo")
            nuevo_id = cur.fetchone()[0]
            cur.execute(
                "INSERT INTO tiempo (id_tiempo, fecha, mes, año) VALUES (%s, %s, %s, %s)",
                (nuevo_id, fecha_obj, mes, año)
            )
            conn.commit()
            print(f"[TIEMPO] Insertada nueva fecha: {fecha_obj} con id: {nuevo_id}")
            return nuevo_id



def insertar_ventas(conn, ventas):
    print(f"\n[INSERTANDO {len(ventas)} VENTAS]")

    with conn.cursor() as cur:
        sql = """
        INSERT INTO hechos_ventas 
            (id_venta, id_pedido_venta, id_producto, id_detalle_producto, id_tiempo, id_cliente, id_canal, id_metodo, id_promo, cantidad, total, fecha_venta, hora_venta)
        VALUES %s ON CONFLICT (id_venta) DO NOTHING;
        """

        values = []
        for v in ventas:
            # Validación mínima
            if not v.get('id_producto'):
                raise ValueError(f"[ERROR] Venta sin id_producto válido: {v}")
            if not v.get('id_tiempo'):
                raise ValueError(f"[ERROR] Venta sin id_tiempo válido: {v}")

            row = (
                v['id_venta'],
                v['id_pedido_venta'],
                v['id_producto'],
                v['id_detalle_producto'],
                v['id_tiempo'],
                v['id_cliente'],
                v['id_canal'],
                v['id_metodo'],
                v['id_promo'] or 0,
                v['cantidad'],
                v['total'],
                v['fecha_venta'],
                v['hora_venta']
            )
            print("Venta:", row)
            values.append(row)

        execute_values(cur, sql, values)
    conn.commit()



def insertar_compras(conn, compras):
    print(f"\n[INSERTANDO {len(compras)} COMPRAS]")
    
    for compra in compras:
        print("Claves en compra:", compra.keys())
    with conn.cursor() as cur:
        sql_compra = """
        INSERT INTO hechos_compra (id_compra, id_pedido_compra, id_tiempo, id_proveedor, id_producto, total, subtotal, fecha_compra, hora_compra, fecha_llegada, hora_llegada)
        VALUES %s ON CONFLICT (id_compra) DO NOTHING;
        """
        values_compra = []
        for compra in compras:
            print('compra:   ', compra)
            row = (
                compra["id_compra"], compra["id_pedido_compra"], compra["id_tiempo"],
                compra["id_proveedor"], compra["id_producto"], compra["total"],
                compra["subtotal"], compra["fecha_compra"], compra["hora_compra"],
                compra["fecha_llegada"], compra["hora_llegada"]
            )
            print("Compra:", row)
            values_compra.append(row)

        execute_values(cur, sql_compra, values_compra)
    conn.commit()

def obtener_datos_usuario():
    """Solicita al usuario ingresar los valores para las variables."""
    while True:
        try:
            n_clientes = int(input("Ingrese el número de clientes[recomendado ~2000]: "))
            if n_clientes >= 0:
                break
            else:
                print("Por favor, ingrese un número no negativo.")
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número entero.")

    while True:
        try:
            n_productos = int(input("Ingrese el número de productos [recomendado ~200]: "))
            if n_productos >= 0:
                break
            else:
                print("Por favor, ingrese un número no negativo.")
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número entero.")

    while True:
        try:
            n_detalles_por_producto = int(input("Ingrese el número de detalles por producto [recomendado ~3]: "))
            if n_detalles_por_producto >= 0:
                break
            else:
                print("Por favor, ingrese un número no negativo.")
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número entero.")

    while True:
        try:
            n_ventas = int(input("Ingrese el número de ventas[recomendado ~2000]: "))
            if n_ventas >= 0:
                break
            else:
                print("Por favor, ingrese un número no negativo.")
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número entero.")

    while True:
        try:
            n_compras = int(input("Ingrese el número de compras[recomendado ~2000]: "))
            if n_compras >= 0:
                break
            else:
                print("Por favor, ingrese un número no negativo.")
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número entero.")

    return n_clientes, n_productos, n_detalles_por_producto, n_ventas, n_compras
    