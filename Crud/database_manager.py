# database_manager.py
import psycopg2
from psycopg2 import sql
import tkinter.messagebox
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_config):
        self.db_config = db_config

    def get_connection(self):
        """Establece y devuelve una conexión a la base de datos."""
        try:
            conn = psycopg2.connect(**self.db_config)
            return conn
        except psycopg2.Error as e:
            tkinter.messagebox.showerror("Error de Conexión", f"No se pudo conectar a la base de datos: {e}")
            return None

    # --- Obtener stock del producto ---
    def get_product_stock(self, id_detalle_producto):
        conn = self.get_connection()
        if conn:
            try:
                with conn.cursor() as cur:
                    query = "SELECT stock_disponible FROM detalle_productos WHERE id_detalle_producto = %s;"
                    cur.execute(query, (id_detalle_producto,))
                    result = cur.fetchone()
                    return int(result[0]) if result else None
            except psycopg2.Error as e:
                print(f"Error al obtener stock del producto {id_detalle_producto}: {e}")
                return None
            finally:
                conn.close()
        return None

    def insert_new_sale(self, client_id, channel_id, method_id, fecha_pedido, hora_pedido, estado_pedido, product_details):
        conn = self.get_connection()
        if not conn:
            return False, "No se pudo conectar a la base de datos."

        try:
            with conn.cursor() as cur:
                # Primero, verificar stock para todos los productos antes de iniciar la transacción principal
                products_to_process = []
                for p_detail in product_details:
                    detalle_producto_id = p_detail['id_detalle_producto']
                    cantidad = p_detail['cantidad']

                    current_stock = self.get_product_stock(detalle_producto_id)
                    if current_stock is None:
                        # Si el producto no existe o hay un error al obtener stock, abortar la venta.
                        return False, f"Error: Detalle de producto con ID {detalle_producto_id} no encontrado o stock no disponible."
                    if current_stock < cantidad:
                        return False, f"Error: Stock insuficiente para el producto ID {detalle_producto_id}. Stock actual: {current_stock}, Cantidad requerida: {cantidad}."
                    
                    products_to_process.append(p_detail)

                if not products_to_process and product_details:
                    return False, "Ninguno de los productos especificados pudo ser añadido debido a errores de stock o producto no encontrado."
                elif not products_to_process:
                    return False, "No se especificaron productos para la venta."


                insert_pedido_sql = sql.SQL("""
                    INSERT INTO pedidos_venta (id_cliente, fecha_pedido, hora_pedido, estado_pedido, id_canal, id_metodo_pago, subtotal, total)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_pedido_venta;
                """)
                cur.execute(insert_pedido_sql, (client_id, fecha_pedido, hora_pedido, estado_pedido, channel_id, method_id, 0.0, 0.0))
                pedido_venta_id = cur.fetchone()[0]

                total_sale_subtotal = 0.0

                for p_detail in products_to_process:
                    detalle_producto_id = p_detail['id_detalle_producto']
                    cantidad = p_detail['cantidad']
                    promo_id = p_detail['id_promo']

                    price_unitario_actual = self.get_product_detail_price(detalle_producto_id)
                    if price_unitario_actual is None:
                        continue

                    subtotal_linea = price_unitario_actual * cantidad
                    if promo_id:
                        promo_details = self.get_promotion_details(promo_id)
                        if promo_details and promo_details['activa']:
                            if promo_details['tipo_promo'] == 'Descuento Porcentual':
                                subtotal_linea *= (1 - promo_details['valor_descuento'] / 100)

                    insert_detalle_sql = sql.SQL("""
                        INSERT INTO detalle_pedidos_venta (id_pedido_venta, id_detalle_producto, cantidad, precio_unitario_venta, subtotal_linea, id_promo)
                        VALUES (%s, %s, %s, %s, %s, %s);
                    """)
                    cur.execute(insert_detalle_sql, (pedido_venta_id, detalle_producto_id, cantidad, price_unitario_actual, subtotal_linea, promo_id))
                    
                    total_sale_subtotal += subtotal_linea

                    # --- ACTUALIZAR STOCK DISPONIBLE ---
                    update_stock_sql = sql.SQL("""
                        UPDATE detalle_productos
                        SET stock_disponible = stock_disponible - %s
                        WHERE id_detalle_producto = %s;
                    """)
                    cur.execute(update_stock_sql, (cantidad, detalle_producto_id))

                update_pedido_sql = sql.SQL("""
                    UPDATE pedidos_venta SET subtotal = %s, total = %s WHERE id_pedido_venta = %s;
                """)
                cur.execute(update_pedido_sql, (total_sale_subtotal, total_sale_subtotal, pedido_venta_id))

                conn.commit()
                return True, f"Venta {pedido_venta_id} registrada exitosamente!"

        except psycopg2.Error as e:
            conn.rollback()
            return False, f"Error al registrar la venta: {e}"
        finally:
            if conn:
                conn.close()

    def update_sale(self, id_pedido_venta, client_id, fecha_pedido, hora_pedido, estado_pedido, channel_id, method_id, current_product_details, new_product_details):
        """Actualiza una venta existente y sus detalles de producto, ajustando el stock."""
        conn = self.get_connection()
        if not conn:
            return False, "No se pudo conectar a la base de datos."

        try:
            with conn.cursor() as cur:
                # 1. Actualizar Pedidos_Venta
                update_pedido_sql = sql.SQL("""
                    UPDATE pedidos_venta
                    SET id_cliente = %s, fecha_pedido = %s, hora_pedido = %s, estado_pedido = %s, id_canal = %s, id_metodo_pago = %s
                    WHERE id_pedido_venta = %s;
                """)
                cur.execute(update_pedido_sql, (client_id, fecha_pedido, hora_pedido, estado_pedido, channel_id, method_id, id_pedido_venta))

                # Diccionarios para comparar fácilmente
                old_details_map = {item["ID_detalle_pedido_venta"]: item for item in current_product_details}
                
                total_sale_subtotal = 0.0
                
                products_to_delete_from_db = set(old_details_map.keys())

                # 2. Procesar los nuevos/modificados detalles de producto
                for p_detail in new_product_details:
                    detalle_pedido_venta_id = p_detail.get("id_detalle_pedido_venta")
                    detalle_producto_id = p_detail['id_detalle_producto']
                    cantidad_nueva = p_detail['cantidad']
                    promo_id = p_detail['id_promo']

                    price_unitario_actual = self.get_product_detail_price(detalle_producto_id)
                    if price_unitario_actual is None:
                        tkinter.messagebox.showerror("Error", f"No se encontró el precio para el ID de Detalle Producto: {detalle_producto_id}. No se guardará esta línea.")
                        continue

                    subtotal_linea = price_unitario_actual * cantidad_nueva
                    if promo_id:
                        promo_details = self.get_promotion_details(promo_id)
                        if promo_details and promo_details['activa']:
                            if promo_details['tipo_promo'] == 'Descuento Porcentual':
                                subtotal_linea *= (1 - promo_details['valor_descuento'] / 100)

                    if detalle_pedido_venta_id:
                        products_to_delete_from_db.discard(detalle_pedido_venta_id)
                        
                        cantidad_vieja = old_details_map[detalle_pedido_venta_id]['Cantidad']
                        stock_change = cantidad_vieja - cantidad_nueva # Si sube la cantidad, stock_change es negativo

                        if stock_change < 0: # Necesitamos más stock del que teníamos antes
                            current_stock = self.get_product_stock(detalle_producto_id)
                            if current_stock is None:
                                conn.rollback()
                                return False, f"Error: No se pudo obtener stock para el producto ID {detalle_producto_id} al actualizar."
                            if current_stock < abs(stock_change):
                                conn.rollback()
                                return False, f"Error: Stock insuficiente para aumentar cantidad del producto ID {detalle_producto_id}. Stock actual: {current_stock}, Cantidad adicional requerida: {abs(stock_change)}."
                        
                        update_detalle_sql = sql.SQL("""
                            UPDATE detalle_pedidos_venta
                            SET id_detalle_producto = %s, cantidad = %s, precio_unitario_venta = %s, subtotal_linea = %s, id_promo = %s
                            WHERE id_detalle_pedido_venta = %s;
                        """)
                        cur.execute(update_detalle_sql, (detalle_producto_id, cantidad_nueva, price_unitario_actual, subtotal_linea, promo_id, detalle_pedido_venta_id))
                        
                        # Ajustar stock_disponible
                        update_stock_sql = sql.SQL("""
                            UPDATE detalle_productos
                            SET stock_disponible = stock_disponible + %s
                            WHERE id_detalle_producto = %s;
                        """)
                        cur.execute(update_stock_sql, (stock_change, detalle_producto_id))

                    else: # Es un nuevo detalle de producto para esta venta
                        current_stock = self.get_product_stock(detalle_producto_id)
                        if current_stock is None:
                            conn.rollback()
                            return False, f"Error: Detalle de producto con ID {detalle_producto_id} no encontrado para nueva adición."
                        if current_stock < cantidad_nueva:
                            conn.rollback()
                            return False, f"Error: Stock insuficiente para añadir el producto ID {detalle_producto_id}. Stock actual: {current_stock}, Cantidad requerida: {cantidad_nueva}."

                        insert_detalle_sql = sql.SQL("""
                            INSERT INTO detalle_pedidos_venta (id_pedido_venta, id_detalle_producto, cantidad, precio_unitario_venta, subtotal_linea, id_promo)
                            VALUES (%s, %s, %s, %s, %s, %s);
                        """)
                        cur.execute(insert_detalle_sql, (id_pedido_venta, detalle_producto_id, cantidad_nueva, price_unitario_actual, subtotal_linea, promo_id))
                        
                        # Disminuir stock_disponible para el nuevo producto
                        update_stock_sql = sql.SQL("""
                            UPDATE detalle_productos
                            SET stock_disponible = stock_disponible - %s
                            WHERE id_detalle_producto = %s;
                        """)
                        cur.execute(update_stock_sql, (cantidad_nueva, detalle_producto_id))

                    total_sale_subtotal += subtotal_linea
                
                # 3. Eliminar los detalles de producto que ya no están en la lista (y devolver stock)
                for id_detalle_pedido_venta_to_delete in products_to_delete_from_db:
                    cur.execute(sql.SQL("SELECT cantidad, id_detalle_producto FROM detalle_pedidos_venta WHERE id_detalle_pedido_venta = %s;"), (id_detalle_pedido_venta_to_delete,))
                    deleted_item = cur.fetchone()
                    if deleted_item:
                        cantidad_devuelta = deleted_item[0]
                        id_detalle_producto_devuelto = deleted_item[1]
                        
                        # Devolver stock_disponible
                        update_stock_sql = sql.SQL("""
                            UPDATE detalle_productos
                            SET stock_disponible = stock_disponible + %s
                            WHERE id_detalle_producto = %s;
                        """)
                        cur.execute(update_stock_sql, (cantidad_devuelta, id_detalle_producto_devuelto))
                    
                    cur.execute(sql.SQL("DELETE FROM detalle_pedidos_venta WHERE id_detalle_pedido_venta = %s;"), (id_detalle_pedido_venta_to_delete,))

                # 4. Recalcular y actualizar Subtotal y Total para Pedidos_Venta
                update_total_sql = sql.SQL("""
                    UPDATE pedidos_venta SET subtotal = %s, total = %s WHERE id_pedido_venta = %s;
                """)
                cur.execute(update_total_sql, (total_sale_subtotal, total_sale_subtotal, id_pedido_venta))

                conn.commit()
                return True, "Venta modificada exitosamente!"
        except psycopg2.Error as e:
            conn.rollback()
            return False, f"Error al guardar los cambios: {e}"
        finally:
            if conn:
                conn.close()

    def delete_sale(self, sale_id):
        """Elimina una venta y sus detalles de producto asociados, devolviendo el stock."""
        conn = self.get_connection()
        if not conn:
            return False, "No se pudo conectar a la base de datos."
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT cantidad, id_detalle_producto FROM detalle_pedidos_venta WHERE id_pedido_venta = %s;", (sale_id,))
                products_to_return_stock = cur.fetchall()

                for cantidad, id_detalle_producto in products_to_return_stock:
                    update_stock_sql = sql.SQL("""
                        UPDATE detalle_productos
                        SET stock_disponible = stock_disponible + %s
                        WHERE id_detalle_producto = %s;
                    """)
                    cur.execute(update_stock_sql, (cantidad, id_detalle_producto))

                cur.execute("DELETE FROM detalle_pedidos_venta WHERE id_pedido_venta = %s;", (sale_id,))
                cur.execute("DELETE FROM pedidos_venta WHERE id_pedido_venta = %s;", (sale_id,))
                
                conn.commit()
                return True, f"Venta ID: {sale_id} eliminada exitosamente. Stock devuelto."
        except psycopg2.Error as e:
            conn.rollback()
            return False, f"Error al eliminar la venta: {e}"
        finally:
            if conn:
                conn.close()

    def delete_sale_product_detail(self, id_detalle_pedido_venta):
        """Elimina un solo detalle de producto de una venta, devolviendo el stock y recalculando el total de la venta."""
        conn = self.get_connection()
        if not conn:
            return False, "No se pudo conectar a la base de datos."
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT id_pedido_venta, id_detalle_producto, cantidad, subtotal_linea FROM detalle_pedidos_venta WHERE id_detalle_pedido_venta = %s;", (id_detalle_pedido_venta,))
                deleted_detail = cur.fetchone()

                if not deleted_detail:
                    return False, "Detalle de producto de venta no encontrado."

                id_pedido_venta = deleted_detail[0]
                id_detalle_producto = deleted_detail[1]
                cantidad_eliminada = deleted_detail[2]
                subtotal_eliminado = deleted_detail[3]

                cur.execute("DELETE FROM detalle_pedidos_venta WHERE id_detalle_pedido_venta = %s;", (id_detalle_pedido_venta,))

                # Devolver el stock_disponible
                update_stock_sql = sql.SQL("""
                    UPDATE detalle_productos
                    SET stock_disponible = stock_disponible + %s
                    WHERE id_detalle_producto = %s;
                """)
                cur.execute(update_stock_sql, (cantidad_eliminada, id_detalle_producto))

                update_sale_totals_sql = sql.SQL("""
                    UPDATE pedidos_venta
                    SET subtotal = subtotal - %s,
                        total = total - %s
                    WHERE id_pedido_venta = %s;
                """)
                cur.execute(update_sale_totals_sql, (subtotal_eliminado, subtotal_eliminado, id_pedido_venta))

                conn.commit()
                return True, "Producto de venta eliminado y stock devuelto."
        except psycopg2.Error as e:
            conn.rollback()
            return False, f"Error al eliminar el producto de venta: {e}"
        finally:
            if conn:
                conn.close()
    
    def fetch_channel_options(self):
        conn = self.get_connection()
        if conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("SELECT nombre_canal FROM canales_venta ORDER BY nombre_canal;")
                    channels = [row[0] for row in cur.fetchall()]
                    return channels
            except psycopg2.Error as e:
                tkinter.messagebox.showerror("Error DB", f"Error al cargar canales de venta: {e}")
                return []
            finally:
                conn.close()
        return []

    def fetch_payment_method_options(self):
        conn = self.get_connection()
        if conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("SELECT nombre_metodo FROM metodos_pago ORDER BY nombre_metodo;")
                    methods = [row[0] for row in cur.fetchall()]
                    return methods
            except psycopg2.Error as e:
                tkinter.messagebox.showerror("Error DB", f"Error al cargar métodos de pago: {e}")
                return []
            finally:
                conn.close()
        return []

    def get_id_from_name(self, table_name, name_column, name_value, id_column):
        conn = self.get_connection()
        if conn:
            try:
                with conn.cursor() as cur:
                    query = sql.SQL("SELECT {id_col} FROM {table} WHERE {name_col} = %s;").format(
                        id_col=sql.Identifier(id_column),
                        table=sql.Identifier(table_name),
                        name_col=sql.Identifier(name_column)
                    )
                    cur.execute(query, (name_value,))
                    result = cur.fetchone()
                    return result[0] if result else None
            except psycopg2.Error as e:
                print(f"Error getting ID from name for {table_name}: {e}")
                return None
            finally:
                conn.close()
        return None

    def get_name_from_id(self, table_name, id_column, id_value, name_column):
        conn = self.get_connection()
        if conn:
            try:
                with conn.cursor() as cur:
                    query = sql.SQL("SELECT {name_col} FROM {table} WHERE {id_col} = %s;").format(
                        name_col=sql.Identifier(name_column),
                        table=sql.Identifier(table_name),
                        id_col=sql.Identifier(id_column)
                    )
                    cur.execute(query, (id_value,))
                    result = cur.fetchone()
                    return result[0] if result else None
            except psycopg2.Error as e:
                print(f"Error getting name from ID for {table_name}: {e}")
                return None
            finally:
                conn.close()
        return None

    def get_product_detail_price(self, id_detalle_producto):
        conn = self.get_connection()
        if conn:
            try:
                with conn.cursor() as cur:
                    query = "SELECT precio_unitario_actual FROM detalle_productos WHERE id_detalle_producto = %s;"
                    cur.execute(query, (id_detalle_producto,))
                    result = cur.fetchone()
                    return float(result[0]) if result else None
            except psycopg2.Error as e:
                print(f"Error getting product detail price: {e}")
                return None
            finally:
                conn.close()
        return None

    def get_promotion_details(self, id_promo):
        conn = self.get_connection()
        if conn:
            try:
                with conn.cursor() as cur:
                    query = "SELECT tipo_promo, valor_descuento, activa, fecha_fin FROM promociones WHERE id_promo = %s;"
                    cur.execute(query, (id_promo,))
                    result = cur.fetchone()
                    if result:
                        return {
                            'tipo_promo': result[0],
                            'valor_descuento': float(result[1]),
                            'activa': result[2] and result[3] >= datetime.now().date()
                        }
                    return None
            except psycopg2.Error as e:
                print(f"Error getting promotion details: {e}")
                return None
            finally:
                conn.close()
        return None

    def fetch_sales_list(self, limit, offset, search_id=None):
        conn = self.get_connection()
        sales = []
        if conn:
            try:
                with conn.cursor() as cur:
                    query_base = """
                        SELECT pv.id_pedido_venta, pv.fecha_pedido, pv.total, c.nombre, c.apellido, pv.id_cliente, pv.id_canal, pv.id_metodo_pago, pv.estado_pedido, pv.hora_pedido
                        FROM pedidos_venta pv
                        JOIN clientes c ON pv.id_cliente = c.id_cliente
                    """
                    params = []

                    if search_id is not None:
                        query_base += " WHERE pv.id_pedido_venta = %s"
                        params.append(search_id)

                    query_base += " ORDER BY pv.fecha_pedido DESC, pv.hora_pedido DESC LIMIT %s OFFSET %s;"
                    params.extend([limit, offset])

                    cur.execute(query_base, tuple(params))
                    sales = cur.fetchall()
            except psycopg2.Error as e:
                tkinter.messagebox.showerror("Error DB", f"Error al cargar el listado de ventas: {e}")
            finally:
                conn.close()
        return sales

    def fetch_sale_products_details(self, id_pedido_venta):
        conn = self.get_connection()
        products_details = []
        if conn:
            try:
                with conn.cursor() as cur:
                    query = """
                        SELECT
                            dpv.id_detalle_pedido_venta,
                            dpv.id_detalle_producto,
                            dpv.cantidad,
                            dpv.precio_unitario_venta,
                            dpv.subtotal_linea,
                            dpv.id_promo,
                            p.nombre_producto,
                            ddp.talla,
                            ddp.color
                        FROM detalle_pedidos_venta dpv
                        JOIN detalle_productos ddp ON dpv.id_detalle_producto = ddp.id_detalle_producto
                        JOIN productos p ON ddp.id_producto = p.id_producto
                        WHERE dpv.id_pedido_venta = %s;
                    """
                    cur.execute(query, (id_pedido_venta,))
                    products_details = cur.fetchall()
            except psycopg2.Error as e:
                tkinter.messagebox.showerror("Error DB", f"Error al obtener detalles de productos de la venta: {e}")
            finally:
                conn.close()
        return products_details