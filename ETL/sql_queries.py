# --- Consultas de Extracción ---
SELECT_CLIENTES = """
    SELECT ID_cliente, Nombre, Apellido, Direccion, Comuna, Region, Telefono
    FROM clientes;
"""

SELECT_CANALES_VENTA = """
    SELECT ID_canal, Nombre_canal, Descripcion
    FROM canales_venta;
"""

SELECT_METODOS_PAGO = """
    SELECT ID_metodo_pago, Nombre_metodo, Tipo_metodo
    FROM metodos_pago;
"""

SELECT_PRODUCTOS = """
    SELECT ID_producto, Nombre_producto, Categoria, Descripcion, Activo
    FROM productos;
"""

SELECT_DETALLE_PRODUCTOS = """
    SELECT ID_detalle_producto, ID_producto, Talla, Color, Genero, Temporada, Material, Marca, Estilo, Precio_unitario_actual, Stock_disponible
    FROM detalle_productos;
"""

SELECT_PROMOCIONES = """
    SELECT ID_promo, Nombre_promo, Tipo_promo, Valor_descuento, Fecha_inicio, Fecha_fin, Activa, ID_detalle_productos
    FROM promociones;
"""

SELECT_PEDIDOS_VENTA = """
    SELECT ID_pedido_venta, ID_cliente, Fecha_pedido, Hora_pedido, Estado_pedido, ID_canal, ID_metodo_pago, Subtotal, Total
    FROM pedidos_venta
"""

SELECT_DETALLE_PEDIDOS_VENTA = """
    SELECT ID_detalle_pedido_venta, ID_pedido_venta, ID_detalle_producto, Cantidad, Precio_unitario_venta, Subtotal_linea, ID_promo
    FROM detalle_pedidos_venta
    WHERE ID_pedido_venta IN {in_clause};
"""

# --- Consultas de Carga ---

INSERT_TIEMPO = """
    INSERT INTO tiempo (id_tiempo, fecha, mes, año, dia)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (id_tiempo) DO NOTHING;
"""

INSERT_CLIENTES = """
    INSERT INTO clientes (id_cliente, nombre, apellido, comuna, region, telefono)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (id_cliente) DO NOTHING;
"""

INSERT_CANAL_VENTAS = """
    INSERT INTO canal_ventas (id_canal, nombre_canal)
    VALUES (%s, %s)
    ON CONFLICT (id_canal) DO NOTHING;
"""

INSERT_METODO_PAGOS = """
    INSERT INTO metodo_pagos (id_metodo, nombre_metodo)
    VALUES (%s, %s)
    ON CONFLICT (id_metodo) DO NOTHING;
"""

INSERT_PRODUCTOS_DW = """
    INSERT INTO productos (id_producto, nombre, categoría, precio_unitario)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (id_producto) DO NOTHING;
"""

INSERT_DETALLE_PRODUCTOS_DW = """
    INSERT INTO detalle_productos (id_detalle_producto, talla, color, genero, temporada, material, marca, estilo)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (id_detalle_producto) DO NOTHING;
"""

INSERT_PROMOCIONES_DW = """
    INSERT INTO promociones (id_promo, nombre_promo, tipo)
    VALUES (%s, %s, %s)
    ON CONFLICT (id_promo) DO NOTHING;
"""

INSERT_HECHOS_VENTAS = """
    INSERT INTO hechos_ventas (
        id_venta, id_pedido_venta, id_producto, id_detalle_producto,
        id_tiempo, id_cliente, id_canal, id_metodo, id_promo,
        cantidad, total, fecha_venta, hora_venta
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (id_venta) DO NOTHING;
"""
