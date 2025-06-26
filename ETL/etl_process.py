from psycopg2 import Error
from datetime import datetime, date, time
import sql_queries as sql # Importar las consultas SQL

def clear_target_database(conn_tgt):
    cursor = conn_tgt.cursor()
    try:
        print("\n--- Vaciando Base de Datos de Destino ---")
        tables_to_truncate = [
            "hechos_ventas",
            "tiempo",
            "clientes",
            "productos",
            "canal_ventas",
            "metodo_pagos",
            "promociones",
            "detalle_productos"
        ]
                                     
        for table in tables_to_truncate:
            print(f"  - Truncando tabla: {table}...")
            cursor.execute(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;")
        conn_tgt.commit()
        print("--- Base de Datos de Destino Vaciada Exitosamente ---")
    except Error as e:
        conn_tgt.rollback()
        print(f"Error al vaciar la base de datos de destino: {e}")
        raise # Relanzar la excepción para detener el proceso ETL
    finally:
        cursor.close()

def extract_data(conn_src, sales_limit=None):
    data = {}
    cursor = conn_src.cursor()

    try:
        print("\n--- Iniciando Extracción de Datos ---")

        # Extracción de clientes
        cursor.execute(sql.SELECT_CLIENTES)
        data['clientes'] = cursor.fetchall()
        print(f"  - Extraídos {len(data['clientes'])} clientes.")

        # Extracción de canales_venta
        cursor.execute(sql.SELECT_CANALES_VENTA)
        data['canales_venta'] = cursor.fetchall()
        print(f"  - Extraídos {len(data['canales_venta'])} canales de venta.")

        # Extracción de metodos_pago
        cursor.execute(sql.SELECT_METODOS_PAGO)
        data['metodos_pago'] = cursor.fetchall()
        print(f"  - Extraídos {len(data['metodos_pago'])} métodos de pago.")

        # Extracción de productos
        cursor.execute(sql.SELECT_PRODUCTOS)
        data['productos'] = cursor.fetchall()
        print(f"  - Extraídos {len(data['productos'])} productos.")

        # Extracción de detalle_productos
        cursor.execute(sql.SELECT_DETALLE_PRODUCTOS)
        data['detalle_productos'] = cursor.fetchall()
        print(f"  - Extraídos {len(data['detalle_productos'])} detalles de productos.")

        # Extracción de promociones
        cursor.execute(sql.SELECT_PROMOCIONES)
        data['promociones'] = cursor.fetchall()
        print(f"  - Extraídas {len(data['promociones'])} promociones.")

        # Extracción de pedidos_venta (con límite si se especifica)
        query_pedidos_venta = sql.SELECT_PEDIDOS_VENTA
        if sales_limit and sales_limit > 0:
            query_pedidos_venta += f" ORDER BY ID_pedido_venta DESC LIMIT {sales_limit}"
        query_pedidos_venta += ";"
        cursor.execute(query_pedidos_venta)
        data['pedidos_venta'] = cursor.fetchall()
        print(f"  - Extraídos {len(data['pedidos_venta'])} pedidos de venta "
              f"(limitado a {sales_limit} si se especificó y es > 0).")

        # Extracción de detalle_pedidos_venta (filtrando por los pedidos extraídos)
        if data['pedidos_venta']:
            # Obtener los IDs de pedido de venta extraídos para filtrar los detalles
            pedido_venta_ids = tuple([p[0] for p in data['pedidos_venta']])
            
            # Formatear la cláusula IN correctamente para uno o múltiples IDs
            if len(pedido_venta_ids) == 1:
                in_clause = f"({pedido_venta_ids[0]})"
            else:
                in_clause = str(pedido_venta_ids)

            cursor.execute(sql.SELECT_DETALLE_PEDIDOS_VENTA.format(in_clause=in_clause))
            data['detalle_pedidos_venta'] = cursor.fetchall()
            print(f"  - Extraídos {len(data['detalle_pedidos_venta'])} detalles de pedidos de venta relacionados.")
        else:
            data['detalle_pedidos_venta'] = []
            print("  - No se extrajeron pedidos de venta, por lo tanto no hay detalles de pedidos de venta.")

        print("--- Extracción de Datos Completada ---")
        return data

    except Error as e:
        print(f"Error durante la extracción de datos: {e}")
        return None
    finally:
        cursor.close()

def transform_data(raw_data):
    transformed = {
        'tiempo': {},
        'clientes': {},
        'canal_ventas': {},
        'metodo_pagos': {},
        'productos': {},
        'detalle_productos': {},
        'promociones': {},
        'hechos_ventas': []
    }
    print("\n--- Iniciando Transformación de Datos ---")
    
    # --- 1. Transformación de Clientes ---
    transformed.setdefault('clientes', {})
    for client in raw_data['clientes']:
        src_id_cliente = client[0]
        transformed['clientes'][src_id_cliente] = {
            'id_cliente': src_id_cliente,
            'nombre': client[1],
            'apellido': client[2],
            'comuna': client[4],
            'region': client[5],
            'telefono': client[6]
        }
    print(f"  - Transformados {len(transformed['clientes'])} clientes.")

    # --- 2. Transformación de Canal_Ventas ---
    transformed.setdefault('canal_ventas', {})
    for canal in raw_data['canales_venta']:
        src_id_canal = canal[0]
        transformed['canal_ventas'][src_id_canal] = {
            'id_canal': src_id_canal,
            'nombre_canal': canal[1]
        }
    print(f"  - Transformados {len(transformed['canal_ventas'])} canales de venta.")

    # --- 3. Transformación de Metodo_Pagos ---
    transformed.setdefault('metodos_pago', {})
    for metodo in raw_data['metodos_pago']:
        src_id_metodo_pago = metodo[0]
        transformed['metodos_pago'][src_id_metodo_pago] = {
            'id_metodo': src_id_metodo_pago,
            'nombre_metodo': metodo[1]
        }
    print(f"  - Transformados {len(transformed['metodos_pago'])} métodos de pago.")

    # --- 4. Transformación de Productos y Detalle_Productos ---
    detalle_productos_map = {dp[0]: dp for dp in raw_data['detalle_productos']}

    transformed.setdefault('productos', {})
    for prod in raw_data['productos']:
        src_id_producto = prod[0]
        precio_unitario_producto = None
        for dp_id, dp_data in detalle_productos_map.items():
            if dp_data[1] == src_id_producto:
                precio_unitario_producto = dp_data[9]
                break
        
        if precio_unitario_producto is None:
            print(f"  - Advertencia: No se encontró Precio_unitario_actual para Producto ID {src_id_producto}. Se usará 0.00.")
            precio_unitario_producto = 0.00

        transformed['productos'][src_id_producto] = {
            'id_producto': src_id_producto,
            'nombre': prod[1],
            'categoria': prod[2],
            'precio_unitario': precio_unitario_producto
        }
    print(f"  - Transformados {len(transformed['productos'])} productos para la dimensión 'productos'.")

    transformed.setdefault('detalle_productos', {})
    for dp in raw_data['detalle_productos']:
        src_id_detalle_producto = dp[0]
        transformed['detalle_productos'][src_id_detalle_producto] = {
            'id_detalle_producto': src_id_detalle_producto,
            'talla': dp[2],
            'color': dp[3],
            'genero': dp[4],
            'temporada': dp[5],
            'material': dp[6],
            'marca': dp[7],
            'estilo': dp[8]
        }
    print(f"  - Transformados {len(transformed['detalle_productos'])} detalles de productos para la dimensión 'detalle_productos'.")

    # --- 5. Transformación de Promociones ---
    transformed.setdefault('promociones', {})
    for promo in raw_data['promociones']:
        src_id_promo = promo[0]
        transformed['promociones'][src_id_promo] = {
            'id_promo': src_id_promo,
            'nombre_promo': promo[1],
            'tipo': promo[2]
        }
    print(f"  - Transformadas {len(transformed['promociones'])} promociones.")

    # --- 6. Transformación de Tiempo ---
    unique_dates = set()
    for pedido in raw_data['pedidos_venta']:
        unique_dates.add(pedido[2])

    time_id_counter = 1
    transformed.setdefault('tiempo', {})
    for d_obj in sorted(list(unique_dates)):
        date_key = d_obj.strftime('%Y-%m-%d')
        transformed['tiempo'][date_key] = {
            'id_tiempo': time_id_counter,
            'fecha': d_obj,
            'mes': d_obj.month,
            'año': d_obj.year,
            'dia': d_obj.day
        }
        time_id_counter += 1
    print(f"  - Transformadas {len(transformed['tiempo'])} entradas de tiempo únicas.")

    # --- 7. Transformación de Hechos_Ventas ---
    pedidos_venta_map = {p[0]: p for p in raw_data['pedidos_venta']}

    id_venta_counter = 1

    for det_pedido in raw_data['detalle_pedidos_venta']:
        src_id_detalle_pedido_venta = det_pedido[0]
        src_id_pedido_venta = det_pedido[1]
        src_id_detalle_producto = det_pedido[2]
        cantidad = det_pedido[3]
        subtotal_linea = det_pedido[5]
        src_id_promo = det_pedido[6]

        pedido_data = pedidos_venta_map.get(src_id_pedido_venta)
        if not pedido_data:
            print(f"  - Advertencia: Pedido de venta ID {src_id_pedido_venta} no encontrado para detalle {src_id_detalle_pedido_venta}. Saltando.")
            continue

        src_id_cliente = pedido_data[1]
        fecha_pedido = pedido_data[2]
        hora_pedido_time = pedido_data[3]
        src_id_canal = pedido_data[5]
        src_id_metodo_pago = pedido_data[6]

        id_producto_asociado = None
        for dp_data_entry in raw_data['detalle_productos']:
            if dp_data_entry[0] == src_id_detalle_producto:
                id_producto_asociado = dp_data_entry[1]
                break
        if id_producto_asociado is None:
            print(f"  - Advertencia: No se encontró ID_producto para Detalle_Producto ID {src_id_detalle_producto}. Saltando línea de venta.")
            continue
        
        hora_venta_int = hora_pedido_time.hour if isinstance(hora_pedido_time, time) else 0

        fecha_key = fecha_pedido.strftime('%Y-%m-%d')
        id_tiempo = transformed['tiempo'].get(fecha_key, {}).get('id_tiempo')
        if id_tiempo is None:
            print(f"  - Advertencia: No se encontró ID de tiempo para la fecha {fecha_key}. Saltando línea de venta.")
            continue
        
        transformed['hechos_ventas'].append({
            'id_venta': id_venta_counter,
            'id_pedido_venta': src_id_pedido_venta,
            'id_producto': id_producto_asociado,
            'id_detalle_producto': src_id_detalle_producto,
            'id_tiempo': id_tiempo,
            'id_cliente': src_id_cliente,
            'id_canal': src_id_canal,
            'id_metodo': src_id_metodo_pago,
            'id_promo': src_id_promo,
            'cantidad': cantidad,
            'total': subtotal_linea,
            'fecha_venta': fecha_pedido,
            'hora_venta': hora_venta_int
        })
        id_venta_counter += 1

    print(f"  - Transformados {len(transformed['hechos_ventas'])} hechos de ventas.")
    print("--- Transformación de Datos Completada ---")
    return transformed

def load_data(conn_tgt, transformed_data):
    cursor = conn_tgt.cursor()

    try:
        # Vaciar la base de datos de destino antes de cargar nuevos datos
        clear_target_database(conn_tgt) # Llama a la función para vaciar las tablas

        print("\n--- Iniciando Carga de Datos ---")


        # Cargar tiempo (ordenar por id_tiempo para asegurar el orden de inserción si es necesario)
        print("  - Cargando dimensión tiempo...")
        sorted_tiempo_data = sorted(transformed_data['tiempo'].values(), key=lambda x: x['id_tiempo'])
        cursor.executemany(sql.INSERT_TIEMPO, [
            (t_data['id_tiempo'], t_data['fecha'], t_data['mes'], t_data['año'], t_data['dia'])
            for t_data in sorted_tiempo_data
        ])
        print(f"    Cargados {len(transformed_data['tiempo'])} registros en dimensión 'tiempo'.")

        # Cargar clientes
        print("  - Cargando dimensión clientes...")
        cursor.executemany(sql.INSERT_CLIENTES, [
            (client_data['id_cliente'], client_data['nombre'], client_data['apellido'],
             client_data['comuna'], client_data['region'], client_data['telefono'])
            for client_data in transformed_data['clientes'].values()
        ])
        print(f"    Cargados {len(transformed_data['clientes'])} registros en dimensión 'clientes'.")

        # Cargar canal_ventas
        print("  - Cargando dimensión canal_ventas...")
        cursor.executemany(sql.INSERT_CANAL_VENTAS, [
            (canal_data['id_canal'], canal_data['nombre_canal'])
            for canal_data in transformed_data['canal_ventas'].values()
        ])
        print(f"    Cargados {len(transformed_data['canal_ventas'])} registros en dimensión 'canal_ventas'.")

        # Cargar metodo_pagos
        print("  - Cargando dimensión metodo_pagos...")
        cursor.executemany(sql.INSERT_METODO_PAGOS, [
            (metodo_data['id_metodo'], metodo_data['nombre_metodo'])
            for metodo_data in transformed_data['metodos_pago'].values()
        ])
        print(f"    Cargados {len(transformed_data['metodos_pago'])} registros en dimensión 'metodo_pagos'.")

        # Cargar productos
        print("  - Cargando dimensión productos...")
        cursor.executemany(sql.INSERT_PRODUCTOS_DW, [ # Usar DW para diferenciar de la tabla de origen
            (prod_data['id_producto'], prod_data['nombre'], prod_data['categoria'], prod_data['precio_unitario'])
            for prod_data in transformed_data['productos'].values()
        ])
        print(f"    Cargados {len(transformed_data['productos'])} registros en dimensión 'productos'.")

        # Cargar detalle_productos
        print("  - Cargando dimensión detalle_productos...")
        cursor.executemany(sql.INSERT_DETALLE_PRODUCTOS_DW, [ # Usar DW para diferenciar
            (dp_data['id_detalle_producto'], dp_data['talla'], dp_data['color'], dp_data['genero'],
             dp_data['temporada'], dp_data['material'], dp_data['marca'], dp_data['estilo'])
            for dp_data in transformed_data['detalle_productos'].values()
        ])
        print(f"    Cargados {len(transformed_data['detalle_productos'])} registros en dimensión 'detalle_productos'.")

        # Cargar promociones
        print("  - Cargando dimensión promociones...")
        cursor.executemany(sql.INSERT_PROMOCIONES_DW, [ # Usar DW para diferenciar
            (promo_data['id_promo'], promo_data['nombre_promo'], promo_data['tipo'])
            for promo_data in transformed_data['promociones'].values()
        ])
        print(f"    Cargados {len(transformed_data['promociones'])} registros en dimensión 'promociones'.")

        # --- Carga de Hechos_Ventas ---
        print("  - Cargando tabla de hechos 'hechos_ventas'...")
        hechos_ventas_data_to_insert = [
            (
                fact_data['id_venta'], fact_data['id_pedido_venta'], fact_data['id_producto'],
                fact_data['id_detalle_producto'], fact_data['id_tiempo'], fact_data['id_cliente'],
                fact_data['id_canal'], fact_data['id_metodo'], fact_data['id_promo'],
                fact_data['cantidad'], fact_data['total'], fact_data['fecha_venta'],
                fact_data['hora_venta']
            )
            for fact_data in transformed_data['hechos_ventas']
        ]
        cursor.executemany(sql.INSERT_HECHOS_VENTAS, hechos_ventas_data_to_insert)
        print(f"    Cargados {len(transformed_data['hechos_ventas'])} registros en 'hechos_ventas'.")

        conn_tgt.commit()  # Confirmar todas las operaciones de carga
        print("--- Carga de Datos Completada Exitosamente ---")

    except Error as e:
        conn_tgt.rollback()  # Revertir todas las operaciones en caso de error
        print(f"Error durante la carga de datos: {e}")
    finally:
        cursor.close()

def run_etl_process(conn_src, conn_tgt, sales_limit):
    raw_data = extract_data(conn_src, sales_limit)
    if raw_data is None:
        print("La extracción de datos falló. Terminando el proceso ETL.")
        return

    transformed_data = transform_data(raw_data)
    if transformed_data is None:
        print("La transformación de datos falló. Terminando el proceso ETL.")
        return

    load_data(conn_tgt, transformed_data)

