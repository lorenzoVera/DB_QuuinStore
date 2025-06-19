import customtkinter as ctk
import tkinter.messagebox
from datetime import datetime
from database_manager import DatabaseManager
from modify_sale_window import ModifySaleWindow
from db_sequence_sync import synchronize_sequence

class SalesApp(ctk.CTk):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager

        self.title("Gestor de ventas Quuin Store")
        self.geometry("1200x780")
        self.resizable(False,False)

        # Configuración de columnas y filas
        self.grid_columnconfigure(0, weight=1) # Columna izquierda
        self.grid_columnconfigure(1, weight=1) # Columna derecha
        self.grid_rowconfigure(0, weight=1) # Fila principal

        self.current_page = 0
        self.sales_per_page = 10
        self.current_search_id = None

        # Sincronización de la secuencia al iniciar la aplicación
        print("Sincronizando la secuencia para pedidos_venta...")
        success, message = synchronize_sequence(self.db_manager.db_config, "pedidos_venta", "id_pedido_venta")
        if not success:
            tkinter.messagebox.showwarning("Sincronización de secuencia", f"No se pudo sincronizar la secuencia de pedidos_venta: {message}\n"
                                                                         "Esto podría causar errores al registrar nuevas ventas si el ID ya existe.")
        else:
            print(f"Sincronización de secuencia de pedidos_venta: {message}")

        self.create_widgets()
        self.update_datetime()
        self.load_sales_list()

    def create_widgets(self):
        # --- Panel Izquierdo: Nueva Venta ---
        self.left_frame = ctk.CTkFrame(self)
        self.left_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.left_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.left_frame, text="Registrar Nueva Venta", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, pady=(0, 20))

        # Fecha y Hora actual
        ctk.CTkLabel(self.left_frame, text="Fecha y Hora Actual:", font=ctk.CTkFont(size=12, weight="bold")).grid(row=1, column=0, sticky="w", padx=10, pady=(0,5))
        self.current_datetime_label = ctk.CTkLabel(self.left_frame, text="", font=ctk.CTkFont(size=12))
        self.current_datetime_label.grid(row=2, column=0, sticky="w", padx=10, pady=(0, 15))

        # ID Cliente
        ctk.CTkLabel(self.left_frame, text="ID Cliente:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.client_id_entry = ctk.CTkEntry(self.left_frame)
        self.client_id_entry.grid(row=4, column=0, sticky="ew", padx=10, pady=5)

        # ID Canal de Venta
        ctk.CTkLabel(self.left_frame, text="ID Canal de Venta:").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        self.channel_id_entry = ctk.CTkEntry(self.left_frame)
        self.channel_id_entry.grid(row=6, column=0, sticky="ew", padx=10, pady=5)

        # ID Método de Pago
        ctk.CTkLabel(self.left_frame, text="ID Método de Pago:").grid(row=7, column=0, sticky="w", padx=10, pady=5)
        self.payment_method_id_entry = ctk.CTkEntry(self.left_frame)
        self.payment_method_id_entry.grid(row=8, column=0, sticky="ew", padx=10, pady=5)
        
        # --- Detalles de Productos para la venta (con Scrollable Frame) ---
        ctk.CTkLabel(self.left_frame, text="Detalles de Productos:", font=ctk.CTkFont(size=16, weight="bold")).grid(row=9, column=0, pady=(20, 10))
        
        # CTkScrollableFrame para contener las filas de productos
        # Altura ajustada a 150. Quitada la línea problemática.
        self.product_entries_scroll_frame = ctk.CTkScrollableFrame(self.left_frame, height=40) 
        self.product_entries_scroll_frame.grid(row=10, column=0, sticky="nsew", padx=10, pady=5)
        self.product_entries_scroll_frame.grid_columnconfigure(0, weight=1) 
        
        # Contenedor interno donde se añaden las filas de productos. Necesario para el scroll.
        self.product_entries_container = ctk.CTkFrame(self.product_entries_scroll_frame, fg_color="transparent")
        self.product_entries_container.grid(row=0, column=0, sticky="nsew")
        self.product_entries_container.grid_columnconfigure(0, weight=1) # Para que las filas de productos se expandan

        self.product_entries = [] # Lista para almacenar los widgets de entrada de productos

        self.add_product_row_button = ctk.CTkButton(self.left_frame, text="Añadir Producto", command=self.add_product_row)
        self.add_product_row_button.grid(row=11, column=0, pady=10)

        # Añadir una fila de producto inicial al cargar la UI
        self.add_product_row()

        # Botón Registrar Venta
        self.register_sale_button = ctk.CTkButton(self.left_frame, text="Registrar Venta", command=self.register_new_sale, fg_color="blue")
        self.register_sale_button.grid(row=12, column=0, pady=20)

        # --- Panel Derecho: Listado de Ventas ---
        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.right_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.right_frame, text="Listado de Ventas", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, pady=(0, 20))

        # Barra de búsqueda
        self.search_frame = ctk.CTkFrame(self.right_frame)
        self.search_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        self.search_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self.search_frame, text="ID de Venta:").pack(side="left", padx=(0, 5))
        self.search_entry = ctk.CTkEntry(self.search_frame)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.search_button = ctk.CTkButton(self.search_frame, text="Buscar", command=self.perform_search)
        self.search_button.pack(side="left", padx=5)
        self.clear_search_button = ctk.CTkButton(self.search_frame, text="Reset", command=self.clear_search)
        self.clear_search_button.pack(side="left", padx=5)

        # Área de visualización de ventas (también con CTkScrollableFrame)
        self.sales_list_frame = ctk.CTkScrollableFrame(self.right_frame, height=400) # Mantengo esta altura porque parece funcionar bien
        self.sales_list_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        self.sales_list_frame.grid_columnconfigure(0, weight=1)

        # Anchos de columna para la cabecera del listado
        self.ID_VENTA_WIDTH = 60
        self.FECHA_WIDTH = 80
        self.TOTAL_WIDTH = 100
        self.CLIENTE_WIDTH = 180
        self.ACCIONES_WIDTH = 180

        # Cabecera de la tabla de ventas
        header_frame = ctk.CTkFrame(self.sales_list_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0,5))
        
        # Configurar las columnas de la cabecera (usando width fijo para control de tamaño)
        header_frame.grid_columnconfigure(0, weight=0)
        header_frame.grid_columnconfigure(1, weight=0)
        header_frame.grid_columnconfigure(2, weight=0)
        header_frame.grid_columnconfigure(3, weight=0)
        header_frame.grid_columnconfigure(4, weight=0)

        ctk.CTkLabel(header_frame, text="ID Venta", font=ctk.CTkFont(weight="bold"), anchor="center", width=self.ID_VENTA_WIDTH).grid(row=0, column=0, padx=5, sticky="ew")
        ctk.CTkLabel(header_frame, text="Fecha", font=ctk.CTkFont(weight="bold"), anchor="center", width=self.FECHA_WIDTH).grid(row=0, column=1, padx=5, sticky="ew")
        ctk.CTkLabel(header_frame, text="Total", font=ctk.CTkFont(weight="bold"), anchor="center", width=self.TOTAL_WIDTH).grid(row=0, column=2, padx=5, sticky="ew")
        ctk.CTkLabel(header_frame, text="Cliente", font=ctk.CTkFont(weight="bold"), anchor="center", width=self.CLIENTE_WIDTH).grid(row=0, column=3, padx=5, sticky="ew")
        ctk.CTkLabel(header_frame, text="Acciones", font=ctk.CTkFont(weight="bold"), anchor="center", width=self.ACCIONES_WIDTH).grid(row=0, column=4, padx=5, sticky="ew")

        # Paginación
        self.pagination_frame = ctk.CTkFrame(self.right_frame)
        self.pagination_frame.grid(row=3, column=0, pady=10)
        self.prev_button = ctk.CTkButton(self.pagination_frame, text="Anterior", command=self.prev_page)
        self.prev_button.pack(side="left", padx=5)
        self.page_label = ctk.CTkLabel(self.pagination_frame, text="Página 1")
        self.page_label.pack(side="left", padx=5)
        self.next_button = ctk.CTkButton(self.pagination_frame, text="Siguiente", command=self.next_page)
        self.next_button.pack(side="left", padx=5)

    def update_datetime(self):
        # Actualiza la etiqueta de fecha y hora cada segundo
        now = datetime.now()
        self.current_datetime_label.configure(text=now.strftime("%Y-%m-%d %H:%M:%S"))
        self.after(1000, self.update_datetime)

    def add_product_row(self):
        # Añade una nueva fila de entrada de producto al contenedor dentro del scrollable frame
        row_num = len(self.product_entries)
        product_frame = ctk.CTkFrame(self.product_entries_container) 
        product_frame.grid(row=row_num, column=0, sticky="ew", pady=5)
        product_frame.grid_columnconfigure((0, 1, 2), weight=1) # Columnas para ID, Cantidad, Promo
        product_frame.grid_columnconfigure(3, weight=0) # Columna para botón 'X'

        ctk.CTkLabel(product_frame, text="ID Producto:").grid(row=0, column=0, sticky="w", padx=5)
        product_id_entry = ctk.CTkEntry(product_frame)
        product_id_entry.grid(row=1, column=0, sticky="ew", padx=5)

        ctk.CTkLabel(product_frame, text="Cantidad:").grid(row=0, column=1, sticky="w", padx=5)
        quantity_entry = ctk.CTkEntry(product_frame)
        quantity_entry.grid(row=1, column=1, sticky="ew", padx=5)

        ctk.CTkLabel(product_frame, text="ID Promo:").grid(row=0, column=2, sticky="w", padx=5)
        promo_id_entry = ctk.CTkEntry(product_frame)
        promo_id_entry.grid(row=1, column=2, sticky="ew", padx=5)

        remove_button = ctk.CTkButton(product_frame, text="X", width=30, fg_color="red", command=lambda f=product_frame: self.remove_product_row_from_new_sale(f))
        remove_button.grid(row=1, column=3, padx=5, sticky="e")

        self.product_entries.append({
            "frame": product_frame,
            "id_entry": product_id_entry,
            "quantity_entry": quantity_entry,
            "promo_entry": promo_id_entry
        })

    def remove_product_row_from_new_sale(self, frame_to_destroy):
        # Destruye la fila de producto seleccionada y la elimina de la lista
        frame_to_destroy.destroy()
        self.product_entries = [pe for pe in self.product_entries if pe["frame"] != frame_to_destroy]
        # Re-grid las filas restantes para evitar huecos en el scrollable frame
        for i, pe in enumerate(self.product_entries):
            pe["frame"].grid(row=i, column=0, sticky="ew", pady=5)

    def register_new_sale(self):
        # Obtener datos de los campos de la interfaz
        client_id_str = self.client_id_entry.get()
        channel_id_str = self.channel_id_entry.get() # Obtener ID directo
        payment_method_id_str = self.payment_method_id_entry.get() # Obtener ID directo
        
        # Validaciones básicas
        if not client_id_str or not channel_id_str or not payment_method_id_str:
            tkinter.messagebox.showerror("Error", "COMPLETE TODOS LOS CAMPOS")
            return

        try:
            client_id = int(client_id_str)
            channel_id = int(channel_id_str) # Convertir a int
            method_id = int(payment_method_id_str) # Convertir a int
        except ValueError:
            tkinter.messagebox.showerror("Error de Formato", "ID Cliente, ID Canal de Venta y ID Método de Pago NO VALIDO")
            return

        # Obtener fecha y hora actuales
        now = datetime.now()
        fecha_pedido = now.date()
        hora_pedido = now.time()
        estado_pedido = "Pendiente" # Estado por defecto al crear una nueva venta

        # Recolectar detalles de productos de las filas de entrada
        product_details = []
        for entry_set in self.product_entries:
            product_id_str = entry_set["id_entry"].get()
            quantity_str = entry_set["quantity_entry"].get()
            promo_id_str = entry_set["promo_entry"].get()

            if not product_id_str or not quantity_str:
                # Ignorar filas vacías, pero advertir si están parcialmente llenas
                if product_id_str or quantity_str or promo_id_str:
                    tkinter.messagebox.showwarning("Advertencia", "FILA de producto incompleta.")
                continue # Saltar esta fila si está vacía

            try:
                id_detalle_producto = int(product_id_str)
                cantidad = int(quantity_str)
                id_promo = int(promo_id_str) if promo_id_str else None # ID de promoción es opcional
                
                if cantidad <= 0:
                    tkinter.messagebox.showerror("Error", f"La cantidad para el producto ID {id_detalle_producto} debe ser mayor que 0.")
                    return

                product_details.append({
                    "id_detalle_producto": id_detalle_producto,
                    "cantidad": cantidad,
                    "id_promo": id_promo
                })
            except ValueError:
                tkinter.messagebox.showerror("Error de Formato", "ID Detalle Producto, Cantidad y ID Promo deben ser números enteros.")
                return

        if not product_details:
            tkinter.messagebox.showerror("Error", "Debe agregar al menos un producto a la venta.")
            return

        # Llamar al método del gestor de base de datos para insertar la venta
        success, message = self.db_manager.insert_new_sale(
            client_id, channel_id, method_id, fecha_pedido, hora_pedido, estado_pedido, product_details
        )

        if success:
            tkinter.messagebox.showinfo("Éxito", message)
            self.clear_new_sale_form() # Limpiar el formulario después del éxito
            self.load_sales_list() # Recargar la lista de ventas
        else:
            tkinter.messagebox.showerror("Error", message)

    def clear_new_sale_form(self):
        # Limpiar todos los campos de entrada de la nueva venta
        self.client_id_entry.delete(0, ctk.END)
        self.channel_id_entry.delete(0, ctk.END) # Limpiar campo de ID
        self.payment_method_id_entry.delete(0, ctk.END) # Limpiar campo de ID
        
        # Limpiar todas las filas de productos existentes
        for entry_set in self.product_entries:
            entry_set["frame"].destroy()
        self.product_entries.clear()
        self.add_product_row() # Añadir una fila vacía de nuevo para comenzar

    def load_sales_list(self):
        # Limpiar el área de visualización de ventas antes de cargar nuevas
        for widget in self.sales_list_frame.winfo_children():
            if widget != self.sales_list_frame.grid_slaves(row=0, column=0)[0]:
                 widget.destroy()

        offset = self.current_page * self.sales_per_page
        sales = self.db_manager.fetch_sales_list(self.sales_per_page, offset, self.current_search_id)

        if not sales and self.current_page > 0:
            self.current_page -= 1
            self.load_sales_list() # Vuelve a cargar si la página actual queda vacía
            return

        if not sales and self.current_search_id is not None:
            ctk.CTkLabel(self.sales_list_frame, text=f"No se encontró ninguna venta con ID: {self.current_search_id}").grid(row=1, column=0, pady=10, sticky="ew")
            self.page_label.configure(text="Página 0")
            self.prev_button.configure(state="disabled")
            self.next_button.configure(state="disabled")
            return

        if not sales:
            ctk.CTkLabel(self.sales_list_frame, text="No hay ventas registradas.").grid(row=1, column=0, pady=10, sticky="ew")
            self.page_label.configure(text="Página 0")
            self.prev_button.configure(state="disabled")
            self.next_button.configure(state="disabled")
            return

        data_start_row = 1 

        for i, sale in enumerate(sales):
            sale_id = sale[0]
            fecha_pedido = sale[1].strftime("%Y-%m-%d")
            total = f"${sale[2]:,.2f}"
            cliente_nombre = sale[3] + " " + sale[4]
            # Extraer otros datos necesarios para ModifySaleWindow
            id_cliente = sale[5]
            id_canal = sale[6]
            id_metodo_pago = sale[7]
            estado_pedido = sale[8]
            hora_pedido = sale[9].strftime("%H:%M:%S")

            sale_data_for_modify = {
                "ID_pedido_venta": sale_id,
                "ID_cliente": id_cliente,
                "Fecha_pedido": fecha_pedido,
                "Hora_pedido": hora_pedido,
                "Estado_pedido": estado_pedido,
                "ID_canal": id_canal,
                "ID_metodo_pago": id_metodo_pago,
                "Total": sale[2]
            }

            row_frame = ctk.CTkFrame(self.sales_list_frame, fg_color="transparent")
            row_frame.grid(row=i + data_start_row, column=0, sticky="ew", pady=2)
            row_frame.grid_columnconfigure(0, weight=0)
            row_frame.grid_columnconfigure(1, weight=0)
            row_frame.grid_columnconfigure(2, weight=0)
            row_frame.grid_columnconfigure(3, weight=0)
            row_frame.grid_columnconfigure(4, weight=0)

            ctk.CTkLabel(row_frame, text=sale_id, anchor="center", width=self.ID_VENTA_WIDTH).grid(row=0, column=0, padx=5, sticky="ew")
            ctk.CTkLabel(row_frame, text=fecha_pedido, anchor="center", width=self.FECHA_WIDTH).grid(row=0, column=1, padx=5, sticky="ew")
            ctk.CTkLabel(row_frame, text=total, anchor="center", width=self.TOTAL_WIDTH).grid(row=0, column=2, padx=5, sticky="ew")
            ctk.CTkLabel(row_frame, text=self.truncate_text(cliente_nombre, 25), anchor="center", width=self.CLIENTE_WIDTH).grid(row=0, column=3, padx=5, sticky="ew")

            actions_frame = ctk.CTkFrame(row_frame, fg_color="transparent", width=self.ACCIONES_WIDTH)
            actions_frame.grid(row=0, column=4, padx=5, sticky="ew")
            actions_frame.grid_columnconfigure(0, weight=1)
            actions_frame.grid_columnconfigure(1, weight=1)

            modify_button = ctk.CTkButton(actions_frame, text="Modificar", width=80, command=lambda data=sale_data_for_modify: self.open_modify_sale_window(data))
            modify_button.grid(row=0, column=0, padx=(0, 5), sticky="ew")

            delete_button = ctk.CTkButton(actions_frame, text="Eliminar", width=80, fg_color="red", command=lambda s_id=sale_id: self.delete_sale(s_id))
            delete_button.grid(row=0, column=1, padx=(5, 0), sticky="ew")
        
        self.page_label.configure(text=f"Página {self.current_page + 1}")
        self.prev_button.configure(state="normal" if self.current_page > 0 else "disabled")
        self.next_button.configure(state="normal" if len(sales) == self.sales_per_page else "disabled")

        if self.current_search_id is not None:
             self.prev_button.configure(state="disabled")
             self.next_button.configure(state="disabled")

    def truncate_text(self, text, length):
        if len(text) > length:
            return text[:length-3] + "..."
        return text

    def perform_search(self):
        search_value = self.search_entry.get().strip()
        if search_value:
            try:
                self.current_search_id = int(search_value)
                self.current_page = 0
                self.load_sales_list()
            except ValueError:
                tkinter.messagebox.showerror("Error", "Ingrese ID válido.")
        else:
            self.clear_search()

    def clear_search(self):
        self.current_search_id = None
        self.search_entry.delete(0, ctk.END)
        self.current_page = 0
        self.load_sales_list()

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.load_sales_list()

    def next_page(self):
        offset_for_next_page = (self.current_page + 1) * self.sales_per_page
        test_sales = self.db_manager.fetch_sales_list(self.sales_per_page, offset_for_next_page, self.current_search_id)
        if test_sales:
            self.current_page += 1
            self.load_sales_list()
        else:
            tkinter.messagebox.showinfo("Fin de la lista", "No hay más ventas para mostrar.")

    def delete_sale(self, sale_id):
        if tkinter.messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de que desea eliminar la venta ID: {sale_id}? Esta acción es irreversible y devolverá el stock de los productos."):
            success, message = self.db_manager.delete_sale(sale_id)
            if success:
                tkinter.messagebox.showinfo("Éxito", message)
                self.load_sales_list()
            else:
                tkinter.messagebox.showerror("Error", message)

    def open_modify_sale_window(self, sale_data):
        sale_products_details = self.db_manager.fetch_sale_products_details(sale_data["ID_pedido_venta"])
        
        modify_window = ModifySaleWindow(
            master=self,
            db_manager=self.db_manager,
            sale_data=sale_data,
            current_product_details_from_db=sale_products_details
        ) 
        
        modify_window.grab_set()
        self.wait_window(modify_window)
        self.load_sales_list()

if __name__ == "__main__":
    db_config = {
        'host': 'localhost',
        'database': 'ventas_db',
        'user': 'tu_usuario',
        'password': 'tu_password',
        'port': '5432'
    }

    db_manager = DatabaseManager(db_config)
    app = SalesApp(db_manager)
    app.mainloop()