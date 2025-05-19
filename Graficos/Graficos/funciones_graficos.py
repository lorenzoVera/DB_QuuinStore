import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasAgg

def generar_grafico_tendencia_ventas(datos):
    """Genera un gráfico de líneas de la tendencia de ventas mensuales."""
    meses = [row[0] for row in datos]
    ventas = [row[1] for row in datos]

    fig = plt.figure(figsize=(10, 6))
    plt.plot(meses, ventas, marker='o', linestyle='-')
    plt.xlabel('Mes - Año')
    plt.ylabel('Total de Ventas')
    plt.grid(True)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    fig.canvas.manager.set_window_title('Tendencia de Ventas Mensuales')
    plt.show()

def generar_grafico_ventas_por_canal(datos):
    """Genera un gráfico de barras de las ventas por canal de venta."""
    canales = [row[0] for row in datos]
    ventas = [row[1] for row in datos]

    fig = plt.figure(figsize=(8, 6))
    plt.bar(canales, ventas, color='skyblue')
    plt.xlabel('Canal de Venta')
    plt.ylabel('Total de Ventas')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    fig.canvas.manager.set_window_title('Ventas por Canal de Venta')
    plt.show()

def generar_grafico_top_n_productos(datos, n=10):
    """Genera un gráfico de barras de los top N productos más vendidos."""
    productos = [row[0] for row in datos]
    cantidades = [row[1] for row in datos]

    fig = plt.figure(figsize=(10, 6))
    plt.bar(productos, cantidades, color='lightcoral')
    plt.xlabel('Producto')
    plt.ylabel('Cantidad Vendida')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    fig.canvas.manager.set_window_title(f'Top {n} Productos Más Vendidos')
    plt.show()

def generar_grafico_ventas_por_categoria(datos):
    """Genera un gráfico de barras de las ventas por categoría de producto."""
    categorias = [row[0] for row in datos]
    ventas = [row[1] for row in datos]

    fig = plt.figure(figsize=(8, 6))
    plt.bar(categorias, ventas, color='mediumseagreen')
    plt.xlabel('Categoría')
    plt.ylabel('Total de Ventas')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    fig.canvas.manager.set_window_title('Ventas por Categoría de Producto')
    plt.show()

def generar_grafico_distribucion_metodos_pago(datos):
    """Genera un gráfico de pastel de la distribución de los métodos de pago."""
    metodos = [row[0] for row in datos]
    cantidades = [row[1] for row in datos]

    fig = plt.figure(figsize=(8, 8))
    plt.pie(cantidades, labels=metodos, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.tight_layout()
    fig.canvas.manager.set_window_title('Distribución de Métodos de Pago')
    plt.show()

def generar_grafico_ventas_por_region(datos):
    """Genera un gráfico de barras de las ventas por región del cliente."""
    regiones = [row[0] for row in datos]
    ventas = [row[1] for row in datos]

    fig = plt.figure(figsize=(8, 6))
    plt.bar(regiones, ventas, color='gold')
    plt.xlabel('Región')
    plt.ylabel('Total de Ventas')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    fig.canvas.manager.set_window_title('Ventas por Región del Cliente')
    plt.show()