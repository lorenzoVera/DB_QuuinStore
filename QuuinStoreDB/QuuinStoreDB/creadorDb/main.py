from datos_chile import (
    generar_cliente, generar_producto, generar_detalle_producto, 
    generar_compras_con_pedidos, proveedores
)
from db_inserts import (
    conectar_db, insertar_canales, insertar_metodos_pago, insertar_promociones,
    insertar_proveedores, insertar_clientes, insertar_productos, 
    insertar_detalle_productos, insertar_ventas, insertar_compras, obtener_datos_usuario
)


def main():
    delete = True  # Cambiar a False si no quieres borrar los datos antes de insertar

    n_clientes, n_productos, n_detalles_por_producto, n_ventas, n_compras = obtener_datos_usuario()

    print("Generando clientes...")
    clientes = [generar_cliente(i+1) for i in range(n_clientes)]
    #print(f"Clientes generados: {len(clientes)}")

    print("Generando productos...")
    productos = [generar_producto(i+1) for i in range(n_productos)]
    #print(f"Productos generados: {len(productos)}")

    print("Generando detalles de productos...")
    detalles = []
    id_detalle = 1
    for producto in productos:
        for _ in range(n_detalles_por_producto):
            detalles.append(generar_detalle_producto(id_detalle, producto))
            id_detalle += 1
    #print(f"Detalles de productos generados: {len(detalles)}")

    from datos_chile import generar_ventas_con_pedidos  # IMPORTA ESTA NUEVA FUNCIÓN
    
    
# ...
    conn = conectar_db()
    cursor = conn.cursor()
    
    #print("Generando ventas...")
    ventas = generar_ventas_con_pedidos(
        n_ventas,
        clientes,
        productos,
        detalles,
        ["facebook", "whatsapp", "instagram", "tiktok"],
        ["Efectivo", "Tarjeta de crédito", "Tarjeta de débito", "Transferencia bancaria", "MercadoPago"],
        [{"nombre": "Descuento Verano"}, {"nombre": "2x1 Zapatillas"}, {"nombre": "Promoción Invierno"}, {"nombre": "Envío Gratis"}, {"nombre": "Rebajas Aniversario"}]
    , cursor)
    #print(f"Ventas generadas: {len(ventas)}")

    print("Conectando a la base de datos...")
    
    
    #print("Generando compras con pedidos y proveedores...")
    compras = generar_compras_con_pedidos(n_compras, productos, cursor)
    #print(f"Compras generadas: {len(compras)}")



    

    if delete:
        print("Borrando datos antiguos de las tablas...")
        with conn.cursor() as cur:
            # El orden es importante para respetar FK
            cur.execute("DELETE FROM hechos_ventas;")
            cur.execute("DELETE FROM hechos_compra;")
            cur.execute("DELETE FROM detalle_productos;")
            cur.execute("DELETE FROM productos;")
            cur.execute("DELETE FROM clientes;")
        conn.commit()
        print("Datos antiguos borrados.")
        
        
    insertar_canales(conn)
    insertar_metodos_pago(conn)
    insertar_promociones(conn)
    insertar_proveedores(conn, proveedores)
    


    print("Insertando clientes...")
    insertar_clientes(conn, clientes)
    print("Clientes insertados correctamente.")

    print("Insertando productos...")
    insertar_productos(conn, productos)
    print("Productos insertados correctamente.")

    print("Insertando detalles de productos...")
    insertar_detalle_productos(conn, detalles)
    print("Detalles de productos insertados correctamente.")

    print("Insertando ventas...")
    insertar_ventas(conn, ventas)
    print("Ventas insertadas correctamente.")

    print("Insertando compras...")
    insertar_compras(conn, compras)
    print("Compras insertadas correctamente.")

    conn.close()
    print("Conexión cerrada. Proceso terminado.")


if __name__ == "__main__":
    main()
