import customtkinter as ctk
import tkinter.messagebox
from datetime import datetime

class ModifySaleWindow(ctk.CTkToplevel):
    def __init__(self, master, db_manager, sale_data, current_product_details_from_db):
        super().__init__(master)
        self.db_manager = db_manager
        self.sale_data = sale_data
        self.original_product_details = [list(item) for item in current_product_details_from_db]
        
        self.live_edited_product_details = [] 
        for p_detail in self.original_product_details:
            self.live_edited_product_details.append({
                "ID_detalle_pedido_venta": p_detail[0],
                "ID_detalle_producto": p_detail[1],
                "Cantidad": p_detail[2],
                "ID_promo": p_detail[5]
            })

        self.title(f"Modificar Venta ID: {sale_data['ID_pedido_venta']}")
        self.geometry("800x700")
        self.transient(master)
        self.grab_set()

        self.create_widgets()
        self.load_sale_data()

    def create_widgets(self):
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(pady=20, padx=20, fill="both", expand=False)
        input_frame.grid_columnconfigure(0, weight=1)
        input_frame.grid_columnconfigure(1, weight=2)

        ctk.CTkLabel(input_frame, text="ID Cliente:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.client_id_entry = ctk.CTkEntry(input_frame)
        self.client_id_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=5)

        ctk.CTkLabel(input_frame, text="Fecha Pedido:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.fecha_entry = ctk.CTkEntry(input_frame)
        self.fecha_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

        ctk.CTkLabel(input_frame, text="Hora Pedido:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.hora_entry = ctk.CTkEntry(input_frame)
        self.hora_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=5)

        ctk.CTkLabel(input_frame, text="Estado Pedido:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.estado_optionmenu = ctk.CTkOptionMenu(input_frame, values=["Pendiente", "Completado", "Cancelado", "En Proceso"])
        self.estado_optionmenu.grid(row=3, column=1, sticky="ew", padx=10, pady=5)

        # ID Canal de Venta
        ctk.CTkLabel(input_frame, text="ID Canal de Venta:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.channel_id_entry = ctk.CTkEntry(input_frame)
        self.channel_id_entry.grid(row=4, column=1, sticky="ew", padx=10, pady=5)

        # ID Método de Pago
        ctk.CTkLabel(input_frame, text="ID Método de Pago:").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        self.payment_method_id_entry = ctk.CTkEntry(input_frame)
        self.payment_method_id_entry.grid(row=5, column=1, sticky="ew", padx=10, pady=5)

        ctk.CTkLabel(self, text="Detalles de Productos:", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 5))
        
        self.product_entries_scroll_frame = ctk.CTkScrollableFrame(self, height=250)
        self.product_entries_scroll_frame.pack(pady=10, padx=20, fill="x", expand=True)
        self.product_entries_scroll_frame.grid_columnconfigure(0, weight=1)

        # Contenedor interno donde se añaden las filas de productos
        self.product_entries_container = ctk.CTkFrame(self.product_entries_scroll_frame, fg_color="transparent")
        self.product_entries_container.grid(row=0, column=0, sticky="nsew")
        self.product_entries_container.grid_columnconfigure(0, weight=1)

        self.product_entry_widgets = [] 

        self.add_product_button = ctk.CTkButton(self, text="Añadir Nuevo Producto", command=self.add_product_row)
        self.add_product_button.pack(pady=10)

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=10)
        ctk.CTkButton(button_frame, text="Guardar Cambios", command=self.save_changes).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="Cancelar", command=self.destroy).pack(side="left", padx=10)

    def load_sale_data(self):
        self.client_id_entry.insert(0, str(self.sale_data.get('ID_cliente', '')))
        self.fecha_entry.insert(0, str(self.sale_data.get('Fecha_pedido', '')))
        self.hora_entry.insert(0, str(self.sale_data.get('Hora_pedido', '')))
        self.estado_optionmenu.set(self.sale_data.get('Estado_pedido', "Pendiente"))

        self.channel_id_entry.insert(0, str(self.sale_data.get('ID_canal', '')))
        self.payment_method_id_entry.insert(0, str(self.sale_data.get('ID_metodo_pago', '')))

        # Cargar los detalles de productos existentes
        self.display_product_details()

    def display_product_details(self):
        for widget_set in self.product_entry_widgets:
            widget_set["frame"].destroy()
        self.product_entry_widgets.clear()

        # Añadir filas para los detalles de productos existentes
        for i, p_detail_data in enumerate(self.live_edited_product_details):
            self._add_product_detail_row(i, p_detail_data)

        # Si no hay productos existentes, añadir una fila vacía por defecto
        if not self.live_edited_product_details:
            self.add_product_row()


    def _add_product_detail_row(self, row_num, p_detail_data=None):
        product_frame = ctk.CTkFrame(self.product_entries_container)
        product_frame.grid(row=row_num, column=0, sticky="ew", pady=5)
        product_frame.grid_columnconfigure((0, 1, 2), weight=1)
        product_frame.grid_columnconfigure(3, weight=0)

        ctk.CTkLabel(product_frame, text="ID Detalle Producto:").grid(row=0, column=0, sticky="w", padx=5)
        id_detalle_producto_entry = ctk.CTkEntry(product_frame)
        id_detalle_producto_entry.grid(row=1, column=0, sticky="ew", padx=5)

        ctk.CTkLabel(product_frame, text="Cantidad:").grid(row=0, column=1, sticky="w", padx=5)
        cantidad_entry = ctk.CTkEntry(product_frame)
        cantidad_entry.grid(row=1, column=1, sticky="ew", padx=5)

        ctk.CTkLabel(product_frame, text="ID Promo (Opcional):").grid(row=0, column=2, sticky="w", padx=5)
        id_promo_entry = ctk.CTkEntry(product_frame)
        id_promo_entry.grid(row=1, column=2, sticky="ew", padx=5)

        if p_detail_data:
            id_detalle_producto_entry.insert(0, str(p_detail_data.get('ID_detalle_producto', '')))
            cantidad_entry.insert(0, str(p_detail_data.get('Cantidad', '')))
            if p_detail_data.get('ID_promo') is not None: 
                id_promo_entry.insert(0, str(p_detail_data['ID_promo']))
        
        detail_id_for_db = p_detail_data.get('ID_detalle_pedido_venta') if p_detail_data else None

        remove_button = ctk.CTkButton(product_frame, text="X", width=30, fg_color="red", command=lambda f=product_frame, d_id=detail_id_for_db: self.remove_product_row(f, d_id))
        remove_button.grid(row=1, column=3, padx=5, sticky="e")

        self.product_entry_widgets.append({
            "frame": product_frame,
            "id_detalle_pedido_venta": detail_id_for_db,
            "id_detalle_producto_entry": id_detalle_producto_entry,
            "cantidad_entry": cantidad_entry,
            "id_promo_entry": id_promo_entry
        })

    def add_product_row(self):
        # Cuando se añade una nueva fila, no tiene un ID de detalle de venta asociado aún
        self._add_product_detail_row(len(self.product_entry_widgets), p_detail_data={"ID_detalle_pedido_venta": None})

    def remove_product_row(self, frame_to_destroy, id_detalle_pedido_venta_to_remove):
        widget_set_to_remove = None
        for i, ws in enumerate(self.product_entry_widgets):
            if ws["frame"] == frame_to_destroy:
                widget_set_to_remove = ws
                break

        if widget_set_to_remove:
            self.product_entry_widgets.remove(widget_set_to_remove)
            frame_to_destroy.destroy()
            # Re-grid las filas restantes para evitar huecos
            for i, pw in enumerate(self.product_entry_widgets):
                pw["frame"].grid(row=i, column=0, sticky="ew", pady=5)
        
    def save_changes(self):
        id_pedido_venta = self.sale_data['ID_pedido_venta']
        client_id_str = self.client_id_entry.get()
        fecha_pedido_str = self.fecha_entry.get()
        hora_pedido_str = self.hora_entry.get()
        estado_pedido = self.estado_optionmenu.get()
        channel_id_str = self.channel_id_entry.get()
        payment_method_id_str = self.payment_method_id_entry.get()

        if not client_id_str or not fecha_pedido_str or not hora_pedido_str or not channel_id_str or not payment_method_id_str:
            tkinter.messagebox.showerror("Error", "Complete todos los campos.")
            return

        try:
            client_id = int(client_id_str)
            fecha_pedido = datetime.strptime(fecha_pedido_str, "%Y-%m-%d").date()
            hora_pedido = datetime.strptime(hora_pedido_str, "%H:%M:%S").time()
            channel_id = int(channel_id_str)
            method_id = int(payment_method_id_str)
        except ValueError as e:
            tkinter.messagebox.showerror("Error de Formato", f"Error en el formato de datos: {e}\nAsegúrese que ID Cliente, ID Canal y ID Método de Pago son números")
            return

        # 2. Collect data from product detail fields
        new_product_details_for_db = []
        for pw in self.product_entry_widgets:
            id_detalle_producto_str = pw["id_detalle_producto_entry"].get()
            cantidad_str = pw["cantidad_entry"].get()
            id_promo_str = pw["id_promo_entry"].get()

            if not id_detalle_producto_str or not cantidad_str:
                if id_detalle_producto_str or cantidad_str or id_promo_str:
                     tkinter.messagebox.showwarning("Advertencia", "Se ha detectado una fila de producto incompleta.")
                continue

            try:
                id_detalle_producto = int(id_detalle_producto_str)
                cantidad = int(cantidad_str)
                id_promo = int(id_promo_str) if id_promo_str else None
                
                if cantidad <= 0:
                    tkinter.messagebox.showerror("Error", f"La cantidad para el producto ID {id_detalle_producto} debe ser mayor que 0.")
                    return

                detail_id_for_db = pw["id_detalle_pedido_venta"] 

                new_product_details_for_db.append({
                    "id_detalle_pedido_venta": detail_id_for_db, # Este será None para nuevas líneas
                    "id_detalle_producto": id_detalle_producto,
                    "cantidad": cantidad,
                    "id_promo": id_promo
                })
            except ValueError as e:
                tkinter.messagebox.showerror("Error de Formato", f"Error en el formato de datos de productos: {e}\nID Detalle Producto, Cantidad y ID Promo deben ser números enteros.")
                return
        
        if not new_product_details_for_db:
            tkinter.messagebox.showerror("Error", "Debe haber al menos un producto en la venta.")
            return

        # 3. Call db_manager.update_sale with both original and new product details
        success, message = self.db_manager.update_sale(
            id_pedido_venta,
            client_id,
            fecha_pedido,
            hora_pedido,
            estado_pedido,
            channel_id,
            method_id,
            self.original_product_details, # Pasar los detalles originales tal como se cargaron de la DB
            new_product_details_for_db # Pasar los detalles actuales de la UI
        )

        if success:
            tkinter.messagebox.showinfo("Éxito", message)
            self.destroy()
        else:
            tkinter.messagebox.showerror("Error", message)