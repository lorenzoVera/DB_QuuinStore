from faker import Faker
import random
from datetime import datetime, timedelta
import random

fake = Faker('es_CL')

from db_inserts import generar_tiempo

# Datos básicos
marcas = [
    "Hush Puppies", "Columbia", "Levi's", "Adidas", "Nike",
    "Patagonia", "Reebok", "Puma", "Lippi", "The North Face",
    "Topper", "Under Armour", "Montagne", "Everlast", "New Balance"
]

canales_venta = [
    "facebook", "whatsapp", "instagram", "tiktok"
]

metodos_pago = [
    "Efectivo", "Tarjeta de crédito", "Tarjeta de débito", "Transferencia bancaria", "MercadoPago"
]

promociones = [
    {"nombre": "Descuento Verano", "tipo": "Descuento"},
    {"nombre": "2x1 Zapatillas", "tipo": "Combo"},
    {"nombre": "Promoción Invierno", "tipo": "Descuento"},
    {"nombre": "Envío Gratis", "tipo": "Promoción especial"},
    {"nombre": "Rebajas Aniversario", "tipo": "Descuento"}
]

proveedores = [
    {"id_proveedor": 1, "nombre": "Textiles Andes", "telefono": "+56912345601", "correo": "contacto@textilesandes.cl"},
    {"id_proveedor": 2, "nombre": "Calzados del Sur", "telefono": "+56912345602", "correo": "ventas@calzadosdelsur.cl"},
    {"id_proveedor": 3, "nombre": "Moda Urbana", "telefono": "+56912345603", "correo": "info@modaurbana.cl"},
    {"id_proveedor": 4, "nombre": "Accesorios Patagonia", "telefono": "+56912345604", "correo": "ventas@accesoriospatagonia.cl"},
    {"id_proveedor": 5, "nombre": "Distribuciones Central", "telefono": "+56912345605", "correo": "contacto@distribucionescentral.cl"},
    {"id_proveedor": 6, "nombre": "Ropa Express", "telefono": "+56912345606", "correo": "ventas@ropaexpress.cl"},
    {"id_proveedor": 7, "nombre": "Zapatos Norte", "telefono": "+56912345607", "correo": "info@zapatosnorte.cl"},
    {"id_proveedor": 8, "nombre": "Calzado y Más", "telefono": "+56912345608", "correo": "contacto@calzadoymas.cl"},
    {"id_proveedor": 9, "nombre": "Importadora Andes", "telefono": "+56912345609", "correo": "ventas@importadoraandes.cl"},
    {"id_proveedor": 10, "nombre": "Textiles Patagonia", "telefono": "+56912345610", "correo": "info@textilespatagonia.cl"},
    {"id_proveedor": 11, "nombre": "Moda y Estilo", "telefono": "+56912345611", "correo": "ventas@modaestilo.cl"},
    {"id_proveedor": 12, "nombre": "Accesorios Chile", "telefono": "+56912345612", "correo": "contacto@accesorioschile.cl"},
    {"id_proveedor": 13, "nombre": "Zapatos Urbanos", "telefono": "+56912345613", "correo": "info@zapatosurbanos.cl"},
    {"id_proveedor": 14, "nombre": "Distribuciones Norte", "telefono": "+56912345614", "correo": "ventas@distribucionesnorte.cl"},
    {"id_proveedor": 15, "nombre": "Textiles Express", "telefono": "+56912345615", "correo": "contacto@textilesexpress.cl"},
    {"id_proveedor": 16, "nombre": "Moda Patagonia", "telefono": "+56912345616", "correo": "info@modapatagonia.cl"},
    {"id_proveedor": 17, "nombre": "Calzado Express", "telefono": "+56912345617", "correo": "ventas@calzadoexpress.cl"},
    {"id_proveedor": 18, "nombre": "Importadora Central", "telefono": "+56912345618", "correo": "contacto@importadoracentral.cl"},
    {"id_proveedor": 19, "nombre": "Accesorios Norte", "telefono": "+56912345619", "correo": "info@accesoriosnorte.cl"},
    {"id_proveedor": 20, "nombre": "Ropa Patagonia", "telefono": "+56912345620", "correo": "ventas@ropapatagonia.cl"},
]

regiones_y_comunas = {
    "Arica y Parinacota": ["Arica", "Putre", "Camarones", "General Lagos", "Codpa", "Belén", "Chungara", "Poconchile", "Visviri", "Camiña"],
    "Tarapacá": ["Iquique", "Alto Hospicio", "Pica", "Pozo Almonte", "Camiña", "Colchane", "Huara", "Pisagua", "Mollo", "Camarones"],
    "Antofagasta": ["Antofagasta", "Calama", "Tocopilla", "Mejillones", "San Pedro de Atacama", "Maria Elena", "Ollagüe", "Sierra Gorda", "Baquedano", "Chilecito"],
    "Atacama": ["Copiapó", "Caldera", "Vallenar", "Chañaral", "Diego de Almagro", "Freirina", "Huasco", "Alto del Carmen", "Tierra Amarilla", "El Salvador"],
    "Coquimbo": ["La Serena", "Coquimbo", "Ovalle", "Illapel", "Salamanca", "Andacollo", "Monte Patria", "Los Vilos", "Combarbalá", "Canela"],
    "Valparaíso": ["Valparaíso", "Viña del Mar", "Quilpué", "San Antonio", "Villa Alemana", "Limache", "Olmué", "Casablanca", "Catemu", "La Ligua"],
    "Región Metropolitana": ["Santiago", "Puente Alto", "Maipú", "La Florida", "Las Condes", "Pudahuel", "Quilicura", "San Bernardo", "Peñalolén", "Huechuraba"],
    "O'Higgins": ["Rancagua", "San Fernando", "Santa Cruz", "Pichilemu", "Machalí", "Rengo", "Graneros", "Mostazal", "Codegua", "Lolol"],
    "Maule": ["Talca", "Curicó", "Linares", "Constitución", "San Javier", "Molina", "Colbún", "Longaví", "Parral", "Romeral"],
    "Ñuble": ["Chillán", "Quillón", "San Carlos", "Bulnes", "Coihueco", "Yungay", "Pinto", "El Carmen", "Chillán Viejo", "Quirihue"],
    "Biobío": ["Concepción", "Talcahuano", "Los Ángeles", "Coronel", "Hualpén", "Chiguayante", "San Pedro de la Paz", "Lota", "Cabrero", "Tome"],
    "La Araucanía": ["Temuco", "Villarrica", "Angol", "Carahue", "Loncoche", "Pucón", "Nueva Imperial", "Padre Las Casas", "Collipulli", "Victoria"],
    "Los Ríos": ["Valdivia", "La Unión", "Lanco", "Máfil", "Mariquina", "Paillaco", "Panguipulli", "Futrono", "Río Bueno", "Corral"],
    "Los Lagos": ["Puerto Montt", "Osorno", "Chiloé", "Castro", "Calbuco", "Ancud", "Puerto Varas", "Quellón", "Fresia", "Purranque"],
    "Aysén": ["Coyhaique", "Puerto Aysén", "Chile Chico", "Cisnes", "Guaitecas", "Futaleufú", "Lago Verde", "Aysén", "Río Ibáñez", "Tortel"],
    "Magallanes": ["Punta Arenas", "Puerto Natales", "Porvenir", "Puerto Williams", "Cabo de Hornos", "Laguna Blanca", "San Gregorio", "Torres del Paine", "Primavera", "Natales"]
}

tallas_ropa = {
    "Mujer": ["XS", "S", "M", "L", "XL"],
    "Niña": ["XS", "S"]
}

tallas_calzado = {
    "Mujer": list(range(35, 46)),
    "Niña": list(range(28, 35))
}

colores = ["Rojo", "Azul", "Negro", "Blanco", "Verde", "Gris", "Amarillo"]

generos = ["Mujer", "Niña"]

temporadas = ["Verano", "Invierno", "Otoño", "Primavera"]

materiales = ["Algodón", "Poliéster", "Lana", "Cuero", "Nylon", "Seda", "Lino", "Cachemira", "Rayón"]

estilos = ["Casual", "Formal", "Deportivo", "Elegante"]

categorias = ["Ropa", "Calzado", "Accesorios"]

# Funciones generadoras

def generar_cliente(id_cliente):
    region = random.choice(list(regiones_y_comunas.keys()))
    comuna = random.choice(regiones_y_comunas[region])
    genero = random.choice(generos)
    # Edad según género: Niña entre 4-12, Mujer 13-60
    if genero == "Niña":
        edad = random.randint(4, 12)
        nombre = fake.first_name_female()
    else:
        edad = random.randint(13, 60)
        nombre = fake.first_name_female()
    apellido = fake.last_name()
    telefono = f"+56 9 {random.randint(10000000, 99999999)}"
    return {
        "id_cliente": id_cliente,
        "nombre": nombre,
        "apellido": apellido,
        "genero": genero,
        "edad": edad,
        "comuna": comuna,
        "region": region,
        "telefono": telefono
    }


def generar_producto(id_producto):
    categoria = random.choice(categorias)
    # Se puede validar género para evitar incoherencias (comentar/descomentar según necesidad)
    if categoria == "Calzado":
        nombre = random.choice(["Zapatillas", "Zapatos", "Pantuflas"])
    elif categoria == "Ropa":
        nombre = random.choice(["Polera", "Pantalón", "Chaqueta", "Blusa", "Falda"])
    else:
        nombre = random.choice(["Bolso", "Cinturón", "Bufanda", "Gorro"])
        
    precio_unitario = round(random.uniform(5000, 100000), 2)
    
    return {
        "id_producto": id_producto,
        "nombre": nombre,
        "categoría": categoria,
        "precio_unitario": precio_unitario 
    }

def generar_detalle_producto(id_detalle_producto, producto):
    categoria = producto["categoría"]
    genero = random.choice(generos)

    # Validar coherencia género - talla
    if categoria == "Calzado":
        talla = str(random.choice(tallas_calzado[genero]))
    elif categoria == "Ropa":
        talla = random.choice(tallas_ropa[genero])
    else:
        talla = None

    color = random.choice(colores)
    temporada = random.choice(temporadas)
    material = random.choice(materiales)
    marca = random.choice(marcas)
    estilo = random.choice(estilos)

    return {
        "id_detalle_producto": id_detalle_producto,
        "talla": talla,
        "color": color,
        "genero": genero,
        "temporada": temporada,
        "material": material,
        "marca": marca,
        "estilo": estilo,
        "id_producto": producto["id_producto"]
    }



def generar_venta(id_venta, clientes, productos, detalle_productos, canales_venta, metodos_pago, promociones, cursor):
    cliente = random.choice(clientes)
    producto = random.choice(productos)
    detalle_producto = random.choice(detalle_productos)
    tiempo = generar_tiempo(cursor)

    cantidad = random.randint(1, 5)
    precio_unitario = producto["precio_unitario"]
    total = round(precio_unitario * cantidad, 2)

    canal_venta = random.choice(canales_venta)
    metodo_pago = random.choice(metodos_pago)
    promocion = random.choice(promociones)

    return {
        "id_venta": id_venta,
        "id_pedido_venta": None,  # si usas pedidos, asignar fuera o en otra función
        "id_cliente": cliente["id_cliente"],
        "id_detalle_producto": detalle_producto["id_detalle_producto"],
        "id_producto": producto["id_producto"],
        "id_tiempo": tiempo["id_tiempo"],
        "cantidad": cantidad,
        "total": total,
        "fecha_venta": tiempo["fecha"],
        "hora_venta": random.randint(8, 22),
        "id_canal": canales_venta.index(canal_venta) + 1,  # suponiendo id_canal es 1-based index
        "id_metodo": metodos_pago.index(metodo_pago) + 1,  # idem
        "id_promo": promociones.index(promocion) + 1 if promocion else None
    }


def generar_ventas_con_pedidos(n_ventas, clientes, productos, detalle_productos, canales_venta, metodos_pago, promociones, cursor):
    ventas = []
    
    n_pedidos = max(1, n_ventas // 2)  # La mitad de ventas se agrupan en pedidos
    pedidos = list(range(1, n_pedidos + 1))
    
    for i in range(1, n_ventas + 1):
        compra = generar_venta(i, clientes, productos, detalle_productos, canales_venta, metodos_pago, promociones, cursor)
        compra["id_pedido_venta"] = random.choice(pedidos)
        ventas.append(compra)

    return ventas



def generar_compra(id_compra, productos, cursor):
    #print(productos)
    proveedor = random.choice(proveedores)
    producto = random.choice(productos)
    tiempo = generar_tiempo(cursor)  # Retorna dict con ID_tiempo, Fecha y Hora
    #print(tiempo)

    cantidad = random.randint(1, 10)  # Compran más cantidad que en ventas, ejemplo
    precio_unitario = producto["precio_unitario"]
    subtotal = precio_unitario
    total = (precio_unitario * cantidad)# Sin descuentos ni impuestos

    fecha_compra = tiempo["fecha"]
    hora_compra = random.randint(9, 18)

    # Simular fecha y hora de llegada 1 a 5 días después, hora entre 8 y 18 hrs
    
    dias_llegada = random.randint(1, 5)
    fecha_compra_dt = datetime.strptime(fecha_compra, "%Y-%m-%d")
    # Luego sumas timedelta
    fecha_llegada = fecha_compra_dt + timedelta(days=dias_llegada)
    hora_llegada = random.randint(8, 18)

    return {
        "id_compra": id_compra,
        "id_pedido_compra": None,  # Se asigna fuera si agrupas pedidos
        "id_tiempo": tiempo["id_tiempo"],
        "id_proveedor": proveedor["id_proveedor"],
        "id_producto": producto["id_producto"],
        "subtotal": subtotal,
        "total": total,
        "fecha_compra": fecha_compra,
        "hora_compra": hora_compra,
        "fecha_llegada": fecha_llegada,
        "hora_llegada": hora_llegada,
    }

def generar_compras_con_pedidos(n_compras, productos, cursor):
    compras = []

    n_pedidos = max(1, n_compras // 3)  # Ejemplo: cada pedido agrupa ~3 compras
    pedidos = list(range(1, n_pedidos + 1))

    for i in range(1, n_compras + 1):
        compra = generar_compra(i, productos, cursor)
        compra["id_pedido_compra"] = random.choice(pedidos)
        compras.append(compra)

    return compras
