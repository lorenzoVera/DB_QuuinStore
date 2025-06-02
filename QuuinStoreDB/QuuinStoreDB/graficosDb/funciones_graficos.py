import matplotlib.pyplot as plt
from datetime import datetime
import os


# Obtén la ruta del directorio donde se encuentra el script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define la carpeta base para guardar los gráficos dentro del directorio del script
carpeta_base = os.path.join(script_dir, 'graficosImagenes')
if not os.path.exists(carpeta_base):
    os.makedirs(carpeta_base)

def generar_grafico_tendencia_ventas(datos, año):
    """Genera y guarda un gráfico de líneas de la tendencia de ventas mensuales en la carpeta del año."""
    meses_anio = [row[0] for row in datos]
    ventas = [row[1] for row in datos]
    meses_formateados = []

    nombres_meses = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]

    for fecha_str in meses_anio:
        try:
            fecha_obj = datetime.strptime(fecha_str, '%Y-%m')
            mes_numero = fecha_obj.month - 1
            mes_nombre = nombres_meses[mes_numero]
            meses_formateados.append(mes_nombre)
        except ValueError:
            meses_formateados.append(fecha_str)
        except IndexError:
            meses_formateados.append(fecha_str)

    fig = plt.figure(figsize=(12, 7))
    plt.plot(meses_formateados, ventas, marker='o', linestyle='-')
    plt.xlabel('Mes', fontsize=13)
    plt.ylabel('Total de Ventas', fontsize=13)
    plt.grid(True)
    plt.xticks(meses_formateados, rotation=45, ha='right')
    plt.tight_layout()
    plt.title(f'Tendencia de Ventas Mensuales - Año {año}',fontsize=17, wrap=True)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
   
    carpeta_año = os.path.join(carpeta_base, str(año))
    if not os.path.exists(carpeta_año):
        os.makedirs(carpeta_año)
    nombre_archivo = os.path.join(carpeta_año, f'tendencia_ventas_{año}.png')
    plt.savefig(nombre_archivo)
    plt.close(fig) 

def generar_grafico_ventas_por_canal(datos, año):
    """Genera y guarda un gráfico de barras de las ventas por canal de venta en la carpeta del año."""
    canales = [row[0] for row in datos]
    ventas = [row[1] for row in datos]

    fig = plt.figure(figsize=(12, 7))
    plt.bar(canales, ventas, color='skyblue')
    plt.xlabel('Canal de Venta', fontsize=13)
    plt.ylabel('Total de Ventas', fontsize=13)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.title(f'Ventas por Canal de Venta - Año {año}',fontsize=17, wrap=True)
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    carpeta_año = os.path.join(carpeta_base, str(año))
    if not os.path.exists(carpeta_año):
        os.makedirs(carpeta_año)
    nombre_archivo = os.path.join(carpeta_año, f'ventas_por_canal_{año}.png')
    plt.savefig(nombre_archivo)
    plt.close(fig)

def generar_grafico_top_n_productos(datos, año, n):
    """Genera y guarda un gráfico de barras de los top N productos más vendidos en la carpeta del año."""
    productos = [row[0] for row in datos]
    cantidades = [row[1] for row in datos]

    fig = plt.figure(figsize=(12, 7))
    plt.bar(productos, cantidades, color='lightcoral')
    plt.xlabel('Producto', fontsize=13)
    plt.ylabel('Cantidad Vendida', fontsize=13)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.title(f'Top {n} Productos Más Vendidos - Año {año}')
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    carpeta_año = os.path.join(carpeta_base, str(año))
    if not os.path.exists(carpeta_año):
        os.makedirs(carpeta_año)
    nombre_archivo = os.path.join(carpeta_año, f'top_{n}_productos_{año}.png')
    plt.savefig(nombre_archivo)
    plt.close(fig)

def generar_grafico_ventas_por_categoria(datos, año):
    """Genera y guarda un gráfico de barras de las ventas por categoría de producto en la carpeta del año."""
    categorias = [row[0] for row in datos]
    ventas = [row[1] for row in datos]

    fig = plt.figure(figsize=(12, 7))
    plt.bar(categorias, ventas, color='mediumseagreen')
    plt.xlabel('Categoría', fontsize=13)
    plt.ylabel('Total de Ventas', fontsize=13)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.title(f'Ventas por Categoría de Producto - Año {año}',fontsize=17, wrap=True)
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    carpeta_año = os.path.join(carpeta_base, str(año))
    if not os.path.exists(carpeta_año):
        os.makedirs(carpeta_año)
    nombre_archivo = os.path.join(carpeta_año, f'ventas_por_categoria_{año}.png')
    plt.savefig(nombre_archivo)
    plt.close(fig)

def generar_grafico_distribucion_metodos_pago(datos, año):
    """Genera y guarda un gráfico de pastel de la distribución de los métodos de pago en la carpeta del año."""
    metodos = [row[0] for row in datos]
    cantidades = [row[1] for row in datos]

    fig = plt.figure(figsize=(12, 7))
    plt.pie(cantidades, labels=metodos, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.tight_layout()
    plt.title(f'Distribución de Métodos de Pago - Año {año}',fontsize=17, wrap=True)
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    carpeta_año = os.path.join(carpeta_base, str(año))
    if not os.path.exists(carpeta_año):
        os.makedirs(carpeta_año)
    nombre_archivo = os.path.join(carpeta_año, f'distribucion_metodos_pago_{año}.png')
    plt.savefig(nombre_archivo)
    plt.close(fig)

def generar_grafico_ventas_por_region(datos, año):
    """Genera y guarda un gráfico de barras de las ventas por región del cliente en la carpeta del año."""
    orden_regiones = [
        "Arica y Parinacota", "Tarapacá", "Antofagasta", "Atacama", "Coquimbo",
        "Valparaíso", "Metropolitana", "O'Higgins", "Maule", "Ñuble",
        "Biobío", "Araucanía", "Los Ríos", "Los Lagos", "Aysén", "Magallanes"
    ]
    ventas_por_region = {row[0]: row[1] for row in datos}

    # Filtra y ordena según la lista
    regiones_ordenadas = [r for r in orden_regiones if r in ventas_por_region]
    ventas_ordenadas = [ventas_por_region[r] for r in regiones_ordenadas]

    fig = plt.figure(figsize=(12, 7))
    plt.bar(regiones_ordenadas, ventas_ordenadas, color='gold')
    plt.xlabel('Región', fontsize=13)
    plt.ylabel('Total de Ventas', fontsize=13)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.title(f'Ventas por Región - Año {año}',fontsize=17, wrap=True)
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    carpeta_año = os.path.join(carpeta_base, str(año))
    if not os.path.exists(carpeta_año):
        os.makedirs(carpeta_año)
    nombre_archivo = os.path.join(carpeta_año, f'ventas_por_region_{año}.png')
    plt.savefig(nombre_archivo)
    plt.close(fig)
