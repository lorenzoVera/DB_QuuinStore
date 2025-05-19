def consulta_tendencia_ventas(año):
    return f"""
        SELECT
            TO_CHAR(hv.fecha_venta, 'YYYY-MM') AS mes_anio,
            SUM(hv.total) AS total_ventas
        FROM hechos_ventas hv
        WHERE EXTRACT(YEAR FROM hv.fecha_venta) = {año}
        GROUP BY mes_anio
        ORDER BY mes_anio;
    """

def consulta_ventas_por_canal(año):
    return f"""
        SELECT
            cv.nombre_canal,
            SUM(hv.total) AS total_ventas
        FROM hechos_ventas hv
        JOIN canal_ventas cv ON hv.id_canal = cv.id_canal
        WHERE EXTRACT(YEAR FROM hv.fecha_venta) = {año}
        GROUP BY cv.nombre_canal
        ORDER BY total_ventas DESC;
    """

def consulta_top_n_productos(año, n=10):
    return f"""
        SELECT
            p.nombre,
            SUM(hv.cantidad) AS cantidad_vendida
        FROM hechos_ventas hv
        JOIN productos p ON hv.id_producto = p.id_producto
        WHERE EXTRACT(YEAR FROM hv.fecha_venta) = {año}
        GROUP BY p.nombre
        ORDER BY cantidad_vendida DESC
        LIMIT {n};
    """

def consulta_ventas_por_categoria(año):
    return f"""
        SELECT
            p.categoría,
            SUM(hv.total) AS total_ventas
        FROM hechos_ventas hv
        JOIN productos p ON hv.id_producto = p.id_producto
        WHERE EXTRACT(YEAR FROM hv.fecha_venta) = {año}
        GROUP BY p.categoría
        ORDER BY total_ventas DESC;
    """

def consulta_distribucion_metodos_pago(año):
    return f"""
        SELECT
            mp.nombre_metodo,
            COUNT(hv.id_venta) AS cantidad_ventas
        FROM hechos_ventas hv
        JOIN metodo_pagos mp ON hv.id_metodo = mp.id_metodo
        WHERE EXTRACT(YEAR FROM hv.fecha_venta) = {año}
        GROUP BY mp.nombre_metodo
        ORDER BY cantidad_ventas DESC;
    """

def consulta_ventas_por_region(año):
    return f"""
        SELECT
            c.region,
            SUM(hv.total) AS total_ventas
        FROM hechos_ventas hv
        JOIN clientes c ON hv.id_cliente = c.id_cliente
        WHERE EXTRACT(YEAR FROM hv.fecha_venta) = {año}
        GROUP BY c.region
        ORDER BY total_ventas DESC;
    """